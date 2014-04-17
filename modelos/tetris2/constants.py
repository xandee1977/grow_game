'''
constants.py

Contains all the game constants. As a rule all constants are named in all caps.
'''
import pygame
from pygame.locals import *

# todo: tweak constants for best gameplay

# gameplay
HORIZONTAL_MOVE_RATE = 20 # the number of pixels a piece moves in one frame when moving horizontally
FALL_RATE = 2.5 # the number of pixels a piece moves down every frame (can be a float, it is rounded)
PROGRESSIVE_SPEED_INCREASE = 0.2 # when difficulty is increased this is added to FALL_RATE
DIFFICULTY_INCREASE_RATE = 2 # the number of lines in between when difficulty is increased
SPEED_FALL_MULTIPLIER = 10 # FALL_RATE is multiplied by this when down is pressed to fall faster (can be a float)
LANDING_COUNTDOWN_LENGTH = 12 # the number of frames the player has to move the piece after it has landed
MOVE_COUNTDOWN_LENGTH = 2 # the number of frames the player must wait before they can move left/right again after they stop moving
TELEPORT_COUNTDOWN_LENGTH = 16 # number of frames the movement key is held down for the player to teleport all the way to the left/right

# getting a line animation
BRICK_FADE_RATE = 10 # this is subtracted from the brick's visibility every frame when fading
BASE_FALL_RATE = 2 # the base number of pixels a brick falls in a frame when falling (can be a float)
FALL_RATE_MULTIPLIER = 2 # the brick's falling rate is multiplied by this every frame to make it speed up when falling

# general gameplay
FIELD_WIDTH = 13
FIELD_HEIGHT = 20
POINTS_PER_LINE = 100

# keys accepted to move piece
LEFT_KEYS = [K_LEFT, K_KP4]
RIGHT_KEYS = [K_RIGHT, K_KP6]
UP_KEYS = [K_UP, K_KP8]
DOWN_KEYS = [K_DOWN, K_KP5, K_KP2]

# misc.
TILE_SIZE = (25, 25) # the size of the tiles and bricks, in pixels
WINDOW_CAPTION = 'Tetris'
SCREEN_SIZE = (800, 600)
FPS = 20

# colors & margins & such
SCORE_MARGINS = 5
SCORE_DIVISION = 10 # pixels in between the 2 displays
PREVIEWER_MARGINS = 5
PREVIEWER_DIVISION = 5 # pixels in between the text and piece in previewer
BUTTON_COLOR = (255, 255, 255)
PAUSE_BUTTON_COLOR1 = (255, 0, 0) # the first color the pause button switches between when blinking
PAUSE_BUTTON_COLOR2 = (100, 0, 0) # the second color the pause button switches between when blinking
PAUSE_BUTTON_COLOR_CHANGE_RATE = 25 # the amount of red changed per frame while blinking
BG_ANIMATION_CREATE_INTERVAL = 2 # seconds in between creation of falling pieces on background
BG_ANIMATION_FALL_RATE = 5

# high score entry/viewer menu stuff
NUM_HIGH_SCORES = 10
HIGH_VIEWER_HEADER_FONT_SIZE = 64
HIGH_VIEWER_LIST_FONT_SIZE = 18
HIGH_ENTRY_HEADER_TOP_FONT_SIZE = 48
HIGH_ENTRY_HEADER_BOTTOM_FONT_SIZE = 18
HIGH_VIEWER_SCORE_PADDING = 3
ACCEPTED_ENTRY_CHARS = 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ!1234567890'
ENTRY_MAX_NAME_LEN = 15
ENTRY_FONT_SIZE = 18
ENTRY_CURSOR_WIDTH = 3
ENTRY_CURSOR_COLOR = (255, 255, 255)
ENTRY_TEMPLATE = 'Your Name: %s '
ENTRY_CURSOR_BLINK_RATE = 1 # seconds in between toggling on/off

# default high score lists
DEFAULT_LINES_LIST = [(x, 'Daniel') for x in range(NUM_HIGH_SCORES)] # todo: make me
DEFAULT_SCORE_LIST = [(x * POINTS_PER_LINE, 'Daniel') for x in range(NUM_HIGH_SCORES)] # todo: make me

PIECE_MAPS = [
			  """
			  ....
			  .gg.
			  .gg.
			  ....
			  """,
			  """
			  .r..
			  .r..
			  .r..
			  .r..
			  """,
			  """
			  ....
			  ppp.
			  .p..
			  ....
			  """,
			  """
			  ....
			  oo..
			  .oo.
			  ....
			  """,
			  """
			  ....
			  .yy.
			  yy..
			  ....
			  """,
			  """
			  ....
			  ttt.
			  t...
			  ....
			  """,
			  """
			  ....
			  bbb.
			  ..b.
			  ....
			  """
			 ]