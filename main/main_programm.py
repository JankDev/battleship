import pygame

from gui.screen import StartScreen, MainScreen, GameScreen
from main.game import battle_loop

pygame.init()
FPS = 60
music = pygame.mixer.music.load("../resources/bensound-epic.mp3")

window = pygame.display.set_mode((2000, 1300))
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
    pygame.mixer.music.play(-1)
    while running:
        running = handle_events()
        pygame.display.update()
        fpstime.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    run()
