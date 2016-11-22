import socket
import threading
import os
import sys
import webbrowser
import random
import time

# there's some problem with the parser
from PDU import PDU



serverAddress = ('localhost', 10001)

# setting up response header
responseHeaders = {}

responseHeaders[200] =\
"""HTTP/1.0 200 OK
Server: ws30
Content-type: %s
Set-Cookie: %s

%s
"""

responseHeaders[301] =\
"""HTTP/1.0 301 Move
Server: ws30
Content-type: %s
Location: %s

%s
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
def routingHandler(pduResult, session, conn, addr):

	# remove beginning /
	addr = pduResult.uri.split('/')

	content = ''
	fsource = ''

	#not working for god sake 
	cookie = setCookie("__session", session)
	mime = 'text/html'
	
	if (addr[1] == ''):
		fsource = 'index.html'
	elif (addr[1] == 'edit'):
		fsource = 'edit.html'
	elif (addr[1] == 'main'):
		fsource = 'main.html'
	elif (addr[1] == 'style.css'):
		fsource = 'main.html'

	if (pduResult.req_type != "POST"):
		if (fsource != ''):
			f = open(fsource, 'r')
			mime = getMime(fsource)
			content = f.read()
			f.close()
		else: 
			content = 'Hello world! Page not found'

		if (mime != "text/html"):
			cookie = ''	

		component = (200, content, mime, cookie)
		sendResponse(conn, component)

	else:
		if (addr[1] == 'createdoc'):
			createDocument(pduResult.content.strip(), "test-address")


		if (addr[1] == 'signin'):

			username = pduResult.content.strip().lower()
			content = 'http://localhost:10001/main/%s' % username 

			#create folder of the user if previously not exist
			if not os.path.exists("files/" + username):
				os.makedirs("files/" + username)

			component = (200, content, mime, cookie)
			sendResponse(conn, component)
			


# handling response, combining content
def sendResponse(conn, component):
	template = responseHeaders[component[0]]

	data = template % (component[2], component[3], component[1])
	#print >> sys.stderr, 'send response data :'
	#print >> sys.stderr, data

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
	# print >> sys.stderr, "==================================================================="
	# print >> sys.stderr, PDU(data)
	# print >> sys.stderr, "==================================================================="

	return PDU(data)

def setSession():
	# generate random hash
	randhash = random.getrandbits(128)
	return randhash


def setCookie(name, content):
	# sample: Set-Cookie: id=a3fWa; Expires=Wed, 21 Oct 2015 07:28:00 GMT; Secure; HttpOnly
	expiresYear = int(time.strftime("%Y")) + 10 
	expiresMonth = time.strftime("%a, %d %b")
	expiresTime = time.strftime("%X")

	cookie = "%s=%s; Expires=%s %s %s GMT; Secure; HttpOnly" % (name, content, expiresMonth, expiresYear, expiresTime)
	#print >> sys.stderr, 'Cookie content : %s' % cookie

	return cookie

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

def handler(conn, addr, session):

	#print >> sys.stderr, 'Session : %s' % session

	# parsing uri request
	pduResult = parseRequest(conn)
	print pduResult
	#print >> sys.stderr, 'URI accessed : %s' % pduResult.uri

	# handling URI and print suitable pages
	routingHandler(pduResult, session, conn, addr)

	conn.close()

# ===================================================================
# main application here
# ===================================================================
def main():
	
	server = socketServer(serverAddress)
	print >> sys.stderr, 'server is starting on %s port %s' % serverAddress

	#connected		
	try:	
		while True: 	
			conn, addr = server.accept()
			session = setSession()

			# checking connected client ip address
			print >> sys.stderr, 'client connected with ip :  %s' % str(addr)
	
			#start threading
			thrd = threading.Thread(target=handler, args=(conn, addr, session))

			try:
				thrd.start()
			except:
				print >> sys.stderr, 'exit thread'
				thrd.exit()

	# handling keyboard interrupt
	except KeyboardInterrupt:
		print >> sys.stderr, 'keyboardInterrupt exception'
				
    	     
	server.close()
	

if __name__ == '__main__':
    main()
