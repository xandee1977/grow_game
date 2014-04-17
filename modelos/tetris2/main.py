'''
'''
import pygame
import resources
from pygame.locals import *
from constants import *
from main_submenu import main_submenu
from high_score_keeper import high_score_keeper

import debug

class main(object):
	'''
	The primary runner of the game, it regulates the sub-menus, provides
	them with input from the user, keeps track of the high scores, and holds
	the mainloop.
	'''
	def make_screen(self):
		if debug.debug:
			flags = 0
		else:
			flags = pygame.FULLSCREEN
		screen = pygame.display.set_mode(SCREEN_SIZE, flags)
		pygame.display.set_caption(WINDOW_CAPTION)
		return screen
	
	def __init__(self):
		print "initializing"
		pygame.init()
		self.screen = self.make_screen()
		self.screenrect = self.screen.get_rect()
		
		resources.images = resources.load_all_images()
		resources.sounds = resources.load_all_sounds()
		
		self.lines_scores = high_score_keeper(resources.linesfilename, NUM_HIGH_SCORES, DEFAULT_LINES_LIST)
		self.score_scores = high_score_keeper(resources.scorefilename, NUM_HIGH_SCORES, DEFAULT_SCORE_LIST)
		
		pygame.display.set_icon(resources.images.icon)
		
		self.submenu = main_submenu(self, self.screenrect)
		self.submenu.draw_all(self.screen)
		
		pygame.display.flip()
		
		self.tochangeto = ''
		
		self.run = True
		
		self.mainloop()
	
	def change_submenu(self, sub):
		self.tochangeto = sub
	
	def destroy(self):
		self.run = False

	def mainloop(self):
		self.timer = pygame.time.Clock()
		while self.run == True:
			##debug.log.write('\n\nFrame:\n')
			if self.tochangeto != '':
				self.submenu.destroy()
				self.submenu = self.tochangeto
				self.submenu.draw_all(self.screen)
				pygame.display.flip()
				self.tochangeto = ''
			# events
			pygame.event.pump()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run = False
				elif event.type == ACTIVEEVENT:
					if event.gain == 1:
						# our window has come to the front after being hidden, refresh
						self.submenu.draw_all(self.screen)
						pygame.display.flip()
					elif event.state == 2: 
						# our window is hidden so wait for the next event
						pygame.event.post(pygame.event.wait())
				elif event.type == pygame.MOUSEMOTION:
					self.submenu.mouse_motion(event)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.submenu.mouse_button_down(event)
				elif event.type == pygame.MOUSEBUTTONUP:
					self.submenu.mouse_button_up(event)
				elif event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:
						self.run = False
					elif event.key in LEFT_KEYS:
						self.submenu.left_pressed()
					elif event.key in RIGHT_KEYS:
						self.submenu.right_pressed()
					elif event.key in UP_KEYS:
						self.submenu.up_pressed()
					elif event.key in DOWN_KEYS:
						self.submenu.down_pressed()
					else:
						self.submenu.key_press(event)
				elif event.type == pygame.KEYUP:
					if event.key in LEFT_KEYS:
						self.submenu.left_unpressed()
					elif event.key in RIGHT_KEYS:
						self.submenu.right_unpressed()
					elif event.key in UP_KEYS:
						self.submenu.up_unpressed()
					elif event.key in DOWN_KEYS:
						self.submenu.down_unpressed()
			# update
			self.submenu.update()
			# display
			pygame.display.update(self.submenu.draw(self.screen))
			# wait and continue
			self.timer.tick(FPS)
		
		# end of game
		pygame.quit()

