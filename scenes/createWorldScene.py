import pygame

import sys
import os
import json
import random
import numpy

from perlin_noise import PerlinNoise

from ui.textbox import TextBox
from ui.button import Button
from scenes.gameScene import GameScene

class CreateWorldScene:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.worldNameInput = TextBox(screen.get_width() // 2 - 100, screen.get_height() // 2 - 40, 200, 50, font)
        self.createButton = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 + 40, 200, 50, "Create new world", (255, 255, 255), font, self.createWorld)
        self.currentScene = None

    def createWorld(self):
        worldName = self.worldNameInput.getText()
        if worldName.strip() == "":
            return
        
        seed = random.seed(random.randint(0, 100000))

        shape = (20,20)
        scale = 10.0
        octaves = 6 

        noise = PerlinNoise(octaves=octaves, seed=seed)

        mapData = numpy.zeros(shape)

        for i in range(shape[0]):
            for j in range(shape[1]):
                noiseValue = noise([i/scale, j/scale])
                scaledValue = numpy.interp(noiseValue, (-1,1), (1,6))
                mapData[i][j] = int(round(scaledValue))

        print(f"{mapData}")
        
        map = noise
        worldData = {
            "name": worldName,
            "resources" : 0,
            "seed" : seed,
            "map" : mapData.tolist()
        }
        filepath = os.path.join("worlds", f"{worldName}.json")
        with open(filepath, 'w') as f:
            json.dump(worldData, f)
        
        self.currentScene = GameScene(self.screen, self.font, worldData)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.worldNameInput.handleEvent(event)
                self.createButton.isClicked(event)

            self.screen.fill((255, 255, 255))
            self.worldNameInput.update()
            self.worldNameInput.draw(self.screen)
            self.createButton.draw(self.screen)
            pygame.display.flip()

            if self.currentScene:
                return self.currentScene.run()
