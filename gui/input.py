import pygame as pg

pg.init()

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 25)
WHITE = (255, 255, 255)


class InputField:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, (0, 0, 0))
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

                self.txt_surface = FONT.render(self.text, True, (0, 0, 0))

    def update(self):

        width = max(400, self.txt_surface.get_width() + 10)
        self.rect.width = width

    def draw(self, screen):

        self.txt_surface = FONT.render(self.text, True, (0, 0, 0))

        pg.draw.rect(screen, WHITE, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
