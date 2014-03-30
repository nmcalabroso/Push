from gameobject import GameObject
from pyglet.window import key
import resources

class Player(GameObject):
	def __init__(self,actual_name,name,world,type,*args,**kwargs):
		super(Player,self).__init__(name = name,*args,**kwargs)
		self.world = world
		self.actual_name = actual_name
		self.tempx = self.x
		self.tempy = self.y
		self.velocity_x = 5
		self.velocity_y = 5
		self.type = type

		self.bounce = 5 #life
		self.power = 5 #pushing power
		self.status = 0 #0 - normal; 1 - dead; 2 - being pushed


	def is_hit(self, obj):
		if self.active:
			actual_distance = resources.get_distance(self.position,obj.position)
			collision_distance = 0.5*(self.width+obj.width)
			print "actual distance of "+self.actual_name+" and "+obj.actual_name+":",actual_distance
			return actual_distance <= collision_distance

	def is_colliding(self):
		lst = []
		for obj in self.world.game_objects:
			if self.is_hit(obj):
				lst.append(obj)
		return lst

	def set_velocity(self,velocity_x = 1, velocity_y = 1):
		self.velocity_x = velocity_x
		self.velocity_y = velocity_y

	def die(self):
		self.status = 1

	def to_pushed(self):
		self.status = 2

	def change_power(self,dp):
		self.power += dp

	def to_continue(self):
		for obj in self.world.game_objects:
			if obj.name != self.name:
				if obj.is_hit(self):
					return False
		return True
				
	def move(self,keyx):
		self.tempx,self.tempy = self.x,self.y

		if keyx == key.UP:
			self.tempy += self.velocity_y
		elif keyx == key.RIGHT:
			self.tempx+=self.velocity_x
		elif keyx == key.DOWN:
			self.tempy-=self.velocity_y
		elif keyx == key.LEFT:
			self.tempx-=self.velocity_x

		if self.to_continue():
			self.x,self.y = self.tempx,self.tempy

	def push_collide(self):
		to_push = self.is_colliding()
		for enemy in to_push:
			enemy.set_status(2)

	def update(self):
		#colliding_obj = self.is_colliding()
		if self.status == 0:
			pass
		elif self.status == 1:
			pass
		elif self.status == 2:
			pass

	def get(self):
		#returns the json format of the player
		return [self.actual_name,self.name,self.type,[self.x,self.y]]

class AirBender(Player):
	def __init__(self,actual_name,name,world,*args,**kwargs):
		super(AirBender,self).__init__(actual_name = actual_name,name = name,world = world,type = 'air',*args,**kwargs)
		#self.x,self.y = Resources.starting_points['char_air']

class EarthBender(Player):
	def __init__(self,actual_name,name,world,*args,**kwargs):
		super(EarthBender,self).__init__(actual_name = actual_name,name = name,world = world,type = 'earth',*args,**kwargs)
		#self.x,self.y = Resources.starting_points['char_earth']

class FireBender(Player):
	def __init__(self,actual_name,name,world,*args,**kwargs):
		super(FireBender,self).__init__(actual_name = actual_name,name = name,world = world,type = 'fire',*args,**kwargs)
		#self.x,self.y = Resources.starting_points['char_fire']

class WaterBender(Player):
	def __init__(self,actual_name,name,world,*args,**kwargs):
		super(WaterBender,self).__init__(actual_name = actual_name,name = name,world = world,type = 'water',*args,**kwargs)
		#self.x,self.y = Resources.starting_points['char_water']
