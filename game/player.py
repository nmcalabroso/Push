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
		if mode == 'move':
			pt1 = (obj.tempx,obj.tempy)
			offset = 0
		elif mode == 'pushed':
			pt1 = (obj.x,obj.y)
			offset = 5

		actual_distance = resources.get_distance(self.position,pt1)
		collision_distance = 0.5*(self.width+obj.width) + offset
		return actual_distance <= collision_distance

	def set_velocity(self,velocity_x = 1, velocity_y = 1):
		self.velocity_x = velocity_x
		self.velocity_y = velocity_y

	def moving(self):
		self.status = 0

	def die(self):
		self.status = 1

	def to_be_pushed(self,angle):
		self.angle = angle
		self.status = 2

	def stop(self):
		self.status = 3

	def is_dead(self):
		return self.bounce <= 0

	def lose_bounce(self):
		self.bounce-=1
		if self.bounce <= 0:
			self.die()

	def lose_power(self):
		self.power-=1
		if self.power <= 0:
			self.power = 0

	def power_up(self,dp):
		self.power += dp
		if self.power >= 5:
			self.power = 5

	def bounce_up(self,db):
		self.bounce += db
		if self.bounce >= 5:
			self.bounce = 5

	def to_continue(self,mode = "normal"):
		for obj in self.world.game_objects:
			if obj.name != self.name:
				if obj.is_hit(self):
					if isinstance(obj,Player):
						self.stop()
						return False
					else:
						obj.apply(self)

		if self.is_wall():
			if mode == "pushed":
				self.lose_bounce()
			self.stop()
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
			if keyx == key.SPACE and self.power > 0:
				self.lose_power()
				self.push_collide()

	def bounce(self):
		pass

	def move(self):
		pass

	def pushed(self):
		self.tempx,self.tempy = self.x,self.y
		self.tempx += (self.velocity_x+3)*cos(self.angle)
		self.tempy += (self.velocity_y+3)*sin(self.angle)

		if self.to_continue(mode = "pushed"):
			self.x,self.y = self.tempx,self.tempy

	def push_collide(self):
		for obj in self.world.game_objects:
			if obj.name != self.name:
				if obj.is_hit(self,mode = "pushed"):
					if isinstance(obj,Player):
						obj.to_be_pushed(resources.get_angle_between(self.position,obj.position))
					else:
						pass

	def update(self):
		if self.status == 0: #moving
			self.move()
		elif self.status == 2: #being push
			self.pushed()

	def get(self):
		#returns the json format of the player
		return [self.actual_name,self.name,self.type,[self.x,self.y],self.bounce,self.power]