import pygame, copy, time, random, piece, resources
from pygame.locals import *
from constants import *

class _frame(pygame.sprite.Sprite):
	'''
	a frame essentially just sits there and does nothing but obscure the
	animated pieces. It has borders and a solid black background.
	'''
	def __init__(self, rect):
		pygame.sprite.Sprite.__init__(self)
		
		# make borders
		size_inside = rect.size		
		ends = resources.images.border_ends
		vert = resources.images.vertical_border
		horiz = resources.images.horizontal_border
		# vertical
		vertical_border = pygame.Surface((TILE_SIZE[0], size_inside[1] + (TILE_SIZE[1] * 2)))
		y = 0
		while y < vertical_border.get_height():
			vertical_border.blit(vert, (0, y))
			y += vert.get_height()
		vertical_border.blit(ends, (0, 0))
		vertical_border.blit(ends, (0, ends.get_height()))
		vertical_border.blit(ends, (0, vertical_border.get_height() - ends.get_height()))
		vertical_border.blit(ends, (0, vertical_border.get_height() - (2 * ends.get_height())))
		# horizontal
		horizontal_border = pygame.Surface((size_inside[0], TILE_SIZE[1]))
		x = 0
		while x < horizontal_border.get_width():
			horizontal_border.blit(horiz, (x, 0))
			x += horiz.get_width()
		horizontal_border.blit(ends, (0, 0))
		horizontal_border.blit(ends, (horizontal_border.get_width() - ends.get_width(), 0))
		
		# make image
		x = (vertical_border.get_width() * 2) + horizontal_border.get_width()
		y = vertical_border.get_height()
		self.image = pygame.Surface((x, y))
		self.image.blit(vertical_border, (0, 0))
		self.image.blit(vertical_border, (x - vertical_border.get_width(), 0))
		self.image.blit(horizontal_border, (vertical_border.get_width(), 0))
		self.image.blit(horizontal_border, (vertical_border.get_width(),
			vertical_border.get_height() - horizontal_border.get_height()))
		
		self.rect = self.image.get_rect()
		self.rect.center = rect.center

class _animation(pygame.sprite.Sprite):
	'''
	displays a falling tetris piece. It goes straight down from where it was
	created and when it goes out of view it kills itself.
	'''
	def __init__(self, piece_map, area_size):
		pygame.sprite.Sprite.__init__(self)
		self.end = area_size[1]
		
		# form image
		piece_map = piece.fix_piece_map(piece_map)
		rows = list(piece_map.splitlines())
		x = len(rows[0]) * TILE_SIZE[0]
		y = len(rows) * TILE_SIZE[1]
		self.image = pygame.Surface((x, y))
		self.image.fill((0, 0, 0))
		self.image.convert()
		for brick in piece.read_map(piece_map):
			self.image.blit(brick.image, brick.rect.topleft)
		
		# position
		self.rect = self.image.get_rect()
		self.rect.topleft = (random.randint(0, area_size[0]), -y)
	
	def update(self):
		self.rect.top += BG_ANIMATION_FALL_RATE
		if self.rect.top > self.end:
			self.kill()

class animated_background(object):
	'''
	A class any submenu can subclass that implements an animated background
	with tetris pieces coming down in the background
	'''
	def __init__(self, size, framed_rects):
		'''
		takes the size of the background and any rects that will be framed
		by borders and have a solid black background
		'''
		self.size = size
		
		# background to the animated pieces and frames (bottom layer)
		self._original_bg = pygame.Surface(size)
		self._original_bg.fill((0, 0, 0))
		# animated background with frames on it: the one used by subclasses
		self.background = copy.copy(self._original_bg)
		
		self.animations = pygame.sprite.RenderUpdates()
		
		self.lasttime = time.time()
		
		self.frames = pygame.sprite.Group(*[_frame(x) for x in framed_rects])
	
	def update_background(self, screen):
		''' updates self.background, returns any modified rects '''
		curtime = time.time()
		if curtime >= self.lasttime + BG_ANIMATION_CREATE_INTERVAL:
			a = _animation(random.choice(PIECE_MAPS), self.size)
			self.animations.add(a)
			self.lasttime = curtime
		
		self.animations.clear(self.background, self._original_bg)
		self.animations.update()
		rects = list(self.animations.draw(self.background))
		self.frames.draw(self.background)
		return rects
