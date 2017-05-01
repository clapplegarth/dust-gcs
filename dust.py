#!/usr/bin/env python

from pprint import pprint
from copy import deepcopy
import libtcodpy
import json
	
class RootClass:
	"""
	Class for certain functions that require all of the objects in the Dust
		data structure.
	Methods:
		RootClass.redraw(Sprite dest_graphics, *args, **kwargs)
	"""

	def redraw(self, dest_graphics, *args, **kwargs):
		"""
		RootClass.redraw(Sprite dest_graphics, *args, **kwargs)
		Drills down recursively through the Dust object heirarchy to
			reach each object's Sprite, and then calls redraw() on the
			sprite.  This effectively redraws the current board.
		"""
		if hasattr(self, 'current_board'):
			self.current_board.redraw(dest_graphics, *args, **kwargs)
		if hasattr(self, 'boards'):
			for x in self.boards:
				x.redraw(dest_graphics, *args, **kwargs)
		if hasattr(self, 'layers'):
			for x in self.layers:
				x.redraw(dest_graphics, *args, **kwargs)
		elif hasattr(self, 'actors'):
			for x in self.actors:
				x.redraw(dest_graphics, *args, **kwargs)
		if hasattr(self, 'sprite'):
			self.get_sprite().redraw(dest_graphics, *args, **kwargs)
	
	def find_main_display(self):
		"""
		RootClass.find_main_display() returns None
		Searches self and then parents for reference for main_display.  If
			found, returns main_display; otherwise iterates with parent.
			This function sets self.main_display and returns None.
		"""
		if hasattr(self, 'main_display'):
			return 
		elif hasattr(self, 'parent'):
			self.main_display = self.parent.find_main_display()
			return
		else:
			print "Couldn't find main_display in any parents for", repr(self)
			raise ReferenceError


class Saveable(RootClass):
	"""
	Class for all Dust objects that can be loaded and saved.
	Methods:
		Saveable.load_from_dict(dict load_dict) returns None
		Saveable.get_footprint() returns dict
		Saveable.serialize() returns dict
	
	"""
	def __init__(self):
		pass
	def load_from_dict(self, load_dict):
		"""
		Saveable.load_from_dict(dict load_dict)
			returns None
		Takes a dictionary loaded from JSON containing properties that
			are in this object's footprint.  The footprint describes how
			the object should be loaded and saved in a file format.  If the
			footprint's value for a given property is False, the value is
			serialized or de-serialized as-is; if the footprint's value is
			a class name, it is loaded as a list of classes, which, in
			turn, have load_from_dict called to deserialize them.
		See also:  Saveable.get_footprint, Saveable.serialize
		"""
		footprint = self.get_footprint()
		for this_attribute in footprint:
			this_class = footprint[this_attribute]
			if not this_class:
				if hasattr(load_dict, this_attribute):
					setattr(self, this_attribute, load_dict[this_attribute])
			else:
				compiled_attribute_list = []
				for each_blueprint in load_dict[this_attribute]:
					if hasattr(each_blueprint, 'subclass'):
						new_object = each_blueprint[subclass]()
					else:
						new_object = this_class()
					new_object.load_from_dict(each_blueprint)
					compiled_attribute_list.append(new_object)
				setattr(self, this_attribute, compiled_attribute_list)
		return None

	def get_footprint(self):
		"""
		Saveable.get_footprint() returns dict
		Returns a comprehensive list of values relevant to saving and
			loading.  The values are in the form {property: obj}, where
			property is the name of the property (i.e., what you would pass
			to getattr), and obj is either False for a static JSONable data
			type (list, int, string), or a class' name if the data type is
			a list of that class.
		See also:  Saveable.load_from_dict, Saveable.serialize
		"""
		return {}
		
	def serialize(self):
		"""
		Saveable.serialize() returns dict
		Serializes the data in this Seriable and all Seriables it
			references, in a format similar to __dict__, except it only respects
			the keys provided from self.get_footprint().
		See also:  Saveable.load_from_dict, Saveable.serialize
		"""
		footprint = self.get_footprint()
		for a in footprint:
			if footprint[a]:
				footprint[a] = []
				for i in getattr(self, a):
					footprint[a].append(i.serialize())
				#footprint[a] = self.serialize_all(getattr(self, a))
			else:
				footprint[a] = getattr(self, a)
		return footprint


class Material(RootClass):
	"""
	Class of positionable objects like Actors and Layers, I guess.
	Methods:
		Material.init_position(int w, int h, int x, int y, Object inherit_from)
			returns None
		Material.get_sprite() returns None or Sprite instance
		Material.get_console() returns None or libtcodpy Console instance
		Material.fill(char, color) returns None
	"""
	def __init__(self):
		pass
		
	def init_postion(self, w=None, h=None, x=None, y=None, inherit_from=None):
		"""
		Material.init_position(int w, int h, int x, int y, Object inherit_from)
			returns None
		Tries to initalize position based on the following rules:
			1. If position arguments are provided, use those.
			2. If parent is provided and has a position, use that.
			3. As a fallback use (0,0) and 1x1 as position and dimensions.
		"""
		if w and h:
			self.w, self.h = w, h
		else:
			if parent != None:
				self.w, self.h = parent.w, parent.h
			else:
				self.w, self.h = 1, 1
		if x and y:
			self.x, self.y = x, y
		else:
			if parent != None:
				self.x, self.y = parent.x, parent.y
			else:
				self.x, self.y = 0, 0
	
	def get_sprite(self):
		"""
		Material.get_sprite() returns None or Sprite instance
		Return a suitable Sprite that refers to the Material's graphical
			representation.
		"""
		if hasattr(self, 'sprite'):
			return self.sprite[0]
		elif hasattr(self, 'layers'):
			return self.layer[-1].sprite[0]
		else:
			return None

	def get_console(self):
		"""
		Material.get_console() returns None or libtcodpy Console instance
		Return a suitable Sprite that refers to the Material's graphical
			representation.
		"""
		if hasattr(self, 'sprite'):
			return self.sprite[0].console
		elif hasattr(self, 'layers'):
			return self.layer[-1].sprite[0].console
		else:
			return None
			
	def fill_sprite(self, *args, **kwargs):
		"""
		Material.fill_sprite(char, color) returns None
		Fill this object's Sprite with the given char and color.
		"""
		self.get_sprite().fill(*args, **kwargs)
		
	def get_bounds(self):
		"""
		Material.get_bounds() returns tuple (int, int, int, int)
		Returns the boundaries of the object as a tuple containing the
			rectangle (x1, y1), (x2, y2).  If the object does not have a
			width or height, returns a single-tile area (equal corners).
		"""

		if hasattr(self, 'w') and hasattr(self, 'h'):
			return (self.x, self.y, self.x+self.w, self.y+self.h)
		else:
			return (self.x, self.y, self.x, self.y)
			
	def clamp_to_bounds(self, x, y):
		"""
		Material.clamp_to_bounds(int x, int y) returns tuple (int, int)
		Takes an x and y value and clamps it to the boundaries of this
		Material based on its position and dimensions.
		"""

		return max(self.x, min(self.x+self.w-1, x)), max(self.y, min(self.y+self.h-1, y))


class World(Saveable):
	"""
	A Dust World is the root container of a project.  It contains global
		counters, boards, actors, and world settings.
	Methods:
		World.get_footprint() returns dict
		World.create_default_world()
		World.tick()
		World.blit(Graphics dest_graphics, ...)
		World.create_default_world()
		World.save(str file_path) returns bool
	"""
	def __init__(self, main_display, name="New World", tilesaurus_path='data/tilesaurus.json', file_path=False):
		with open(tilesaurus_path) as fp:
			global tilesaurus
			tilesaurus = json.load(fp)['types']
		
		# set defaults before loading, so that they may be overridden
		self.main_display = main_display
		self.name = name
		self.counters = {}
		self.boards = []
		self.layers = []
		self.actors = []

		if not file_path:
			wo = self.create_default_world()
		else:
			if file_path == True:
				file_path = "saved.json"
			self.file_path = file_path
			with open(file_path) as fp:
				j = json.load(fp)
			wo = World()
			wo.load_from_dict(j)
			return wo
			self.current_board = self.boards[0]
			
	def create_default_world(self):
		"""
		World.create_default_world()
		Creates a default board with no parameters, and adds a blank Layer.
		"""
		self.current_board = Board(self)
		self.boards.append(self.current_board)
		my_layer = Layer(self, *(getattr(self.current_board, x) for x in ('w','h','x','y')))
		self.current_board.layers.append(my_layer)
		
	def get_footprint(self):
		return {'name': False, 'counters': False, 'actors': Actor, 'layers': Layer, 'boards': Board}
	get_footprint.__doc__ = Saveable.get_footprint.__doc__ # Inherit docstring.
		
	def tick(self):
		"""
		World.tick()
		Ticks the World's Actors, Layers, and Boards.
		"""
		for i in self.actors:
			i.tick()
		for i in self.layers:
			i.tick()
		for i in self.boards:
			i.tick()
			
	def blit(self, dest_graphics):
		"""
		World.blit(Graphics dest_graphics, ...)
		Blits the World's Boards and Layers to dest_graphics and passes other
			arguments through.
		"""
		dest_graphics.clear()
		for i in self.layers[::-1]:
			i.blit(dest_graphics)
		self.current_board.blit(dest_graphics)
		
	def save(self, file_path=None):
		"""
		World.save(str file_path) returns bool
		Saves the world to a JSON Dust World file.  Returns status boolean.
		"""
		if file_path == None:
			if hasattr(self, 'file_path'):
				file_path = self.file_path
			else:
				file_path = 'saved.json'
		try:
			with open(file_path, 'w') as f:
				json.dump(self.serialize(), f)
			return True
		except IOError:
			return False


class Board(Saveable, Material):
	"""
	A Dust Board has a width and height and contains board counters and layers.
	Methods:
		Board.get_footprint() returns dict
		Board.tick()
		Board.blit(Graphics dest_graphics, ...)
		Board.get_sprite() returns Sprite
	"""
	def __init__(self, parent, w=80, h=25, x=0, y=0, name="New Board"):
		self.parent = parent
		self.find_main_display()
		self.w, self.h, self.x, self.y = w, h, x, y
		self.name = name
		self.counters = {}
		self.layers = []
		self.actors = []
		
	def get_footprint(self):
		return {'w': False, 'h': False, 'x': False, 'y': False, 'name': False, 'counters': False, 'actors': Actor, 'layers': Layer}
	get_footprint.__doc__ = Saveable.get_footprint.__doc__ # Inherit docstring.
	
	def get_sprite(self):
		"""
		Board.get_sprite() returns Sprite
		Returns the Board's last layer's Sprite.
		"""
		return self.layers[-1].get_sprite()
		
	def tick(self):
		"""
		Board.tick()
		Ticks the Board's Actors and Layers.
		"""
		for i in self.actors:
			i.tick()
		for i in self.layers:
			i.tick()
			
	def blit(self, dest_graphics):
		"""
		Board.blit(Graphics dest_graphics, ...)
		Blits the Board's Layers to dest_graphics and passes other arguments through.
		"""
		for i in self.layers[::-1]:
			i.blit(dest_graphics)


class Layer(Saveable, Material):
	"""
	A Dust Layer has a width and height, relative position, sprite, Actors.
	Methods:
		Layer.get_footprint() returns dict
		Layer.tick() returns None
		Layer.blit(Graphics dest_graphics, ...)
		Layer.flip(Sprite dest_graphics)
		Layer.render_game_tile(int id, int color, int param)
			returns tuple (int, int)
		Layer.draw_game_tile(int x, int y, int id, int color, int param)
		Layer.set_game_tile(int x, int y, int id, int color, int param)
		Layer.set_game_tile_param(int x, int y, int param)
		Layer.fill(int id, int color, int param)
	"""
	def __init__(self, parent, w=80, h=25, x=0, y=0, name="New Layer"):
		self.parent = parent
		self.find_main_display()
		self.w, self.h, self.x, self.y = w, h, x, y
		self.name = name
		self.sprite = [Sprite(self, w, h, x, y)]
		self.actors = []
		self.gamemap = [(1, 0, 7)] * (self.w * self.h)
		self.dirty = True
		
	def get_footprint(self):
		return {'w': False, 'h': False, 'x': False, 'y': False, 'name': False, 'gamemap': False, 'actors': Actor}
	get_footprint.__doc__ = Saveable.get_footprint.__doc__ # Inherit docstring.

		
	def tick(self):
		"""
		Layer.tick() returns None
		Ticks the Layer's Actors.
		"""
		for i in self.actors:
			i.tick()
			
	def blit(self, dest_graphics):
		"""
		Layer.blit(Graphics dest_graphics, ...)
		Blits the Layer's sprite and Actors to dest_graphics and passes other arguments through.
		"""
		if self.dirty:
			self.flip(dest_graphics)
			self.dirty = False
		self.get_sprite().blit(dest_graphics)
		for i in self.actors[::-1]:
			i.blit(dest_graphics)
			
	def flip(self, dest_graphics):
		"""
		Layer.flip(Sprite dest_graphics) returns None
		Render all of the Layer's Tiles into the Tilemap.
		"""
		t = []
		p=0
		for	i in self.gamemap:
			t.append(self.render_game_tile(*i))
			p+=1
		self.get_sprite().tilemap = t
		self.get_sprite().redraw(dest_graphics)
			
	def render_game_tile(self, id, color, param):
		"""
		Layer.render_game_tile(int id, int color, int param) returns tuple (int, int)
		Look up a tile in the tilesaurus and return its char and color as a tuple.
		"""
		global tilesaurus
		if id < len(tilesaurus):
			return [tilesaurus[id]['floor_char'], tilesaurus[id]['floor_color']]
		else:
			return [32, 7]
			
	def draw_game_tile(self, x, y, id, color=7, param=0):
		"""
		Layer.draw_game_tile(int x, int y, int id, int color, int param) returns None
		Draws the given game tile at the specified coordinates, but does not
		add it to the map.
		"""
		self.get_sprite().put_tile(x, y, *self.render_game_tile(id, color, param))
		return
	
	def set_game_tile(self, x, y, id, color=7, param=0):
		"""
		Layer.set_game_tile(int x, int y, int id, int color, int param) returns None
		Draws the given game tile at the specified coordinates, but does not
		add it to the map.
		"""
		self.gamemap[(y * self.w) + x] = (id, color, param)
		self.dirty = True
		return

	def set_game_tile_param(self, x, y, param=0):
		"""
		Layer.set_game_tile_param(int x, int y, int param) returns None
		Draws the given game tile at the specified coordinates, but does not
		add it to the map.
		"""
		self.gamemap[(y * self.w) + x][2] = param
		return
		
	def fill_sprite(self, *args, **kwargs):
		self.get_sprite().fill(*args, **kwargs)
		
	def fill(self, id, color, param):
		"""
		Layer.fill(int id, int color, int param)
		Fills the Layer with the given tile type.
		"""
		for i in range(len(self.gamemap)):
			self.gamemap[i] = [id, color, param]
		self.dirty = True
	
	def fill_func(self, **kwargs):
		"""
		Layer.fill_func(...)
		Fills the Layer based on passed functions.  Calls to this method can include functions and arguments.
		The functions available to pass are id_func, color_func and param_func.  If id_args, color_args and param_args
		(respectively) are passed, the respective function gets a number of the address of that tile.  For example, to
		make a layer all Grass, you might call:  my_layer.fill_func(id_func = lambda: console.tilesaurus.grass).
		To make a layer have random colors, one would call my_layer.fill_func(color_func = my_console.random_id).
		"""
		for i in range(len(self.gamemap)):
			for f in [['id_func', 'id_args', 0], ['color_func', 'color_args', 1], ['param_func', 'param_args', 2]]:
				if hasattr(kwargs, f[0]):
					if hasattr(kwargs, f[1]):
						self.gamemap[i][f[2]] = f[0](i)
					else:
						self.gamemap[i][f[2]] = f[0]()


class Actor(Saveable, Material):
	"""
	An Actor is a programmable Dust entity that can execute Dramatic code.
	Methods:
		Actor.get_footprint() returns dict
		Actor.tick() returns None
		Actor.blit(Graphics dest_graphics, ...) returns None
	"""
	def __init__(self, parent, w=1, h=1, x=0, y=0, name="New Actor"):
		self.parent = parent
		self.find_main_display()
		self.w, self.h, self.x, self.y = w, h, x, y
		self.name = name
		self.sprite = [Sprite(self, w, h, x, y)]
		self.counters = {}
		self.program = ""
		
	def get_footprint(self):
		return {'w': False, 'h': False, 'x': False, 'y': False, 'name': False, 'sprite': Sprite, 'counters': False, 'program': False}
	get_footprint.__doc__ = Saveable.get_footprint.__doc__ # Inherit docstring.
		
	def tick(self):
		"""
		Actor.tick() returns None
		Runs the Actor's tick...
		"""
		pass
	def blit(self, dest_graphics):
		"""
		Actor.blit(Graphics dest_graphics, ...)
		Blits the Layer's Sprite to dest_graphics and passes other arguments
		through.
		"""
		self.sprite[0].blit(dest_graphics, x=self.x, y=self.y)


class Graphics(Material):
	"""
	A Graphics object is a lower level wrapper for the underlying console
	wrapper.  It is not serializable, because it does not contain map data.
	Methods:
		Graphics.blit(Graphics dest_graphics, ...) returns None
		Graphics.get_color(int c) returns libtcodpy.Color
		Graphics.clear() returns None
	"""
	def __init__(self, parent, w=80, h=25, x=0, y=0, new_console=True):
		self.parent = parent
		self.w, self.h, self.x, self.y = w, h, x, y
		if new_console:
			self.console = libtcodpy.console_new(self.w, self.h)
			libtcodpy.console_set_key_color(self.console, self.get_color(16))
			Material.__init__(self)
		else:
			self.console = False
			
	def blit(self, dest_graphics, x=0, y=0):
		"""
		Graphics.blit(Graphics dest_graphics, ...) returns None
		Prints the libtcodpy console contained in self.console to the Graphics object supplied by dest_graphics.
		"""
		libtcodpy.console_blit(self.console, 0, 0, self.w, self.h, dest_graphics.console, x, y)

	def get_color(self, c):
		"""
		Graphics.get_color(int c) returns libtcodpy.Color
		Returns a libtcodpy.Color object representing the color c of the CGA color set.
		"""
		return [libtcodpy.black, libtcodpy.dark_blue, libtcodpy.dark_green, libtcodpy.dark_cyan, libtcodpy.dark_red, libtcodpy.dark_purple, libtcodpy.dark_orange, libtcodpy.light_gray, libtcodpy.dark_gray, libtcodpy.light_blue, libtcodpy.light_green, libtcodpy.light_cyan, libtcodpy.light_red, libtcodpy.light_magenta, libtcodpy.light_yellow, libtcodpy.white, libtcodpy.han][c]
		
	def clear(self):
		"""
		Graphics.clear() returns None
		Tells the builtin console to clear itself.
		"""
		libtcodpy.console_clear(self.console)


class Sprite(Graphics, Saveable):
	"""
	A Sprite object is a higher level wrapper that extends Graphics and is
	seriable.  It contains a list of (char, color) tuples that represent a map
	of ASCII characters and CGA color codes.
	Methods:
		Sprite.get_tile_ref(int x, int y) returns int
		Sprite.get_tile(int x, int y) returns tuple (int, int)
		Sprite.put_tile(int x, int y, int char, int color) returns None
		Sprite.fill_sprite(int char, int color) returns None
		Sprite.redraw(Graphics dest_graphics) returns none
	"""

	def __init__(self, parent, w=80, h=25, x=0, y=0, new_console=True):
		Graphics.__init__(self, parent, w, h, x, y, new_console) # call parent init function to do grunt work: position & open console
		self.tilemap = [[0, 7]] * (self.w * self.h)
		self.tilemask = 0
		self.dirty = True
		self.redraw(self)
		
	def get_footprint(self):
		return {'w': False, 'h': False, 'x': False, 'y': False, 'tilemap': False, 'tilemask': False}
	get_footprint.__doc__ = Saveable.get_footprint.__doc__ # Inherit docstring.

	def get_tile_ref(self, x, y):
		"""
		Sprite.get_tile_ref(int x, int y) returns int
		Based on the given coordinates, returns an integer that can be used as a reference to the Sprite's internal map with an expression such as Sprite.tilemap[x].  Does not, however, return the contents of the map at that position.
		"""
		return (y * self.w) + x
	def get_tile(self, x, y):
		"""
		Sprite.get_tile(int x, int y) returns tuple (int, int)
		Based on the given coordinates, returns a (char, color) tuple of the contents of the map at that position.
		"""
		return self.tilemap[((y * self.w) + x)]
	def put_tile(self, x, y, char, color=False):
		"""
		Sprite.put_tile(int x, int y, int char, int color) returns None
		Based on the given coordinates, places a tile of the given character and color at the correct position.  If color is not provided, the color remains the same.
		"""
		if color:
			self.tilemap[self.get_tile_ref(x, y)] = (char, color)
			libtcodpy.console_set_default_foreground(self.console, self.get_color(color % 16))
			libtcodpy.console_put_char(self.console, x, y, char, libtcodpy.BKGND_SET)
		else:
			self.tilemap[self.get_tile_ref(x, y)][0] = char
			libtcodpy.console_set_char(self.console, x, y, char, libtcodpy.BKGND_SET)
		self.dirty = True
			
	def fill_sprite(self, char, color):
		"""
		Sprite.fill(int char, int color) returns None
		Fill the whole map with the given char and/or color.
		"""
		if (char == None) and (color == None):
			return
		elif char == None:
			for i in range(len(self.tilemap)):
				self.tilemap[i][1] = color
		elif color == None:
			for i in range(len(self.tilemap)):
				self.tilemap[i][0] = char
		else:
			for i in range(len(self.tilemap)):
				self.tilemap[i] = [char, color]
		self.dirty = True
				
	def redraw(self, dest_graphics, blit=True):
		"""
		Sprite.redraw(Graphics dest_graphics) returns none
		Redraw the Sprite's entire console with the contents of its tilemap, and then blit it to screen.
		"""
		if not self.dirty:
			return
		p = 0
		for i in self.tilemap:
			if i[0] == self.tilemask:
				libtcodpy.console_put_char_ex(self.console, (p % self.w), (p / self.w), i[0], self.get_color(i[1]%16), self.get_color(16))
			else:
				libtcodpy.console_put_char_ex(self.console, (p % self.w), (p / self.w), i[0], self.get_color(i[1]%16), self.get_color(i[1]/16))
			p += 1
		self.blit(dest_graphics)


class Console(Graphics):
	"""
	A Console object is an extension of Graphics that borrows console manipulations in order to create a viable class to use as the main console screen.  Ultimately, this is where all graphics must be blitted to in order to be displayed.
	Methods:
		Console.end_cycle() returns None
		Console.get_key() returns libtcodpy.KeyEvent or something, probably...
		Console.is_terminated() returns boolean
		Console.randint(...) returns int
		Console.random_char() returns int
		Console.random_color() returns int
		Console.random_id() returns int
		Console.get_random_position(Material material) returns tuple (x, y)
	"""
	import libtcodpy
	
	def __init__(self, w=80, h=25, fps=50):
		self.w, self.h, self.fps = w, h, fps
		libtcodpy.console_set_custom_font('data/fonts/terminal8x14_gs_ro.png', libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_ASCII_INROW)
		libtcodpy.console_init_root(w, h, 'Dust v0.01', False)
		self.console = 0
		libtcodpy.sys_set_fps(fps)
		self.rng = libtcodpy.random_new_from_seed(15121197032)
		
	def end_cycle(self):
		"""
		Console.end_cycle() returns None
		End the graphical frame and flush the console, sleeping until the next frame.
		"""
		libtcodpy.console_flush()
			
	def get_key(self):
		"""
		Console.get_key() returns libtcodpy.KeyEvent or something, probably... ~~
		Check for keypresses and return an event representing the state of the keyboard.
		"""
		return libtcodpy.console_check_for_keypress(libtcodpy.KEY_PRESSED | libtcodpy.KEY_RELEASED)

	def is_terminated(self):
		"""
		Console.is_terminated() returns boolean
		Check whether or not the screen has been closed out of.  Returns False if the window is still open and running, True otherwise.
		"""
		return libtcodpy.console_is_window_closed()
	
	def randint(self, *args):
		"""
		Console.randint(...) returns int
		Returns a random integer from the RNG.  Arguments are passed directly
		to console function but generally take the form min, max.
		"""
		return libtcodpy.random_get_int(self.rng, *args)

	def random_char(self):
		"""
		Console.random_char() returns int
		Returns a random character code.
		"""
		return self.randint(0, 255)

	def random_color(self):
		"""
		Console.random_color() returns int
		Returns a random color code.
		"""
		return self.randint(0, 15)
		
	def random_id(self):
		"""
		Console.random_id() returns int
		Returns a random tile ID code.
		"""
		global tilesaurus
		return self.randint(0, len(tilesaurus))
		
	def get_random_position(self, material):
		"""
		Console.get_random_position(Material material) returns tuple (x, y)
		Get a random (x, y) position inside the bounds of the given material.
		"""
		return (self.randint(material.x, material.x+material.w), self.randint(material.y, material.y+material.h))
		
	def brownian_iterxy(self, obj, func, num_iterations=100, x=0, y=0, **kwargs):
		"""
		dust.brownian_iterxy(Material obj, function func, int num_iterations,
			int x, inty, **kwargs)
		Perform a random walk of num_iterations steps, starting at x, y.  The
		walk does not go outside of the dimensions of obj.  For every step of
		the walk, func is called with the walk's current x and y position as
		well as a copy of the arguments passed in **kwargs; for example, this
		could be a draw function that takes x, y, char and color.
		"""
		for i in range(num_iterations):
			n = self.randint(0,3)
			x += [0,0,1,-1][n]
			y += [-1,1,0,0][n]
			x, y = obj.clamp_to_bounds(x, y)
			getattr(obj, func)(x, y, **kwargs)
	
	def line_iter(self, obj, func, x1, y1, x2, y2, heavy=False, **kwargs):
		x, y = x1, y1
		if heavy:
			s = abs(x1-x2) + abs(y1-y2)
		else:
			s = max(abs(x1-x2), abs(y1-y2))
		for i in range(s):
			m1 = (i / float(s))
			m2 = ((s - i) / float(s))
			x, y = obj.clamp_to_bounds( int((x1 * m1) + (x2 * m2)), int((y1 * m1) + (y2 * m2)) )
			getattr(obj, func)(x, y, **kwargs)

