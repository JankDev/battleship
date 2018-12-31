import pygame

from gui.screen import StartScreen, MainScreen, GameScreen
from main.game import battle_loop

pygame.init()
FPS = 60
music = pygame.mixer.music.load("../resources/bensound-epic.mp3")

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
main_screen = MainScreen(StartScreen())
main_screen.screen.draw(window)


def is_valid_game(event: pygame.event):
    if isinstance(main_screen.screen, GameScreen) and main_screen.screen.game_started \
            and event.type == pygame.MOUSEBUTTONDOWN and 1900 >= event.pos[0] >= 1100 \
            and 800 >= event.pos[1] >= 0 \
            and event.button == 1 and not main_screen.screen.game_over:
        return True
    return False


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        if is_valid_game(event):
            battle_loop(pygame.mouse.get_pos(), main_screen.screen)
        main_screen.handle_events(event, pygame.mouse.get_pos())
    main_screen.screen.update(window)
    return True


def run():
    fpstime = pygame.time.Clock()
    running = handle_events()
    pygame.mixer.music.play(-1)
    while running:
        running = handle_events()
        pygame.display.update()
        fpstime.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    run()
