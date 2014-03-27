from pyglet.app import run
from pyglet.media import Player as MediaPlayer
from pyglet.clock import ClockDisplay
from pyglet.clock import set_fps_limit
from pyglet.clock import schedule_interval
from pyglet.window import Window
from client.gui import Background
from client.gui import Button
from client.gui import TextWidget
from client.gui import UILabel
from client.manager import GameManager
from game.resources import Resources

game_window = Window(Resources.window_width, Resources.window_height)
game_window.set_caption("Push")
game_window.set_location(Resources.center_x,Resources.center_y)
fps = ClockDisplay()

manager = GameManager()
manager.set_window(game_window)

# Object Batches per state #
title_batch = Resources.batches['title']
setup_batch = Resources.batches['setup']
host_batch = Resources.batches['host']
join_batch = Resources.batches['join']
game_batch = Resources.batches['game']
end_batch = Resources.batches['end']
# End of Batches

my_bg = Background(name = 'my_bg',
				img =  Resources.sprites['title_bg'])
mp = MediaPlayer()

@game_window.event
def on_draw():
	game_window.clear()
	my_bg.draw()
	if manager.state == Resources.states['TITLE']:
		title_batch.draw()
	elif manager.state == Resources.states['SETUP']:
		setup_batch.draw()
	elif manager.state == Resources.states['HOST']:
		host_batch.draw()
	elif manager.state == Resources.states['JOIN']:
		join_batch.draw()
	elif manager.state == Resources.states['GAME']:
		game_batch.draw() #only UI elements
		
		#drawing the actual game elements
		for obj in manager.get_game_objects():
			obj.draw()
	elif manager.state == Resources.states['END']:
		end_batch.draw()

	fps.draw()

def update(dt):
	manager.update(dt)

#<-- States -->
def title_screen():
	mp.queue(Resources.audio['title_bgm'])
	
	# Instantiation section #
	play_button = Button(name = 'start_button',
						curr_state = 'TITLE',
						target_state = 'SETUP',
						world = manager,
						img = Resources.sprites['play_button'],
						x = Resources.window_width*0.5,
						y = Resources.window_height*0.5,
						batch = title_batch)
	# End of Instantiation #

	# Handler specification #
	game_window.push_handlers(play_button)
	# End of specification #

	# Importation section #
	manager.add_widget(play_button)
	# End of importation #

def setup_screen():
	# Instantiation section #
	host_button = Button(name = 'host_button',
						curr_state = 'SETUP',
						target_state = 'HOST',
						world = manager,
						img = Resources.sprites['host_button'],
						x = Resources.window_width*0.5 + 200,
						y = Resources.window_height*0.6,
						batch = setup_batch)

	join_button = Button(name = 'join_button',
						curr_state = 'SETUP',
						target_state = 'JOIN',
						world = manager,
						img = Resources.sprites['join_button'],
						x = host_button.x,
						y = host_button.y - 65,
						batch = setup_batch)
	# End of Instantiation #

	# Handler specification #
	game_window.push_handlers(host_button)
	game_window.push_handlers(join_button)
	# End of specification #

	# Importation section #
	manager.add_widget(host_button)
	manager.add_widget(join_button)
	# End of importation #

def host_screen():
	x1 = int((Resources.window_width*0.5))+50
	y1 = int((Resources.window_height*0.5)+50)

	start_button = Button(name = 'start_button1',
						curr_state = 'HOST',
						target_state = 'GAME',
						world = manager,
						img = Resources.sprites['start_button'],
					   	x = x1+120,
						y = y1-50,
					   	batch = host_batch)

	# Handler specification #
	game_window.push_handlers(start_button)
	# End of specification #

	# Importation section #
	manager.add_widget(start_button)
	# End of importation #

def join_screen():
	x1 = int((Resources.window_width*0.5))+15
	y1 = int((Resources.window_height*0.5)+50)

	input_p1 = UILabel(name = 'label_ip',
					text = 'IP Address:',
					x = x1,
					y = y1,
					anchor_y = 'bottom',
                  	color = (57, 255, 20, 255),
                  	batch = join_batch)

	text_p1 = TextWidget(text = '',
						x = x1+100,
						y = y1,
						width = 200,
						batch = join_batch,
						cursor = game_window.get_system_mouse_cursor('text'),
						curr_state = 'JOIN',
						world = manager,
						name = 'text_ip')
	
	input_p2 = UILabel(name = 'label_port',
					text = 'Port:',
					x = input_p1.x,
					y = input_p1.y-50,
					anchor_y = 'bottom',
                  	color = (57, 255, 20, 255),
                  	batch = join_batch)

	text_p2 = TextWidget(text = '',
						x = text_p1.x,
						y = input_p1.y-50,
						width = 200,
						batch = join_batch,
						cursor = game_window.get_system_mouse_cursor('text'),
						curr_state = 'JOIN',
						world = manager,
						name = 'text_port')

	input_p3 = UILabel(name = 'label_name',
					text = 'Name:',
					x = input_p2.x,
					y = input_p2.y-50,
					anchor_y = 'bottom',
                  	color = (57, 255, 20, 255),
                  	batch = join_batch)

	text_p3 = TextWidget(text = '',
						x = text_p2.x,
						y = input_p2.y-50,
						width = 200,
						batch = join_batch,
						cursor = game_window.get_system_mouse_cursor('text'),
						curr_state = 'JOIN',
						world = manager,
						name = 'text_name')

	start_button = Button(name = 'start_button',
						curr_state = 'JOIN',
						target_state = 'GAME',
						world = manager,
						img = Resources.sprites['start_button'],
					   	x = input_p3.x+120,
						y = input_p3.y-50,
					   	batch = join_batch)

	# Handler specification #
	game_window.push_handlers(start_button)
	game_window.push_handlers(text_p1)
	game_window.push_handlers(text_p2)
	game_window.push_handlers(text_p3)
	# End of specification #

	# Importation section #
	manager.add_label(input_p1)
	manager.add_label(input_p2)
	manager.add_label(input_p3)
	manager.add_widget(text_p1)
	manager.add_widget(text_p2)
	manager.add_widget(text_p3)
	manager.add_widget(start_button)
	# End of importation #

def game_screen():
	mp.queue(Resources.audio['game_bgm'])

def end_screen():
	pass
#<-- End of States -->

def main():
	title_screen()
	setup_screen()
	join_screen()
	host_screen()
	game_screen()
	end_screen()

	manager.set_media(mp)
	manager.add_widget(my_bg)
	game_window.push_handlers(manager)
	#Pyglet Settings
	schedule_interval(update, 1/120.0)
	set_fps_limit(120)
	run()

if __name__ == '__main__':
	main()