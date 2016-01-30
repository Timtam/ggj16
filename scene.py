import pygame
import commons
from commons import *
import button
from button import *
import slider
from slider import *
import time

class Scene:
	textBoxHeight = 200
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
		sound = "assets\\sound\\" + handle.readline().strip()
		bg = "assets\\bg\\" + handle.readline().strip()
		text = ""
		for line in handle:
			text += line	
		return Scene(screen, sound, bg, text, next, choices)
		
	def __init__(self, screen, sound, bg, text, next, choices):
		self.screen = screen
		sw, sh = self.screen.get_width(), self.screen.get_height()
		self.background = pygame.transform.scale(pygame.image.load(bg), (sw, sh))
		self.text = text
		self.downIcon = pygame.transform.scale(getCommon().getUI().Icon("down"), (25, 25))
		self.next = next
		self.choices = choices
		self.time = 0
		self.switchScene = None
		self.state = 0 # 0 - normal, 1 - present choice
		
		bass = getCommon().getBass()
		stream = bass.StreamCreateFile(False, sound)
		stream.Channel.Play()
		#  File "C:\Python27\lib\site-packages\Bass4Py\basschannel.py", line 157, in Bytes2Seconds
		#    result=self.__bass_channelbytes2seconds(self._stream,bytes)
		#TypeError: this function takes 3 arguments (2 given)
		self.endtime = time.time() + 10#stream.Channel.Bytes2Seconds(stream.Channel.GetLength(BASS_POS_BYTE))
		
	def HandleEvent(self, event):
		# TODO: handle keydown for skipping
		if self.state == 1:
			self.slider.HandleEvent(event)
			
	def Update(self):
		if self.state == 0:
			if time.time() >= self.endtime:
				# create slider for text box
				self.slider = Slider(self.screen, self.screen.get_width() - 20, 20, self.textBoxHeight - 20)
				# render text
				lines = self.text.split("\n")
				height, width = 0, 0
				font = getCommon().getTextFont()
				for line in lines:
					tw, th = font.size(line)
					height += th + 2
					if tw > width:
						width = tw
				self.textSurface = pygame.Surface((width, height), pygame.SRCALPHA)
				self.textHeight = height
				self.textWidth = width
				height = 0
				for line in lines:
					tw, th = font.size(line)
					ts = font.render(line, 0, (255, 255, 255))
					self.textSurface.blit(ts, (0, height))
					height += th + 2
				# create buttons for choice
				self.buttons = list()
				xOff = (self.screen.get_width() - (240 * len(self.choices) - 50)) / 2
				for c in self.choices:
					self.buttons.append(Button(c, 1, xOff, self.screen.get_height() - 75))
					xOff += 240
				self.state = 1
		elif self.state == 1:
			for i in range(len(self.next)):
				b = self.buttons[i]
				b.Update()
				if b.GetState():
					self.switchScene = self.next[i]
					
	def GetNextScene(self):
		return self.switchScene
		
	def Draw(self):
		self.screen.blit(self.background, (0,0))
		if self.state == 1:
			sw, sh = self.screen.get_width(), self.screen.get_height()
			self.screen.blit(getCommon().getUI().Panel(sw - 20, self.textBoxHeight), (10, 10))
			if self.textHeight > self.textBoxHeight - 20:
				self.slider.Draw()
				self.screen.blit(self.textSurface, (20, 20), pygame.Rect(0, (self.textHeight - self.textBoxHeight + 20) * self.slider.GetSliderPos(), self.textWidth, self.textBoxHeight - 20))
			else:
				self.screen.blit(self.textSurface, (20, 20))
			for b in self.buttons:
				b.Draw(self.screen)