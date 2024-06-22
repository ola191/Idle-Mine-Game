import pygame
import sys
import os
import json
from ui.button import Button
from scenes.gameScene import GameScene

class LoadWorldScene:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.worldsFolder = "worlds"
        self.worldButtons = []
        self.loadWorldButtons()
        self.currentScene = None

        self.bgScale = 1
        self.bgImage = pygame.image.load("./assets/textures/bg/mainMenu.png").convert_alpha()
        self.bgImage = pygame.transform.scale(self.bgImage, (self.screen.get_width() * self.bgScale, self.screen.get_height() * self.bgScale))

    def loadWorldButtons(self):
        worldFiles = os.listdir(self.worldsFolder)
        worldFiles = [f for f in worldFiles if f.endswith('.json')]

        for idx, filename in enumerate(worldFiles):
            worldName = filename.split('.')[0]
            

            button = Button(self.screen.get_width() // 2 - 100, 50 + idx * 70, 200, 50, worldName, (255, 255, 255), self.font, lambda: self.loadWorld(worldName), "./assets/textures/ui/button.png", (0,0,0))
            self.worldButtons.append(button)

    def loadWorld(self, worldName):
        filepath = os.path.join(self.worldsFolder, f"{worldName}.json")
        with open(filepath, 'r') as f:
            worldData = json.load(f)
        
        self.currentScene = GameScene(self.screen, self.font, worldData) 

    def changeResolution(self):
        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)
        for button in self.worldButtons:
            button.rect.center = (self.screen.get_width() // 2, 50 + self.worldButtons.index(button) * 70)
            button.textRect = button.textSurface.get_rect(center=button.rect.center)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.changeResolution()
                for button in self.worldButtons:
                    button.isClicked(event)

            self.bgImage = pygame.transform.scale(self.bgImage, (self.screen.get_width() * self.bgScale, self.screen.get_height() * self.bgScale))
            self.screen.blit(self.bgImage, (0, 0))
            for button in self.worldButtons:
                button.draw(self.screen)
            pygame.display.flip()

            if self.currentScene:
                return self.currentScene.run()

