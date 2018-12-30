from main.computer import Computer
from main.player import Player
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
player = Player("")
computer = Computer()
game_started = False


def start_game(game_screen):
    global player, computer, game_started
    game_started = True
    player = Player("Jacek")

    ships = list()
    for ship in game_screen.ship_container.sprites():
        if ship.rect.width > ship.rect.height:
            ship.rect = ship.rect.clamp(
                [(ship.rect.x // 80) * 80, (ship.rect.center[1] // 80) * 80, 80 * ship.fields, 80])
        else:
            ship.rect = ship.rect.clamp(
                [(ship.rect.center[0] // 80) * 80, (ship.rect.y // 80) * 80, 80, 80 * ship.fields])
        ships.append(ship.get_game_coordinates())

    player.set_ships(ships)
    computer.setBoard()

    game_screen.game_started = True


def battle_loop(pos, game_screen):

    x = (pos[0] - 1100) // 80
    y = pos[1] // 80
    tmp_rect = [x * 80 + 1100, y * 80, 80, 80]

    y = y + 1
    x = chr(x + 65)

    game_screen.guesses = game_screen.guesses + 1
    for field in game_screen.computer_grid.fields:
        if tmp_rect == field.rect and field.color != RED:
            field.color = WHITE
    for ship in computer.ships:
        if (x, y) in ship:
            for field in game_screen.computer_grid.fields:
                if tmp_rect == field.rect:
                    field.color = RED
            ship.remove((x, y))
            break

    computer.remove_empty_ships()
    if not computer.ships:
        game_screen.game_started = False
        game_screen.game_over = True
        game_screen.display_text = "YOU WON"
    computer_guess = computer.point_selection()

    tmp_rect = [computer_guess[0] * 80, (computer_guess[1] - 1) * 80, 80, 80]
    for field in game_screen.player_grid.fields:
        if tmp_rect == field.rect:
            field.color = WHITE
            field.draw_function = field.on_click_draw
            break

    for ship in player.ships:
        if con(computer_guess) in ship:

            for field in game_screen.player_grid.fields:
                if tmp_rect == field.rect:
                    field.color = RED
                    break
            ship.remove(con(computer_guess))
            break

    player.delete_empty_ships()
    if not player.ships:
        game_screen.game_started = False
        game_screen.game_over = True
        game_screen.display_text = "YOU LOST"


def con(point):
    temp = (chr(point[0] + 65), point[1])
    return temp
