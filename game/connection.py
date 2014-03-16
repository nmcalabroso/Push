import socket
import simplejson as json

class Connection:
	def __init__(self):
		self.my_socket = socket.socket()
		self.test = ''

	def connect_client(self, configs):
		self.my_socket.connect(configs)

	def join_server(self,configs):
		pass

	def send_message(self,message):
		to_json = json.dumps(message)
		self.test = to_json
 		self.my_socket.send(to_json)

	def receive_message(self):
		to_string = self.test#self.my_socket.recv(1024)
		if len(to_string) > 0:
			return json.loads(to_string)
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
