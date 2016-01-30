# coding=utf-8
import os, sys
import pygame
import scene
from pygame.locals import *
from scene import *
import commons
from commons import *
import button
from button import *

class MainClass:
	def __init__(self, width=1280, height=720):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		y = (self.height - 250) / 2
		self.newGameButton = Button("Neues Spiel", 1, (self.width - 190) / 2, y)
		self.loadGameButton = Button("Spiel laden", 1, (self.width - 190) / 2, y + 100)
		self.exitButton = Button("Beenden", 1, (self.width - 190) / 2, y + 200)
		self.buttonIdx = 0
		self.state = 0 # 0 - main menu, 1 - game, 2 - pause, 3 - load game, 4 - save game
	
	def MainLoop(self):
		bass = getCommon().getBass()
		bass.Init()
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				self.HandleEvent(event)
			self.Update()
			self.Render()
			
	def HandleEvent(self, event):
		if self.state == 0:
			if event.type == pygame.KEYDOWN:
				if event.key == K_DOWN:
					self.buttonIdx -= 1
				if event.key == K_UP:
					self.buttonIdx += 1
				if self.buttonIdx < 0: self.buttonIdx = 2
				elif self.buttonIdx > 2: self.buttonIdx = 0
				if event.key == K_RETURN:
					if self.buttonIdx == 0:
						self.newGameButton.SetState(True)
					elif self.buttonIdx == 1:
						self.continueButton.SetState(True)
					elif self.buttonIdx == 2:
						self.exitButton.SetState(True)
		elif self.state == 1:
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					self.state = 2
					self.currentScene.Pause()
					self.continueButton = Button("Fortsetzen", 1, (self.width - 190) / 2, (self.height - 250) / 2)
					self.saveButton = Button("Speichern", 1, (self.width - 190) / 2, (self.height - 250) / 2 + 100)
					self.mainMenuButton = Button("Hauptmenü", 1, (self.width - 190) / 2, (self.height - 250) / 2 + 200)
			self.currentScene.HandleEvent(event)
		elif self.state == 2:
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					self.state = 1
					self.currentScene.Unpause()
		elif self.state == 3:
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					self.state = 0
		elif self.state == 4:
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					self.state = 0
				elif event.key == K_RETURN:
					handle = open("save\\" + self.inputText, "w")
					handle.write(self.loadedScene)
					handle.close()
					self.state = 2
				elif event.key == K_BACKSPACE:
					self.inputText = self.inputText[:-1]
				elif len(self.inputText) < 20:
					self.inputText += event.unicode
					
	def LoadScene(self, scene):
		self.loadedScene = scene
		self.currentScene = Scene.fromFile("assets\\scene\\" + scene, self.screen)
		self.darken = pygame.Surface((self.width, self.height))
		self.darken.fill((0, 0, 0))
		self.darken.set_alpha(127)
		
	def Update(self):
		if self.state == 0:
			self.newGameButton.Update()
			self.loadGameButton.Update()
			self.exitButton.Update()
			if self.exitButton.GetState():
				sys.exit()
			if self.newGameButton.GetState():
				self.newGameButton.SetState(False)
				self.LoadScene("scene1.txt")
				self.state = 1
			if self.loadGameButton.GetState():
				self.loadGameButton.SetState(False)
				_,_,files = os.walk("save\\").next()
				self.loadSavesButtons = list()
				y = 10
				for file in files:
					self.loadSavesButtons.append([Button(file, 1, 10, y), file])
					y += 60
				self.state = 3
		elif self.state == 1:
			self.currentScene.Update()
			next = self.currentScene.GetNextScene()
			if next:
				self.LoadScene(next)
		elif self.state == 2:
			self.continueButton.Update()
			self.mainMenuButton.Update()
			self.saveButton.Update()
			if self.mainMenuButton.GetState():
				self.state = 0
			if self.continueButton.GetState():
				self.state = 1
			if self.saveButton.GetState():
				self.saveButton.SetState(False)
				self.inputText = ""
				self.state = 4
		elif self.state == 3:
			for b in self.loadSavesButtons:
				b[0].Update()
				if b[0].GetState():
					b[0].SetState(False)
					handle = open("save\\" + b[1], "r")
					self.LoadScene(handle.readline().strip())
					self.state = 1
					handle.close()
					
					
	def Render(self):
		# TODO: draw stuff
		self.screen.fill((0,0,0))
		if self.state == 0:
			self.newGameButton.Draw(self.screen)
			self.loadGameButton.Draw(self.screen)
			self.exitButton.Draw(self.screen)
		elif self.state == 1:
			self.currentScene.Draw()
		elif self.state == 2:
			self.currentScene.Draw()
			self.screen.blit(self.darken, (0, 0))
			self.mainMenuButton.Draw(self.screen)
			self.continueButton.Draw(self.screen)
			self.saveButton.Draw(self.screen)
		elif self.state == 3:
			for b in self.loadSavesButtons:
				b[0].Draw(self.screen)
		elif self.state == 4:
			ui = getCommon().getUI()
			font = getCommon().getTextFont()
			self.screen.blit(ui.Panel(300, 80), (10, 10))
			self.screen.blit(font.render("File: " + self.inputText, 0, (255, 255, 255)), (20, 40))
		pygame.display.flip()
					
if __name__ == "__main__":
	game = MainClass()
	game.MainLoop()