import socket
import json
import logging

# MCP Server Configuration
HOST = "127.0.0.1"
PORT = 65432

# Setup logging
logging.basicConfig(filename="mcp_client.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Request ID counter
REQUEST_ID = 1

def send_query(query):
    """Send a JSON-RPC formatted query to the MCP server for llm_service."""
    global REQUEST_ID
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        # JSON-RPC 2.0 Request
        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "process_query",
            "params": {
                # "tool_name": "llm_service",
                "tool_name": "to be determined by the server",
                "params": {
                    "query": query
                }
            },
            "id": REQUEST_ID
        }

        # Increment request ID
        REQUEST_ID += 1        

        # Log request
        logging.info(f"Sending request: {json.dumps(json_rpc_request)}")

        # Send JSON data
        client_socket.send(json.dumps(json_rpc_request).encode("utf-8"))

        # Receive and decode response
        response = client_socket.recv(1024).decode("utf-8")

        # Log response
        logging.info(f"Received response: {response}")

        print(f"Server Response: {response}")

        client_socket.close()


    except ConnectionRefusedError:
        logging.error("Error: Cannot connect to MCP server. Make sure it's running.")
        print("Error: Cannot connect to MCP server. Make sure it's running.")

if __name__ == "__main__":
    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        send_query(user_query)