import pyglet
from game.gui import Background
from game.gui import Button
from game.gui import TextWidget
from game.gui import UILabel
from game.manager import GameManager
from game.player import Player
from game.resources import Resources

game_window = pyglet.window.Window(Resources.window_width, Resources.window_height)
game_window.set_caption("Push")
game_window.set_location(Resources.center_x,Resources.center_y)
fps = pyglet.clock.ClockDisplay()

manager = GameManager()
manager.set_window(game_window)

# Object Batches per state #
title_batch = pyglet.graphics.Batch()
setup_batch = pyglet.graphics.Batch()
game_batch = pyglet.graphics.Batch()
end_batch = pyglet.graphics.Batch()
# End of Batches

my_bg = Background(name = 'my_bg',
				img =  Resources.sprites['title_bg'])

@game_window.event
def on_draw():
	game_window.clear()
	my_bg.draw()
	if manager.state == Resources.states['TITLE']:
		title_batch.draw()
	elif manager.state == Resources.states['SETUP']:
		setup_batch.draw()
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
	x1 = int((Resources.window_width*0.5))+50
	y1 = int((Resources.window_height*0.5)+50)

	input_p1 = UILabel(name = 'label_ip',
					text = 'IP Address:',
					x = x1,
					y = y1,
					anchor_y = 'bottom',
                  	color = (57, 255, 20, 255),
                  	batch = setup_batch)

	text_p1 = TextWidget(text = '',
						x = x1+100,
						y = y1,
						width = 250,
						batch = setup_batch,
						cursor = game_window.get_system_mouse_cursor('text'),
						curr_state = 'SETUP',
						world = manager,
						name = 'text_ip')
	
	input_p2 = UILabel(name = 'label_port',
					text = 'Port:',
					x = input_p1.x,
					y = input_p1.y-50,
					anchor_y = 'bottom',
                  	color = (57, 255, 20, 255),
                  	batch = setup_batch)

	text_p2 = TextWidget(text = '',
						x = text_p1.x,
						y = input_p1.y-50,
						width = 250,
						batch = setup_batch,
						cursor = game_window.get_system_mouse_cursor('text'),
						curr_state = 'SETUP',
						world = manager,
						name = 'text_port')

	input_p3 = UILabel(name = 'label_name',
					text = 'Name:',
					x = input_p2.x,
					y = input_p2.y-50,
					anchor_y = 'bottom',
                  	color = (57, 255, 20, 255),
                  	batch = setup_batch)

	text_p3 = TextWidget(text = '',
						x = text_p2.x,
						y = input_p2.y-50,
						width = 250,
						batch = setup_batch,
						cursor = game_window.get_system_mouse_cursor('text'),
						curr_state = 'SETUP',
						world = manager,
						name = 'text_name')

	start_button = Button(name = 'start_button',
						curr_state = 'SETUP',
						target_state = 'GAME',
						world = manager,
						img = Resources.sprites['start_button'],
					   	x = input_p3.x+120,
						y = input_p3.y-50,
					   	batch = setup_batch)

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
	pass

def end_screen():
	pass
#<-- End of States -->

def main():
	title_screen()
	setup_screen()
	game_screen()
	end_screen()

	manager.add_widget(my_bg)
	game_window.push_handlers(manager)
	#Pyglet Settings
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.clock.set_fps_limit(120)
	pyglet.app.run()

if __name__ == '__main__':
	main()