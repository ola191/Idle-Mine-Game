import pygame
import sys
from ui.button import Button

class GameScene:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.resources = 0
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.screen.fill((255, 255, 255))
            text = self.font.render(f"Resources: {self.resources}", True, (0, 0, 0))
            self.screen.blit(text, (10, 10))
            pygame.display.flip()
            return self
