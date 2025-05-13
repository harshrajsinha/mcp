import socket
import requests
import json

# Configuration
HOST = '127.0.0.1'
PORT = 65432
FASTAPI_URL = "http://127.0.0.1:8050/llm_process"  # FastAPI endpoint
SSMP_URL = "http://127.0.0.1:9000/session"    # SSMP session manager

def get_session(client_id):
    """Retrieve session ID from SSMP."""
    response = requests.post(SSMP_URL, json={"client_id": client_id})
    return response.json().get("session_id", None)

def process_query(session_id, query):
    """Send JSON-RPC request with SSMP session management."""
    payload = {
        "jsonrpc": "2.0",
        "method": "process_query",
        "params": {
            "session_id": session_id,
            "query": query
        },
        "id": 1
    }
    
    response = requests.post(FASTAPI_URL, json=payload)
    result = response.json()
    
    return result.get("result", {})

# MCP Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"MCP Server running on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    client_id = addr[0]  # Identify client
    print(f"Connected by {client_id}")

    # Get or Create SSMP Session
    session_id = get_session(client_id)
    
    data = conn.recv(1024).decode('utf-8')
    if not data:
        break
    
    print(f"Received query: {data}")
    
    # Process query using FastAPI microservice with session tracking
    response = process_query(session_id, data)

    conn.send(response.get("answer", "No response").encode('utf-8'))
    conn.close()