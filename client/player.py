from game.gameobject import GameObject
from game.resources import Resources
from pyglet.window import key

class Player(GameObject):
	def __init__(self,actual_name,name,*args,**kwargs):
		super(Player,self).__init__(name = name,*args,**kwargs)
		self.actual_name = actual_name
		self.name = name