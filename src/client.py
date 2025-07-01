import socket
import sys

SERVER_PORT = 12345   #port number and buffer as in the c client file
BUF_SIZE = 4096

def fatal(message):
    print(message)
    sys.exit(1)

if len(sys.argv) != 3:
    fatal("Usage: python3 client.py server-name file-name")

try:
    sName= sys.argv[1]
    sIP = socket.gethostbyname(sName)
except socket.gaierror:
    fatal("gethostbyname failed")

#TCP socket is the default here in python's socket module for the IPV4 addresse
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    fatal("Socket")
#trying to Connect
sAddr = (sIP, SERVER_PORT)
try:
    s.connect(sAddr)
except socket.error:
    fatal("Connect failed")

#To include the 0 byte at the end
fileName= sys.argv[2]
fileName= fileName + '\0'
s.send(fileName.encode())

#recv returns a bytes object with the maximum of buf-size
while True:
    data= s.recv(BUF_SIZE)
    if not data:
        break
    sys.stdout.buffer.write(data)
s.close()

