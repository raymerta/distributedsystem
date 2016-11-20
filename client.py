import socket
import os
import sys

def main():
	sock = socket.socket()

        serverAddress = ('localhost', 10001)
	print >> sys.stderr, 'connecting to %s port %s' % serverAddress	
	sock.connect(serverAddress)
	sock.send("index.html")
	htmlText = sock.recv(1024)
	
	print htmlText
if __name__ == '__main__':
    main()
