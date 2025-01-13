import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message == "terminate":
                    print("All users said 'bye'. Exiting the chat.")
                    break
                elif "has joined the chat" in message or "has left the chat" in message:
                    print(f"\033[92m{message}\033[0m")  # Green for system messages
                else:
                    print(message)
            else:
                print("Connection closed by the server.")
                break
        except:
            print("Error receiving message. Connection may have closed.")
            break

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message.lower() == 'bye':
            print("You said 'bye'. Waiting for others to say 'bye'.")
            break

# Start the client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '127.0.0.1'
    server_port = 12345

    try:
        client_socket.connect((server_ip, server_port))
        username = input("Enter your username: ")
        client_socket.send(username.encode('utf-8'))

        print(f"Welcome to the chat, {username}! Type 'bye' to exit.")

        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
        send_messages(client_socket)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
