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
		self.state = 0 # 0 - main menu, 1 - game, 2 - pause
	
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
		if self.state == 1:
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
		
	def Update(self):
		if self.state == 0:
			self.newGameButton.Update()
			self.loadGameButton.Update()
			self.exitButton.Update()
			if self.exitButton.GetState():
				sys.exit()
			if self.newGameButton.GetState():
				self.currentScene = Scene.fromFile("assets\\scene\\test.txt", self.screen)
				self.darken = pygame.Surface((self.width, self.height))
				self.darken.fill((0, 0, 0))
				self.darken.set_alpha(127)
				self.state = 1
		elif self.state == 1:
			self.currentScene.Update()
			next = self.currentScene.GetNextScene()
			if next:
				self.currentScene = Scene.fromFile(next, self.screen)
		elif self.state == 2:
			self.continueButton.Update()
			self.mainMenuButton.Update()
			self.saveButton.Update()
			if self.mainMenuButton.GetState():
				self.state = 0
				return
			if self.continueButton.GetState():
				self.state = 1
				return
					
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
		pygame.display.flip()
					
if __name__ == "__main__":
	game = MainClass()
	game.MainLoop()