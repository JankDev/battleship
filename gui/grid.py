import pygame

pygame.init()

aqua = (102, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
field_width = 80
field_height = 80


class Field:
    def __init__(self, rect):
        self.rect = rect
        self.draw_function = self.draw
        self.clicked = False
        self.color = None

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect, 2)

    def on_click_draw(self, screen):
        screen.fill(self.color, self.rect)


class Grid:
    def __init__(self, x, y):
        self.height = 10
        self.width = 10
        self.fields = list()
        for i in range(y, y + 10 * field_height, field_height):
            for j in range(x, x + 10 * field_width, field_width):
                rect = pygame.Rect(j, i, field_width, field_height)
                field = Field(rect)
                self.fields.append(field)

    def draw(self, screen):
        for field in self.fields:
            field.draw_function(screen)

    def handle_events(self, event, pos):
        for field in self.fields:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and field.rect.collidepoint(pos):
                field.draw_function = field.on_click_draw
                field.clicked = True
                break
