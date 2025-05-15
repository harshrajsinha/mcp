import socket
import requests
import json
import grpc
from concurrent import futures
import copy

from email_handler import send_email  # Placeholder for email function
from llm_handler import get_task_list  # Placeholder for LLM function
from __init__ import TOOLS, RESPONSE_FORMAT

# Configuration
HOST = '127.0.0.1'
PORT = 65432
# FASTAPI_URL = "http://127.0.0.1:8050/llm_process"  # FastAPI endpoint
SSMP_URL = "http://127.0.0.1:9000/session"    # SSMP session manager




def register_tool(name, description, tool_type, parameters, url=None, function=None):
    """Register a new tool in the MCP Server with details."""
    if name in TOOLS:
        return {"jsonrpc": "2.0", "error": f"Tool {name} is already registered.", "id": 1}

    tool_entry = {
        "name": name,
        "description": description,
        "type": tool_type,
        "parameters": parameters
    }

    if tool_type == "rest_api":
        tool_entry["url"] = url
    elif tool_type == "local_function":
        tool_entry["function"] = function
    elif tool_type == "rpc":
        tool_entry["url"] = url  # RPC services require a URL
    
    TOOLS[name] = tool_entry

    return {"jsonrpc": "2.0", "result": f"Tool {name} registered successfully.", "id": 1}



def get_session(client_id):
    """Retrieve session ID from SSMP."""

    response = requests.post(SSMP_URL, json={"client_id": client_id})
    return response.json().get("session_id", None)



def process_query(tool_name, session_id, params, task_result={}):
    """Process queries using different types of tools and pass results to dependent tasks."""

    if tool_name not in TOOLS:
        print("I am in else......")

        final_res = copy.deepcopy(RESPONSE_FORMAT)
        final_res["result"]["session_id"] = session_id   
        final_res["result"]["answer"] = {}

        try: 
            tasks = get_task_list(request["params"]["params"]["query"])
            for task in tasks["tasks"]:
                tool = TOOLS[task["name"]]
                task_name = task["name"]
                task_id = task["id"]

                final_res["result"]["answer"][task_name] = {} 
                final_res["result"]["answer"][task_name]["error"] = 0
                final_res["result"]["answer"][task_name]["name"] = task["name"]
                final_res["result"]["answer"][task_name]["task_parameters"] = task["parameters"]

                # Resolve dependencies by injecting results from dependent tasks
                if "depends_on" in task:
                    dependency_id = task["depends_on"]
                    if dependency_id in task_result:
                        for param_key, param_value in task["parameters"].items():
                            if param_value == f"{{{{{dependency_id}.result}}}}":
                                task["parameters"][param_key] = task_result[dependency_id]["result"]["answer"]

                try:
                    if tool["type"] == "rest_api":
                        payload = {"jsonrpc": "2.0", "method": "process_query", "params": {"session_id": session_id, **task["parameters"]}, "id": 1}
                        result = requests.post(tool["url"], json=payload)
                        final_res["result"]["answer"][task_name]["task_response"] = result.json()
                        task_result[task_id] = result.json()

                    elif tool["type"] == "local_function":
                        function_name = tool["function"]
                        function_object = globals()[function_name]
                        res = function_object(**task["parameters"])
                        final_res["result"]["answer"][task_name]["task_response"] = res
                        task_result[task_id] = res

                    elif tool["type"] == "rpc":
                        with grpc.insecure_channel(tool["url"]) as channel:
                            stub = tool["stub"](channel)
                            result = stub.process_query(**task["parameters"])
                            final_res["result"]["answer"][task_name]["task_response"] = json.loads(result)
                            task_result[task_id] = json.loads(result)

                except Exception as e:
                    final_res["result"]["answer"][task_name]["error"] = 1
                    final_res["result"]["answer"][task_name]["msg"] = str(e)

        except Exception as e:        
            final_res["result"]["error"] = f"Tool {tool_name} not registered."
            final_res["result"]["answer"] = "Unable to process the query."
            final_res["result"]["session_id"] = session_id

        return final_res

    else:    
        tool = TOOLS[tool_name]

        if tool["type"] == "rest_api":
            payload = {"jsonrpc": "2.0", "method": "process_query", "params": {"session_id": session_id, **params}, "id": 1}
            final_res = requests.post(tool["url"], json=payload)
            return final_res.json()
        
        elif tool["type"] == "local_function":
            function_name = tool["function"]
            function_object = globals()[function_name]
            return function_object(*params.values())

        elif tool["type"] == "rpc":
            with grpc.insecure_channel(tool["url"]) as channel:
                stub = tool["stub"](channel)
                final_res = stub.process_query(params)
                return json.loads(final_res)


# MCP Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"MCP Server running on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    client_id = addr[0]
    print(f"Connected by {client_id}")

    session_id = get_session(client_id)

    data = conn.recv(1024).decode('utf-8')
    if not data:
        break

    try:
        request = json.loads(data)
        if request["method"] == "register_tool":
            response = register_tool(
                request["params"]["name"],
                request["params"]["description"],
                request["params"]["type"],
                request["params"]["parameters"],
                request["params"].get("url"),
                request["params"].get("function")
            )
        elif request["method"] == "process_query":
            tool_name = request["params"]["tool_name"]
            response = process_query(tool_name, session_id, request["params"]["params"])
        elif request["method"] == "send_email":
            response = send_email(
                request["params"]["receiver_email"],
                request["params"]["subject"],
                request["params"]["body"]
            )            
        else:
            response = {"jsonrpc": "2.0", "error": "Unknown method.", "id": request["id"]}

    except json.JSONDecodeError:
        response = {"jsonrpc": "2.0", "error": "Invalid JSON format.", "id": 1}




    conn.send(json.dumps(response).encode('utf-8'))
    conn.close()