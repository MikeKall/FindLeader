from os import system, sys
import socket
import subprocess
from threading import *
import threading
import socketserver

clients = set()
clients_lock = threading.Lock()
def server_program():


    host = str(system('hostname -I'))

    port = 5000

    s = socket.socket()

    # permit reuse of local address at bind. This option allows us to connect more than 1 client to the server
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    print("Server has started. Waiting for connections")
    s.listen()
    th = []

    #print("Server has started. Waiting for connections.")

    while True:
        try:
            # Wait for connections. When a client connects make a thread for that client an wait again for another connection
            client, address = s.accept()
            th.append(Thread(target=listener, args = (client,address)).start())
        except(KeyboardInterrupt):
            print("\n\nExiting")
            sys.exit()

def listener(client, address):
    print("Device connected: ", address)
    with clients_lock:
        clients.add(client)
    while True:
        data = input("")
        with clients_lock:
            for c in clients:
                c.sendall(data.encode())
if __name__ == '__main__':
    server_program()
