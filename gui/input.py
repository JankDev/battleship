from resources.colors import *
from resources.fonts import *

pg.init()


class InputField:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = INPUT_FONT.render(text, True, (0, 0, 0))
        self.active = False

    def handle_events(self, event, pos):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:

                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.txt_surface = INPUT_FONT.render(self.text, True, (0, 0, 0))

    def update(self):

        width = max(400, self.txt_surface.get_width() + 10)
        self.rect.width = width

    def draw(self, screen):

        self.txt_surface = INPUT_FONT.render(self.text, True, (0, 0, 0))
        pg.draw.rect(screen, self.color, self.rect, 3)
        pg.draw.rect(screen, WHITE, [self.rect.x + 3, self.rect.y + 3, self.rect.width - 6, self.rect.height - 6])

        screen.blit(self.txt_surface, (self.rect.x + 8, self.rect.y + 8))
