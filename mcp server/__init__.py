
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
    "finance_dataq_service": {
        "name": "finance_dataq_service",
        "description": "Finance DataQ Service to process user queries. This service processes user queries related to finance data.",
        "type": "rest_api",
        "parameters": [
            {
                "name": "msg",
                "desc": "User query to process",
                "optional": 0,  # Mandatory
                "value_type": "str"
            },
            {
                "name": "dataset_id",
                "desc": "Dataset ID for the finance data",
                "optional": 0,  # Mandatory
                "value_type": "str",
                "default": "DSETCLNT0015000211"
            },            
            {
                "name": "client_key",
                "desc": "Resource key for the client",
                "optional": 0,  # Mandatory
                "value_type": "str",
                "default": "CLNT0015"
            },
            {
                "name": "user_key",
                "desc": "Resource key for the user",
                "optional": 0,  # Mandatory
                "value_type": "str",
                "default": "USERCLNT0015000001"
            },
            {
                "name": "request_id",
                "desc": "Unique request ID for tracking",
                "optional": 0,  # Mandatory
                "value_type": "str",
                "default": "REQ0015"
            },
            {
                "name": "conn_key",
                "desc": "LLM connection key",
                "optional": 0,  # Mandatory
                "value_type": "str",    
                "default": "DSRCCLNT0015000192" 
            },
            {
                "name": "llm_mdl",
                "desc": "LLM model name",
                "optional": 0,  # Mandatory
                "value_type": "str",
                "default": "gpt-3.5-turbo-16k"
            },
            {
                "name": "table_name",
                "desc": "Table name for the finance data",
                "optional": 0,  # Mandatory
                "value_type": "str",
                "default": "ebit"
            }
        ],
        "url": "http://127.0.0.1:8050/dams/chat/dashboard",
        "payload_type": "form data",
    },    
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
        "url": "http://127.0.0.1:8051/llm_process",
        "payload_type": "json rpc",
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
    }
}