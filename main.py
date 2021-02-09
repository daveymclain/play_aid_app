import gui
import pygame, sys
from pygame.locals import *
from tkinter import filedialog

WINDOW_DIMENSIONS = (700, 500)
BLACK = (0, 0, 0)

main_clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Play Aid!')
window = pygame.display.set_mode(WINDOW_DIMENSIONS, 0, 32)
font = pygame.font.SysFont("comicsansms", 20)


def exit_manager(events, sub_menu=False):
    for event in events:
        if event.type == QUIT:
            if not sub_menu:
                pygame.quit()
                sys.exit()
            else:
                return False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if not sub_menu:
                    pygame.quit()
                    sys.exit()
                else:
                    return
    return True


def main_menu():
    add_button = gui.Button(window, name="New Toy", pos=(10, 10))
    button_group = pygame.sprite.Group(add_button)

    while True:
        window.fill(BLACK)
        event_list = pygame.event.get()
        button_group.update(event_list)
        pygame.display.update()
        main_clock.tick(60)

        exit_manager(event_list)
        if add_button.pressed:
            add_button.pressed = False
            new_toy_menu()


def new_toy_menu():
    run = True
    text_input_box = gui.TextInputBox(10, 10, 400, font, default_text="New toy name?")
    group = pygame.sprite.Group(text_input_box)
    browser_button = gui.Button(window, name="Pick Image", pos=(10, 60))
    button_group = pygame.sprite.Group(browser_button)
    while run:
        window.fill(BLACK)
        event_list = pygame.event.get()
        button_group.update(event_list)
        run = exit_manager(event_list, sub_menu=True)
        group.update(event_list)
        main_clock.tick(60)
        group.draw(window)
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
