
#!/usr/bin/env python
import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AZURE_OPENAI_API_KEY=os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION=os.environ.get("AZURE_OPENAI_API_VERSION") 
AZURE_OPENAI_ENDPOINT=os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

RESPONSE_FORMAT = {
    "jsonrpc": "2.0",
    "result": {
        "answer": "",
        "session_id": ""
    },
    "id": 1
}



# Registry for tools
TOOLS = {
    "llm_service": {
        "name": "llm_service",
        "description": "Language Model Processing Service to process user queries",
        "type": "rest_api",
        "parameters": [
            {
                "name": "query",
                "desc": "User query to process",
                "optional": 0,  # Mandatory
                "value_type": "str"
            }
        ],
        "url": "http://127.0.0.1:8050/llm_process"
    },
    "email_service": {
        "name": "email_service",
        "description": "Email Sending Service",
        "type": "local_function",
        "parameters": [
            {
                "name": "receiver_email",
                "desc": "Recipient email address",
                "optional": 0,
                "value_type": "str"
            },
            {
                "name": "subject",
                "desc": "Email subject",
                "optional": 0,
                "value_type": "str"
            },
            {
                "name": "body",
                "desc": "Email body content",
                "optional": 0,
                "value_type": "str"
            }
        ],
        "function": "send_email",  # Placeholder for email function
    },
    "example_function": {
        "name": "example_function",
        "description": "Local function example",
        "type": "local_function",
        "parameters": [
            {
                "name": "number",
                "desc": "A number to square",
                "optional": 0,
                "value_type": "int"
            }
        ],
        "function": lambda x: {"result": x**2}  # Example local function
    }
}