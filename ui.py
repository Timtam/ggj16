import pygame
from pygame.locals import *

class UI:
	def __init__(self):
		color = "blue"
		borderSize = 7
		renderBorderSize = 7
		panelSurf = pygame.image.load("assets\\ui\\bg\\" + color + "_panel.png").convert_alpha()
		pw, ph = panelSurf.get_width(), panelSurf.get_height()
		
		self.panel_UL = pygame.Surface((borderSize, borderSize), pygame.SRCALPHA)
		self.panel_UM = pygame.Surface((1, borderSize))
		self.panel_UR = pygame.Surface((borderSize, borderSize), pygame.SRCALPHA)
		self.panel_ML = pygame.Surface((borderSize, 1))
		self.panel_MM = pygame.Surface((1, 1))
		self.panel_MR = pygame.Surface((borderSize, 1))
		self.panel_DL = pygame.Surface((borderSize, borderSize), pygame.SRCALPHA)
		self.panel_DM = pygame.Surface((1, borderSize))
		self.panel_DR = pygame.Surface((borderSize, borderSize), pygame.SRCALPHA)
		
		self.panel_UL.blit(panelSurf, (0, 0), pygame.Rect(0, 0, borderSize, borderSize))
		self.panel_UM.blit(panelSurf, (0, 0), pygame.Rect(borderSize, 0, 1, borderSize))
		self.panel_UR.blit(panelSurf, (0, 0), pygame.Rect(pw - borderSize, 0, borderSize, borderSize))
		self.panel_ML.blit(panelSurf, (0, 0), pygame.Rect(0, borderSize, borderSize, 1))
		self.panel_MM.blit(panelSurf, (0, 0), pygame.Rect(borderSize, borderSize, 1, 1))
		self.panel_MR.blit(panelSurf, (0, 0), pygame.Rect(pw - borderSize, borderSize, borderSize, 1))
		self.panel_DL.blit(panelSurf, (0, 0), pygame.Rect(0, pw - borderSize, borderSize, borderSize))
		self.panel_DM.blit(panelSurf, (0, 0), pygame.Rect(borderSize, pw - borderSize, 1, borderSize))
		self.panel_DR.blit(panelSurf, (0, 0), pygame.Rect(pw - borderSize, pw - borderSize, borderSize, borderSize))
		
		self.panel_UL = pygame.transform.scale(self.panel_UL, (renderBorderSize, renderBorderSize))
		self.panel_UR = pygame.transform.scale(self.panel_UR, (renderBorderSize, renderBorderSize))
		self.panel_DL = pygame.transform.scale(self.panel_DL, (renderBorderSize, renderBorderSize))
		self.panel_DR = pygame.transform.scale(self.panel_DR, (renderBorderSize, renderBorderSize))
		
		self.button0_up = pygame.image.load("assets\\ui\\bg\\" + color + "_button0up.png").convert_alpha()
		self.button0_dn = pygame.image.load("assets\\ui\\bg\\" + color + "_button0dn.png").convert_alpha()
		self.button1_up = pygame.image.load("assets\\ui\\bg\\" + color + "_button1up.png").convert_alpha()
		self.button1_dn = pygame.image.load("assets\\ui\\bg\\" + color + "_button1dn.png").convert_alpha()
		
		self.icon_save = pygame.image.load("assets\\ui\\icon\\save.png").convert_alpha()
		self.icon_down = pygame.image.load("assets\\ui\\icon\\down.png").convert_alpha()
		
	def Panel(self, width, height):
		surface = pygame.Surface((width, height), pygame.SRCALPHA)
		borderSize = 7 # same as renderBorderSize in __init__
		#corners
		surface.blit(self.panel_UL, (0, 0))
		surface.blit(self.panel_UR, (width - borderSize, 0))
		surface.blit(self.panel_DL, (0, height - borderSize))
		surface.blit(self.panel_DR, (width - borderSize, height - borderSize))
		#borders
		surface.blit(pygame.transform.scale(self.panel_UM, (width - 2 * borderSize, borderSize)), (borderSize, 0))
		surface.blit(pygame.transform.scale(self.panel_DM, (width - 2 * borderSize, borderSize)), (borderSize, height - borderSize))
		surface.blit(pygame.transform.scale(self.panel_ML, (borderSize, height - 2 * borderSize)), (0, borderSize))
		surface.blit(pygame.transform.scale(self.panel_MR, (borderSize, height - 2 * borderSize)), (width - borderSize, borderSize))
		#middle
		surface.blit(pygame.transform.scale(self.panel_MM, (width - 2 * borderSize, height - 2 * borderSize)), (borderSize, borderSize))
		return surface
		
	def Button(self, state, type):
		if state:
			if type == 0:
				return self.button0_dn
			elif type == 1:
				return self.button1_dn
		else:
			if type == 0:
				return self.button0_up
			elif type == 1:
				return self.button1_up
		return None
		
	def Icon(self, key):
		if key == "save":
			return self.icon_save
		elif key == "down":
			return self.icon_down
		else:
			return None