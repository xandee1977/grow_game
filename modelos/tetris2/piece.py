'''
'''
import pygame
import brick
from pygame.locals import *
from constants import *
import debug
import resources

def fix_piece_map(map):
	'''
	This function takes a map and removes any user error in entry from it,
	or if the error is unfixable raises an exception. For instance, whitespace
	may screw things up, or any other totally stupid error could be made typing
	it in.
	'''
	class PieceMapError(ValueError): pass
	# fix whitespace errors and put into rows
	rows = [x.strip() for x in map.splitlines()]
	rows = [x for x in rows if x != '']
	# check for consistent width
	length = len(rows[0])
	for row in rows:
		if len(row) != length:
			raise PieceMapError, 'inconsistent width'
	# make sure all characters are recognized
	allowed = piece.bricktypes.keys()
	allowed.append(piece.emptytile)
	for char in ''.join(rows):
		if not char in allowed:
			raise PieceMapError, 'unrecognized character: "%s"' % char
	# return fixed, validated map
	finished = '\n'.join(rows)
	return finished

def read_map(map):
	''' reads the map and yields the bricks '''
	for rownumber, row in enumerate(map.splitlines()):
		for colnumber, char in enumerate(row):
			if char in piece.bricktypes:
				pos = (colnumber * TILE_SIZE[0], rownumber * TILE_SIZE[1])
				bricktype = piece.bricktypes[char]
				yield bricktype(pos)


class piece(object):
	''' an invisible manager of the current moving blocks '''
	# dict of characters in map to the appropriate classes
	bricktypes = {'r' : brick.redbrick,
				  'g' : brick.greenbrick,
				  'b' : brick.bluebrick,
				  't' : brick.tealbrick,
				  'y' : brick.yellowbrick,
				  'o' : brick.orangebrick,
				  'p' : brick.purplebrick
				  }
	emptytile = '.' # the character representing an empty tile
	
	def __init__(self, startingpos, map, field):
		self.field = field
		self.movement = 0 # -1 = left, 0 = no movement, 1 = right
		self.overto = 0
		self.y = 0
		self.counting_down = False
		self.landing_count = 0
		self.move_count = 0
		self.pressed = {'left' : False,
						'down' : False,
						'up' : False,
						'right' : False
					   }
		self.map = map # store for later
		# read map and create bricks
		self.bricks = list(read_map(map))
		# position ourselves
		self.pos = (0, 0)
		self.move_to(*startingpos)
		self.y = self.pos[1]
		self.teleport_count = 0
	
	def move(self, x, y):
		''' moves the entire piece by the amounts provided '''
		self.pos = (self.pos[0] + x, self.pos[1] + y)
		for brick in self.bricks:
			brick.move(x, y)
			brick.dirty = True
	
	def move_to(self, x, y):
		'''
		moves the topleft of the piece to the coordinates,
		includes empty spaces in the map in the final position
		'''
		# simply move() the appropriate amount to leave us at the position
		self.move(x - self.pos[0], y - self.pos[1])
	
	def rotate(self):
		''' rotates the piece clockwise '''
		posdict = {}
		for brick in self.bricks:
			# thanks to the internet for this:  (x, y) rotated 90 degrees = (y, -x) (x and y being coordinates from the piece's origin)
			t = brick.rect.topleft
			posdict[brick] = t # save in case we have to undo
			brick.rect.topleft = ((t[1] - self.pos[1]) + self.pos[0], -(t[0] - self.pos[0]) + self.pos[1] + (TILE_SIZE[1] * len(self.map.splitlines())))
		# check to make sure the effects dont leave us colliding with any bricks or outside the play area
		if self.get_collides():
			# undo changes
			for brick in self.bricks:
				brick.rect.topleft = posdict[brick]
	
	def teleport(self, direction):
		'''
		called when the player has had either left or right held down for a while,
		this method moves the piece as far as it can go in that direction, instantly.
		'''
		return # teleportation disabled, it is actually worse for the game in our (me + testers) opinion
		
		if direction == 'right':
			while True:
				l, b, r = self.get_all_almosts()
				if not r:
					self.move(TILE_SIZE[0], 0)
				else:
					resources.sounds.teleport.play()
					break
		elif direction == 'left':
			while True:
				l, b, r = self.get_all_almosts()
				if not l:
					self.move(-TILE_SIZE[0], 0)
				else:
					resources.sounds.teleport.play()
					break
		else:
			raise TypeError, 'direction must be either "left" or "right"'
	
	def get_almost_collisions(self, brick):
		'''
		Returns a tuple of 3 lists, bricks almost-colliding with the provided
		brick on the left, bottom and right (in that order).
		Also returns almost collisions with the sides by putting a string in
		the list (what it collides with is never actually checked)
		'''
		l = []
		b = []
		r = []
		rect1 = brick.rect
		# check for almost collisions with the sides
		if rect1.left == 0: # left
			l.append('left side')
		if rect1.left == TILE_SIZE[0] * (self.field.width - 1): # right
			r.append('right side')
		if rect1.top == TILE_SIZE[1] * (self.field.height - 1): # bottom
			b.append('bottom')
		# check with other bricks
		for nonpiecebrick in self.field.bricks:
			rect2 = nonpiecebrick.rect
			# check for bottom
			# check for possibility of touch on x axis
			if rect2.left <= rect1.left + 1 <= rect2.right or rect2.left <= rect1.right - 1 <= rect2.right:
				# right where it should be on y?
				if rect2.top == rect1.bottom:
					b.append(nonpiecebrick)
					continue # impossible for more than 1 almost-collision to occur
			# could they be at least touching on the y axis?
			if rect2.top <= rect1.top + 1 <= rect2.bottom or rect2.top <= rect1.bottom - 1 <= rect2.bottom:
				# check for left
				if rect2.right == rect1.left:
					l.append(nonpiecebrick)
					continue
				# check for right
				if rect2.left == rect1.right:
					r.append(nonpiecebrick)
					continue
		return (l, b, r)
	
	def get_all_almosts(self):
		''' combines all the detected collisions for all our bricks '''
		l = []
		b = []
		r = []
		for brick in self.bricks:
			bl, bb, br = self.get_almost_collisions(brick)
			l += bl
			b += bb
			r += br
		return (l, b, r)
	
	def get_collides(self):
		''' gets the _actual_ collisions between our bricks and those of the field '''
		collides = []
		others = list(self.field.bricks)
		# add polymorphic brick-mimickers that tell bricks they hit the bottom or sides
		bottom = pygame.sprite.Sprite()
		width = TILE_SIZE[0] * self.field.width
		y = TILE_SIZE[1] * self.field.height
		bottom.rect = pygame.Rect(0, y, width, 1000)
		others.append(bottom)
		
		left = pygame.sprite.Sprite()
		height = TILE_SIZE[1] * self.field.height
		left.rect = pygame.Rect(0, 0, 1000, height)
		left.rect.right = 0
		others.append(left)
		
		right = pygame.sprite.Sprite()
		height = TILE_SIZE[1] * self.field.height
		right.rect = pygame.Rect(TILE_SIZE[0] * self.field.width, 0, 1000, height)
		others.append(right)
		# check collisions
		for brick in self.bricks:
			for other in others:
				if brick.rect.colliderect(other.rect):
					collides.append((brick, other))
		return collides
	
	def update(self):
		'''
		If we are moving horizontally, move.
		If on, progress the countdown for landing, if done, and we arent
		moving, tell the playing_field.
		If not those, check for our bricks being right next to other bricks, then
		check the keys pressed, if left/right then start us moving in those
		directions (if we arent right next to any pieces in that direction),
		if down move fast downwards, and if nothing then move down slowly
		(but only if the countdown for landing isnt going), if up rotate. Check
		for collisions, if we are colliding with any bricks assume they are below
		us and we overshot when moving, put ourselves right above them. If we are
		right above any now, then start the countdown for landing (if not already
		started).
		'''
		# teleporting
		if not self.pressed['down'] and not self.pressed['up']:
			if self.pressed['right'] and not self.pressed['left']:
				self.teleport_count += 1
			elif self.pressed['left'] and not self.pressed['right']:
				self.teleport_count += 1
			else:
				self.teleport_count = 0
		else:
			self.teleport_count = 0
		
		if self.movement != 0:
			m = HORIZONTAL_MOVE_RATE * self.movement
			if self.movement == -1: # move to the left
				if self.pos[0] + m < self.overto:
					m = self.overto - self.pos[0]
					self.movement = 0
			else: # move to the right
				if self.pos[0] + m > self.overto:
					m = self.overto - self.pos[0]
					self.movement = 0
			self.move(m, 0)
			# progress landing timer if necessary
			if self.counting_down and self.landing_count > 0:
				self.landing_count -= 1
		else:
			if self.move_count > 0:
				self.move_count -= 1
			# get almost-collisions
			left, bottom, right = self.get_all_almosts()
			# countdown if neccessary
			if self.counting_down:
				self.landing_count -= 1
				if self.landing_count <= 0:
					if bottom:
						self.field.piece_landed()
					else:
						# during the countdown the user moved us off of the brick
						# below us, so we should keep moving down again
						self.counting_down = False
			else:
				if bottom:
					self.counting_down = True
					self.landing_count = LANDING_COUNTDOWN_LENGTH
			if self.pressed['left'] and not left and not self.pressed['right'] and not self.move_count:
				self.movement = -1
				self.move_count = MOVE_COUNTDOWN_LENGTH
				self.overto = self.pos[0] - TILE_SIZE[0]
			elif self.pressed['right'] and not right and not self.pressed['left'] and not self.move_count:
				self.movement = 1
				self.move_count = MOVE_COUNTDOWN_LENGTH
				self.overto = self.pos[0] + TILE_SIZE[0]
			else:
				if self.pressed['up']:
					self.rotate()
					self.pressed['up'] = False
				if not bottom:
					m = self.field.fall_rate
					if self.pressed['down']:
						m *= SPEED_FALL_MULTIPLIER
					self.y += m
					self.move_to(self.pos[0], round(self.y, 0))
					# make sure we didnt move inside other bricks accidentally
					collides = self.get_collides()
					if collides:
						# we overshot when moving down, we need to move back up to sit on top.
						# as the bricks are restricted to specific columns, we assume that the
						# collision is with a brick below us.
						moveup = 0
						for brick, other in collides:
							difference = brick.rect.bottom - other.rect.top
							moveup = max(moveup, difference)
						self.move(0, -moveup)
						self.counting_down = True
						self.landing_count = LANDING_COUNTDOWN_LENGTH
