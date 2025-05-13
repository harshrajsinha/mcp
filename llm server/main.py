from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from openai import OpenAI, AzureOpenAI

from __init__ import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT_NAME,
    SSMP_URL,
)



class QueryRequest(BaseModel):
    session_id: str
    query: str

# Request Format for JSON-RPC 2.0
class JSONRPCRequest(BaseModel):
    jsonrpc: str
    method: str
    params: dict
    id: int

llm_config = {
    "api_key": AZURE_OPENAI_API_KEY,
    "azure_endpoint": AZURE_OPENAI_ENDPOINT,
    "api_version": AZURE_OPENAI_API_VERSION,
}

client = AzureOpenAI(**llm_config)

app = FastAPI()

def get_session_context(session_id, query):
    """Retrieve session context from SSMP."""
    response = requests.post(SSMP_URL, json={"session_id": session_id, "query": query})
    return response.json().get("context", {})

@app.post("/llm_process")
async def jsonrpc_handler(request: JSONRPCRequest):
    """Handles JSON-RPC 2.0 formatted requests for LLM query processing with session context."""
    
    # Validate JSON-RPC format
    if request.jsonrpc != "2.0":
        raise HTTPException(status_code=400, detail="Invalid JSON-RPC version")

    if request.method != "process_query":
        raise HTTPException(status_code=400, detail="Unsupported method")

    session_id = request.params.get("session_id")
    query = request.params.get("query")

    if not session_id or not query:
        raise HTTPException(status_code=400, detail="Missing session_id or query")

    # ✅ Fetch session context from SSMP
    context = get_session_context(session_id, query)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(f"Session ID: {session_id}")  
    print(f"Session Context: {context}")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    


    # ✅ Modify query messages using session context
    messages = [
        {"role": "system", "content": "You are an AI assistant with session memory."},
        {"role": "user", "content": query}
    ]

    # Include past context in conversation history
    if context:
        messages.insert(1, {"role": "system", "content": f"Previous context: {context}"})

    params = {
        "model": AZURE_OPENAI_DEPLOYMENT_NAME,
        "messages": messages,
        "temperature": 1,
    }
    
    response = client.chat.completions.create(**params)

    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "result": {
            "answer": response.choices[0].message.content.strip(),
            "session_id": session_id  # Returning session ID for continuity
        }
    }

   

