from game.gameobject import GameObject
from game.resources import Resources
from connection import Connection
from client.player import Player
from random import randint
from random import choice

class GameManager(GameObject):

	def __init__(self,*args,**kwargs):
		super(GameManager,self).__init__(name = 'manager',
									img = Resources.sprites['no_sprite'],
									*args,**kwargs)
		
		self.me = None

		self.game_objects = [] #gameobject pool
		self.widgets = [] #gui pool
		self.labels = [] #label pool
		
		self.media = None
		self.window = None
		self.active = True
		self.visible = False
		
		self.state = Resources.states['TITLE']
		self.focus = None
		self.set_focus(self.find_widget('text_ip'))
		self.my_connection = Connection()

	#State transitions
	def switch_to_setup(self,batch):
		bg = self.find_widget('my_bg')
		bg.set_image(Resources.sprites['setup_bg'])
		self.delete_widgets_by_batch(batch)
		self.state += 1

	def switch_to_host(self,batch):
		self.delete_widgets_by_batch(batch)
		self.state += 1

	def switch_to_join(self,batch):
		self.delete_widgets_by_batch(batch)
		self.state += 2

	def switch_to_game(self,batch):
		bg = self.find_widget('my_bg')
		bg.set_image(Resources.sprites['game_bg'])
		self.set_player_data()

		self.delete_widgets_by_batch(Resources.batches['host'])
		self.delete_labels_by_batch(Resources.batches['host'])	

		self.delete_widgets_by_batch(Resources.batches['join'])
		self.delete_labels_by_batch(Resources.batches['join'])

		self.state = Resources.states['GAME']
		self.media.next()
		self.media.eos_action = self.media.EOS_LOOP

	def switch_to_end(self):
		pass

	def set_player_data(self):
		if self.state == Resources.states['JOIN']:
			#connect to server mode
			text_ip = self.find_widget('text_ip')
			text_port = self.find_widget('text_port')
			text_name = self.find_widget('text_name')

			ip_address = text_ip.document.text
			port_num = int(text_port.document.text)
			name = text_name.document.text
		else:
			#debug mode
			#text_ip = "127.0.0.1"
			text_ip = "192.168.254.103"
			text_port = "8080"
			text_name = "DebugX"

			ip_address = text_ip
			port_num = int(text_port)
			name = text_name
			
			
		#attributes
		player_class = choice(Resources.types)
		player_x,player_y = randint(5+34,Resources.window_width-(5+34)),randint(5+34,Resources.window_height-(5+34))
		player_actual_name = name

		#connect to server
		self.my_connection.join_server((ip_address,port_num))

		self.me.set_data(player_class,player_actual_name,"temp")
		self.me.x,self.me.y = player_x,player_y
		
		#register player to server
		print "me:",self.me.get()
		print "Sending player..."
		if self.my_connection.send_message(self.me.get()) is None:
			self.me.name = self.my_connection.receive_message()
			print "Complete!"
		else:
			print "Error!"

		#socket details
		print "IP Address:",ip_address
		print "Port:",port_num
		print "Name:",name

	#Utilities
	def set_client(self,player):
		self.me = player

	def set_window(self,window):
		self.window = window

	def set_media(self,media):
		self.media = media
		self.media.volume = 0.75
		self.media.play()

	def set_focus(self,focus):
		if self.focus:
			self.focus.caret.visible = False
			self.focus.caret.mark = self.focus.caret.position = 0
		
		self.focus = focus
		
		if self.focus:
			self.focus.caret.visible = True
			self.focus.caret.mark = 0
			self.focus.caret.position = len(self.focus.document.text)

	def add_game_object(self,obj):
		obj.active = True
		self.game_objects.append(obj)

	def find_game_objects(self,name):
		found_objects = []
		for obj in self.game_objects:
			if obj.name == name:
				found_objects.append(obj)
		return found_objects

	def find_game_object(self,name):
		for obj in self.game_objects:
			if obj.name == name:
				return obj
		return None
 
	def get_game_objects(self,active = True):
		new_pool = []
		for obj in self.game_objects:
			if active and obj.active:
				new_pool.append(obj)
			elif not active and not obj.active:
				new_pool.append(obj)
		return new_pool

	def get_objects_by_batch(self,batch):
		new_pool = []
		for obj in self.game_objects:
			if obj.batch is batch:
				new_pool.append(obj)

	def delete_game_object(self,name):
		for i in range(len(self.game_objects)):
			if self.game_objects[i].name == name:
				obj = self.game_objects[i]
				obj.delete()
				del self.game_objects[i]
				break

	def delete_game_object_by_batch(self):
		for i in range(len(self.game_objects)):
			obj = self.game_objects[i]
			obj.delete()
			del self.game_objects[i]

	def add_label(self,label):
		self.labels.append(label)

	def find_label(self,name):
		for label in self.labels:
			if label.name == name:
				return label

	def delete_label(self,text):
		for i in range(len(self.labels)):
			if self.labels[i].text == text:
				label = self.labels[i]
				label.delete()
				del self.labels[i]
				break

	def get_labels(self,batch):
		new_labels = []
		for label in self.labels:
			if label.batch is batch:
				new_labels.append(label)

	def delete_labels_by_batch(self,batch):
		delete_labels = []
		for label in self.labels:
			if label.batch is batch:
				delete_labels.append(label)

		for label in delete_labels:
			self.window.remove_handlers(label)
			label.delete()
			self.labels.remove(label)

	def update_label(self,text,newtext):
		label = self.find_label(text)
		label.text = newtext

	def add_widget(self,widget):
		widget.active = True
		self.widgets.append(widget)

	def find_widget(self,name):
		for widget in self.widgets:
			if widget.name == name:
				return widget
		return None

	def get_widgets(self,active = True):
		new_pool = []
		for obj in self.widgets:
			if obj.name != 'my_bg':
				if active and obj.active:
					new_pool.append(obj)
				elif not active and not obj.active:
					new_pool.append(obj)
		return new_pool

	def get_text_widgets(self,active = True):
		new_pool = []
		for obj in self.widgets:
			if obj.name != 'my_bg' and obj.__class__.__name__ == 'TextWidget':
				if active and obj.active:
					new_pool.append(obj)
				elif not active and not obj.active:
					new_pool.append(obj)
		return new_pool

	def get_widgets_by_batch(self,batch):
		new_pool = []
		for widget in self.widgets:
			if widget.batch is batch:
				new_pool.append(widget)		

	def delete_widget(self,name):
		for i in range(len(self.widgets)):
			if self.widgets[i].name == name:
				widget = self.widgets[i]
				widget.delete()
				del self.widgets[i]
				break

	def delete_widgets_by_batch(self,batch):
		delete_widgets = []
		for widget in self.widgets:
			if widget.batch is batch and widget.name != 'my_bg':
				delete_widgets.append(widget)

		for widget in delete_widgets:
			self.window.remove_handlers(widget)
			widget.delete()
			self.widgets.remove(widget)

	def on_mouse_motion(self,x,y,dx,dy):
		self.window.set_mouse_cursor(None)

	#Game Logic
	def update(self,dt):
		if self.state == Resources.states['GAME']:
			self.my_connection.send_message(self.me.represent()) #change HAHAHA to ['name',key]
			world_objects = self.my_connection.receive_message() #receive message in format of [['type',[pos_x,pos_y],'actual_name']...list of objects]
			if world_objects is not None:
				x = len(world_objects)
				y = len(self.game_objects)
				diff = x - y
				if diff >= 0:
					#creating of new objects
					for i in range(diff):
						print "creating..."
						obj = world_objects[i+y]
						self.add_game_object(Player(actual_name = obj[0],
													name = obj[1],
													typex = obj[2],
													img = Resources.sprites['char_'+obj[2]],
													x = obj[3][0],
													y = obj[3][1]))
				else:
					#deletion of deleted game objects
					print "deleting..."
					for i in range(len(world_objects)):
						while world_objects[i][1] != self.game_objects[i].name:
							self.delete_game_object(self.game_objects[i].name)






