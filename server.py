import socket
import threading
import os
import sys
import webbrowser

from PDU import PDU

# setting up response header
responseHeaders = {}

responseHeaders[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: %s

%s
"""

responseHeaders[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s


"""

responseHeaders[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

# TODO Handling local CSS and Javascript file

# setting mime types
mimeTypes = {
	'.jpg': 'image/jpg',
	'.gif': 'image/gif',
	'.png': 'image/png',
	'.html': 'text/html',
	'.pdf': 'application/pdf',
	'.css': 'text/css',
	'.js': 'application/javascript'}

# getMime
def getMime(uri):
	return mimeTypes.get(os.path.splitext(uri)[1], 'text/plain')

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
def routingHandler(pduResult):

	# remove beginning /
	addr = pduResult.uri[1:].lower()
	fsource = ''
	content = ''
	mime = 'text/html'

	print >> sys.stderr, 'URI accessed trimmed : %s' % addr
	
	if (addr == ''):
		fsource = 'index.html'
	elif (addr == 'edit'):
		fsource = 'edit.html'
	elif (addr == 'main'):
		fsource = 'main.html'
	elif (addr == 'style.css'):
		fsource = 'style.css'

	if (pduResult.req_type != "POST"):
		if (fsource != ''):
			f = open(fsource, 'r')
			mime = getMime(fsource)
			content = f.read()
			f.close()
		else: 
			content = 'Hello world! Page not found'
	else:
		if (addr == 'createdoc'):
			createDocument(pduResult.content.strip(), "test-address")

	return (200, content, mime)

# handling response, combining content
def sendResponse(conn, content):
	template = responseHeaders[content[0]]
	data = template % (content[2],content[1])
	conn.sendall(data)

# parse request
def parseRequest(conn):
	data = conn.recv(4096)
	print 

	if not data:
		print >> sys.stderr, 'Bad request: no data'
		return ''

	line = data[0:data.find("\r")]
	
	#print line
	#header format = data[0:data.find("\r\n\r\n")]
	print >> sys.stderr
	print >> sys.stderr, "==================================================================="
	print >> sys.stderr, PDU(data)
	print >> sys.stderr, "==================================================================="
	print >> sys.stderr	

	return PDU(data)

def createDocument(name, address):	
	# default response is ok
	response = 200

	# try catch 
	try:
		f = open("files/%s-%s.txt" % (name, address), "w+")
		f.close()
	except:
		print >> sys.stderr, 'Error : %s' % sys.exc_info()[0]

def openDocument(doc):
	return 

# ===================================================================
# main application here
# ===================================================================
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
			pduResult = parseRequest(conn)
			print >> sys.stderr, 'URI accessed : %s' % pduResult.uri

			# finding request type
			print >> sys.stderr, 'Access type : %s' % pduResult.req_type

			# handling URI and print suitable pages
			content = routingHandler(pduResult)

			# send response
			sendResponse(conn, content)

			conn.close()
	# handling keyboard interrupt
	except KeyboardInterrupt:
		print >> sys.stderr, 'keyboardInterrupt exception'
				
    	     
	server.close()
	

if __name__ == '__main__':
    main()
