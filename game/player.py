from gameobject import GameObject
from pyglet.window import key
from math import cos,sin,pi
import resources

class Player(GameObject):

	def __init__(self,actual_name,name,world,type,*args,**kwargs):
		super(Player,self).__init__(name = name,*args,**kwargs)
		self.world = world
		self.actual_name = actual_name
		
		self.tempx = self.x
		self.tempy = self.y
		
		self.velocity_x = 0
		self.velocity_y = 0
		self.velocity_angle = 0

		self.acceleration_x = 3
		self.acceleration_y = 3
		self.acceleration_angle = 0
		
		self.type = type

		self.bounce = 5 #life
		self.power = 5 #pushing power
		self.status = 3 #0 - moving; 1 - dead; 2 - stop
		self.is_pushed = False

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

	def moving(self):
		self.tempx = self.x + self.velocity_x
		self.tempy = self.y + self.velocity_y
		if self.to_continue():
			self.status = 0

	def stop(self):
		self.status = 3

	def die(self):
		self.status = 1

	def to_be_pushed(self,angle):
		self.velocity_angle = angle
		self.is_pushed = True

	def stop(self):
		self.velocity_x = 0
		self.velocity_y = 0
		self.status = 2

	def is_dead(self):
		return self.bounce <= 0

	def lose_bounce(self):
		self.bounce-=1
		if self.bounce <= 0:
			self.die()

	def lose_power(self):
		self.power-=1

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
			self.moving()
			
			if keyx == key.UP:
				print "UP!"
				self.acceleration_angle = pi/2
			elif keyx == key.RIGHT:
				print "RIGHT!"
				self.acceleration_angle = 0
			elif keyx == key.DOWN:
				print "DOWN!"
				self.acceleration_angle = (3*pi)/2
			elif keyx == key.LEFT:
				print "LEFT!"
				self.acceleration_angle = pi
						
			self.velocity_x += self.acceleration_x*cos(self.acceleration_angle)
			self.velocity_y += self.acceleration_y*sin(self.acceleration_angle)

			print "(acceleration,angle)",((self.acceleration_x,self.acceleration_y),self.acceleration_angle)
			print "(velocity,angle)",((self.velocity_x,self.velocity_y),self.velocity_angle)

		else:
			if keyx == key.SPACE:
				self.push_collide()

	def move(self):
		self.tempx,self.tempy = self.x,self.y
		self.tempx += self.velocity_x*cos(self.velocity_angle)
		self.tempy += self.velocity_y*sin(self.velocity_angle)

		if self.to_continue():
			self.x,self.y = self.tempx,self.tempy

		self.stop()

	def pushed(self):
		self.tempx,self.tempy = self.x,self.y
		self.tempx += self.velocity_x*cos(self.angle)
		self.tempy += self.velocity_y*sin(self.angle)

		if self.to_continue(mode = "pushed"):
			self.x,self.y = self.tempx,self.tempy

	def push_collide(self):
		for obj in self.world.game_objects:
			if obj.name != self.name:
				obj.to_be_pushed(resources.get_angle_between(self.position,obj.position))
				if obj.is_hit(self,mode = "pushed"):
					obj.to_be_pushed(resources.get_angle_between(self.position,obj.position))
	def update(self):
		#colliding_obj = self.is_colliding()
		if self.status == 0:
			self.move()
		if self.is_pushed: #being push
			self.pushed()