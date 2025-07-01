import socket
import sys
import os

SERVER_PORT = 12345
BUF_SIZE = 4096
QUEUE_SIZE = 10


def fatal(message):
    print(message)
    sys.exit(1)


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    fatal("Socket failed")

# for on=1 in python to enable reuseaddr
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# empty string in sockets for inaddr_any i.e any interface including localhost
try:
    s.bind(('', SERVER_PORT))
except socket.error:
    fatal("Bind failed")

try:
    s.listen(QUEUE_SIZE)
except socket.error:
    fatal("Listen failed")

while True:
    cSocket, cAddr = s.accept()

    fName = cSocket.recv(BUF_SIZE).decode().strip().replace('\0', '')  # the zero byte at the end from client

    try:
        with open(fName, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                cSocket.send(data)
    except FileNotFoundError:
        fatal("open failed")
    cSocket.close()
