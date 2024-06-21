import pygame

class Button:
    def __init__(self, x, y, width, height, text=None, textColor=None, font=None, action=None, imagePath=None, bgColor=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.image = None
        self.textColor = textColor
        self.bgColor = bgColor

        if imagePath:
            self.loadImage(imagePath)
        self.renderText()

    def loadImage(self, imagePath):
        try:
            self.image = pygame.image.load(imagePath).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        except pygame.error as e:
            print(f"Error loading image: {imagePath}")
            raise SystemExit(e)

    def renderText(self):
        if self.text and self.font:
            self.textSurface = self.font.render(self.text, True, self.textColor)
            self.textRect = self.textSurface.get_rect(center=self.rect.center)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
            screen.blit(self.textSurface, self.textRect)
        else:
            screen.fill(self.bgColor, self.rect)
            screen.blit(self.textSurface, self.textRect)

    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                    return True
        return False
