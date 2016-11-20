import socket
import os
import sys

def main():
	sock = socket.socket()

    serverAddress = ('localhost', 10000)
    print >> sys.stderr, 'connecting to %s port %s' % serverAddress
    sock.connect(serverAddress)

    

if __name__ == '__main__':
    main()