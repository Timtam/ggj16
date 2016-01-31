import pygame
import commons
from commons import *
import button
from button import *
import slider
from slider import *
import speech
import sys
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
			next.append(handle.readline().strip() + ".txt")
		if numNext > 1:
			for i in range(numNext):
				choices.append(handle.readline().strip())
		else:
			choices.append("Weiter")
		#sound = "assets\\sound\\" + handle.readline().strip()
		bg = "assets\\bg\\" + handle.readline().strip()
                bgm = ""
		text = handle.readline()
                if text[0] == ":":
                        bgm = "assets\\sound\\music\\" + text[1:].strip()
                        text = ""
		for line in handle:
			text += line
		handle.close()
		return Scene(screen, bg, text, next, choices, bgm)
		
	def __init__(self, screen, bg, text, next, choices, bgm):
		self.screen = screen
		sw, sh = self.screen.get_width(), self.screen.get_height()
		try:
			self.background = pygame.image.load(bg)
		except:
			self.background = pygame.image.load("assets\\bg\\blank.png")
		self.background = pygame.transform.scale(self.background, (sw, sh))
		self.texts = text.split("#")
		self.textSurfs = list()
		self.currentText = 0
		self.downIcon = pygame.transform.scale(getCommon().getUI().Icon("down"), (25, 25))
		self.selectedChoice = 0
		self.next = next
		self.choices = choices
		self.time = 0
		self.switchScene = None
		self.state = 0 # 0 - normal, 1 - present choice
		bass = getCommon().getBass()
		
		# create slider for text box
		# self.slider = Slider(self.screen, self.screen.get_width() - 20, 20, self.textBoxHeight - 20)
		# render text
		font = getCommon().getTextFont()
		for box in self.texts:
			lines = box.strip().split("\n")
			try:
				sound = "assets\\sound\\" + lines.pop(0)
				stream = bass.StreamCreateFile(False, sound)
			except:
				stream = bass.StreamCreateFile(False, "assets\\sound\\silence.mp3")
			#print(stream.Channel.Bytes2Seconds(stream.Channel.GetLength(BASS_POS_BYTE)))
			height, width = 0, 0
			for line in lines:
				tw, th = font.size(line)
				height += th + 2
				if tw > width:
					width = tw
			surf = [pygame.Surface((width, height), pygame.SRCALPHA), height, width, stream, False, '\n'.join(lines)]
			height = 0
			for line in lines:
				tw, th = font.size(line)
				ts = font.render(line.decode(sys.getfilesystemencoding()), 0, (255, 255, 255))
				surf[0].blit(ts, (0, height))
				height += th + 2
			self.textSurfs.append(surf)
                
                self.bgmStream = None
                if not bgm == "":
                        try:
                                self.bgmStream = bass.StreamCreateFile(False, bgm, 0, 0, BASS_SAMPLE_LOOP)
                        except:
                                print("load bgm failed")
                
                if self.bgmStream:
                        self.bgmStream.Channel.Play()
			
		self.textSurfs[0][3].Channel.Play()
		if self.textSurfs[0][3].Channel.Filename.endswith("silence.mp3"):
				speech.Speaker.output(self.textSurfs[0][5].decode(sys.getfilesystemencoding()),True)

	def Pause(self):
		try:
			self.textSurfs[self.currentText][3].Channel.Pause()
			self.textSurfs[self.currentText][4] = True
		except:
			return
			
	def Unpause(self):
		if self.textSurfs[self.currentText][4]:
			self.textSurfs[self.currentText][3].Channel.Play()
			self.textSurfs[self.currentText][4] = False
		
	def HandleEvent(self, event):
		if self.state == 0:
			if event.type == pygame.KEYDOWN:
				if event.key == K_SPACE or event.key == K_RETURN:
					self.textSurfs[self.currentText][3].Channel.Stop()
					self.currentText += 1
					if self.currentText == len(self.textSurfs):
						self.currentText -= 1
						self.state = 1
						if len(self.choices) > 1:
							# create buttons for choice
							self.buttons = list()
							xOff = (self.screen.get_width() - (240 * len(self.choices) - 50)) / 2
							i = 0
							for c in self.choices:
								counter = ""
								if "#" in c:
									idx = c.find("#")
									counter = c[(idx + 1):]
									c = c[:idx]
								self.choices[i] = counter
								i += 1
								self.buttons.append(Button(c, 1, xOff, self.screen.get_height() - self.textBoxHeight - 70))
								xOff += 240
                                                elif len(self.next) >= 1:
                                                        self.switchScene = self.next[0]
						else:
							self.switchScene = "end"
					else:
						self.textSurfs[self.currentText][3].Channel.Play()
						if self.textSurfs[self.currentText][3].Channel.Filename.endswith("silence.mp3"):
								speech.Speaker.output(self.textSurfs[self.currentText][5].decode(sys.getfilesystemencoding()),True)

		elif self.state == 1:
			if event.type == pygame.KEYDOWN:
				if event.key == K_LEFT:
					self.selectedChoice -= 1;
				if event.key == K_RIGHT:
					self.selectedChoice += 1;
				if self.selectedChoice < 0: self.selectedChoice = len(self.choices) - 1
				if self.selectedChoice >= len(self.choices): self.selectedChoice = 0
				if event.key == K_RETURN:
					self.switchScene = self.next[self.selectedChoice]
                                        if not self.choices[self.selectedChoice] == "":
                                                self.switchScene += "#" + self.choices[self.selectedChoice]
			
	def Update(self):
		if self.state == 0:
			return
		elif self.state == 1 and self.switchScene == None:
			for i in range(len(self.next)):
				b = self.buttons[i]
				b.Update()
				if b.GetState():
					self.switchScene = self.next[i]
                                        if not self.choices[i] == "":
                                                self.switchScene += "#" + self.choices[i]
					
	def GetNextScene(self):
		return self.switchScene
                
        def GetBgmStream(self):
                return self.bgmStream
		
	def Draw(self):
		self.screen.blit(self.background, (0,0))
		sw, sh = self.screen.get_width(), self.screen.get_height()
		self.screen.blit(getCommon().getUI().Panel(sw - 20, self.textBoxHeight), (10, sh - self.textBoxHeight - 10))
		self.screen.blit(self.textSurfs[self.currentText][0], (20, sh - self.textBoxHeight))
		if self.state == 1:
			for b in self.buttons:
				b.Draw(self.screen)
			yOff = (time.time() * 20) % 20
			if yOff > 10: yOff = 20 - yOff
			y = sh - self.textBoxHeight - 120 + yOff
			x = (sw - (240 * len(self.choices) - 50)) / 2 + self.selectedChoice * 240 + 70
			self.screen.blit(getCommon().getUI().Icon("down"), (x, y))