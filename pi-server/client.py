import socket
from secret import *
import sys
import time

my_host = SERVER_IP
my_port = 8000

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((my_host, my_port))
except Exception:
    print("Couldn't dial host/port. Try again.")
    sys.exit(1)
sock.send(bytearray(PASSWORD, 'utf-8'))
print(bytes.decode(sock.recv(151)))