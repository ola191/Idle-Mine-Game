import pygame

import numpy
import sys
import time

from ui.button import Button

class GameScene:
    def __init__(self, screen, font, worldData):
        self.screen = screen
        self.font = font
        self.worldData = worldData
        self.mapData = numpy.array(self.worldData["map"])
        self.resources = self.worldData['resources']
        self.running = True

        self.screenWidth, self.screenHeight = screen.get_size()
        self.mapHeight, self.mapWidth = self.mapData.shape
        self.tileSize = min(self.screenWidth // self.mapWidth, self.screenHeight // self.mapHeight)

        self.colorMap = {
            1: (140, 70, 20),  # Dirt
            2: (100, 100, 100),# blackStone
            3: (130, 130, 130),# Stone
            4: (200, 255, 200),# Andezit
            5: (0, 0, 255),    # Water
            6: (210, 210, 210) # Gravel
        }

    def drawMap(self):
        for y in range(self.mapHeight):
            for x in range(self.mapWidth):
                value = int(self.mapData[y][x])
                color = self.colorMap.get(value, (0,0,0))
                pygame.draw.rect(self.screen, color, pygame.Rect(x*self.tileSize, y*self.tileSize, self.tileSize, self.tileSize))

    def run(self):  
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.screen.fill((255, 255, 255))
            # startTime = time.time()
            self.drawMap()
            # print(f"Drawing map : {time.time() - startTime}")
            # text = self.font.render(f"World: {self.worldData['name']}", True, (0,0,0))
            # self.screen.blit(text, (10, 10))
            # textResources = self.font.render(f"Resources: {self.resources}", True, (0, 0, 0))
            # self.screen.blit(textResources, (10, 60))
            pygame.display.flip()
            return self
