from gameobject import GameObject
import resources

class Upgrades(GameObject):
	def __init__(self,name,world,*args,**kwargs):
		super(Upgrades,self).__init__(name = name,*args,**kwargs)
		self.world = world
		self.type = None
		self.amt = 1

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

	def get(self):
		return [self.name,self.type,[self.x,self.y]]

class PowerUp(Upgrades):
	def __init__(self,name,world,*args,**kwargs):
		super(PowerUp,self).__init__(name = name,
									world = world,
									img = resources.Resources.sprites['power_up'], 
									*args, **kwargs)
		self.type = "power_up"
	
	def apply(self,player):
		player.power_up(self.amt)
		self.world.delete_game_object(self.name)
		self.world.powerup_count -= 1

class BounceUp(Upgrades):
	def __init__(self,name,world,*args,**kwargs):
		super(BounceUp,self).__init__(name = name,
									world = world,
									img = resources.Resources.sprites['bounce_up'], 
									*args, **kwargs)
		self.type = "bounce_up"

	def apply(self,player):
		player.bounce_up(self.amt)
		self.world.delete_game_object(self.name)
		self.world.powerup_count -= 1