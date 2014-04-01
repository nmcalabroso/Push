from __future__ import division
from pyglet.graphics import Batch
from pyglet import image
from pyglet import media
from pyglet import window
from pyglet import font
from os.path import join
from math import sqrt
from math import atan2

def get_center_coordinates(window_width,window_height):
	screen = window.get_platform().get_default_display().get_default_screen()
	x = (screen.width*0.5)-(window_width*0.5)
	y = (screen.height*0.5)-(window_height*0.5)
	return int(x),int(y)

def center_image(image):
	image.anchor_x = int(image.width*0.5)
	image.anchor_y = int(image.height*0.5)
	return image

def get_distance(pt1 = (0,0), pt2 = (0,1)):
	return sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

def get_angle_between(pt1 = (0,0), pt2 = (0,1)):
	x = pt2[0]-pt1[0]
	y = pt2[1]-pt1[1]

	angle = atan2(y,x)

	return angle

class Resources:
	states = {'TITLE':1,'SETUP':2,'HOST':3,'JOIN':4,'GAME':5,'END':6} #game states
	types = ['green','lblue','red','mblue'] #player types
	window_width = 800
	window_height = 600
	center_x,center_y = get_center_coordinates(window_width,window_height)

	# Starting Points of Characters (x,y)
	starting_points = {}

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
	fonts = {}
	fonts_path = './assets/font'
	font.add_file(join(fonts_path,"nexa.otf"))

	fonts['nexa']					= font.load('Nexa Bold')

	audio = {}
	sfx_path = './assets/sfx'

	#Sound Effects
	audio['title_bgm'] 				= media.load(join(sfx_path,"title_bgm.wav"))
	audio['end_bgm'] 				= media.load(join(sfx_path,"end_bgm.wav"))
	audio['game_bgm']				= media.load(join(sfx_path,"game_bgm.wav"))
	audio['button']					= media.load(join(sfx_path,"button.wav"),streaming=False)
	audio['push_all']				= media.load(join(sfx_path,"push.wav"),streaming=False)
	audio['hit_upgrade']			= media.load(join(sfx_path,"hit_upgrade.mp3"),streaming=False)
	audio['game_win']				= media.load(join(sfx_path,"game_win.mp3"),streaming=False)
	audio['transition_to_game']		= media.load(join(sfx_path,"transition_to_game.mp3"))
	audio['transition_to_end']		= media.load(join(sfx_path,"transition_to_end.mp3"))

	sprites = {}
	res_path = './assets/img'

	#UI Elements
	sprites['no_sprite'] 			= image.load(join(res_path,'blank.png'))
	sprites['start_button']			= center_image(image.load(join(res_path,'start_button.gif')))
	#sprites['start_button_mv']		= image.load_animation(join(res_path,'start_button.gif'))
	sprites['play_button']			= center_image(image.load(join(res_path,'play_button_shadow.gif')))
	sprites['host_button']			= center_image(image.load(join(res_path,'debug_button.gif')))
	sprites['join_button']			= center_image(image.load(join(res_path,'join_button.gif')))
	sprites['quit_button']			= center_image(image.load(join(res_path,'quit_button.gif')))
	sprites['logo']					= center_image(image.load(join(res_path,'logo.png')))
	sprites['push_all']				= center_image(image.load(join(res_path,'push_all.png')))
	sprites['marker']				= center_image(image.load(join(res_path,'marker.png')))
	sprites['push_all']				= center_image(image.load(join(res_path,'push_all.png')))
	sprites['info_bar']				= image.load(join(res_path,'info_bar.png'))
	sprites['bounces']				= image.load(join(res_path,'bounces2.png'))
	sprites['powers']				= image.load(join(res_path,'powers.png'))
	sprites['game_over']			= image.load(join(res_path,'game_over.png'))
	sprites['game_win']				= image.load(join(res_path,'game_win2.png'))
	#Thumbnails
	sprites['thumb_green']			= image.load(join(res_path,'thumbnails/thumb_air.png'))
	sprites['thumb_mblue']			= image.load(join(res_path,'thumbnails/thumb_earth.png'))
	sprites['thumb_red']			= image.load(join(res_path,'thumbnails/thumb_fire.png'))
	sprites['thumb_lblue']			= image.load(join(res_path,'thumbnails/thumb_water.png'))
	#Backgrounds
	sprites['title_bg']				= center_image(image.load(join(res_path,'title_bg.jpg')))
	sprites['setup_bg']				= center_image(image.load(join(res_path,'setup_bg.jpg')))
	sprites['game_bg']				= center_image(image.load(join(res_path,'game_bg.jpg')))
	#Game Elements
	sprites['char_green']			= center_image(image.load(join(res_path,'char_air.png')))
	sprites['char_mblue']			= center_image(image.load(join(res_path,'char_earth.png')))
	sprites['char_red']				= center_image(image.load(join(res_path,'char_fire.png')))
	sprites['char_lblue']			= center_image(image.load(join(res_path,'char_water.png')))
	sprites['power_up']				= center_image(image.load(join(res_path,'power_up.png')))
	sprites['bounce_up']			= center_image(image.load(join(res_path,'bounce_up.png')))