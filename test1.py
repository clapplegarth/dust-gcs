import dust, json, libtcodpy
import pprint


def mainer():
	import json
	my_console = dust.Console()
	my_world = dust.World(my_console, 'j.json')
	my_board = my_world.boards[-1]
	my_layer = my_board.layers[-1]
	#my_world.redraw(my_console)
	
	# main loop
	running = True
	while running and not my_console.is_terminated():
		my_world.blit(my_console)
	
		my_console.end_cycle()
		
		while True:
			key = my_console.get_key()
			if (key.vk == libtcodpy.KEY_NONE) or (not key.pressed):
				break
			elif key.vk == libtcodpy.KEY_CHAR:
				if key.c == ord('q'):
					# Quit
					running = False
					break

				elif key.c == ord('a'):
					# Add Actor
					x, y = my_console.get_random_position(my_layer)
					my_layer.actors.append(dust.Actor(my_layer, 1, 1, x, y))
					my_layer.actors[-1].get_sprite().fill_sprite(my_console.random_char(), my_console.random_color())
					#my_layer.actors[-1].get_sprite().redraw(my_console)

				elif key.c == ord('l'):
					# Random Line
					x1, y1 = my_console.get_random_position(my_layer)
					x2, y2 = my_console.get_random_position(my_layer)
					id, color, param = my_console.random_id(), my_console.random_color(), my_console.random_char()
					my_console.line_iter(my_layer, 'set_game_tile', x1, y1, x2, y2, heavy=True, id=id, color=color, param=param)

				elif key.c == ord('d'):
					# Brownian
					print chr(key.c), key.vk, key.pressed
					for i in range(10):
						id, color, param = my_console.random_id(), my_console.random_color(), my_console.random_char()
						my_console.brownian_iterxy(my_layer, 'set_game_tile', 100, *my_console.get_random_position(my_layer), id=id, color=color, param=param)

				elif key.c == ord('f'):
					# Fill
					for l in my_board.layers:
						l.fill(1, 7, 0)
			# else:
				# print "non-char:", chr(key.vk), key.vk, key.pressed
		
	my_world.save('j.json')
	
if __name__=="__main__":
	profile = False
	if profile:
		import cProfile
		cProfile.run('mainer()')
	else:
		mainer()
