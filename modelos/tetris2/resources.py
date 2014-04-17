'''
resources.py

contains the image and sound loading functions and all the images and all the
sounds used in the game
'''
import pygame
from pygame.locals import *
import os

def load_image(name, colorkey=None, perpixel_alpha = False):
	'''
	This loads an image and returns a surface.
	This takes care of all the stuff like converting pixel depths,
	error checking, and colorkeys for you.
	'''
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	if perpixel_alpha:
		image = image.convert_alpha()
	else:
		image = image.convert()
	if colorkey != None and not perpixel_alpha:
		colorkey = image.get_at(colorkey)
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image


class dummysound:
	def play(self): pass

def load_sound(file):
	import debug
	if not pygame.mixer or not debug.playsounds: return dummysound()
	file = os.path.join('data', file)
	try:
		sound = pygame.mixer.Sound(file)
		return sound
	except pygame.error:
		print 'Warning, unable to load sound,', str(file)
	return dummysound()


# --------------------------------------------------------------------------- #
fontfilename = os.path.join('data', 'font.ttf')
linesfilename = 'lines.scores'
scorefilename = 'score.scores'

class load_all_images(object):
	def __init__(self):
		self.icon = load_image('icon.bmp')
		self.main_menu_header = load_image('main_header.tga', perpixel_alpha = True)
		self.main_menu_background = load_image('main_background.bmp')
		self.play_background = self.main_menu_background
		self.high_entry_background = self.main_menu_background
		self.high_view_background = self.main_menu_background
		
		self.bg_tile = load_image('bg_tile.bmp')
		
		self.redbrick = load_image('redbrick.png')
		self.greenbrick = load_image('greenbrick.png')
		self.bluebrick = load_image('bluebrick.png')
		self.orangebrick = load_image('orangebrick.png')
		self.yellowbrick = load_image('yellowbrick.png')
		self.tealbrick = load_image('tealbrick.png')
		self.purplebrick = load_image('purplebrick.png')
		
		self.border_ends = load_image('borderends.png')
		self.vertical_border = load_image('border.bmp')
		self.horizontal_border = pygame.transform.rotate(self.vertical_border, 90)

class load_all_sounds(object):
	def __init__(self):
		self.high_score = load_sound('highscore.wav')
		self.game_over = load_sound('gameover.wav')
		self.change_submenu = load_sound('switchsubmenu.wav')
		self.launch_new_piece = load_sound('newpiece.wav')
		self.got_lines = load_sound('gotlines.wav')
		self.teleport = load_sound('teleport.wav')
