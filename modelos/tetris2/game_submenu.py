import pygame
import resources
import debug
from pygame.locals import *
from constants import *
from playing_field import playing_field
from score_display import score_display
from next_previewer import next_previewer
from TextWidget import TextWidget
from high_score_entry_submenu import high_score_entry_submenu
from high_score_viewer_submenu import high_score_viewer_submenu

class game_submenu(object):
	'''
	the main game screen, it has on it the playing field, the next piece
	previewer, the score displayer, a quit button, and a pause button.
	When the pause button is clicked it toggles between the playing field
	being updated and not. When not the pause button also flashes.
	'''
	def __init__(self, main, screenrect):
		self.main = main
		self.screenrect = screenrect
		
		self.paused = False
		self.colorchange = PAUSE_BUTTON_COLOR_CHANGE_RATE
		
		self.background = resources.images.play_background
		
		self.field = playing_field(FIELD_WIDTH, FIELD_HEIGHT, resources.images.bg_tile, PIECE_MAPS, self.end_game)
		
		fieldrect = pygame.Rect(0, 0, (FIELD_WIDTH + 2) * TILE_SIZE[0], (FIELD_HEIGHT + 2) * TILE_SIZE[1])
		fieldrect.center = (screenrect.center[0] / 2, screenrect.center[1])
		self.fieldpos = fieldrect.topleft
		
		rightsiderect = pygame.Rect(screenrect.centerx, 0, screenrect.width / 2, screenrect.height)
		
		self.next_previewer = next_previewer(self.field)
		previewer_rect = pygame.Rect(0, 0, 140, 225)
		previewer_rect.midtop = (round(screenrect.width * 0.75, 0), 30)
		self.previewer_pos = previewer_rect.topleft
		
		self.score_display = score_display(self.field)
		score_display_rect = pygame.Rect(0, 0, 150, 150)
		score_display_rect.midtop = previewer_rect.midbottom
		score_display_rect.top += 30
		self.score_display_pos = score_display_rect.topleft
		
		self.textwidgets = []
		
		self.pausebutton = TextWidget(text = 'Pause', color = BUTTON_COLOR, font_filename = resources.fontfilename)
		self.pausebutton.on_mouse_click = self.pause_click
		self.pausebutton.rect.midtop = score_display_rect.midbottom
		self.pausebutton.rect.top += 30
		self.textwidgets.append(self.pausebutton)
		
		self.quitbutton = TextWidget(text = 'Quit', color = BUTTON_COLOR, font_filename = resources.fontfilename)
		self.quitbutton.on_mouse_click = self.quit_click
		self.quitbutton.rect.midtop = self.pausebutton.rect.midbottom
		self.quitbutton.rect.top += 30
		self.textwidgets.append(self.quitbutton)
	
	def draw(self, screen):
		rects = []
		rects += self.field.render(screen, self.fieldpos)
		rects += self.score_display.render(screen, self.score_display_pos)
		rects += self.next_previewer.render(screen, self.previewer_pos)
		for widget in self.textwidgets:
			if widget.dirty:
				r = widget.draw(screen, self.background)
				if r != None:
					rects.append(r)
		return rects
	
	def draw_all(self, screen):
		screen.blit(self.background, (0, 0))
		self.field.render_all(screen, self.fieldpos)
		self.score_display.render_all(screen, self.score_display_pos)
		self.next_previewer.render_all(screen, self.previewer_pos)
		for widget in self.textwidgets:
			widget.dirty = True
			widget.draw(screen, self.background)
	
	
	def update(self):
		if self.paused:
			current = self.pausebutton.colour
			red = current[0] + self.colorchange
			if red > max(PAUSE_BUTTON_COLOR1[0], PAUSE_BUTTON_COLOR2[0]):
				red = max(PAUSE_BUTTON_COLOR1[0], PAUSE_BUTTON_COLOR2[0])
				self.colorchange *= -1
			elif red < min(PAUSE_BUTTON_COLOR1[0], PAUSE_BUTTON_COLOR2[0]):
				red = min(PAUSE_BUTTON_COLOR1[0], PAUSE_BUTTON_COLOR2[0])
				self.colorchange *= -1
			self.pausebutton.colour = (red, 0, 0)
		else:
			self.field.update()
			self.score_display.update()
			self.next_previewer.update()

	def destroy(self):
		self.field.destroy()
		self.score_display.destroy()
		self.next_previewer.destroy()
		del self.field, self.score_display, self.next_previewer
	
	
	def key_press(self, event): pass
	
	
	def mouse_button_down(self, event):
		for text in self.textwidgets:
			text.on_mouse_button_down(event)
	
	def mouse_button_up(self, event):
		for text in self.textwidgets:
			text.on_mouse_button_up(event)
	
	def mouse_motion(self, event):
		for text in self.textwidgets:
			text.highlight = text.rect.collidepoint(event.pos)
	
	def up_pressed(self):
		if self.field.piece != None:
			self.field.piece.pressed['up'] = True
	
	def up_unpressed(self):
		if self.field.piece != None:
			self.field.piece.pressed['up'] = False
	
	def down_pressed(self):
		if self.field.piece != None:
			self.field.piece.pressed['down'] = True
	
	def down_unpressed(self):
		if self.field.piece != None:
			self.field.piece.pressed['down'] = False
	
	def left_pressed(self):
		if self.field.piece != None:
			self.field.piece.pressed['left'] = True
	
	def left_unpressed(self):
		if self.field.piece != None:
			self.field.piece.pressed['left'] = False
	
	def right_pressed(self):
		if self.field.piece != None:
			self.field.piece.pressed['right'] = True
	
	def right_unpressed(self):
		if self.field.piece != None:
			self.field.piece.pressed['right'] = False
	
	
	def pause_click(self, event):
		if self.paused:
			self.paused = False
			self.pausebutton.colour = BUTTON_COLOR
			self.pausebutton.bold_rect = self.pausebutton.rect # set the current area to be erased next frame
			self.pausebutton.text = 'Pause'
		else:
			self.paused = True
			self.pausebutton.colour = PAUSE_BUTTON_COLOR1
			self.colorchange = PAUSE_BUTTON_COLOR_CHANGE_RATE
			self.pausebutton.text = 'Paused'
	
	def quit_click(self, event):
		self.end_game(False)
		resources.sounds.change_submenu.play()
	
	def end_game(self, lost):
		'''
		ends the game.
		if lost is true and no high score was acheived a game over sound is played.
		if a high score was achieved, regardless of what is passed, a high
		score sound is played and you are taken to a name entry screen.
		if no high score is achieved you are taken to the high score screen.
		'''
		lines = self.field.linecount
		score = self.field.score
		high = (self.main.lines_scores.check_score(lines) or
			self.main.score_scores.check_score(score))
		if high:
			resources.sounds.high_score.play()
			self.main.change_submenu(high_score_entry_submenu(self.main, self.screenrect, score, lines))
		else:
			if lost: resources.sounds.game_over.play()
			self.main.change_submenu(high_score_viewer_submenu(self.main, self.screenrect))
