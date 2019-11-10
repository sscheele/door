import socket
from secret import *
import sys
import time

def establish_connection():
    my_host = SERVER_IP
    my_port = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((my_host, my_port))
    sock.send(bytearray("pi" + PASSWORD, 'utf-8'))
    print(bytes.decode(sock.recv(151)))
    return sock

def main():
    try:
        sock = establish_connection()
    except:
        print("Couldn't dial host")
        sys.exit(1)
    while True:
        msg = bytes.decode(sock.recv(151))
        if msg:
            print(msg)
            if msg == "Open":
                print("Opening...")
        else:
            try:
                sock = establish_connection()
            except:
                time.sleep(5)

if __name__ == "__main__":
    main()