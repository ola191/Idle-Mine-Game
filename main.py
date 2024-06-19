import pygame
import sys

pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Idle Mine")

font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, color, font, action):
        self.rect = pygame.Rect(x,y, width, height)
        self.text = text
        self.color = color
        self.font = font
        self.action = action

    def draw(self,screen):
        pygame.draw.rect(screen, (200,200,200), self.rect)
        text_surface = font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()



def loadWorld():
    global currentScene
    currentScene = gameScene
    
def createWorld():
    global currentScene
    currentScene = gameScene    

loadButton = Button(width // 2 - 100, height // 2- 60, 200, 50, "Load World", (255,255,255), font, loadWorld)
createButton = Button(width // 2 - 100, height // 2+ 10, 200, 50, "Create World", (255,255,255), font, createWorld)

def mainMenu():
    running = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            loadButton.isClicked(event)
            createButton.isClicked(event)
        
        screen.fill((255, 255, 255))
        loadButton.draw(screen)
        createButton.draw(screen)
        pygame.display.flip()

def gameScene():
    resources = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((255, 255, 255))
        text = font.render(f"Resources: {resources}", True, (0,0,0))
        screen.blit(text, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    currentScene = mainMenu
    while True:
        currentScene()