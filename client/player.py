from game.gameobject import GameObject
from game.resources import Resources
from pyglet.window import key

class Player(GameObject):
	def __init__(self,actual_name,name,typex,*args,**kwargs):
		super(Player,self).__init__(name = name,*args,**kwargs)
		self.actual_name = actual_name
		self.name = name
		self.type = typex
		self.key = None

	def set_data(self,typex,actual_name,name):
		self.type = typex
		self.actual_name = actual_name
		self.name = name

	def get(self):
		#returns the json format of the player
		return [self.actual_name,self.name,self.type,[self.x,self.y]]

	def represent(self):
		#returns the regular json format for the position of the player
		return [self.name,self.key]

	def on_key_press(self,button,modifiers):
		pass

	def update(self,dt):
		pass