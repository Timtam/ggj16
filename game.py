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
import time
import speech

class MainClass:
        def __init__(self, width=1280, height=720):
                pygame.init()
                self.width = width
                self.height = height
                self.screen = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption("No Buddy's Grey")
                y = (self.height - 250) / 2
                self.newGameButton = Button("Neues Spiel", 1, (self.width - 190) / 2, y)
                self.loadGameButton = Button("Spiel laden", 1, (self.width - 190) / 2, y + 100)
                self.exitButton = Button("Beenden", 1, (self.width - 190) / 2, y + 200)
                self.buttonIdx = 0
                self.maxButtonIdx = 2
                self.buttonTexts = ["Neues Spiel", "Spiel laden", "Beenden"]
                self.state = 0 # 0 - main menu, 1 - game, 2 - pause, 3 - load game, 4 - save game, 5 - credits
                self.fadeOutStream = None
                self.oldBgmStream = None
                
                f = []
                for (_,_,files) in os.walk("save\\"):
                        f.extend(files)
                if len(f) == 0: self.loadGameButton.Disable()
        
        def MainLoop(self):
                bass = getCommon().getBass()
                bass.Init()
                while True:
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        self.stop()
                                self.HandleEvent(event)
                        self.Update()
                        self.Render()

        def stop(self):
                pygame.quit()
                sys.exit()
                        
        def MoveMenuPointer(self, event):
                if event.type == pygame.KEYDOWN:
                        prevIdx = self.buttonIdx
                        if event.key == K_DOWN:
                                self.buttonIdx += 1
                        if event.key == K_UP:
                                self.buttonIdx -= 1
                        if self.buttonIdx < 0: self.buttonIdx = self.maxButtonIdx
                        elif self.buttonIdx > self.maxButtonIdx: self.buttonIdx = 0
                        if not prevIdx == self.buttonIdx:
                                speech.Speaker.output(self.buttonTexts[self.buttonIdx], True)
                        
        def HandleEvent(self, event):
                if self.state == 0:
                        self.MoveMenuPointer(event)
                        if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                                if self.buttonIdx == 0:
                                        self.newGameButton.SetState(True)
                                elif self.buttonIdx == 1:
                                        self.loadGameButton.SetState(True)
                                elif self.buttonIdx == 2:
                                        self.exitButton.SetState(True)
                elif self.state == 1:
                        if event.type == pygame.KEYDOWN:
                                if event.key == K_ESCAPE:
                                        self.state = 2
                                        self.currentScene.Pause()
                                        speech.Speaker.output("Pausiert", True)
                                        self.continueButton = Button("Fortsetzen", 1, (self.width - 190) / 2, (self.height - 250) / 2)
                                        self.saveButton = Button("Speichern", 1, (self.width - 190) / 2, (self.height - 250) / 2 + 100)
                                        self.mainMenuButton = Button("Hauptmenü".decode("utf-8"), 1, (self.width - 190) / 2, (self.height - 250) / 2 + 200)
                                        self.maxButtonIdx = 2
                                        self.buttonTexts = ["Fortsetzen", "Speichern", "Hauptmenü".decode("utf-8")]
                        self.currentScene.HandleEvent(event)
                elif self.state == 2:
                        self.MoveMenuPointer(event)
                        if event.type == pygame.KEYDOWN:
                                if event.key == K_ESCAPE:
                                        self.state = 1
                                        self.currentScene.Unpause()
                                if event.key == K_RETURN:
                                        if self.buttonIdx == 0:
                                                self.continueButton.SetState(True)
                                        elif self.buttonIdx == 1:
                                                self.saveButton.SetState(True)
                                        elif self.buttonIdx == 2:
                                                self.mainMenuButton.SetState(True)
                elif self.state == 3:
                        self.MoveMenuPointer(event)
                        if event.type == pygame.KEYDOWN:
                                if event.key == K_ESCAPE:
                                        self.state = 0
                                if event.key == K_RETURN:
                                        self.loadSavesButtons[self.buttonIdx][0].SetState(True)
                elif self.state == 4:
                        if event.type == pygame.KEYDOWN:
                                if event.key == K_ESCAPE:
                                        self.state = 0
                                elif event.key == K_RETURN and len(self.inputText) > 0:
                                        if not os.path.exists("save\\"):
                                                os.makedirs("save\\")
                                        handle = open("save\\" + self.inputText, "w")
                                        handle.write(self.loadedScene + "\n" + str(self.scoreCounter))
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
                                self.stop()
                        if self.newGameButton.GetState():
                                self.newGameButton.SetState(False)
                                self.LoadScene("scene1.txt")
                                self.scoreCounter = 0
                                self.state = 1
                        if self.loadGameButton.GetState():
                                self.loadGameButton.SetState(False)
                                speech.Speaker.output("Spielstand wählen.".decode("utf-8"), True)
                                _,_,files = os.walk("save\\").next()
                                self.loadSavesButtons = list()
                                sw = self.screen.get_width()
                                y = 20
                                self.buttonTexts = list()
                                for file in files:
                                        self.loadSavesButtons.append([Button(file, 1, (sw - 190) / 2, y), file])
                                        self.buttonTexts.append(file.decode(sys.getfilesystemencoding()))
                                        y += 60
                                self.maxButtonIdx = len(files) - 1
                                self.buttonIdx = 0
                                self.state = 3
                elif self.state == 1:
                        self.currentScene.Update()
                        next = self.currentScene.GetNextScene()
                        if next:
                                if "#" in next:
                                        idx = next.find("#")
                                        counter = next[(idx + 1):]
                                        next = next[:idx]
                                        if counter[0] == "+":
                                                self.scoreCounter += int(counter[1:])
                                        else:
                                                self.scoreCounter -= int(counter[1:])
                                if next == "end":
                                        self.state = 5
                                        sw, sh = 0, 0
                                        handle = open("assets\\scene\\credits.txt", "r")
                                        lines = list()
                                        font = getCommon().getTextFont()
                                        for line in handle:
                                                l = line.strip()
                                                lines.append(l)
                                                if len(l) > 0 and l[0] == '#':
                                                        if l[1] == 'i':
                                                                isurf = pygame.image.load("assets\\credits\\" + l[2:])
                                                                tw, th = isurf.get_width(), isurf.get_height()
                                                else:
                                                        tw, th = font.size(l)
                                                sh += th + 2
                                                if sw < tw: sw = tw
                                        surf = pygame.Surface((sw, sh))
                                        sh = 0
                                        for line in lines:
                                                if len(line) > 0 and line[0] == '#':
                                                        if line[1] == 'i':
                                                                ts = pygame.image.load("assets\\credits\\" + line[2:]).convert_alpha()
                                                                tw, th = isurf.get_width(), isurf.get_height()
                                                else:
                                                        tw, th = font.size(line)
                                                        ts = font.render(line, 0, (255, 255, 255))
                                                surf.blit(ts, ((sw - tw) / 2, sh))
                                                sh += th + 2
                                        self.creditsSurf = surf
                                        self.creditsStartTime = time.time()
                                        self.creditsScrollStart = self.screen.get_height()
                                        self.creditsScroll = self.creditsScrollStart
                                        self.creditsScrollEnd = -surf.get_height()
                                        self.creditsScrollRange = self.screen.get_height() + surf.get_height()
                                        bass = getCommon().getBass()
                                        try:
                                                creditsStream = boss.CreateStreamFile(False, "assets\\credits\\music.ogg")
                                                creditsStream.Channel.Play()
                                        except:
                                                print("no credits music found")
                                        self.fadeOutStream = self.oldBgmStream
                                        self.fadeOutStartTime = time.time()
                                        self.fadeOutDuration = 1
                                else:
                                        self.LoadScene(next)
                                        newStream = self.currentScene.GetBgmStream()
                                        if newStream:
                                                if self.fadeOutStream:
                                                        self.fadeOutStream.Channel.Stop()
                                                self.fadeOutStream = self.oldBgmStream
                                                self.oldBgmStream = newStream
                                                self.fadeOutStartTime = time.time()
                                                self.fadeOutDuration = 1
                elif self.state == 2:
                        self.continueButton.Update()
                        self.mainMenuButton.Update()
                        self.saveButton.Update()
                        if self.mainMenuButton.GetState():
                                self.maxButtonIdx = 2
                                self.buttonIdx = 0
                                self.buttonTexts = ["Neues Spiel", "Spiel laden", "Beenden"]
                                self.state = 0
                        if self.continueButton.GetState():
                                self.state = 1
                                self.currentScene.Unpause()
                        if self.saveButton.GetState():
                                self.saveButton.SetState(False)
                                self.inputText = ""
                                speech.Speaker.output("Dateinamen eingeben", True)
                                self.state = 4
                elif self.state == 3:
                        for b in self.loadSavesButtons:
                                b[0].Update()
                                if b[0].GetState():
                                        b[0].SetState(False)
                                        handle = open("save\\" + b[1], "r")
                                        self.LoadScene(handle.readline().strip())
                                        self.scoreCounter = int(handle.readline().strip())
                                        self.state = 1
                                        handle.close()
                elif self.state == 5:
                        alpha = (time.time() - self.creditsStartTime) / 20
                        self.creditsScroll = self.creditsScrollEnd * alpha + self.creditsScrollStart * (1 - alpha)
                        if self.creditsScroll <= self.creditsScrollEnd:
                                self.state = 0
                                
                if self.fadeOutStream:
                        stream = self.fadeOutStream
                        start = self.fadeOutStartTime
                        duration = self.fadeOutDuration
                        alpha = (time.time() - start) / duration
                        if alpha > 1:
                                self.fadeOutStream.Channel.Stop()
                                self.fadeOutStream = None
                        else:
                                self.fadeOutStream.Channel.SetAttribute(BASS_ATTRIB_VOL, (1 - alpha) * BGM_MAX_VOL)
                                        
        def RenderMenuPointer(self, variant = 0):
                xOff = (time.time() * 20) % 20
                if xOff > 10: xOff = 20 - xOff
                if variant:
                        y = 20 + self.buttonIdx * 60
                else:
                        y = (self.height - 250) / 2 + self.buttonIdx * 100
                self.screen.blit(getCommon().getUI().Icon("right"), ((self.width - 190) / 2 - 50 + xOff, y))
                self.screen.blit(getCommon().getUI().Icon("left"), ((self.width + 190) / 2 - xOff, y))
                                        
        def Render(self):
                # TODO: draw stuff
                self.screen.fill((0,0,0))
                if self.state == 0:
                        self.newGameButton.Draw(self.screen)
                        self.loadGameButton.Draw(self.screen)
                        self.exitButton.Draw(self.screen)
                        self.RenderMenuPointer()
                elif self.state == 1:
                        self.currentScene.Draw()
                elif self.state == 2:
                        self.currentScene.Draw()
                        self.screen.blit(self.darken, (0, 0))
                        self.mainMenuButton.Draw(self.screen)
                        self.continueButton.Draw(self.screen)
                        self.saveButton.Draw(self.screen)
                        self.RenderMenuPointer()
                elif self.state == 3:
                        for b in self.loadSavesButtons:
                                b[0].Draw(self.screen)
                        self.RenderMenuPointer(1)
                elif self.state == 4:
                        ui = getCommon().getUI()
                        font = getCommon().getTextFont()
                        self.screen.blit(ui.Panel(300, 80), (10, 10))
                        self.screen.blit(font.render("File: " + self.inputText, 0, (255, 255, 255)), (20, 40))
                elif self.state == 5:
                        self.screen.blit(self.creditsSurf, ((self.screen.get_width() - self.creditsSurf.get_width()) / 2, self.creditsScroll))
                pygame.display.flip()
                                        
if __name__ == "__main__":
        game = MainClass()
        game.MainLoop()
