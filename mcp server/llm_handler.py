from openai import AzureOpenAI
import json

from __init__ import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT_NAME, 
    TOOLS
)

llm_config = {
    "api_key": AZURE_OPENAI_API_KEY,
    "azure_endpoint": AZURE_OPENAI_ENDPOINT,
    "api_version": AZURE_OPENAI_API_VERSION,
}

client = AzureOpenAI(**llm_config)


def get_task_list(query):
    base_prompt = """
    Given the user query and the available tool definitions, determine the necessary tools to fulfill the request. 
    Identify the required tool(s), their names, and the parameters needed based on the user query.

    Available Tools:
    <TOOLS_JSON>

    Expected Output:
    Return a JSON object containing a list of selected tools with their names and parameters.

    Example:

    User Query: "Fetch the list of 5 longest rivers in India and send it to harsh.raj@scikiq.com"

    Output:
    {
        "tasks": [
            {
                "id": "task_1",
                "name": "llm_service",
                "parameters": {
                    "query": "List the 5 longest rivers in India"
                }
            },
            {
                "id": "task_2",
                "name": "email_service",
                "parameters": {
                    "receiver_email": "harsh.raj@scikiq.com",
                    "subject": "List of 5 longest rivers in India",
                    "body": "{{task_1.result}}"
                },
                "depends_on": "task_1"
            }
        ]
    }
    """

    messages = [
        {"role": "system", "content": base_prompt.replace("<TOOLS_JSON>", str(TOOLS))},
        {"role": "user", "content": query},
    ]

    params = {
        "model": AZURE_OPENAI_DEPLOYMENT_NAME,
        "messages": messages,
        "temperature": 1,
    }

    response = client.chat.completions.create(**params)

    task_list = json.loads(response.choices[0].message.content.strip())

    # Iterate over tasks to set default values for missing parameters
    for task in task_list["tasks"]:
        tool_name = task["name"]
        if tool_name in TOOLS:
            for param in TOOLS[tool_name]["parameters"]:
                param_name = param["name"]
                default_value = param.get("default", None)  # Check if a default value is provided
                if param_name not in task["parameters"] and not task.get("depends_on"):  
                    # Assign default only if the parameter is missing and NOT dependent on another task
                    if default_value is not None:
                        task["parameters"][param_name] = default_value

    return task_list