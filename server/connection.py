import socket
import time
import sys
import select
import simplejson

delay = 0
buffer_size = 2000

class Server:
	def __init__(self,port):
		self.clients = []
		self.data = None

		#Server Socket
		self.my_socket = socket.socket()
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			print 'Binding address...'
			self.my_socket.bind(('',port))
		except Exception as e:
			print "Server error!",e
			sys.exit(1)

	def send_message(self,target_client,message):
		pass

	def receive_message(self,client):
		pass

	def accept(self):
		remote_socket, addr = self.my_socket.accept()
		print "Client "+ addr[0] +" has connected."
		self.clients.append(remote_socket)

	def close(self,client):
		addr = client.getpeername()
		print "%s has  disconnected" % addr[0]
		self.clients.remove(client)

	def start(self,backlog=5): #main loop
		self.my_socket.listen(backlog)
		while True:
			time.sleep(delay)
			inputr, outputr, exceptr = select.select(self.clients, [], [])
			for s in inputr:
				if s is self.my_socket:
					self.accept()
				else:
					self.data = s.recv(buffer_size)
					if len(self.data) == 0:
						self.close(s)
					else:
						self.receive_message(s)