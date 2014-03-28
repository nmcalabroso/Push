from gameobject import GameObject
from game.resources import Resources
from pyglet.window import key

class Player(GameObject):
	def __init__(self,actual_name,name,type,*args,**kwargs):
		super(Player,self).__init__(name = name,*args,**kwargs)
		self.actual_name = actual_name
		self.velocity_x = 3
		self.velocity_y = 3
		self.type = type

		self.keys = {}
		self.keys['up'] = False
		self.keys['down'] = False
		self.keys['right'] = False
		self.keys['left'] = False 

	def is_colliding(self,x,y):
		if self.active:
			if x > (self.x - (self.width*0.5)) and x < (self.x + (self.width*0.5)):
				if y > (self.y - self.height*0.5) and y < (self.y + (self.height*0.5)):
					return True
		return False

	def set_velocity(self,velocity_x = 1, velocity_y = 1):
		self.velocity_x = velocity_x
		self.velocity_y = velocity_y

	def move(self,key):
		print "Key:",key

	def on_key_press(self,symbol,modifiers):
		if symbol == key.LEFT:
			self.keys['left'] = True
		elif symbol == key.UP:
			self.keys['up'] = True
		elif symbol == key.RIGHT:
			self.keys['right'] = True
		elif symbol == key.DOWN:
			self.keys['down'] = True

	def on_key_release(self,symbol,modifiers):
		if symbol == key.LEFT:
			self.keys['left'] = False
		elif symbol == key.UP:
			self.keys['up'] = False
		elif symbol == key.RIGHT:
			self.keys['right'] = False
		elif symbol == key.DOWN:
			self.keys['down'] = False
	
	def update(self,dt):
		if self.keys['left']:
			self.x -= self.velocity_x
		elif self.keys['up']:
			self.y += self.velocity_y
		elif self.keys['right']:
			self.x += self.velocity_x
		elif self.keys['down']:
			self.y -= self.velocity_y
		#print "x,y",(self.x,self.y)

class AirBender(Player):
	def __init__(self,actual_name,name,*args,**kwargs):
		super(AirBender,self).__init__(actual_name = actual_name,name = name,type = 'air',*args,**kwargs)
		#self.x,self.y = Resources.starting_points['char_air']

class EarthBender(Player):
	def __init__(self,actual_name,name,*args,**kwargs):
		super(EarthBender,self).__init__(actual_name,name,type = 'earth',*args,**kwargs)
		#self.x,self.y = Resources.starting_points['char_earth']

class FireBender(Player):
	def __init__(self,actual_name,name,*args,**kwargs):
		super(FireBender,self).__init__(actual_name,name,type = 'fire',*args,**kwargs)
		#self.x,self.y = Resources.starting_points['char_fire']

class WaterBender(Player):
	def __init__(self,actual_name,name,*args,**kwargs):
		super(WaterBender,self).__init__(actual_name,name,type = 'water',*args,**kwargs)
		#self.x,self.y = Resources.starting_points['char_water']
