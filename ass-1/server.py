import socket
import threading

# List to keep track of connected clients
clients = []
usernames = {}

# Function to handle client messages
def handle_client(client_socket, client_address):
    # Receive and store username
    username = client_socket.recv(1024).decode('utf-8')
    usernames[client_socket] = username
    print(f"{username} connected from {client_address}")

    broadcast_message(f"{username} has joined the chat.", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == 'bye':
                broadcast_message(f"{username} has left the chat.", client_socket)
                remove_client(client_socket)
                # Check if all clients have left
                if not clients:
                    broadcast_message("All users have exited. Terminating chat.", None)
                break
            else:
                broadcast_message(f"{username}: {message}", client_socket)
        except:
            remove_client(client_socket)
            break

# Function to broadcast message to all clients except the sender
def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

# Function to remove a client from the list
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

# Main server function
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Bind to all interfaces on port 12345
    server_socket.listen(5)
    print("Server is listening on port 12345...")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        # Start a new thread for each client
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
