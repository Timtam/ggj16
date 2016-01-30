# coding=utf-8
import pygame
from pygame.locals import *
import commons
from commons import *

class Button:
	def __init__(self, text, buttonType, left, top):
		self.ui = getCommon().getUI()
		self.top = top
		self.left = left
		self.state = 0
		self.buttonType = buttonType
		self.enabled = True
		self.height = 50
		if self.buttonType == 0:
			self.icon = self.ui.Icon(text)
			self.width = 50
		elif self.buttonType == 1:
			self.text = text
			self.width = 190
		
	def Update(self):
		if not self.enabled: return
		lmb, mmb, rmb = pygame.mouse.get_pressed()
		if self.state == 1 and not lmb:
			self.state = 2
			return
		if self.state == 0 and lmb:
			mx, my = pygame.mouse.get_pos()
			if (mx >= self.left and mx <= self.left + self.width and my >= self.top and my <= self.top + self.height):
				self.state = 1
				getCommon().getBass().StreamCreateFile(False, "assets\\sound\\ui\\switch26.ogg").Channel.Play()
				
	def GetState(self):
		if not self.enabled: return False
		return self.state == 2
		
	def SetState(self, state):
		if not self.enabled: return
		if state:
			self.state = 2
		else:
			self.state = 0
			
	def Disable(self):
		self.enabled = False
	def Enable(self):
		self.enabled = True
	
	def Draw(self, screen):
		if self.state:
			screen.blit(self.ui.Button(self.state, self.buttonType, self.enabled), (self.left, self.top + 4))
			if self.buttonType == 0:
				screen.blit(self.icon, (self.left, self.top))
			elif self.buttonType == 1:
				font = getCommon().getTextFont()
				tw, th = font.size(self.text)
				ts = font.render(self.text, 0, (255, 255, 255))
				screen.blit(ts, (self.left + (self.width - tw) / 2, self.top + (self.height - th) / 2))
		else:
			screen.blit(self.ui.Button(self.state, self.buttonType, self.enabled), (self.left, self.top))
			if self.buttonType == 0:
				screen.blit(self.icon, (self.left, self.top - 4))
			elif self.buttonType == 1:
				font = getCommon().getTextFont()
				tw, th = font.size(self.text)
				ts = font.render(self.text, 0, (255, 255, 255))
				screen.blit(ts, (self.left + (self.width - tw) / 2, self.top - 4 + (self.height - th) / 2))