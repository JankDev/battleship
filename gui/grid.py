from db.database import Database
from resources.colors import *
from resources.fonts import *

pygame.init()


class Field:
    def __init__(self, x, y, field_width=80, field_height=80):
        self.rect = pygame.Rect(x, y, field_width, field_height)
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
        self.fields = list()
        for i in range(y, y + 10 * 80, 80):
            for j in range(x, x + 10 * 80, 80):
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

    def change_field_color(self, rect: pygame.rect, color):
        for field in self.fields:

            if rect == field.rect and not field.color:
                field.color = color
                field.draw_function = field.on_click_draw
                break


class Table:
    def __init__(self, x, y):
        self.fields = list()
        for i in range(y, y + 10 * 70, 70):
            for j in range(x, x + 2 * 350, 350):
                field = Field(j, i, 350, 70)
                self.fields.append(field)

    def draw(self, screen):
        db_result = Database().get_all()
        i = 0

        for field in self.fields:
            field.draw_function(screen)

            if int(i) == i:
                text = table_font.render(db_result[int(i)][0], True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = ((field.rect.x + (field.rect.width / 2)),
                                    (field.rect.y + (field.rect.height / 2)))
                screen.blit(text, text_rect)
            else:
                text = table_font.render(str(db_result[int(i - 0.5)][1]), True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = ((field.rect.x + (field.rect.width / 2)),
                                    (field.rect.y + (field.rect.height / 2)))
                screen.blit(text, text_rect)
            i = i + 0.5
