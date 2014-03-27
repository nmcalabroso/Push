import socket
import simplejson as json
from time import sleep

buffer_size = 4096
delay = 1

class Connection:
	def __init__(self):
		self.my_socket = socket.socket()
		#self.my_socket.setblocking(0)
		self.test = ''

	def connect_client(self, configs):
		self.my_socket.connect(configs)

	def join_server(self,configs):
		self.my_socket.connect(configs)
		print "Connection established!"

	def send_message(self,message):
		to_json = json.dumps(message)
 		a = self.my_socket.sendall(to_json)
 		sleep(delay)
 		return a

	def receive_message(self):
		to_string = ''
		try:
			to_string = self.my_socket.recv(buffer_size)
		except socket.error as e:
			print "Client: Receiving error."
			print "Error:",e
		if len(to_string) > 0:
			lst = json.loads(to_string)
			lst.append('name') #temporary
			return lst
		return ''

# class _myConnection(object):

# 	def __init__(self, s):
# 		self.socket = s

# 	def sendMessage(self, msg):
# 		return self.socket.send(msg)

# 	def getMessage(self):
# 		return self.socket.recv(1024)

# def connection(s):
# 	return _myConnection(s)
