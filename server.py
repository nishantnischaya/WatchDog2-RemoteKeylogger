import socket
import threading 
import logging
import signal
import sys
from Crypto.Cipher import AES

logging.basicConfig(filename="keylog.log", format='%(asctime)s - %(message)s', filemode='w')
logger = logging.getLogger() 
logger.setLevel(logging.DEBUG)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 5050
ADDR = (host, port)

user_database = {
    "user1": "password1",
    "user2": "password2"
}

def decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_EAX)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode('utf-8')

def authenticate(client):
    encrypted_username = client.recv(1024)
    encrypted_password = client.recv(1024)
    
    # Decrypt the username and password
    key = b'secret_key_16bit'
    username = decrypt(key, encrypted_username)
    password = decrypt(key, encrypted_password)
    
    if username in user_database and user_database[username] == hashlib.sha256(password.encode()).hexdigest():
        client.sendall(b"Authentication successful. Welcome!\n")
        return True
    else:
        client.sendall(b"Invalid username or password. Closing connection.\n")
        return False

# Remaining code remains unchanged...
