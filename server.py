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

# ===================================================================
# networking section
# ===================================================================

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


	# home page
	if (addr[1] == ''):
		fsource = 'index.html'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()

		component = (200, content, mime, cookie)
		sendResponse(conn, component)

	# edit page style
	if (addr[1] == 'edit'):
		fsource = 'edit.html'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()

		component = (200, content, mime, cookie)
		sendResponse(conn, component)

	# main page
	if (addr[1] == 'main'):
		fsource = 'main.html'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()

		component = (200, content, mime, cookie)
		sendResponse(conn, component)

	# css
	if (addr[1] == 'style.css'):
		fsource = 'style.css'
		f = open(fsource, 'r')
		mime = getMime(fsource)
		content = f.read()
		f.close()

		component = (200, content, mime, cookie)
		sendResponse(conn, component)

	# get files inside folder
	if (addr[1] == '_folder'):
		username = addr[2]
		content = getAllFiles()

		component = (200, content, "text/plain", cookie)
		sendResponse(conn, component)

	# get document content
	if (addr[1] == '_document'):
		docname = addr[2]
		content = getDocContent(docname)

		component = (200, content, "text/plain", cookie)
		sendResponse(conn, component)


	if (addr[1] == 'docedit'):
		username = addr[2]
		docname = addr[3]

		doc = pduResult.content.strip()

		content = content = 'http://localhost:10001/main/%s' % username
		editContent(docname, doc)

		component = (200, content, mime, cookie)
		sendResponse(conn, component)

	# creating document
	if (addr[1] == 'createdoc'):
		username = pduResult.content.strip().split(":")[0]
		docname = pduResult.content.strip().split(":")[1]
		filename = '%s-%s' % (docname, username)

		content = 'http://localhost:10001/edit/%s/%s' % (username, filename)
		createDocument(username, docname)

		component = (200, content, mime, cookie)
		sendResponse(conn, component)

	# creating username
	if (addr[1] == 'signin'):

		username = pduResult.content.strip().lower()
		content = 'http://localhost:10001/main/%s' % username
		# communal sharing
		# createFolder(username)

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
# editing section
# ===================================================================

def getDocContent(filename):
	content = ''
	try:
		f = open("files/communal/%s.txt" % filename, 'r')
		content = f.read()
		f.close()
	except:
		print >> sys.stderr, 'Error : %s' % sys.exc_info()[0]

	return content

def editContent(filename, content):
	try:
		f = open("files/communal/%s.txt" % filename, 'w')
		f.write(content)
		f.close()
	except:
		print >> sys.stderr, 'Error : %s' % sys.exc_info()[0]

def createFolder(username):
	#create folder of the user if previously not exist
	if not os.path.exists("files/" + username):
		os.makedirs("files/" + username)


def createDocument(username, name):
	# try catch
	try:
		f = open("files/communal/%s-%s.txt" % (name, username), "w+")
		f.close()

		f = open("files/communal/%s-%s.md" % (name, username), "w+")
		f.close()
	except:
		print >> sys.stderr, 'Error : %s' % sys.exc_info()[0]

# get all files inside folder
def getAllFiles():

	files = []
	for file in os.listdir("files/communal"):
		if file.endswith(".txt"):
			files.append(file)

	return str(files).strip('[]')

def openDocument(doc):
	return


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
