from pygame.sprite import Group

from gui.button import *
from gui.grid import Grid
from main.game import start_game
from main.ship import Ship, ShipContainer

pygame.init()

game_screen_bg = pygame.image.load("../images/ocean.jpg")
start_screen_bg = pygame.image.load("../images/ship_background")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SHIP_HEIGHT = 65


def quit_game():
    pygame.quit()
    quit()


class EventObjectsContainer:
    def __init__(self, containers):
        self.container = containers


class Screen:
    def __init__(self):
        self.image = None
        self.event_container = None
        self.parent = self

    def draw(self, window):
        pass

    def update(self, window):
        pass


class MainScreen(Screen):
    def __init__(self, screen):
        self.screen = screen
        self.screen.parent = self

    def draw(self, window):
        self.screen.draw(window)

    def update(self, window):
        self.screen.update()

    def handle_events(self, event, pos):
        for object in self.screen.event_container.container:
            object.handle_events(event, pos)

    def change_screen(self, screen, window):
        self.screen = screen
        self.screen.parent = self
        self.screen.draw(window)


class StartScreen(Screen):
    def __init__(self):
        super().__init__()
        self.image = start_screen_bg
        self.button_container = None
        self.event_container = None

    def draw(self, window):
        window.blit(self.image, (0, 0))
        exit_button = Button(350, 70, window.get_rect().width / 2 - 175, 700, BLACK, "Exit")
        exit_button.on_click(lambda: quit_game())
        play_button = Button(350, 70, window.get_rect().width / 2 - 175, 400, BLACK, "Play vs Computer")
        play_button.on_click(lambda: self.parent.change_screen(GameScreen(), window))
        help_button = Button(350, 70, window.get_rect().width / 2 - 175, 500, BLACK, "Help")
        help_button.on_click(lambda: self.parent.change_screen(HelpScreen(), window))
        scores_button = Button(350, 70, window.get_rect().width / 2 - 175, 600, BLACK, "Scores")
        self.button_container = ButtonContainer((exit_button, play_button, scores_button, help_button))
        tmp = [self.button_container]
        self.event_container = EventObjectsContainer(tmp)
        for button in self.button_container.buttons:
            button.draw(window)

    def update(self, window):
        pass

    def next_screen(self, screen):
        return screen


class GameScreen(Screen):
    def __init__(self):
        self.image = game_screen_bg
        self.ship_container = Group()
        self.player_grid = Grid(0, 0)
        self.computer_grid = Grid(1100, 0)
        self.button_container = list()
        self.event_container = None
        self.game_started = False
        self.game_over = False
        self.display_text = ""

    def draw(self, window):
        window.blit(self.image, (0, 0))

        self.player_grid.draw(window)
        self.computer_grid.draw(window)

        start_button = Button(280, 50, 810, 100, BLACK, "Start")
        start_button.on_click(lambda: [start_game(self), self.button_container.buttons.remove(start_button),
                                       self.event_container.container.append(self.computer_grid)])
        quit_button = Button(280, 50, 810, 200, BLACK, "Quit")
        quit_button.on_click(lambda: quit_game())
        self.button_container = ButtonContainer([start_button, quit_button])

        ship1 = Ship(200, SHIP_HEIGHT, 3, (300, 800))
        ship2 = Ship(130, SHIP_HEIGHT, 2, (100, 800))
        ship3 = Ship(300, SHIP_HEIGHT, 4, (500, 800))
        ship4 = Ship(130, SHIP_HEIGHT, 2, (100, 900))
        ship5 = Ship(370, SHIP_HEIGHT, 5, (800, 800))

        self.ship_container = ShipContainer([ship1, ship2, ship3, ship4, ship5])
        for button in self.button_container.buttons:
            button.draw(window)
        self.ship_container.draw(window)
        self.event_container = EventObjectsContainer([self.ship_container, self.button_container])

    def update(self, window):
        window.blit(self.image, (0, 0))
        self.player_grid.draw(window)
        self.computer_grid.draw(window)
        for button in self.button_container.buttons:
            button.draw(window)
        self.ship_container.draw(window)
        if self.game_started:
            if self.ship_container in self.event_container.container:
                self.event_container.container.remove(self.ship_container)
        if self.game_over:
            if self.computer_grid in self.event_container.container:
                self.event_container.container.remove(self.computer_grid)
            head_font = pygame.font.Font(pygame.font.get_default_font(), 130)
            text = head_font.render(self.display_text, True, GREEN)
            text_rect = text.get_rect()
            text_rect.center = (window.get_rect().width / 2, window.get_rect().height / 2)
            window.blit(text, text_rect)
            quit_button2 = Button(280, 50, window.get_rect().width / 2, 900, BLACK, "Quit")
            quit_button2.on_click(lambda: quit_game())
            quit_button2.draw(window)


class HelpScreen(Screen):
    def __init__(self):
        super().__init__()
        self.image = start_screen_bg
        self.button_container = None
        self.event_container = None

    def draw(self, window):
        window.fill(WHITE)
        back_button = Button(350, 50, window.get_rect().width / 2 - 175, 900, BLACK, "Back")
        back_button.on_click(lambda: self.parent.change_screen(StartScreen(), window))
        self.button_container = ButtonContainer([back_button])

        for button in self.button_container.buttons:
            button.draw(window)

        self.event_container = EventObjectsContainer([self.button_container])
        font = pygame.font.Font(pygame.font.get_default_font(), 50)
        head_font = pygame.font.Font(pygame.font.get_default_font(), 80)
        text = head_font.render("Rules:", True, RED)
        text2 = font.render("The goal of this game is to hit all ships of the enemy", True, RED)
        text3 = font.render("Each player has 5 ships: 2 of length 2, 1 of length 3,4,5", True, RED)
        text4 = font.render("The player who first hits all enemy ships wins", True, RED)
        text5 = head_font.render("Mechanics:", True, GREEN)
        text6 = font.render("Drag the ship to move it, to rotate it right click it", True, GREEN)
        text7 = font.render("After clicking start the game starts.Click on the right for your guesses", True, GREEN)

        text_rect = text.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()
        text_rect4 = text4.get_rect()
        text_rect5 = text5.get_rect()
        text_rect6 = text6.get_rect()
        text_rect7 = text7.get_rect()
        text_rect.topleft = (100, 100)
        text_rect2.topleft = (100, 200)
        text_rect3.topleft = (100, 300)
        text_rect4.topleft = (100, 400)
        text_rect5.topleft = (100, 500)
        text_rect6.topleft = (100, 600)
        text_rect7.topleft = (100, 700)
        window.blit(text, text_rect)
        window.blit(text2, text_rect2)
        window.blit(text3, text_rect3)
        window.blit(text4, text_rect4)
        window.blit(text5, text_rect5)
        window.blit(text6, text_rect6)
        window.blit(text7, text_rect7)
