import dust, json, libtcodpy



def mainer():
	import json
	my_console = dust.Console()
	my_world = dust.World('j.json')
	my_board = my_world.boards[-1]
	my_layer = my_board.layers[-1]
	my_world.redraw(my_console)
	
	# main loop
	while not my_console.is_terminated():
		my_world.blit(my_console)
	
		my_console.end_cycle()
		key = my_console.get_key()
		if key.c == ord('q'):
			break
		elif key.c == ord('d'):
			for i in range(10):
				id, color, param = my_console.random_id(), my_console.random_color(), my_console.random_char()
				dust.brownian_iterxy(my_layer, 'set_game_tile', 100, *my_console.get_random_position(my_layer), id=id, color=color, param=param)
		elif key.c == ord('a'):
			for l in my_board.layers:
				l.fill(1, 7, 0)
		
	my_world.save('j.json')
	
if __name__=="__main__":
	profile = False
	if profile:
		import cProfile
		cProfile.run('mainer()')
	else:
		mainer()
