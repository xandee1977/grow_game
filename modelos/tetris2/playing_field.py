'''
playing_field.py

'''
import pygame, random, copy, resources, debug
from pygame.locals import *
from piece import *
from constants import *

class playing_field(object):
	'''
	The main tetris playing field. It keeps track of the bricks and tells them
	what to do. It keeps track of the score, the lines made and the next piece
	as well.
	
	It has 2 states: moving and falling
	moving is the primary state of the game where the player has control over
	a falling piece. When the piece hits the bottom and stops moving the game
	checks if any lines have been made, if so it triggers their explosion and
	goes into falling mode. If not another piece is launched and the cycle
	starts again.
	falling is when a full line has been made and the effected blocks fade away,
	and the blocks above fall down to occupy the space. When no more explosion
	animations exist and no more blocks are moving it launches another piece
	and it goes into moving mode.
	'''
	def __init__(self, width, height, bgtile, pieces, endingfunction):
		'''
		args:
			width: the width (in columns) of the play area
			height: the height (in rows) of the play area
			bgtile: the image that serves as the background to empty tiles
			pieces: a list of all the possible configurations of pieces
			endingfunction: a function that is called when the game is over
		'''
		self.width = width # in columns
		self.height = height # in rows
		
		self.endingfunction = endingfunction
		
		self.score = 0
		self.linecount = 0
		
		self.fall_rate = FALL_RATE
		
		self.bgtile = bgtile
		
		# make the borders
		ends = resources.images.border_ends
		vert = resources.images.vertical_border
		horiz = resources.images.horizontal_border
		# vertical
		self.vertical_border = pygame.Surface((TILE_SIZE[0], TILE_SIZE[1] * (self.height + 2)))
		y = 0
		while y < self.vertical_border.get_height():
			self.vertical_border.blit(vert, (0, y))
			y += vert.get_height()
		self.vertical_border.blit(ends, (0, 0))
		self.vertical_border.blit(ends, (0, ends.get_height()))
		self.vertical_border.blit(ends, (0, self.vertical_border.get_height() - ends.get_height()))
		self.vertical_border.blit(ends, (0, self.vertical_border.get_height() - (2 * ends.get_height())))
		# horizontal
		self.horizontal_border = pygame.Surface((TILE_SIZE[0] * self.width, TILE_SIZE[1]))
		x = 0
		while x < self.horizontal_border.get_width():
			self.horizontal_border.blit(horiz, (x, 0))
			x += horiz.get_width()
		self.horizontal_border.blit(ends, (0, 0))
		self.horizontal_border.blit(ends, (self.horizontal_border.get_width() - ends.get_width(), 0))
		
		# make the background
		self.background = pygame.Surface((TILE_SIZE[0] * self.width, TILE_SIZE[1] * self.height))
		for x in [x * TILE_SIZE[0] for x in range(self.width)]:
			for y in [y * TILE_SIZE[1] for y in range(self.height)]:
				self.background.blit(self.bgtile, (x, y))
		
		self.pieces = [fix_piece_map(x) for x in pieces]
		self.piece = None
		self.nextpiece = random.choice(self.pieces)
		
		self.bricks = []
		
		self.fades = []
		
		self.state = 'moving'
		
		self.launch_new_piece()
	
	def update(self):
		if self.state == 'moving':
			self.piece.update()
		else: # falling
			activity = False
			for fading in self.fades:
				activity = True
				fading.update()
			if not activity:
				for brick in self.bricks:
					if brick.falling:
						activity = True
						brick.update()
			if not activity:
				self.launch_new_piece()
	
	def render(self, image, topleft):
		'''
		draws only the things that have changed onto the image, positioning 
		the playing field at topleft. returns a list of changed rects.
		'''
		def offset(x, y):
			''' offsets to place pos onto the playing field on the screen '''
			return (x + topleft[0] + self.vertical_border.get_width(), y + topleft[1] + self.horizontal_border.get_height())
		image.set_clip(offset(0, 0), self.background.get_size()) # stop drawing of out of bounds bricks
		rects = []
		bricks = list(self.bricks)
		if self.piece != None: bricks += self.piece.bricks
		bricks += self.fades
		# erase
		for obj in bricks:
			if obj.dirty:
				r = image.blit(self.background, offset(*obj.previous_rect.topleft), obj.previous_rect)
				rects.append(r)
		# draw
		for obj in bricks:
			if obj.dirty:
				obj.dirty = False
				obj.previous_rect = copy.copy(obj.rect)
				r = image.blit(obj.image, offset(*obj.rect.topleft)) # draw new
				rects.append(r)
		image.set_clip() # reset
		return rects
	
	def render_all(self, image, topleft):
		'''
		renders the whole playing field onto the image, positioning
		the playing field at topleft.
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
		def backoffset(pos):
			''' Offsets to place pos on the playing field '''
			return offset((self.vertical_border.get_width() + pos[0], self.horizontal_border.get_height() + pos[1]))
		# draw the bricks
		image.set_clip(backoffset((0, 0)), self.background.get_size()) # stop drawing of out of bounds bricks
		bricks = list(self.bricks)
		if self.piece != None: bricks += self.piece.bricks
		bricks += self.fades
		for brick in bricks:
			image.blit(brick.image, backoffset(brick.rect.topleft))
		image.set_clip() # reset
	
	def destroy(self):
		''' cleans us up and prepares us for garbage collection '''
		del self.bricks, self.fades, self.piece, self.endingfunction
	
	def piece_landed(self):
		'''
		Called when the piece has landed on the bottom and is ready to be
		cleaned up. This deconstructs the piece, looks for full lines and
		if it finds any it changes our state, explode()s the offending pieces
		and puts the pieces above into falling mode. If it does not find any
		lines it launches a new piece.
		'''
		# deconstruct
		self.bricks += self.piece.bricks
		self.piece = None
		# look for lines
		possible_loss = False
		linebricks = []
		lines = []
		nonlinebricks = []
		for row in range(self.height):
			# we find lines by making a 1 pixel tall rect that spans the entire center of the row,
			# and looking for collisions with all the bricks,  if we find the same number of
			# collisions as columns, then we have a line
			y = round((row * TILE_SIZE[1]) + TILE_SIZE[1] / 2, 0)
			r = pygame.Rect(0, y, TILE_SIZE[0] * self.width, 1)
			collisions = 0
			currentline = []
			for brick in self.bricks:
				if r.colliderect(brick.rect):
					if row == 0:
						possible_loss = True # there is a brick on the top row, if no lines are made, we lose
					collisions += 1
					currentline.append(brick)
			if collisions == self.width:
				# yay, a line!
				linebricks += currentline
				lines.append(row)
			else:
				# awwww, this row isnt a line
				nonlinebricks += currentline
		if lines != []:
			# we have lines
			resources.sounds.got_lines.play()
			# add to scores
			self.linecount += len(lines)
			self.score += ((len(lines) ** 2) * POINTS_PER_LINE)
			# increase difficulty
			num_increases = round(self.linecount / DIFFICULTY_INCREASE_RATE, 0)
			current_difficulty_increase = num_increases * PROGRESSIVE_SPEED_INCREASE
			self.fall_rate = FALL_RATE + current_difficulty_increase
			##debug.log.write('Line made!\nlines: %s\nnum increases: %s\ncurrent increase: %s\nfall rate: %s\n' % (str(self.linecount), str(num_increases), str(current_difficulty_increase), str(self.fall_rate)))
			# change state
			self.state = 'falling'
			# blow up bricks that were in lines
			for brick in linebricks:
				brick.fade(self)
			# tell others to fall to appropriate places
			for brick in nonlinebricks:
				falldistance = 0
				for line in lines:
					# if below, add a tile to the amount to fall
					y = line * TILE_SIZE[1]
					if y > brick.rect.top:
						falldistance += TILE_SIZE[1]
				if not falldistance == 0:
					brick.set_fall(falldistance)
		else:
			# we do not have lines
			if possible_loss:
				# there was a brick on the top row, we lose
				self.lose()
			# we didnt lose, launch a new piece
			self.launch_new_piece()
	
	def get_new_piece(self):
		''' returns the new piece and queues a new one '''
		next = self.nextpiece
		self.nextpiece = random.choice(self.pieces)
		return next
	
	def launch_new_piece(self):
		'''
		launch a new piece and make the necessary
		changes to put the user in control
		'''
		resources.sounds.launch_new_piece.play()
		self.state = 'moving'
		# choose a map for the new piece
		m = self.get_new_piece()
		# decide where the new piece will start
		rows = m.splitlines()
		size = (len(rows[0]), len(rows)) # in columns/rows
		# get x position ( in the middle of playing field)
		midfield = round(self.width / 2, 0)
		midpiece = round(size[0] / 2, 0)
		x = (midfield - midpiece) * TILE_SIZE[0]
		# y position
		y = size[1] * -TILE_SIZE[1]
		pos = (x, y) # in pixels
		# make the new piece
		self.piece = piece(pos, m, self)
	
	def lose(self):
		''' we lost, end the game '''
		self.endingfunction(True)
