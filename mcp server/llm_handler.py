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
    Given the user query and the available tool definitions, determine the necessary tools to fulfill the request. Identify the required tool(s), their names, and the parameters needed based on the user query.

    Available Tools:
    <TOOLS_JSON>

    Expected Output:
    Return a JSON object containing a list of selected tools with their names and parameters.

    Example:

    User Query: "Fetch the list of 5 longest rivers in India and send it to harsh.raj@scikiq.com"

    Output:
    {
        "tools": [
            {
                "name": "llm_service",
                "parameters": {
                    "query": "List the 5 longest rivers in India"
                }
            },
            {
                "name": "email_service",
                "parameters": {
                    "receiver_email": "harsh.raj@scikiq.com",
                    "subject": "List of 5 longest rivers in India",
                    "body": "<RESULT_FROM_LLM_SERVICE>"
                }
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

    return json.loads(response.choices[0].message.content.strip())