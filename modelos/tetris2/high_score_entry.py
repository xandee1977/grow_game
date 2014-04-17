from constants import *
import pygame, copy, time
from pygame.locals import *
import resources

class high_score_entry(object):
	def __init__(self, template, midtop, background):
		self.midtop = midtop
		self.template = template.split('%s')
		
		self.name = ''
		
		self.background = background
		
		self.font = pygame.font.Font(resources.fontfilename, ENTRY_FONT_SIZE)
		
		self.index = 0
		
		self.lastrect = pygame.Rect(midtop, (0, 0))
		self.dirty = True
		
		self.last_time = time.time()
		
		self.showcursor = True
	
	def get_name(self):
		return self.name
	
	def key_press(self, event):
		if event.key == K_BACKSPACE:
			self.backspace()
		else:
			char = str(event.unicode)
			if char != '' and char in ACCEPTED_ENTRY_CHARS and len(self.name) < ENTRY_MAX_NAME_LEN:
				self.insert_character(char)
	
	def backspace(self):
		if self.index > 0:
			self.dirty = True
			self.name = self.name[:self.index - 1] + self.name[self.index:]
			self.index -= 1
	
	def right_arrow(self):
		if self.index < len(self.name):
			self.dirty = True
			self.index += 1
	
	def left_arrow(self):
		if self.index > 0:
			self.dirty = True
			self.index -= 1
	
	def insert_character(self, char):
		self.name = self.name[:self.index] + char + self.name[self.index:]
		self.index += 1
		self.dirty = True
	
	
	def update(self):
		curtime = time.time()
		if curtime >= self.last_time + ENTRY_CURSOR_BLINK_RATE:
			self.last_time = curtime
			self.showcursor = not self.showcursor
			self.dirty = True
	
	
	def render(self):
		# get two halves of the text, split where the cursor should go
		lefttext = self.template[0] + self.name[:self.index]
		righttext = self.name[self.index:] + self.template[1]
		# render them
		left = self.font.render(lefttext, True, BUTTON_COLOR)
		right = self.font.render(righttext, True, BUTTON_COLOR)
		# draw cursor on the far right of the left half
		if self.showcursor:
			r = pygame.Rect(left.get_width() - ENTRY_CURSOR_WIDTH, 0, ENTRY_CURSOR_WIDTH, max(left.get_height(), right.get_height()))
			left.fill(ENTRY_CURSOR_COLOR, r)
		# merge
		surf = pygame.Surface((left.get_width() + right.get_width(), max(left.get_height(), right.get_height())))
		surf.blit(left, (0, 0))
		surf.blit(right, (left.get_width(), 0))
		# if we didnt have a solid black background we would add a colorkey to surf here, but now its unneccessary
		return surf
	
	
	def draw(self, screen):
		if self.dirty:
			# get image and rect
			img = self.render()
			imgrect = img.get_rect()
			imgrect.midtop = self.midtop
			self.dirty = False # reset
			# erase
			r = imgrect.union(self.lastrect)
			screen.blit(self.background, r.topleft, r)
			self.lastrect = copy.copy(imgrect)
			# draw
			screen.blit(img, imgrect.topleft)
			return r
	
	def draw_all(self, screen):
		self.dirty = True
		return self.draw(screen)
