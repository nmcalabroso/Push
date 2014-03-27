import socket
import time
import sys
import select
from server.world import GameWorld
import simplejson as json

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
		msg = client.recv(buffer_size)

		if len(msg) is 0:
			self.close(client)
			return None

		return json.loads(msg)

	def accept(self):
		remote_socket, addr = self.my_socket.accept()
		self.clients.append(remote_socket)
		name = addr[0] + "!" + str(addr[1])
		print "Client "+ name +" has connected."
		
		print "Creating game object..."
		player = self.receive_message(remote_socket)
		player.append(name)
		self.world.add_player(player)
		print "OK!"
		self.send_message(remote_socket,"OK!")

	def close(self,client):
		addr = client.getpeername()
		print "%s has  disconnected" % addr[0]
		self.clients.remove(client)
		#self.world.delete_game_object(clientsname)

	def start(self,backlog=5): #main loop
		self.my_socket.listen(backlog)
		self.clients.append(self.my_socket)
		while True:
			time.sleep(delay)
			print "Before waiting..."
			print "clients:",self.clients
			inputr, outputr, exceptr = select.select(self.clients,[],[])
			for s in inputr:
				if s is self.my_socket:
					self.accept()
				else:
					self.data = self.receive_message(s) #receive json from client in inputr
					obj = self.world.find_game_object(self.data[0]) #get obj that has name data[0]
					obj.move(self.data[1]) #move obj according to the sent key
					msg = self.world.get()
					print "msg:",msg
					self.send_message(s,msg)