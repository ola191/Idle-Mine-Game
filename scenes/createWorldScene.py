import pygame

import time
import sys
import os
import ujson
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
        random.seed(seed)
        noise = PerlinNoise(octaves=4, seed=seed)

        startTime = time.time()

        def initializeMap(width, height, fillProb=0.45, airHeight=10):
            mapData = np.ones((width, height), dtype=int)  # 1: blackStone

            mapData[:airHeight, :] = 4  # 4: air

            mapData[airHeight:, :] = np.random.choice([0, 1], size=(width - airHeight, height), p=[1-fillProb, fillProb])  # 0: stone, 1: blackStone
            return mapData

        def smoothMap(mapData, iterations=5):
            for _ in range(iterations):
                newMap = mapData.copy()
                for x in range(1, mapData.shape[0] - 1):
                    for y in range(1, mapData.shape[1] - 1):
                        wallCount = np.sum(mapData[x-1:x+2, y-1:y+2] == 1)  # Count only blackStone
                        if wallCount > 4:
                            newMap[x, y] = 1  # 1: blackStone
                        elif wallCount < 4:
                            newMap[x, y] = 0  # 0: stone
                mapData = newMap
            return mapData

        def addAirLayer(mapData, airHeight, grassLayer):
            height, width = mapData.shape
            for x in range(width):
                grassLevel = grassLayer[x]
                if grassLevel < height:  
                    mapData[:grassLevel, x] = 4
            return mapData

        def addGrassLayer(mapData, airHeight, grassHeight, minGrassHeight=2):
            height, width = mapData.shape
            grassLayer = []

            noise = PerlinNoise(octaves=4, seed=1)
            
            for x in range(width):
                grassBaseHeight = airHeight + int((noise([x / width]) + 1) * grassHeight / 2)
                highestGrassHeight = grassBaseHeight + grassHeight - 1 
                
                if x > 0:
                    prevGrassHeight = grassLayer[-1]
                    if highestGrassHeight > prevGrassHeight + 1:
                        highestGrassHeight = prevGrassHeight + 1
                    elif highestGrassHeight < prevGrassHeight - 1:
                        highestGrassHeight = prevGrassHeight - 1

                if highestGrassHeight < minGrassHeight:
                    highestGrassHeight = minGrassHeight

                mapData[highestGrassHeight, x] = 2  # 2: grass
                grassLayer.append(highestGrassHeight)

            return [mapData, grassLayer]

        def makeNoise():
            width, height = 200, 200
            airHeight = 50
            grassHeight = 10  
            minGrassHeight = 3 
            
            mapData = initializeMap(width, height, airHeight=airHeight)
            mapData = smoothMap(mapData)
            response = addGrassLayer(mapData, airHeight, grassHeight, minGrassHeight=minGrassHeight)
            mapData = response[0]
            grassLayer = response[1]
            mapData = addAirLayer(mapData, airHeight, grassLayer)
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
