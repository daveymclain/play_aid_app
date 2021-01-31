import gui
import pygame, sys
from pygame.locals import *

WINDOW_DIMENSIONS = (700, 500)

main_clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Play Aid!')
window = pygame.display.set_mode(WINDOW_DIMENSIONS, 0, 32)


def event_manager(click, release):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
            else:
                click = False
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                release = True
                click = False
        else:
            release = False
    return click, release


def main_menu():
    add_button = gui.Button(window, name="Add Toy", pos=(10, 10))
    click, release = False, False
    while True:
        add_button.collide_point(pygame.mouse.get_pos())

        add_button.draw(click)
        pygame.display.update()
        main_clock.tick(60)
        click, release = event_manager(click, release)
        if add_button.mouse_over and release:
            print("go to new menu")
            release = False



main_menu()
