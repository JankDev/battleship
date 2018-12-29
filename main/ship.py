import pygame
from pygame.sprite import Sprite, Group

pygame.init()


class Ship(Sprite):
    def __init__(self, width, height, fields, coordinates):
        Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("../images/battleship_image").convert_alpha(),
                                            (width, height))
        self.width = width
        self.height = height
        self.fields = fields
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.coordinates = (self.rect.x, self.rect.y)
        self.dragging = False
        self.game_coordinates = list()

    def update(self, dragging, rect, image):
        self.dragging = dragging
        self.rect = rect
        self.rect.width = rect.x + self.width
        self.rect.height = rect.y + self.height
        self.image = image

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect.width, self.rect.height = self.rect.height, self.rect.width
        print(self.rect)

    def on_right_click(self, event, position):
        if self.is_clicked(event, position) and event.button == 3:
            self.rotate()

    def is_clicked(self, event, position):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(position):
                return True
        return False

    def on_drag(self, event, position):
        global offset_x
        global offset_y
        if self.is_clicked(event, position) and event.button == 1:
            mouse_x, mouse_y = event.pos
            offset_x = self.rect.x - mouse_x
            offset_y = self.rect.y - mouse_y
            self.dragging = True
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.x = position[0] + offset_x
            self.rect.y = position[1] + offset_y
        else:
            self.dragging = False

    def get_game_coordinates(self):
        x = self.rect.x // 80
        y = self.rect.y // 80
        y = y + 1
        if self.rect.width > self.rect.height:
            for i in range(x, x + self.fields):
                self.game_coordinates.append((chr(i + 65), y))
        else:
            for i in range(y, y + self.fields):
                self.game_coordinates.append((chr(x + 65), i))
        return self.game_coordinates

    def got_ship_hit(self, coords):
        if coords in self.game_coordinates:
            self.game_coordinates.remove(coords)


class ShipContainer(Group):
    def __init__(self, ships):
        super().__init__(ships)

    def handle_events(self, event, pos):
        for ship in self.sprites():
            ship.on_right_click(event, pos)
            ship.on_drag(event, pos)
