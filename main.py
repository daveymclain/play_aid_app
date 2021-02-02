import gui
import pygame, sys
from pygame.locals import *

WINDOW_DIMENSIONS = (700, 500)
BLACK = (0, 0, 0)

main_clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Play Aid!')
window = pygame.display.set_mode(WINDOW_DIMENSIONS, 0, 32)
font = pygame.font.SysFont("comicsansms", 20)


def click_manager(click, release, events, sub_menu=False):
    run = True
    for event in events:
        if event.type == QUIT:
            if not sub_menu:
                pygame.quit()
                sys.exit()
            else:
                run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if not sub_menu:
                    pygame.quit()
                    sys.exit()
                else:
                    run = False
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
    return click, release, run


def main_menu():
    add_button = gui.Button(window, name="New Toy", pos=(10, 10))
    click, release = False, False
    while True:
        window.fill(BLACK)
        add_button.collide_point(pygame.mouse.get_pos())
        add_button.draw(click)
        pygame.display.update()
        main_clock.tick(60)
        event_list = pygame.event.get()
        click, release, run = click_manager(click, release, event_list)
        if add_button.mouse_over and release:
            release = False
            new_toy_menu()


def new_toy_menu():
    run = True
    click, release = False, False
    text_input_box = gui.TextInputBox(10, 10, 400, font)
    group = pygame.sprite.Group(text_input_box)
    while run:
        window.fill(BLACK)
        event_list = pygame.event.get()
        click, release, run = click_manager(click, release, event_list, sub_menu=True)
        group.update(event_list)
        main_clock.tick(60)
        group.draw(window)
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
