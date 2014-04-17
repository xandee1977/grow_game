'''
contains the base brick class and all the subclasses used
'''
import pygame
import resources
import copy
import debug
from pygame.locals import *
from constants import *

current_id = 0

class brick(pygame.sprite.Sprite):
	''' a single brick '''
	def __init__(self, image, initialpos):
		''' all subclasses take only the initialpos '''
		pygame.sprite.Sprite.__init__(self)
		
		global current_id
		self.ID = current_id
		current_id += 1
		
		self.image = copy.copy(image)
		self.rect = self.image.get_rect()
		
		self.previous_rect = copy.copy(self.rect)
		self.dirty = True
		
		self.mode = 'to be replaced with either "fading" or "falling"'
		self.fadelist = 'to be replaced with a playing fields fades list'
		self.vis = 255
		self.fallto = 'to be replaced with the y coordinate to fall down to'
		self.fallrate = BASE_FALL_RATE
		self.falling = False
		
		self.moveto(*initialpos)
	
	def __hash__(self):
		return self.ID
	
	def move(self, x, y):
		''' moves the block by the amount provided '''
		self.rect.topleft = (self.rect.topleft[0] + x, self.rect.topleft[1] + y)
		self.dirty = True
	
	def moveto(self, x, y):
		''' places the topleft of the brick on the point '''
		self.rect.topleft = (x, y)
		self.dirty = True
	
	def update(self):
		''' called when falling: updates position, and when fading: progresses animation '''
		if self.mode == 'fading':
			if self.vis <= 0:
				self.fadelist.remove(self) # kill
			self.vis -= BRICK_FADE_RATE
			if self.vis <= 0:
				# we wait a frame to kill ourselves so we are erased, so kill above
				self.vis = 0
			self.image.set_alpha(self.vis)
			self.dirty = True
		else: # 'falling'
			self.fallrate *= FALL_RATE_MULTIPLIER
			self.move(0, round(self.fallrate, 0))
			self.dirty = True
			if self.rect.top >= self.fallto:
				self.rect.top = self.fallto
				self.mode = 'neither'
				self.falling = False
	
	def set_fall(self, distance):
		''' set us up to fall the provided distance '''
		self.mode = 'falling'
		self.fallrate = BASE_FALL_RATE
		self.fallto = self.rect.top + distance
		self.falling = True

	def fade(self, field):
		''' plays the fading animation, takes our playing_field '''
		# remove ourselves from field.bricks and add to field.fades
		field.bricks.remove(self)
		field.fades.append(self)
		self.fadelist = field.fades
		self.mode = 'fading'
	


class redbrick(brick):
	def __init__(self, initialpos):
		brick.__init__(self, resources.images.redbrick, initialpos)
class greenbrick(brick):
	def __init__(self, initialpos):
		brick.__init__(self, resources.images.greenbrick, initialpos)
class bluebrick(brick):
	def __init__(self, initialpos):
		brick.__init__(self, resources.images.bluebrick, initialpos)
class purplebrick(brick):
	def __init__(self, initialpos):
		brick.__init__(self, resources.images.purplebrick, initialpos)
class yellowbrick(brick):
	def __init__(self, initialpos):
		brick.__init__(self, resources.images.yellowbrick, initialpos)
class orangebrick(brick):
	def __init__(self, initialpos):
		brick.__init__(self, resources.images.orangebrick, initialpos)
class tealbrick(brick):
	def __init__(self, initialpos):
		brick.__init__(self, resources.images.tealbrick, initialpos)