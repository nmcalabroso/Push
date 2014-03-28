import socket
import time
import sys
import select
from server.world import GameWorld
import simplejson as json

delay = 0.1
buffer_size = 4096

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
			#self.my_socket.setblocking(0)
		except Exception as e:
			print "Server error!",e
			sys.exit(1)

	def send_message(self,message,target_client):
		to_json = json.dumps(message)
 		#self.my_socket.send(to_json)
 		target_client.send(to_json)
 		time.sleep(delay*0.5)

	def receive_message(self,client):
		msg = client.recv(buffer_size)
		if len(msg) is 0:
			self.close(client)
			return None
		print "recv:",msg
		return json.loads(msg)

	def accept(self):
		remote_socket, addr = self.my_socket.accept()
		self.clients.append(remote_socket)
		name = addr[0] + "!" + str(addr[1])
		print "Client "+ name +" has connected."
		print "Creating game object..."
		player = self.receive_message(remote_socket)
		player[1] = name

		self.send_message(name,remote_socket)
		self.world.add_player(player)

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
			#print "Before waiting..."
			#print "clients:",self.clients
			inputr, outputr, exceptr = select.select(self.clients,[],[])
			for s in inputr:
				if s is self.my_socket:
					self.accept()
				else:
					self.data = self.receive_message(s) #receive json from client in inputr
					#obj = self.world.find_game_object(self.data[0]) #get obj that has name data[0]
					#if obj is not None:
						#obj.move(self.data[1]) #move obj according to the sent key
					my_msg = self.world.get() #get all game objects
					#print "gameobjects:",self.world.game_objects
					print "From world:",my_msg
					self.send_message(my_msg,s)