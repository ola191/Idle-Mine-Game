import pygame
import sys
from ui.button import Button
from scenes.gameScene import GameScene

class MainMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.loadButton = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 - 60, 200, 50, "Load World", (255, 255, 255), font, self.loadWorld)
        self.createButton = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 + 10, 200, 50, "Create World", (255, 255, 255), font, self.createWorld)
        self.currentScene = None

    def loadWorld(self):
        self.currentScene = GameScene(self.screen, self.font)

    def createWorld(self):
        self.currentScene = GameScene(self.screen, self.font)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.loadButton.isClicked(event)
                self.createButton.isClicked(event)

            self.screen.fill((255, 255, 255))
            self.loadButton.draw(self.screen)
            self.createButton.draw(self.screen)
            pygame.display.flip()

            if self.loadButton.isClicked(event):
                self.loadWorld
            elif self.createButton.isClicked(event):
                self.createWorld

            if self.currentScene:
                return self.currentScene.run()