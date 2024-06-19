import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, font, action):
        self.rect = pygame.Rect(x,y, width, height)
        self.text = text
        self.color = color
        self.font = font
        self.action = action

    def draw(self,screen):
        pygame.draw.rect(screen, (200,200,200), self.rect)
        text_surface = self.font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                    return True
        return False