import pygame, resources
from pygame.locals import *
from TextWidget import TextWidget
from image_holder import image_holder
from high_score_viewer_submenu import high_score_viewer_submenu
from constants import *
from high_score_entry import high_score_entry
from animated_background import animated_background

class high_score_entry_submenu(animated_background):
	'''
	The submenu that you only get to when you get a high score after a game.
	its contents are: a big header, the entry widget where you record your name,
	and a done button.
	'''
	def __init__(self, main, screenrect, score, lines):
		self.main = main
		self.screenrect = screenrect
		
		self.score = score
		self.lines = lines
		
		self.background = resources.images.high_entry_background
		
		# make header
		font = pygame.font.Font(resources.fontfilename, HIGH_ENTRY_HEADER_TOP_FONT_SIZE)
		headtop = font.render('High Score!', True, BUTTON_COLOR)
		headtoprect = headtop.get_rect()
		fontbottom = pygame.font.Font(resources.fontfilename, HIGH_ENTRY_HEADER_BOTTOM_FONT_SIZE)
		headbottom = fontbottom.render('Type your name.', True, BUTTON_COLOR)
		headbottomrect = headbottom.get_rect()
		headbottomrect.midtop = headtoprect.midbottom
		header = pygame.Surface((max(headtop.get_width(), headbottom.get_width()),
			headtop.get_height() + headbottom.get_height()))
		header.blit(headtop, headtoprect.topleft)
		header.blit(headbottom, headbottomrect.topleft)
		header.convert()
		header.set_colorkey((0, 0, 0))
		headerrect = header.get_rect()
		headerrect.midtop = screenrect.midtop
		self.header = image_holder(header, headerrect)
		
		self.entry = high_score_entry(ENTRY_TEMPLATE, (headerrect.midbottom[0], headerrect.midbottom[1] + 100), self.background)
		
		r = pygame.Rect(0, 0, 250, 50)
		r.midtop = self.entry.midtop
		r.top -= 10
		animated_background.__init__(self, screenrect.size, [r])
		
		self.textwidgets = []
		self.quitbutton = TextWidget(text = 'Done', color = BUTTON_COLOR, font_filename = resources.fontfilename)
		self.quitbutton.on_mouse_click = self.done_click
		self.quitbutton.rect.midbottom = screenrect.midbottom
		self.quitbutton.rect.top -= 10
		self.textwidgets.append(self.quitbutton)
	
	def done_click(self, event):
		# add entry/entries to lists
		# lines
		ls = self.main.lines_scores # shorten it
		if ls.check_score(self.lines):
			ls.add_score(self.lines, self.entry.get_name())
		# score
		ss = self.main.score_scores # shorten it
		if ss.check_score(self.score):
			ss.add_score(self.score, self.entry.get_name())
		# exit
		self.main.change_submenu(high_score_viewer_submenu(self.main, self.screenrect))
		resources.sounds.change_submenu.play()
	
	def draw(self, screen):
		rects = []
		rects += self.update_background(screen)
		screen.blit(self.background, (0, 0))
		self.header.draw(screen)
		rects.append(self.entry.draw_all(screen))
		for widget in self.textwidgets:
			widget.dirty = True
			rects.append(widget.draw(screen, self.background))
		return rects
	
	def draw_all(self, screen):
		self.update_background(screen)
		screen.blit(self.background, (0, 0))
		self.header.draw(screen)
		self.entry.draw_all(screen)
		for widget in self.textwidgets:
			widget.dirty = True
			widget.draw(screen, self.background)
	
	
	def update(self):
		self.entry.update()
	
	
	def destroy(self):
		del self.main, self.screenrect, self.entry, self.header, self.quitbutton, self.lines, self.score, self.background
	
	
	def mouse_button_down(self, event):
		for text in self.textwidgets:
			text.on_mouse_button_down(event)
	
	def mouse_button_up(self, event):
		for text in self.textwidgets:
			text.on_mouse_button_up(event)
	
	def mouse_motion(self, event):
		for text in self.textwidgets:
			text.highlight = text.rect.collidepoint(event.pos)
	
	
	def key_press(self, event):
		self.entry.key_press(event)
	
	
	def up_pressed(self):
		pass
	
	def up_unpressed(self):
		pass
	
	def down_pressed(self):
		pass
	
	def down_unpressed(self):
		pass
	
	def left_pressed(self):
		self.entry.left_arrow()
	
	def left_unpressed(self):
		pass
	
	def right_pressed(self):
		self.entry.right_arrow()
	
	def right_unpressed(self):
		pass
