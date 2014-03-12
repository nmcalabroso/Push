from server.connection import Server

def main():
	print "PUSH! Server"
	port = int(raw_input('Enter port number:'))
	print "Initializing..."
	s = Server(port)
	print "Set-up complete."
	print "Server starting..."
	s.start()

if __name__ == '__main__':
	main()