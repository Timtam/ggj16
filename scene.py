import pygame
import commons
from commons import *
import button
from button import *
import slider
from slider import *
import time

class Scene:
	textBoxHeight = 80
	@staticmethod
	def fromFile(filename, screen):
		handle = open(filename, "r")
		numNext = int(handle.readline().strip())
		next = list()
		choices = list()
		for i in range(numNext):
			next.append("assets\\scene\\" + handle.readline().strip() + ".txt")
		if numNext > 1:
			for i in range(numNext):
				choices.append(handle.readline().strip())
		else:
			choices.append("Weiter")
		#sound = "assets\\sound\\" + handle.readline().strip()
		bg = "assets\\bg\\" + handle.readline().strip()
		text = ""
		for line in handle:
			text += line
		return Scene(screen, bg, text, next, choices)
		
	def __init__(self, screen, bg, text, next, choices):
		self.screen = screen
		sw, sh = self.screen.get_width(), self.screen.get_height()
		self.background = pygame.transform.scale(pygame.image.load(bg), (sw, sh))
		self.texts = text.split("#")
		self.textSurfs = list()
		self.currentText = 0
		self.downIcon = pygame.transform.scale(getCommon().getUI().Icon("down"), (25, 25))
		self.next = next
		self.choices = choices
		self.time = 0
		self.switchScene = None
		self.state = 0 # 0 - normal, 1 - present choice
		
		# create slider for text box
		# self.slider = Slider(self.screen, self.screen.get_width() - 20, 20, self.textBoxHeight - 20)
		# render text
		font = getCommon().getTextFont()
		for box in self.texts:
			lines = box.strip().split("\n")
			height, width = 0, 0
			for line in lines:
				tw, th = font.size(line)
				height += th + 2
				if tw > width:
					width = tw
			surf = [pygame.Surface((width, height), pygame.SRCALPHA), height, width]
			height = 0
			for line in lines:
				tw, th = font.size(line)
				ts = font.render(line, 0, (255, 255, 255))
				surf[0].blit(ts, (0, height))
				height += th + 2
			self.textSurfs.append(surf)
		
		bass = getCommon().getBass()
		
	def HandleEvent(self, event):
		# TODO: handle keydown for skipping
		if self.state == 0:
			if event.type == pygame.KEYDOWN:
				if event.key == K_SPACE or event.key == K_RETURN:
					self.currentText += 1
					if self.currentText == len(self.textSurfs):
						self.currentText -= 1
						self.state = 1
						if len(self.choices) > 1:
							# create buttons for choice
							self.buttons = list()
							xOff = (self.screen.get_width() - (240 * len(self.choices) - 50)) / 2
							for c in self.choices:
								self.buttons.append(Button(c, 1, xOff, self.screen.get_height() - self.textBoxHeight - 70))
								xOff += 240
						else:
							#no choise --> advance directly
							self.switchScene = self.next[0]
			
	def Update(self):
		if self.state == 0:
			return
		elif self.state == 1 and self.switchScene == None:
			for i in range(len(self.next)):
				b = self.buttons[i]
				b.Update()
				if b.GetState():
					self.switchScene = self.next[i]
					
	def GetNextScene(self):
		return self.switchScene
		
	def Draw(self):
		self.screen.blit(self.background, (0,0))
		sw, sh = self.screen.get_width(), self.screen.get_height()
		self.screen.blit(getCommon().getUI().Panel(sw - 20, self.textBoxHeight), (10, sh - self.textBoxHeight - 10))
		self.screen.blit(self.textSurfs[self.currentText][0], (20, sh - self.textBoxHeight))
		if self.state == 1:
			for b in self.buttons:
				b.Draw(self.screen)