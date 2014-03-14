import socket
import time
import sys
import select
import simplejson as json
from server.world import GameWorld

delay = 0
buffer_size = 2000

class Server:
	def __init__(self,port):
		self.clients = []
		self.data = None
		self.world = GameWorld()

		#Server Socket
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
		self.world.add_player(addr[0])
		self.clients.append(remote_socket)

	def close(self,client):
		addr = client.getpeername()
		print "%s has  disconnected" % addr[0]
		self.clients.remove(client)

	def start(self,backlog=5): #main loop
		self.my_socket.listen(backlog)
		self.clients.append(self.my_socket)
		while True:
			time.sleep(delay)
			print "Before waiting..."
			print "clients:",self.clients
			inputr, outputr, exceptr = select.select(self.clients, [], [])
			print "inputr:",inputr
			for s in inputr:
				if s is self.my_socket:
					self.accept()
				else:
					self.data = s.recv(buffer_size)
					if len(self.data) == 0:
						self.close(s)
					else:
						self.receive_message(s)