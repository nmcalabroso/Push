import socket
import time
import sys
import select
import simplejson as json
from server.world import GameWorld

delay = 0.003
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
		except socket.error as e:
			print "Server error!",e
			sys.exit(1)

	def send_message(self,message,target_client):
		to_json = json.dumps(message)
 		try:
 			target_client.send(to_json)
 		except socket.error:
 			print "Server error: Sending..."
 			self.close(target_client)
 		time.sleep(delay*0.5)

	def receive_message(self,client):
		try:
			msg = client.recv(buffer_size)
		except socket.error:
 			print "Server error: Receiving..."
 			self.close(client)
 			return None

		if  msg is not None and len(msg) is 0:
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
		player[1] = name
		self.send_message(name,remote_socket)
		self.world.add_player(player)

	def close(self,client):
		addr = client.getpeername()
		client.close()
		print "%s has  disconnected" % addr[0]
		clientsname = addr[0]+"!"+str(addr[1])
		self.clients.remove(client)
		self.world.delete_game_object(clientsname)

	def shutdown(self):
		print "\nPUSH admin: Server is shutting down..."
		sys.exit(1)

	def start(self,backlog=5): #main loop
		self.my_socket.listen(backlog)
		self.clients.append(self.my_socket)
		cont = True
		try:
			while cont:
				time.sleep(delay)
				inputr, outputr, exceptr = select.select(self.clients,[],[])
				for s in inputr:
					if s is self.my_socket:
						self.accept()
					else:
						self.data = self.receive_message(s) #receive json from client in inputr
						if self.data:
							self.world.update(self.data)
							my_world = self.world.get() #get all game object
							if not self.world.is_over():
								state = "GAME"
							else:
								state = "END"
								cont = False

							my_msg = [my_world,state]
							self.send_message(my_msg,s)

			print "Round ended. Please restart."
			self.shutdown()
		except KeyboardInterrupt:
			self.shutdown()