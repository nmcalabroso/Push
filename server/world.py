from game.gameobject import GameObject
from game.resources import Resources
from game.player import Player
from game.upgrades import PowerUp
from game.upgrades import BounceUp
from random import randint

class GameWorld(GameObject):

	def __init__(self,*args,**kwargs):
		super(GameWorld,self).__init__(name = 'World',img = Resources.sprites['no_sprite'], *args,**kwargs)
		self.game_objects = [] #gameobject pool
		self.start = False
		self.powerup_count = 0

	def add_player(self,player):
		print "player:",player
		
		actual_name = player[0]
		name_id = player[1]
		cl = player[2]
		x,y = player[3]
		
		p = Player(actual_name = actual_name,
					name = name_id,
					world = self,
					type = cl,
					img = Resources.sprites['char_'+cl],
					x = x,
					y = y)

		self.add_game_object(p)

		if len(self.game_objects) > 1:
			print "Game starts!"
			self.start = True

	def add_game_object(self,obj):
		obj.active = True
		self.game_objects.append(obj)

	def find_game_object(self,name):
		for obj in self.game_objects:
			if obj.name == name:
				return obj
		return None
 
	def get_game_objects(self,active = True):
		new_pool = []
		for obj in self.game_objects:
			if active and obj.active:
				new_pool.append(obj)
			elif not active and not obj.active:
				new_pool.append(obj)
		return new_pool

	def get_objects_by_batch(self,batch):
		new_pool = []
		for obj in self.game_objects:
			if obj.batch is batch:
				new_pool.append(obj)

	def delete_game_object(self,name):
		for i in range(len(self.game_objects)):
			if self.game_objects[i].name == name:
				obj = self.game_objects[i]
				obj.delete()
				del self.game_objects[i]
				break

	def generate_upgrade(self):
		if self.powerup_count < 5:
			num = randint(1,100)
			if num is 5:
				obj = None
				num2 = randint(1,10)
				if num2 is 5:
					obj = BounceUp(name = "bounce_up_"+str(self.powerup_count),
									world = self,
									x = randint(5,Resources.window_width-25),
									y = randint(5,Resources.window_height-25))
				elif num2 is 3 or num2 is 4:
					obj = PowerUp(name = "power_up_"+str(self.powerup_count),
									world = self,
									x = randint(5,Resources.window_width-25),
									y = randint(5,Resources.window_height-25))
				if obj:
					print "Creating Upgrade!"
					self.powerup_count+=1
					self.add_game_object(obj)		

	def get(self): #world representation
		wrld = []
		for obj in self.get_game_objects():
			wrld.append(obj.get())
		return wrld

	def get_players(self):
		pl = []
		for obj in self.game_objects:
			if obj.type != "power_up" and obj.type != "bounce_up":
				pl.append(obj)
		return pl

	def is_over(self):
		return len(self.get_players()) == 1 and self.start

	def update(self,data):
		obj = self.find_game_object(data[0]) #get obj that has name data[0]
		self.generate_upgrade()
		if obj is not None:
			obj.key_press(data[1]) #move obj according to the sent key
			if not obj.is_dead():
				obj.update()
			else:
				self.delete_game_object(obj.name)