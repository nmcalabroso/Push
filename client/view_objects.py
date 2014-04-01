from game.gameobject import GameObject
from pyglet.window import key
from pyglet.sprite import Sprite
from game.resources import Resources

class Player(GameObject):
	def __init__(self,actual_name,name,typex,*args,**kwargs):
		super(Player,self).__init__(name = name,*args,**kwargs)
		self.actual_name = actual_name
		self.name = name
		self.type = typex
		self.active_key = None

		self.bounce = 5
		self.power = 5
		self.push_sfx = Resources.audio['push_all']
		self.push_all = Sprite(x = self.x,
							y = self.y,
							img = Resources.sprites['push_all'])
		self.push_all.visible = False


	def set_data(self,typex,actual_name,name):
		self.type = typex
		self.actual_name = actual_name
		self.name = name

	def get(self):
		#returns the json format of the player
		return [self.actual_name,self.name,self.type,[self.x,self.y]]

	def represent(self):
		#returns the regular json format for the position of the player
		self.push_all.x = self.x
		self.push_all.y = self.y
		my = [self.name,self.active_key]
		if self.active_key == key.SPACE:
			self.active_key = None
		return my

	def on_key_press(self,symbol,modifiers):
		self.active_key = int(symbol)
		if self.active_key == key.SPACE and self.power > 0:
			self.push_sfx.play()
			self.push_all.visible = True

	def on_key_release(self,symbol,modifiers):
		self.active_key = None
		self.push_all.visible = False

	def update(self,dt):
		pass

class Upgrade(GameObject):
	def __init__(self,name,typex,*args,**kwargs):
		super(Upgrade,self).__init__(name = name,*args,**kwargs)
		self.name = name
		self.type = typex