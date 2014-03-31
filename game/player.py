from gameobject import GameObject
from pyglet.window import key
from math import cos,sin
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
		self.accelaration_x = 0
		self.accelaration_y = 0
		self.angle = 0
		self.type = type

		self.bounce = 5 #life
		self.power = 5 #pushing power
		self.status = 3 #0 - moving; 1 - dead; 2 - being pushed; 3 - stop

	def is_wall(self,mode = 'move'):
		if self.active:
			if mode == 'move':
				pt = (self.tempx,self.tempy)
			else:
				pt = self.position

			if pt[0]-(self.width*0.5) <= 0 or pt[0]+(self.width*0.5) >= resources.Resources.window_width:
				return True

			if pt[1]-(self.height*0.5) <= 0 or pt[1]+(self.height*0.5) >= resources.Resources.window_height:
				return True
				
			return False

	def is_hit(self, obj, mode = 'move'):
		if self.active:
			if mode == 'move':
				pt1 = (obj.tempx,obj.tempy)
			else:
				pt1 = obj.position

			actual_distance = resources.get_distance(self.position,pt1)
			collision_distance = 0.5*(self.width+obj.width)
			return actual_distance <= collision_distance

	def set_velocity(self,velocity_x = 1, velocity_y = 1):
		self.velocity_x = velocity_x
		self.velocity_y = velocity_y

	def die(self):
		self.status = 1

	def stop(self):
		self.stop = 3

	def to_be_pushed(self,angle):
		self.angle = angle
		self.status = 2

	def change_power(self,dp):
		self.power += dp

	def to_continue(self):
		for obj in self.world.game_objects:
			if obj.name != self.name:
				if obj.is_hit(self):
					return False

		if self.is_wall():
			return False

		return True
				
	def key_press(self,keyx):
		self.tempx,self.tempy = self.x,self.y

		if keyx == key.UP or keyx == key.RIGHT or keyx == key.DOWN or keyx == key.LEFT:
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
		else:
			if keyx == key.SPACE:
				self.push_collide()

	def move(self):
		pass

	def push_collide(self):
		for obj in self.world.game_objects:
			if obj.name != self.name:
				obj.to_be_pushed(resources.get_angle_between(self.position,obj.position))

	def update(self):
		#colliding_obj = self.is_colliding()
		if self.status == 0: #moving
			pass
		elif self.status == 1: #dead
			pass
		elif self.status == 2: #being push
			self.x += self.velocity_x*cos(self.angle)
			self.y += self.velocity_y*sin(self.angle)

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
