import pygame

pygame.init()


class Button:
    def __init__(self, width, height, x, y, color, text):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.function = None
        self.active = False

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render(self.text, True, (0xff, 0xff, 0xff))
        text_rect = text.get_rect()
        text_rect.center = ((self.x + (self.width / 2)), (self.y + (self.height / 2)))
        screen.blit(text, text_rect)

    def handle_events(self, event, pos):
        if self.width + self.x > pos[0] > self.x and self.height + self.y > pos[1] > self.y:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click(self.function)
        else:
            pass

    def on_click(self, do):
        self.function = do
        if self.active:
            self.function()
        self.active = True


class ButtonContainer:
    def __init__(self, buttons):
        self.buttons = buttons

    def handle_events(self, event, pos):
        for button in self.buttons:
            button.handle_events(event, pos)
