from pygame.sprite import Group

from db.database import Database
from gui.button import *
from gui.grid import Grid, Table
from gui.input import InputField
from main.game import start_game
from main.ship import Ship, ShipContainer
from resources.colors import *
from resources.fonts import *

pygame.init()

game_screen_bg = pygame.image.load("../resources/ocean.jpg")
start_screen_bg = pygame.image.load("../resources/ship_background")

SHIP_HEIGHT = 65


class EventObjectsContainer:
    container: list

    def __init__(self, containers: list):
        self.container = containers

    def add(self, container):
        self.container.append(container)

    def remove(self, container):
        self.container.remove(container)


class Screen:
    event_container: EventObjectsContainer

    def __init__(self):
        self.image = None
        self.event_container = None
        self.parent = self

    def draw(self, window):
        pass

    def update(self, window):
        pass


class MainScreen(Screen):
    def __init__(self, screen: Screen):
        self.screen = screen
        self.screen.parent = self

    def draw(self, window):
        self.screen.draw(window)

    def update(self, window):
        self.screen.update(window)

    def handle_events(self, event, pos):
        for event_container in self.screen.event_container.container:
            event_container.handle_events(event, pos)

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
        exit_button.on_click(quit_game)
        play_button = Button(350, 70, window.get_rect().width / 2 - 175, 400, BLACK, "Play vs Computer")
        play_button.on_click(lambda: self.parent.change_screen(GameScreen(), window))
        help_button = Button(350, 70, window.get_rect().width / 2 - 175, 500, BLACK, "Help")
        help_button.on_click(lambda: self.parent.change_screen(HelpScreen(), window))
        scores_button = Button(350, 70, window.get_rect().width / 2 - 175, 600, BLACK, "Scores")
        scores_button.on_click(lambda: self.parent.change_screen(ScoreScreen(), window))
        self.button_container = ButtonContainer((exit_button, play_button, scores_button, help_button))

        self.event_container = EventObjectsContainer([self.button_container])
        for button in self.button_container.buttons:
            button.draw(window)

    def update(self, window):
        window.blit(self.image, (0, 0))

        for button in self.button_container.buttons:
            button.draw(window)


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
        self.text_color = DARK_GREEN
        self.display_text = ""
        self.input_field = InputField(300, 800, 400, 50)
        self.guesses = 0
        self.pop_up = False

    def draw(self, window):
        window.blit(self.image, (0, 0))

        self.player_grid.draw(window)
        self.computer_grid.draw(window)

        start_button = Button(280, 50, 810, 100, BLACK, "Start")
        start_button.on_click(lambda: start_game(self))
        quit_button = Button(280, 50, 810, 200, BLACK, "Quit")
        quit_button.on_click(quit_game)
        self.button_container = ButtonContainer([start_button, quit_button])

        ship1 = Ship(200, SHIP_HEIGHT, 3, (300, 800))
        ship2 = Ship(130, SHIP_HEIGHT, 2, (100, 800))
        ship3 = Ship(300, SHIP_HEIGHT, 4, (500, 800))
        ship4 = Ship(130, SHIP_HEIGHT, 2, (100, 900))
        ship5 = Ship(370, SHIP_HEIGHT, 5, (800, 800))

        self.ship_container = ShipContainer([ship1, ship2, ship3, ship4, ship5])

        guess_text = font.render("Number of guesses: " + str(self.guesses), True, RED)
        window.blit(guess_text, [1200, 900, 150, 40])
        for button in self.button_container.buttons:
            button.draw(window)
        self.ship_container.draw(window)
        self.input_field.rect.x = window.get_rect().width / 2 - 200
        self.event_container = EventObjectsContainer([self.ship_container, self.button_container])
        self.event_container.add(self.input_field)

    def update(self, window):

        window.blit(self.image, (0, 0))
        guess_text = font.render("Number of guesses: " + str(self.guesses), True, RED)
        window.blit(guess_text, [1200, 900, 150, 40])
        self.player_grid.draw(window)
        self.computer_grid.draw(window)
        self.ship_container.draw(window)
        ok_button = Button(100, 30, window.get_rect().width / 2 - 50, window.get_rect().height / 2 + 30, BLACK, "Ok")
        ok_button.on_click(self.no_pop)

        if self.pop_up:
            box = pygame.Rect(window.get_rect().width / 2, window.get_rect().height / 2, 700, 300)
            box.center = (window.get_rect().width / 2, window.get_rect().height / 2)
            pygame.draw.rect(window, WHITE, box)
            text = small_font.render("Invalid ship position!Change it ", True, RED)
            text_rect = text.get_rect()
            text_rect.center = (window.get_rect().width / 2, window.get_rect().height / 2)
            window.blit(text, text_rect)

            ok_button.draw(window)
            self.event_container.add(ok_button)
        for button in self.button_container.buttons:
            button.draw(window)

        if self.game_started:
            if self.ship_container in self.event_container.container:
                self.event_container.remove(self.ship_container)

        if self.game_over:
            if self.button_container:
                self.button_container.clear()
            if self.computer_grid in self.event_container.container:
                self.event_container.remove(self.computer_grid)

            text = game_over_font.render(self.display_text, True, self.text_color)
            text_rect = text.get_rect()
            text_rect.center = (window.get_rect().width / 2, window.get_rect().height / 2 - 100)
            window.blit(text, text_rect)
            if self.text_color == DARK_GREEN:
                text2 = font.render("Type in your name", True, VIOLET)
                text_rect2 = text2.get_rect()
                text_rect2.center = (window.get_rect().width / 2, 700)
                window.blit(text2, text_rect2)
                self.input_field.update()
                self.input_field.draw(window)
            submit_button = Button(350, 80, window.get_rect().width / 2 - 175, 900, BLACK, "Ok")
            submit_button.on_click(lambda: [Database().save(self.input_field.text, self.guesses),
                                            self.parent.change_screen(StartScreen(), window)])
            submit_button.draw(window)

            self.button_container.add(submit_button)

    def no_pop(self):
        self.pop_up = False


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

        text = head_font.render("Rules:", True, RED)
        text2 = font.render("The goal of this game is to hit all ships of the enemy", True, RED)
        text3 = font.render("Each player has 5 ships: 2 of length 2, 1 of length 3,4,5", True, RED)
        text4 = font.render("The player who first hits all enemy ships wins", True, RED)
        text5 = head_font.render("Mechanics:", True, GREEN)
        text6 = font.render("Drag the ship to move it, to rotate it right click it", True, GREEN)
        text7 = font.render("After clicking start the game starts.Click on the right for your guesses", True, GREEN)
        text_container = [text, text2, text3, text4, text5, text6, text7]
        for i in range(7):
            window.blit(text_container[i], (100, (i + 1) * 100))


class ScoreScreen(Screen):
    def __init__(self):
        super().__init__()
        self.button_container = None
        self.event_container = None

    def draw(self, window):
        window.fill(GOLD)

        back_button = Button(350, 50, window.get_rect().width / 2 - 175, 1000, BLACK, "Back")
        back_button.on_click(lambda: self.parent.change_screen(StartScreen(), window))
        self.button_container = ButtonContainer([back_button])
        for button in self.button_container.buttons:
            button.draw(window)

        table = Table(window.get_rect().width // 2 - 350, 200)
        table.draw(window)
        self.event_container = EventObjectsContainer([self.button_container])

    def update(self, window):
        window.fill(GOLD)

        for button in self.button_container.buttons:
            button.draw(window)

        table = Table(window.get_rect().width // 2 - 350, 200)
        table.draw(window)
        text = head_font.render("Best scores!", True, RED)
        text_rect = text.get_rect()
        text_rect.center = (window.get_rect().width / 2, 60)
        window.blit(text, text_rect)


def quit_game():
    pygame.quit()
    quit()
