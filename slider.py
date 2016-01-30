import pygame
from pygame.locals import *

class Slider:
	def __init__(self, screen, left, top, height):
		self.bar = pygame.transform.scale(pygame.image.load("assets\\ui\\bg\\slider_bar.png").convert_alpha(), (2, height)).convert_alpha()
		self.tick = pygame.image.load("assets\\ui\\bg\\slider_tick.png").convert_alpha()
		self.left, self.top = left, top
		self.height = height
		self.tickPos = 0
		self.screen = screen
		self.grabbed = False
		
	def HandleEvent(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos
			button = event.button
			if button == 1 and x >= self.left - 3 and x <= self.left + 3 and y >= self.top - 3 + self.tickPos and y <= self.top + 3 + self.tickPos:
				self.grabbed = True
		elif event.type == pygame.MOUSEBUTTONUP:
			self.grabbed = False
		elif event.type == pygame.MOUSEMOTION:
			if self.grabbed:
				x, y = event.pos
				self.tickPos = y - self.top
				if self.tickPos < 0:
					self.tickPos = 0
				elif self.tickPos > self.height:
					self.tickPos = self.height
	
	def GetSliderPos(self):
		return float(self.tickPos) / float(self.height)
		
	def Draw(self):
		self.screen.blit(self.bar, (self.left, self.top))
		self.screen.blit(self.tick, (self.left - 3, self.top - 3 + self.tickPos))