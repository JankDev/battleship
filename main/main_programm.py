import pygame

from gui.screen import StartScreen, MainScreen, GameScreen
from main.game import *

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
main_screen = MainScreen(StartScreen())
main_screen.screen.draw(window)


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        if isinstance(main_screen.screen,
                      GameScreen) and main_screen.screen.game_started and event.type == pygame.MOUSEBUTTONDOWN and not main_screen.screen.game_over:
            battle_loop(pygame.mouse.get_pos(), main_screen.screen)
        main_screen.handle_events(event, pygame.mouse.get_pos())
    main_screen.screen.update(window)
    return True


def run():
    fpstime = pygame.time.Clock()
    running = handle_events()
    while running:
        running = handle_events()
        pygame.display.update()
        fpstime.tick(FPS)

    pygame.quit()
    quit()


run()
