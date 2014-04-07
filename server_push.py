from server.connection import Server

def main():
	print "PUSH! Server"
	#ort = int(raw_input('Enter port number:'))
	port = 8000
	print "Initializing..."
	s = Server(port)
	print "Set-up complete."
	print "Server starting..."
	s.start()

if __name__ == '__main__':
	main()