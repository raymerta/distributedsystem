import socket
import threading
import os
import sys
import webbrowser

def main():
	sock = socket.socket()
	serverAddress = ('localhost', 10000)
	
	print >> sys.stderr, 'server is starting on %s port %s' % serverAddress
	sock.bind(serverAddress)

	#listen to maximum value
	sock.listen(5)

	#connected
	while True:
		conn, addr = sock.accept()

		print >> sys.stderr, 'client connected with ip :  %s' % str(addr)
		# thrd = threading.Thread(target=manageFile, args=("manageFile", conn ))
		# thrd.start()

		# try: 
		# 	print >> sys.stderr, 'client connected with ip :  %s' % str(addr)
		# 	thrd = threading.Thread(target=manageFile, args=("manageFile", conn ))
		# 	thrd.start()

		# except (KeyboardInterrupt, SystemExit):
		# 	print >> sys.stderr, 'Error KeyboardInterrupt or system exit'
		# 	sock.close()
		# except: 
		# 	print >> sys.stderr, 'other error'

		pageUrl = conn.recv(1024)
		
	
    		print 'rendering', pageUrl
		webbrowser.open_new_tab(pageUrl)
    	     
	sock.close()
	

if __name__ == '__main__':
    main()
