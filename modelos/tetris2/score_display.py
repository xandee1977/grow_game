import pygame, resources, debug
from pygame.locals import *
from constants import *

class score_display(object):
	'''
	displays the score and the number of lines with a fancy border.
	'''
	def __init__(self, field):
		self.field = field
		self.score = 0
		self.lines = 0
		self.dirty = True
		
		self.scoretemplate = 'Score: %s'
		self.linestemplate = 'Lines: %s'
		
		self.font = pygame.font.Font(resources.fontfilename, 16)
		
		self.scoreimg = 'to be replaced with the rendered text of the score'
		self.linesimg = 'to be replaced with the rendered text of the lines'
		self.previous_scorerect = pygame.Rect(0, 0, 0, 0)
		self.previous_linesrect = pygame.Rect(0, 0, 0, 0)
		
		# make the borders
		scorerendered = self.font.render(self.scoretemplate % str(9999999), True, BUTTON_COLOR)
		linesrendered = self.font.render(self.linestemplate % str(9999999), True, BUTTON_COLOR)
		xneeded = max(scorerendered.get_width(), linesrendered.get_width()) + (SCORE_MARGINS * 2)
		yneeded = scorerendered.get_height() + linesrendered.get_height() + (SCORE_MARGINS * 2) + SCORE_DIVISION
		
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
		if self.score != self.field.score or self.lines != self.field.linecount:
			self.dirty = True
			self.score = self.field.score
			self.lines = self.field.linecount
	
	def render_text(self):
		''' render the 2 images of our score and lines '''
		self.scoreimg = self.font.render(self.scoretemplate % self.score, True, BUTTON_COLOR)
		self.linesimg = self.font.render(self.linestemplate % self.lines, True, BUTTON_COLOR)
		self.dirty = False
	
	def render(self, image, topleft):
		'''
		draws only the things that have changed onto the image, positioning 
		it at topleft. returns a list of changed rects.
		'''
		rects = []
		if self.dirty:
			self.render_text()
			# erase
			rects.append(image.blit(self.background, self.previous_scorerect, ((0, 0), self.previous_scorerect.size)))
			rects.append(image.blit(self.background, self.previous_linesrect, ((0, 0), self.previous_linesrect.size)))
			# draw
			toppos = (self.vertical_border.get_width() + SCORE_MARGINS + topleft[0], self.horizontal_border.get_height() + SCORE_MARGINS + topleft[1])
			self.previous_scorerect = image.blit(self.scoreimg, toppos)
			self.previous_linesrect = image.blit(self.linesimg, (toppos[0], toppos[1] + self.scoreimg.get_height() + SCORE_DIVISION))
			rects.append(self.previous_scorerect)
			rects.append(self.previous_linesrect)
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
		self.dirty = True
		self.render(image, topleft)

	
	def destroy(self):
		''' cleans us up and prepares us for garbage collection '''
		del self.field
