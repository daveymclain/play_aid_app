import gui
import pygame, sys
from pygame.locals import *

WINDOW_DIMENSIONS = (700, 500)

main_clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Play Aid!')
window = pygame.display.set_mode(WINDOW_DIMENSIONS, 0, 32)
font = pygame.font.SysFont("comicsansms", 72)


def event_manager(click, release, sub_menu=False):
    run = True
    for event in pygame.event.get():
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
        window.fill((0, 0, 0))
        add_button.collide_point(pygame.mouse.get_pos())
        add_button.draw(click)
        pygame.display.update()
        main_clock.tick(60)
        click, release, run = event_manager(click, release)
        if add_button.mouse_over and release:
            release = False
            new_toy_menu()


def new_toy_menu():
    run = True
    click, release = False, False
    text_input_box = gui.TextInputBox(50, 50, 400, font)
    group = pygame.sprite.Group(text_input_box)
    while run:
        window.fill((255, 255, 255))
        # click, release, run = event_manager(click, release, sub_menu=True)
        main_clock.tick(60)
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
        group.update(event_list)

        window.fill(0)
        group.draw(window)
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
