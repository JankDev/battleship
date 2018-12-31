import pygame

from main.computer import Computer
from main.player import Player
from resources.colors import *

FIELD_SIZE = 80

pygame.init()

player = Player()
computer = Computer()
game_started = False
hit_sound = pygame.mixer.Sound("../resources/bomb.wav")


def start_game(game_screen):
    global player, computer, game_started
    game_started = True
    player = Player()

    ships = list()
    for ship in game_screen.ship_container.sprites():
        if ship.rect.width > ship.rect.height:
            ship.rect = ship.rect.clamp(
                [(ship.rect.x // FIELD_SIZE) * FIELD_SIZE, (ship.rect.center[1] // FIELD_SIZE) * FIELD_SIZE,
                 FIELD_SIZE * ship.fields, FIELD_SIZE])
        else:
            ship.rect = ship.rect.clamp(
                [(ship.rect.center[0] // FIELD_SIZE) * FIELD_SIZE, (ship.rect.y // FIELD_SIZE) * FIELD_SIZE, FIELD_SIZE,
                 FIELD_SIZE * ship.fields])

        ships.append(ship.get_game_coordinates())

    if not is_valid(ships):
        game_screen.pop_up = True
    else:
        player.set_ships(ships)
        computer = Computer()
        computer.set_board()

        game_screen.game_started = True
        game_screen.button_container.buttons.pop(0),
        game_screen.event_container.container.append(game_screen.computer_grid)


def battle_loop(pos, game_screen):
    x = (pos[0] - 1100) // FIELD_SIZE
    y = pos[1] // FIELD_SIZE
    tmp_rect = [x * FIELD_SIZE + 1100, y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE]

    game_screen.guesses = game_screen.guesses + 1
    if computer.got_ship_hit((x, y)):
        pygame.mixer.Sound.play(hit_sound)
        game_screen.computer_grid.change_field_color(tmp_rect, RED)
        computer.remove_point_from_ship((x, y))

    else:
        game_screen.computer_grid.change_field_color(tmp_rect, WHITE)

    computer.remove_empty_ships()

    if not computer.ships:
        game_screen.game_started = False
        game_screen.game_over = True
        game_screen.display_text = "YOU WON"

    computer_guess = computer.point_selection()
    tmp_rect = [computer_guess[0] * FIELD_SIZE, computer_guess[1] * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE]

    if player.got_ship_hit(computer_guess):

        pygame.mixer.Sound.play(hit_sound)
        game_screen.player_grid.change_field_color(tmp_rect, RED)
        player.remove_point_from_ship(computer_guess)

    else:
        game_screen.player_grid.change_field_color(tmp_rect, WHITE)

    player.delete_empty_ships()

    if not player.ships:
        game_screen.game_started = False
        game_screen.game_over = True
        game_screen.display_text = "YOU LOST"
        game_screen.text_color = RED


def is_valid(ships):
    near_points = list()
    for ship in ships:
        for point in ship:

            if 9 < point[0] or 9 < point[1] or point[0] < 0 or point[1] < 0 or (point in near_points):
                return False
            near_points.append(point)
            near_points.append((point[0] + 1, point[1] + 1))
            near_points.append((point[0] - 1, point[1] - 1))
            near_points.append((point[0] + 1, point[1] - 1))
            near_points.append((point[0] - 1, point[1] + 1))
    return True
