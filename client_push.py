from pyglet.app import run
from pyglet.graphics import OrderedGroup
from pyglet.media import Player as MediaPlayer
from pyglet.clock import ClockDisplay
from pyglet.clock import set_fps_limit
from pyglet.clock import schedule_interval
from pyglet.window import Window
from client.gui import Background
from client.gui import Button
from client.gui import QuitButton
from client.gui import TextWidget
from client.gui import UILabel
from client.gui import MyRectangle
from client.manager import GameManager
from client.view_objects import Player
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

bounce_sprites = []
power_sprites = []

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
		manager.me.draw() #drawing the marker
		#drawing the actual game elements
		for obj in manager.get_game_objects():
			obj.draw()

		if manager.me.push_all.visible:
			manager.me.push_all.draw()

		game_batch.draw() #only UI elements

		for i in range(manager.me.bounce):
			bounce_sprites[i].draw()

		for i in range(manager.me.power):
			power_sprites[i].draw()

	elif manager.state == Resources.states['END']:
		end_batch.draw()

def update(dt):
	manager.update(dt)


#<-- States -->
def title_screen():
	mp.queue(Resources.audio['title_bgm'])
	my_logo = OrderedGroup(0)
	my_button = OrderedGroup(1)
	
	# Instantiation section #
	logo = MyRectangle(name = "logo",
						curr_state = 'TITLE',
						img = Resources.sprites['logo'],
						x = Resources.window_width*0.5,
						y = Resources.window_height*0.5,
						batch = title_batch,
						group = my_logo)
	logo.opacity = 255

	play_button = Button(name = 'start_button',
						curr_state = 'TITLE',
						target_state = 'SETUP',
						world = manager,
						img = Resources.sprites['play_button'],
						x = Resources.window_width*0.5+50,
						y = Resources.window_height*0.5-110,
						batch = title_batch,
						group = my_button)
	# End of Instantiation #

	# Handler specification #
	game_window.push_handlers(play_button)
	# End of specification #

	# Importation section #
	manager.add_widget(play_button)
	manager.add_widget(logo)
	# End of importation #

def setup_screen():
	# Instantiation section #
	mp.queue(Resources.audio['transition_to_game'])

	join_button = Button(name = 'join_button',
						curr_state = 'SETUP',
						target_state = 'JOIN',
						world = manager,
						img = Resources.sprites['join_button'],
						x = Resources.window_width*0.5,
						y = Resources.window_height*0.6,
						batch = setup_batch)

	host_button = Button(name = 'host_button',
						curr_state = 'SETUP',
						target_state = 'HOST',
						world = manager,
						img = Resources.sprites['host_button'],
						x = join_button.x,
						y = join_button.y-60,
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
					   	x = input_p3.x+110,
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
	my_rectangle = OrderedGroup(0)
	elements = OrderedGroup(1)

	info_bar = MyRectangle(name = 'info_bar',
						curr_state = 'GAME',
						img = Resources.sprites['info_bar'],
						x = 20,
						y = Resources.window_height-80,
						batch = game_batch,
						group = my_rectangle)

	thumbnail = MyRectangle(name = 'thumbnail',
						curr_state = 'GAME',
						img = Resources.sprites['thumb_green'],
						x = 5,
						y = Resources.window_height-55,
						batch = game_batch,
						group = elements)
	thumbnail.opacity = 255

	player_name = UILabel(name = 'player_name',
					text = 'My Player',
					x = info_bar.x + 38,
					y = info_bar.y+info_bar.height-27,
					anchor_y = 'bottom',
                  	font_size = 17.0,
                  	batch = game_batch,
                  	group = elements)

	label_bounce = UILabel(name = 'label_bounce',
					text = 'Bounce',
					x = player_name.x,
					y = player_name.y-20,
					anchor_y = 'bottom',
                  	font_size = 12.0,
                  	batch = game_batch,
                  	group = elements)

	label_power = UILabel(name = 'label_power',
					text = 'Power',
					x = label_bounce.x,
					y = label_bounce.y-20,
					anchor_y = 'bottom',
                  	font_size = 12.0,
                  	batch = game_batch,
                  	group = elements)

	player_name.color = (255, 255, 255, 255)
	label_bounce.color = (255, 255, 255, 255)
	label_power.color = (255, 255, 255, 255)

	# Importation section #
	manager.add_widget(info_bar)
	manager.add_label(player_name)
	manager.add_label(label_bounce)
	manager.add_label(label_power)
	manager.add_widget(thumbnail)
	# End of importation #

	mp.queue(Resources.audio['game_bgm'])
	my_player = Player(actual_name = "player",name = "player",typex = "green",img = Resources.sprites['marker'])
	manager.set_client(my_player)

	for i in range(my_player.bounce):
		bouncex = MyRectangle(name = 'bounce_'+str(i),
							curr_state = 'GAME',
							img = Resources.sprites['bounces'],
							x = label_bounce.x+60+(i*(Resources.sprites['bounces'].width+3)),
							y = label_bounce.y+3)
		bouncex.opacity = 255
		bounce_sprites.append(bouncex)

	for i in range(my_player.power):
		powerx = MyRectangle(name = 'power_'+str(i),
							curr_state = 'GAME',
							img = Resources.sprites['powers'],
							x = label_power.x+60+(i*(Resources.sprites['powers'].width+3)),
							y = label_power.y+3)
		bouncex.opacity = 255
		power_sprites.append(powerx)

def end_screen():
	game_over = MyRectangle(name = "game_over",
							curr_state = 'END',
							img = Resources.sprites['game_over'],
							x = 150,
							y = 225,
							batch = end_batch)
	game_over.opacity = 255

	quit_button = QuitButton(name = "quit_button",
							curr_state = 'END',
							img = Resources.sprites['quit_button'],
							world = manager,
							x = 400,
							y = 150,
							batch = end_batch)

	# Handler specification #
	game_window.push_handlers(quit_button)
	# End of specification #

	# Importation section #
	manager.add_widget(quit_button)
	manager.add_widget(game_over)
	# End of importation #

	mp.queue(Resources.audio['end_bgm'])
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