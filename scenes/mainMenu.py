import pygame
import sys
import os 

from scenes.createWorldScene import CreateWorldScene
from scenes.loadWorldScene import LoadWorldScene
from ui.button import Button
from scenes.gameScene import GameScene


class MainMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.loadButton = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 - 40, 200, 50, "Load World", (255, 255, 255), font, self.loadWorld, "./assets/textures/ui/button.png", (0,0,0))
        self.createButton = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 + 40, 200, 50, "Create World", (255, 255, 255), font, self.createWorld, "./assets/textures/ui/button.png", (0,0,0))
        self.currentScene = None

        self.bgScale = 1
        self.bgImage = pygame.image.load("./assets/textures/bg/mainMenu.png").convert_alpha()
        self.bgImage = pygame.transform.scale(self.bgImage, (self.screen.get_width() * self.bgScale, self.screen.get_height() * self.bgScale))

    def loadWorld(self):
        self.currentScene = LoadWorldScene(self.screen, self.font)

    def createWorld(self):
        self.currentScene = CreateWorldScene(self.screen, self.font)
    
    def changeResolution(self):
        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)
        self.loadButton.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 - 40)
        self.createButton.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 40)
        self.loadButton.textRect = self.loadButton.textSurface.get_rect(center=self.loadButton.rect.center)
        self.createButton.textRect = self.createButton.textSurface.get_rect(center=self.createButton.rect.center)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.changeResolution()
                self.loadButton.isClicked(event)
                self.createButton.isClicked(event)

            self.bgImage = pygame.transform.scale(self.bgImage, (self.screen.get_width() * self.bgScale, self.screen.get_height() * self.bgScale))
            self.screen.blit(self.bgImage, (0, 0))
            self.loadButton.draw(self.screen)
            self.createButton.draw(self.screen)
            pygame.display.flip()

            if self.loadButton.isClicked(event):
                self.loadWorld
            elif self.createButton.isClicked(event):
                self.createWorld

            if self.currentScene:
                return self.currentScene.run()