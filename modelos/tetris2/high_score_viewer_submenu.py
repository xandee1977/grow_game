from TextWidget import TextWidget
from image_holder import image_holder
from constants import *
import resources, pygame
from pygame.locals import *
from animated_background import animated_background

class high_score_viewer_submenu(animated_background):
	'''
	The submenu accessable from the main menu where you see the list of high
	scores for lines and scores.
	its contents are: a big header, the list of lines on the left, the list
	scores on the right and a back button.
	'''
	def __init__(self, main, screenrect):
		self.main = main
		self.screenrect = screenrect
		
		self.background = resources.images.high_view_background
		
		# make header
		headerfont = pygame.font.Font(resources.fontfilename, HIGH_VIEWER_HEADER_FONT_SIZE)
		header = headerfont.render('High Scores', True, BUTTON_COLOR)
		header.convert()
		headerrect = header.get_rect()
		headerrect.midtop = screenrect.midtop
		headerrect.top += 50
		self.header = image_holder(header, headerrect)
		
		# make lists
		def make_list(keeper, title):
			''' makes the image of the high scores keeper provided '''
			font = pygame.font.Font(resources.fontfilename, HIGH_VIEWER_LIST_FONT_SIZE)
			entries = []
			entries.append(font.render('     ' + title, False, BUTTON_COLOR))
			for index, entry in enumerate(keeper.get_scores()):
				text = '%s %s: %s' % (index + 1, entry[1], entry[0])
				rendered = font.render(text, False, BUTTON_COLOR)
				entries.append(rendered)
			surf = pygame.Surface((max([x.get_width() for x in entries]),
				sum([x.get_height() for x in entries]) + (HIGH_VIEWER_SCORE_PADDING * len(entries))))
			y = 0
			for entry in entries:
				surf.blit(entry, (0, y))
				y += (entry.get_height() + HIGH_VIEWER_SCORE_PADDING)
			surf.convert()
			return surf
		
		Lsurf = make_list(self.main.lines_scores, 'Lines')
		Lrect = Lsurf.get_rect()
		Lrect.top = headerrect.bottom + 10
		Lrect.right = (screenrect.width / 2) - 20
		self.lineslist = image_holder(Lsurf, Lrect)
		
		Ssurf = make_list(self.main.score_scores, 'Score')
		Srect = Ssurf.get_rect()
		Srect.top = headerrect.bottom + 10
		Srect.left = (screenrect.width / 2) + 20
		self.scorelist = image_holder(Ssurf, Srect)
		
		r = headerrect.unionall([Lrect, Srect])
		r.inflate_ip(30, 30)
		animated_background.__init__(self, screenrect.size, [r])
		
		# make back button
		self.textwidgets = []
		self.quitbutton = TextWidget(text = 'Back', color = BUTTON_COLOR, font_filename = resources.fontfilename)
		self.quitbutton.on_mouse_click = self.back_click
		self.quitbutton.rect.midbottom = screenrect.midbottom
		self.quitbutton.rect.top -= 30
		self.textwidgets.append(self.quitbutton)
	
	def back_click(self, event):
		from main_submenu import main_submenu # has to be here because it barfs when at the top (both importing each other at the same time)
		self.main.change_submenu(main_submenu(self.main, self.screenrect))
		resources.sounds.change_submenu.play()
	
	def draw(self, screen):
		rects = []
		rects += self.update_background(screen)
		screen.blit(self.background, (0, 0))
		self.header.draw(screen)
		self.lineslist.draw(screen)
		self.scorelist.draw(screen)
		for widget in self.textwidgets:
			widget.dirty = True
			rects.append(widget.draw(screen, self.background))
		return rects
	
	def draw_all(self, screen):
		self.update_background(screen)
		screen.blit(self.background, (0, 0))
		self.header.draw(screen)
		self.lineslist.draw(screen)
		self.scorelist.draw(screen)
		for widget in self.textwidgets:
			widget.dirty = True
			widget.draw(screen, self.background)
	
	
	def update(self):
		pass
	
	
	def destroy(self):
		del self.main, self.screenrect, self.background, self.header, self.lineslist, self.scorelist, self.quitbutton, self.textwidgets
	
	
	def mouse_button_down(self, event):
		for text in self.textwidgets:
			text.on_mouse_button_down(event)
	
	def mouse_button_up(self, event):
		for text in self.textwidgets:
			text.on_mouse_button_up(event)
	
	def mouse_motion(self, event):
		for text in self.textwidgets:
			text.highlight = text.rect.collidepoint(event.pos)
	
	
	def key_press(self, event): pass
	
	
	def up_pressed(self):
		pass
	
	def up_unpressed(self):
		pass
	
	def down_pressed(self):
		pass
	
	def down_unpressed(self):
		pass
	
	def left_pressed(self):
		pass
	
	def left_unpressed(self):
		pass
	
	def right_pressed(self): 
		pass
	
	def right_unpressed(self):
		pass
