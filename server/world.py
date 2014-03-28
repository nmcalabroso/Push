from game.gameobject import GameObject
from game.resources import Resources
from game.player import Player
from game.player import AirBender
from game.player import FireBender
from game.player import EarthBender
from game.player import WaterBender

class GameWorld(GameObject):

	def __init__(self,*args,**kwargs):
		super(GameWorld,self).__init__(name = 'World',img = Resources.sprites['no_sprite'], *args,**kwargs)
		self.game_state = Resources.states['GAME']
		self.game_objects = [] #gameobject pool
		self.widgets = [] #gui pool
		self.labels = [] #label pool

	def switch_to_end(self):
		pass

	def set_players(self):
		pass

	def add_player(self,player):
		print "player:",player
		
		actual_name = player[0]
		name_id = player[1]
		cl = player[2]
		x,y = player[3]

		if cl.lower() == 'air':
			p = AirBender(actual_name = actual_name,
						name = name_id,
						img = Resources.sprites['char_air'],
						x = x,
						y = y)
		elif cl.lower() == 'fire':
			p = FireBender(actual_name = actual_name,
						name = name_id,
						img = Resources.sprites['char_fire'],
						x = x,
						y = y)

		elif cl.lower() == 'earth':
			p = EarthBender(actual_name = actual_name,
						name = name_id,
						img = Resources.sprites['char_earth'],
						x = x,
						y = y)
		elif cl.lower() == 'water':
			p = WaterBender(actual_name = actual_name,
						name = name_id,
						img = Resources.sprites['char_earth'],
						x = x,
						y = y)

		self.add_game_object(p)

	def add_game_object(self,obj):
		obj.active = True
		self.game_objects.append(obj)

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

	def add_label(self,label):
		self.labels.append(label)

	def find_label(self,name):
		for label in self.labels:
			if label.name == name:
				return label

	def get_labels(self,batch):
		new_labels = []
		for label in self.labels:
			if label.batch is batch:
				new_labels.append(label)

	def delete_label(self,text):
		for i in range(len(self.labels)):
			if self.labels[i].text == text:
				label = self.labels[i]
				label.delete()
				del self.labels[i]
				break

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

	def get(self): #world representation
		wrld = []
		for obj in self.get_game_objects():
			#print "name:",obj.name
			if isinstance(obj,Player):
				#e = [obj.name,obj.type,[obj.x,obj.y]]
				wrld.append(obj.get())
		return wrld