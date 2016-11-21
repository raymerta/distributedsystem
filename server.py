import socket
import threading
import os
import sys
import webbrowser

# setting up response header
responseHeaders = {}

responseHeaders[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: text/html

%s
"""

responseHeaders[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s

moved
"""

responseHeaders[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

# handling routing
def routing(): 
	return null

# socketServer handling
def socketServer(serverAddress):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(serverAddress)
    sock.listen(5)
    return sock

# handling routing TODO
def routingHandler(uri):
	addr = uri[1:].lower()

	print >> sys.stderr, 'URI accessed trimmed : %s' % addr

	content = ''
	if (addr == ''):
		f = open('index.html', 'r')
		content = f.read()
		print >> sys.stderr, '%s' % content
	elif (addr == 'edit'):
		f = open('edit.html', 'r')
		content = f.read()
		print >> sys.stderr, '%s' % content
	elif (addr == 'main'):
		f = open('main.html', 'r')
		content = f.read()
		print >> sys.stderr, '%s' % content
	else:
		content = 'Hello world! Page not found'

	return (200, content)

# handling response, combining content
def sendResponse(conn, content):
	template = responseHeaders[content[0]]
	data = template % content[1]
	conn.sendall(data)

# parse request
def parseRequest(conn):
	data = conn.recv(4096)
	if not data:
		print >> sys.stderr, 'Bad request: no data'
		return ''
	line = data[0:data.find("\r")]
	
	#print line
	#header format = data[0:data.find("\r\n\r\n")]
	print >> sys.stderr, 'Data collected: %s' % line

	method, uri, protocol = line.split()


	return uri

def main():
	serverAddress = ('localhost', 10001)
	server = socketServer(serverAddress)
	print >> sys.stderr, 'server is starting on %s port %s' % serverAddress

	#connected		
	try:	
		while True: 	
			conn, addr = server.accept()

			# checking connected client ip address
			print >> sys.stderr, 'client connected with ip :  %s' % str(addr)
			
			# parsing uri request
			uri = parseRequest(conn)
			print >> sys.stderr, 'URI accessed : %s' % uri

			# handling URI and print suitable pages
			content = routingHandler(uri)

			# send response
			sendResponse(conn, content)

			conn.close()
	
	except KeyboardInterrupt:
		print >> sys.stderr, 'keyboardInterrupt exception'
				
    	     
	server.close()
	

if __name__ == '__main__':
    main()
