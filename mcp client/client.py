import socket

# MCP Server Configuration
HOST = "127.0.0.1"
PORT = 65432

def send_query(query):
    """Send a query to the MCP server and receive a response."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        client_socket.send(query.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")

        print(f"Server Response: {response}")

        client_socket.close()
    except ConnectionRefusedError:
        print("Error: Cannot connect to MCP server. Make sure it's running.")

if __name__ == "__main__":
    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        send_query(user_query)