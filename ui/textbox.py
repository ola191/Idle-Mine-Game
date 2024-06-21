import pygame

class TextBox:
    def __init__(self, x, y, width, height, font, textColor=(0, 0, 0), bgColor=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.textColor = textColor
        self.bgColor = bgColor
        self.text = ''
        self.active = False

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def getText(self):
        return self.text

    def update(self):
        if self.active:
            self.bgColor = (200, 200, 200)
        else:
            self.bgColor = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgColor, self.rect)
        textSurface = self.font.render(self.text, True, self.textColor)
        screen.blit(textSurface, (self.rect.x + 5, self.rect.y + 5))