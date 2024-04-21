import socket
import hashlib
from Crypto.Cipher import AES

# AES encryption function
def encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, _ = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    return ciphertext

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname(socket.gethostname())
port = 5050
ADDR = (host, port)

client.connect(ADDR)

def authenticate():
    username = input("Username: ")
    password = input("Password: ")
    
    # Hash the password before sending
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Encrypt the username and hashed password
    key = b'secret_key_16bit'
    encrypted_username = encrypt(key, username)
    encrypted_password = encrypt(key, hashed_password)
    
    # Send encrypted credentials to the server
    client.sendall(encrypted_username)
    client.sendall(encrypted_password)
    
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
