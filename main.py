import gui

# Setup Python ----------------------------------------------- #
import pygame, sys
from pygame.locals import *

# Setup pygame/window ---------------------------------------- #
WINDOW_DIMENSIONS = (700, 500)

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Play Aid!')
window = pygame.display.set_mode(WINDOW_DIMENSIONS, 0, 32)


def main_menu():
    add_button = gui.Button(window)
    while True:
        add_button.draw()
        add_button.collide_point(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        mainClock.tick(60)


main_menu()
