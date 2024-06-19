import pygame
import sys

from scenes.mainMenu import MainMenu

pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Idle Mine")

font = pygame.font.Font(None, 36)

def start():
    currentScene = MainMenu(screen, font)
    while True:
        currentScene = currentScene.run()
        pygame.display.flip()

if __name__ == "__main__":
    start()