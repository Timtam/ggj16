import pygame
import ui
from pygame.locals import *
from ui import *
try:
  import Bass4Py.Bass4Py
  from Bass4Py.Bass4Py import *
except ImportError:
  import Bass4Py
  from Bass4Py import *

BGM_MAX_VOL = 0.20
BGM_FADE_DURATION = 2

class commons:
	def __init__(self):
		self.font = pygame.font.Font("assets\\font\\KenVector Future.ttf", 14)
		self.ui = UI()
		self.bass = BASS("bass.dll", True)
		
	def getUI(self):
		return self.ui
	
	def getTextFont(self):
		return self.font
	
	def getBass(self):
		return self.bass
	
def getCommon():
	try:
		return _commons_inst;
	except UnboundLocalError:
		_commons_inst = commons();
		return _commons_inst;
