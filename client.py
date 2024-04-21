import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname(socket.gethostname())
port = 5050
ADDR = (host, port)

client.connect(ADDR)

def authenticate():
    username = input("Username: ")
    password = input("Password: ")
    client.sendall(username.encode('utf-8'))
    client.sendall(password.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(response)
    return response.startswith("Authentication successful")

def send_message():
    while True:
        message = input("Enter message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client.sendall(message.encode('utf-8'))

def main():
    if authenticate():
        print("Authentication successful. You are now connected to the server.")
        send_message()
    else:
        print("Authentication failed. Closing connection.")
        client.close()

if __name__ == "__main__":
    main()
