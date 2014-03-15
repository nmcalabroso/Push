from gameobject import GameObject
from resources import Resources
from connection import Connection
from game.player import Player


class GameManager(GameObject):

	def __init__(self,*args,**kwargs):
		super(GameManager,self).__init__(name = 'manager',
									img = Resources.sprites['no_sprite'],
									*args,**kwargs)
		self.game_objects = [] #gameobject pool
		self.widgets = [] #gui pool
		self.labels = [] #label pool
		self.window = None
		self.active = True
		self.visible = False
		self.state = Resources.states['TITLE']
		self.focus = None
		self.set_focus(self.find_widget('text_ip'))
		self.my_connection = Connection()

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

		self.delete_widgets_by_batch(batch)
		self.delete_labels_by_batch(batch)

		self.delete_widgets_by_batch(Resources.batches['host'])
		self.delete_labels_by_batch(Resources.batches['host'])	

		self.delete_widgets_by_batch(Resources.batches['join'])
		self.delete_labels_by_batch(Resources.batches['join'])

		self.state = Resources.states['GAME']

	def set_player_data(self):
		if self.state == Resources.states['JOIN']:
			#player = Player(actual_name='sample',name='192.168.0.104',img = Resources.sprites['char_air'], x = 100, y = 200)

			text_ip = self.find_widget('text_ip')
			text_port = self.find_widget('text_port')
			text_name = self.find_widget('text_name')

			ip_address = '192.168.0.107'#text_ip.document.text
			port_num = 8080#int(text_port.document.text)
			name = text_name.document.text
			self.my_connection.connect_client((ip_address,port_num))

			player_class = "air"
			player_x = 100
			player_y = 200
			player_actual_name = "actual"
			player_name = "id"

			player_attr = [player_class,(player_x,player_y),player_actual_name,player_name]

			self.my_connection.send_message(player_attr)

		else:
			text_port = self.find_widget('text_port1')
			text_name = self.find_widget('text_name1')

			ip_address = "None"
			port_num = text_port.document.text
			name = text_name.document.text
			x,y = Resources.starting_points['char_air']

			my_player = Player(name = "host_player",
							actual_name = name,
							x = x,
							y = y,
							img = Resources.sprites['char_air']
							)

			self.add_game_object(my_player)
			self.window.push_handlers(my_player)
			
		print "IP Address:",ip_address
		print "Port:",port_num
		print "Name:",name
		print self.game_objects

	def switch_to_end(self):
		pass

	def set_player_names(self):
		pass
		
	def set_window(self,window):
		self.window = window

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

	def update(self,dt):
		if self.state == Resources.states['GAME']:
			player_attr = self.my_connection.receive_message()
			if player_attr != '':
				player_class,player_coordinates,player_actual_name,player_name = player_attr
				player = Player(actual_name=player_actual_name,name=player_name,img = Resources.sprites['char_air'], x = player_coordinates[0], y = player_coordinates[1])
				self.add_game_object(player)
				# self.window.push_handlers(player)
				for obj in self.get_game_objects():
					obj.update(dt)

				# print player.keys['up']
				# if player.keys['up'] == True or player.keys['down'] == True or player.keys['left'] == True or player.keys['right'] == True:
				# 	print 'asdkflasjdf'
				# 	self.delete_game_object_by_batch()
