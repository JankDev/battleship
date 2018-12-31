import pygame

from main.computer import Computer
from main.player import Player
from resources.colors import *

pygame.init()

player = Player()
computer = Computer()
game_started = False
hit_sound = pygame.mixer.Sound("../resources/bomb.wav")


def start_game(game_screen):
    global player, computer, game_started
    game_started = True
    player = Player()
    computer = Computer()
    ships = list()
    for ship in game_screen.ship_container.sprites():
        if ship.rect.width > ship.rect.height:
            ship.rect = ship.rect.clamp(
                [(ship.rect.x // 80) * 80, (ship.rect.center[1] // 80) * 80, 80 * ship.fields, 80])
        else:
            ship.rect = ship.rect.clamp(
                [(ship.rect.center[0] // 80) * 80, (ship.rect.y // 80) * 80, 80, 80 * ship.fields])
        ships.append(ship.get_game_coordinates())

    if not is_valid(ships):
        game_screen.pop_up = True
    else:
        player.set_ships(ships)
        computer.set_board()
        game_screen.game_started = True
        game_screen.button_container.buttons.pop(0),
        game_screen.event_container.container.append(game_screen.computer_grid)


def battle_loop(pos, game_screen):
    x = (pos[0] - 1100) // 80
    y = pos[1] // 80
    tmp_rect = [x * 80 + 1100, y * 80, 80, 80]

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
    tmp_rect = [computer_guess[0] * 80, computer_guess[1] * 80, 80, 80]

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

            if 9 < (point[0] or point[1]) or (point[0] or point[1]) < 0 or (point in near_points):
                return False
            near_points.append(point)
            near_points.append((point[0] + 1, point[1] + 1))
            near_points.append((point[0] - 1, point[1] - 1))
            near_points.append((point[0] + 1, point[1] - 1))
            near_points.append((point[0] - 1, point[1] + 1))
    return True
