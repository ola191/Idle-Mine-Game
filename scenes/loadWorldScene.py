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

    def loadWorldButtons(self):
        worldFiles = os.listdir(self.worldsFolder)
        worldFiles = [f for f in worldFiles if f.endswith('.json')]

        for idx, filename in enumerate(worldFiles):
            worldName = filename.split('.')[0]
            button = Button(self.screen.get_width() // 2 - 100, 50 + idx * 70, 200, 50, worldName, (255, 255, 255), self.font, lambda: self.loadWorld(worldName))
            self.worldButtons.append(button)

    def loadWorld(self, worldName):
        filepath = os.path.join(self.worldsFolder, f"{worldName}.json")
        with open(filepath, 'r') as f:
            worldData = json.load(f)
        
        self.currentScene = GameScene(self.screen, self.font, worldData) 

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.worldButtons:
                    button.isClicked(event)

            self.screen.fill((255, 255, 255))
            for button in self.worldButtons:
                button.draw(self.screen)
            pygame.display.flip()

            if self.currentScene:
                return self.currentScene.run()

