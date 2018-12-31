import pygame

pygame.init()


class Button:
    def __init__(self, width, height, x, y, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.function = None
        self.active = False

    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render(self.text, True, (0xff, 0xff, 0xff))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text, text_rect)

    def handle_events(self, event: pygame.event, pos):
        if self.rect.collidepoint(pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click(self.function)
        else:
            pass

    def on_click(self, do):
        self.function = do
        if self.active:
            self.function()
        self.active = True

    def update(self):
        pass


class ButtonContainer:
    def __init__(self, buttons: list):
        self.buttons = buttons

    def handle_events(self, event, pos):
        for button in self.buttons:
            button.handle_events(event, pos)

    def add(self, button):
        self.buttons.append(button)

    def remove(self, button):
        self.buttons.remove(button)

    def clear(self):
        self.buttons.clear()
