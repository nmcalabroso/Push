from pyglet.graphics import Batch
from pyglet import image
from pyglet import media
from pyglet import window
from os.path import join

def get_center_coordinates(window_width,window_height):
	screen = window.get_platform().get_default_display().get_default_screen()
	x = (screen.width*0.5)-(window_width*0.5)
	y = (screen.height*0.5)-(window_height*0.5)
	return int(x),int(y)

def center_image(image):
	image.anchor_x = int(image.width*0.5)
	image.anchor_y = int(image.height*0.5)
	return image

class Resources:
	states = {'TITLE':1,'SETUP':2,'HOST':3,'JOIN':4,'GAME':5,'END':6} #game states
	types = ['air','water','fire','earth'] #player types
	#positions = [()]
	window_width = 1080
	window_height = 600
	center_x,center_y = get_center_coordinates(window_width,window_height)

	# Starting Points of Characters (x,y)
	starting_points = {}

	starting_points['char_air'] = (center_x,400)
	starting_points['char_earth'] = (center_x,200)
	starting_points['char_fire'] = (center_y,100)
	starting_points['char_water'] = (center_y,200)

	# Object Batches per state #
	batches = {}

	batches['title'] 	= Batch()
	batches['setup']	= Batch()
	batches['host'] 	= Batch()
	batches['join'] 	= Batch()
	batches['game'] 	= Batch()
	batches['end'] 		= Batch()
	# End of Batches

	# Declare all of your assets here #
	audio = {}
	sfx_path = './assets/sfx'

	#Sound Effects
	audio['ost'] 					= media.load(join(sfx_path,"ost.mp3"))

	sprites = {}
	res_path = './assets/img'

	#UI Elements
	sprites['no_sprite'] 			= image.load(join(res_path,'blank.png'))
	sprites['play_button']			= center_image(image.load(join(res_path,'play_button.png')))
	sprites['start_button']			= center_image(image.load(join(res_path,'start_button.png')))
	sprites['host_button']			= center_image(image.load(join(res_path,'host_button.png')))
	sprites['join_button']			= center_image(image.load(join(res_path,'join_button.png')))
	#Backgrounds
	sprites['title_bg']				= center_image(image.load(join(res_path,'title_bg.jpg')))
	sprites['setup_bg']				= center_image(image.load(join(res_path,'setup_bg.jpg')))
	sprites['game_bg']				= center_image(image.load(join(res_path,'game_bg.jpg')))
	#Game Elements
	sprites['char_air']				= center_image(image.load(join(res_path,'char_air.png')))
	sprites['char_earth']			= center_image(image.load(join(res_path,'char_earth.png')))
	sprites['char_fire']			= center_image(image.load(join(res_path,'char_fire.png')))
	sprites['char_water']			= center_image(image.load(join(res_path,'char_water.png')))