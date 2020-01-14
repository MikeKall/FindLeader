import socket
from os import sys
import time
#import RPi.GPIO as GPIO
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(3, GPIO.OUT)


retries=0

def client_program():
    global retries
    try:
        f = open('leaderIP', 'r')
        builder = f.readline()
        f.close()
        port = 5000  # socket server port
        host = ""

        # for some reason python reads 2 lines when in the file there is only. So we call a custom def
        for i in builder:
            if is_char(i):
                host += i # Building the ip

        # instantiate socket. Use AF_INET and TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))  # connect to the server
        print("Connected!")
    except(ConnectionRefusedError):
        retries+=1
        if retries <= 5:
            time.sleep(2)
            print("Connection refused, retrying...")
            client_program()
        else:
            print("Could not connect to leader")
            sys.exit()

    while True:
        try:
            print("Waiting for leader")
            data = client_socket.recv(1024).decode()  # receive response
            PIcommands(data)
            print(data, "\n")
        except (KeyboardInterrupt):
            client_socket.close()  # close the connection
            sys.exit()

# if you are reading int or '.', then return true.
def is_char(s):
    try:
        int(s)
        return True
    except ValueError:
        if (s == "."):
            return True
        else:
            return False

# All the known commands that a follower can execute
def PIcommands(com):
    if com == "ledon":
        #GPIO.output(3, GPIO.HIGH)
        print("Leds on")
    elif com == "ledoff":
        #GPIO.output(3, GPIO.LOW)
        print("Leds on")
    elif com == "disconnect":
        print("Disconnecting from leader")
        sys.exit()

if __name__ == '__main__':
    client_program()
