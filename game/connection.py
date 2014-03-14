import socket

class Connection:
	def __init__(self):
		self.my_socket = socket.socket()

	def connect_client(self, configs):
		self.my_socket.connect(configs)

	def join_server(self,configs):
		pass

	def send_message(self,message):
		pass

	def receive_message(self):
		pass

# class _myConnection(object):

# 	def __init__(self, s):
# 		self.socket = s

# 	def sendMessage(self, msg):
# 		return self.socket.send(msg)

# 	def getMessage(self):
# 		return self.socket.recv(1024)

# def connection(s):
# 	return _myConnection(s)
