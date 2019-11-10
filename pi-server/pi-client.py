import socket
from secret import *
import sys
import time

# Raspberry Pi imports
import RPi.GPIO as GPIO
servoPin = 17

def establish_connection():
    my_host = SERVER_IP
    my_port = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((my_host, my_port))
    sock.send(bytearray("pi" + PASSWORD, 'utf-8'))
    print(bytes.decode(sock.recv(151)))
    return sock

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPin, GPIO.OUT)

    p = GPIO.PWM(servoPin, 50) # runs at 50 MHz
    p.start(3.5) # start with a 3.5% duty cycle, wait to complete, and remove voltage
    time.sleep(1)
    p.ChangeDutyCycle(0)
    
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
                p.ChangeDutyCycle(5.5)
                time.sleep(1)
                p.ChangeDutyCycle(3.5)
                time.sleep(1)
                p.ChangeDutyCycle(0)
        else:
            try:
                sock = establish_connection()
            except:
                time.sleep(5)

if __name__ == "__main__":
    main()