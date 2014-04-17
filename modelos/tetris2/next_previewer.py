import pygame, resources, debug
from pygame.locals import *
from constants import *
import piece

class next_previewer(object):
	'''
	displays the next piece
	'''
	def __init__(self, field):
		self.field = field
		self.map = """
		....
		....
		....
		....
		"""
		self.dirty = True
		
		font = pygame.font.Font(resources.fontfilename, 16)
		self.header = font.render('Next:', True, BUTTON_COLOR)
		
		# make our piece display surface
		# it is big enough to fit the biggest map in the list
		highestx = 0
		highesty = 0
		for map in PIECE_MAPS:
			map = piece.fix_piece_map(map)
			rows = list(map.splitlines())
			x = len(rows[0]) * TILE_SIZE[0]
			y = len(rows) * TILE_SIZE[1]
			if x > highestx: highestx = x
			if y > highesty: highesty = y
		self.piece_display = pygame.Surface((highestx, highesty))
		self.piece_display.fill((0, 0, 0))
		self.piece_display.convert()
		
		self.display_pos = (PREVIEWER_MARGINS, PREVIEWER_MARGINS + self.header.get_height() + PREVIEWER_DIVISION)
		
		# make the borders
		xneeded = (PREVIEWER_MARGINS * 2) + self.piece_display.get_width()
		yneeded = (PREVIEWER_MARGINS * 2) + self.header.get_height() + PREVIEWER_DIVISION + self.piece_display.get_height()
		
		size_inside = (xneeded, yneeded)
		
		ends = resources.images.border_ends
		vert = resources.images.vertical_border
		horiz = resources.images.horizontal_border
		# vertical
		self.vertical_border = pygame.Surface((TILE_SIZE[0], size_inside[1] + (TILE_SIZE[1] * 2)))
		y = 0
		while y < self.vertical_border.get_height():
			self.vertical_border.blit(vert, (0, y))
			y += vert.get_height()
		self.vertical_border.blit(ends, (0, 0))
		self.vertical_border.blit(ends, (0, ends.get_height()))
		self.vertical_border.blit(ends, (0, self.vertical_border.get_height() - ends.get_height()))
		self.vertical_border.blit(ends, (0, self.vertical_border.get_height() - (2 * ends.get_height())))
		# horizontal
		self.horizontal_border = pygame.Surface((size_inside[0], TILE_SIZE[1]))
		x = 0
		while x < self.horizontal_border.get_width():
			self.horizontal_border.blit(horiz, (x, 0))
			x += horiz.get_width()
		self.horizontal_border.blit(ends, (0, 0))
		self.horizontal_border.blit(ends, (self.horizontal_border.get_width() - ends.get_width(), 0))
		
		# make the background
		self.background = pygame.Surface(size_inside)
		self.background.fill((0, 0, 0))
		self.background.convert()
	
	def update(self):
		if self.map != self.field.nextpiece:
			self.dirty = True
			self.map = self.field.nextpiece
	
	def render_piece_display(self):
		''' render the image of the piece '''
		self.piece_display.fill((0, 0, 0))
		# hijack the functionality right out of the piece module
		for brick in piece.read_map(self.map):
			self.piece_display.blit(brick.image, brick.rect.topleft)
		self.dirty = False
	
	def render(self, image, topleft):
		'''
		draws only the things that have changed onto the image, positioning 
		it at topleft. returns a list of changed rects.
		'''
		rects = []
		if self.dirty:
			self.render_piece_display()
			pos = (topleft[0] + self.display_pos[0] + self.vertical_border.get_width(), topleft[1] + self.display_pos[1] + self.horizontal_border.get_height())
			rects.append(image.blit(self.piece_display, pos))
		return rects
	
	def render_all(self, image, topleft):
		'''
		renders the whole widget onto the image, positioning
		it at topleft.
		'''
		def offset(pos):
			''' Offsets the (x, y) tuple by the topleft. Saves typing time '''
			return (pos[0] + topleft[0], pos[1] + topleft[1])
		# first draw the borders
		image.blit(self.vertical_border, offset((0, 0)))
		image.blit(self.horizontal_border, offset((self.vertical_border.get_width(), 0)))
		image.blit(self.horizontal_border, offset((self.vertical_border.get_width(), self.vertical_border.get_height() - self.horizontal_border.get_height())))
		image.blit(self.vertical_border, offset((self.vertical_border.get_width() + self.horizontal_border.get_width(), 0)))
		# draw the background
		image.blit(self.background, offset((self.vertical_border.get_width(), self.horizontal_border.get_height())))
		# draw the text
		image.blit(self.header, offset((PREVIEWER_MARGINS + self.vertical_border.get_width(), PREVIEWER_MARGINS + self.horizontal_border.get_height())))
		# draw the piece display
		self.dirty = True
		self.render(image, topleft)

	
	def destroy(self):
		''' cleans us up and prepares us for garbage collection '''
		del self.field
