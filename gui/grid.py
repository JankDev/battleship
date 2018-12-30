import pygame

pygame.init()

aqua = (102, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
field_width = 80
field_height = 80


class Field:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.draw_function = self.draw
        self.clicked = False
        self.color = None

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect, 2)

    def on_click_draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        screen.fill(self.color, [self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6])


class Grid:
    def __init__(self, x, y):
        self.height = 10
        self.width = 10
        self.fields = list()
        for i in range(y, y + 10 * field_height, field_height):
            for j in range(x, x + 10 * field_width, field_width):
                field = Field(j, i)
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
