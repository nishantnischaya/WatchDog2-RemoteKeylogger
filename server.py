import socket
import threading 
import logging
import signal
import sys

logging.basicConfig(filename="keylog.log", format='%(asctime)s - %(message)s', filemode='w')
logger = logging.getLogger() 
logger.setLevel(logging.DEBUG)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 5050
ADDR = (host, port)

# Define a simple username/password database
user_database = {
    "user1": "password1",
    "user2": "password2"
}

def authenticate(client):
    client.sendall(b"Username: ")
    username = client.recv(1024).strip().decode("utf-8")
    client.sendall(b"Password: ")
    password = client.recv(1024).strip().decode("utf-8")
    return (username, password)

def write_log(client, address, message, error=False):
    logging_data = f'{client} - {address} - {message}'
    if error:
        logger.error(logging_data)
    else:
        logger.info(logging_data)

def handler(client, address):
    # Authenticate the client
    username, password = authenticate(client)
    if username in user_database and user_database[username] == password:
        client.sendall(b"Authentication successful. Welcome!\n")
        write_log(client, address, 'Connection Established!', error=False)
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if not message:  # If message is empty, the client has disconnected
                    write_log(client, address, 'Disconnected!', error=False)
                    client.close()
                    break
                else:
                    write_log(client, address, message, error=False)
            except Exception as e:  # Catch specific exceptions for better error handling
                write_log(client, address, f'Error: {str(e)}', error=True)
                client.close()
                break
    else:
        client.sendall(b"Invalid username or password. Closing connection.\n")
        write_log(client, address, 'Authentication failed. Closing connection.', error=True)
        client.close()

def receive():
    while True:
        client, address = server.accept()
        write_log(client, address, 'Connection Established!', error=False)
        thread = threading.Thread(target=handler, args=(client, address))
        thread.start()

def shutdown(sig, frame):
    print("Shutting down server...")
    server.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

server.bind(ADDR)
server.listen()

receive()
