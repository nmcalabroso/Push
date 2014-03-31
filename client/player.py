from game.gameobject import GameObject
from pyglet.window import key

class Player(GameObject):
	def __init__(self,actual_name,name,typex,*args,**kwargs):
		super(Player,self).__init__(name = name,*args,**kwargs)
		self.actual_name = actual_name
		self.name = name
		self.type = typex
		self.active_key = None

	def set_data(self,typex,actual_name,name):
		self.type = typex
		self.actual_name = actual_name
		self.name = name

	def get(self):
		#returns the json format of the player
		return [self.actual_name,self.name,self.type,[self.x,self.y]]

	def represent(self):
		#returns the regular json format for the position of the player
		my = [self.name,self.active_key]
		if self.active_key == key.SPACE:
			self.active_key = None
		return my

	def on_key_press(self,symbol,modifiers):
		self.active_key = int(symbol)

	def on_key_release(self,symbol,modifiers):
		self.active_key = None

	def update(self,dt):
		pass