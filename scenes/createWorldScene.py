import pygame

import time
import sys
import os
import json
import random
import numpy as np

from perlin_noise import PerlinNoise

from ui.textbox import TextBox
from ui.button import Button
from scenes.gameScene import GameScene

class CreateWorldScene:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.worldNameInput = TextBox(screen.get_width() // 2 - 100, screen.get_height() // 2 - 40, 200, 50, font)
        self.createButton = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 + 40, 200, 50, "Create", (255, 255, 255), font, self.createWorld, "./assets/textures/ui/button.png", (0,0,0))
        self.currentScene = None

        self.bgScale = 1
        self.bgImage = pygame.image.load("./assets/textures/bg/mainMenu.png").convert_alpha()
        self.bgImage = pygame.transform.scale(self.bgImage, (self.screen.get_width() * self.bgScale, self.screen.get_height() * self.bgScale))

    def createWorld(self):
        worldName = self.worldNameInput.getText()
        if worldName.strip() == "":
            return
        
        seed = random.randint(0, 100000)

        startTime = time.time()

        def initializeMap(width, height, fillProb=0.45):
            return np.random.choice([0, 1], size=(width, height), p=[1-fillProb, fillProb])

        def smoothMap(mapData, iterations=5):
            for _ in range(iterations):
                newMap = mapData.copy()
                for x in range(1, mapData.shape[0] - 1):
                    for y in range(1, mapData.shape[1] - 1):
                        wallCount = np.sum(mapData[x-1:x+2, y-1:y+2]) - mapData[x, y]
                        if wallCount > 4:
                            newMap[x, y] = 1
                        elif wallCount < 4:
                            newMap[x, y] = 0
                mapData = newMap
            return mapData

        def makeNoise():
            width, height = 200, 200
            mapData = initializeMap(width, height)
            mapData = smoothMap(mapData)
            return mapData

        mapData = makeNoise()
        
        print(f"generating map : {time.time() - startTime}")
        
        startTime = time.time()
        worldData = {
            "name": worldName,
            "resources" : 0,
            "seed" : seed,
            "map" : mapData.tolist()
        }
        filepath = os.path.join("worlds", f"{worldName}.json")
        with open(filepath, 'w') as f:
            json.dump(worldData, f)
        
        print(f"saving world : {time.time() - startTime}")
        
        self.currentScene = GameScene(self.screen, self.font, worldData)

    def changeResolution(self):
        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)
        self.createButton.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 40)
        self.createButton.textRect = self.createButton.textSurface.get_rect(center=self.createButton.rect.center)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.changeResolution()
                self.worldNameInput.handleEvent(event)
                self.createButton.isClicked(event)

            self.bgImage = pygame.transform.scale(self.bgImage, (self.screen.get_width() * self.bgScale, self.screen.get_height() * self.bgScale))
            self.screen.blit(self.bgImage, (0, 0))
            self.worldNameInput.update()
            self.worldNameInput.draw(self.screen)
            self.createButton.draw(self.screen)
            pygame.display.flip()

            if self.currentScene:
                return self.currentScene.run()
