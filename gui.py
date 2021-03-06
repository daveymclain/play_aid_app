import pygame, time, math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)


class Button(pygame.sprite.Sprite):
    def __init__(self, surface, name="button", colour=(255, 0, 0), colour_pressed=(100, 0, 0), pos=(50, 100),
                 size=(200, 50), rounded_corner=5, text_colour=(0, 0, 0), text_size=32):
        super().__init__()
        self.font = pygame.font.SysFont('Comic Sans MS', 32)
        self.text = self.font.render(name, True, text_colour)
        self.rect = pygame.Rect(pos, size)
        self.mouse_over = False
        self.surface = surface
        self.button_attr = {"colour": colour, "colour_pressed": colour_pressed, "rounded_corner": rounded_corner,
                            "button_pos": pos, "button_size": size}
        self.button_text_attr = {"name": name, "text_colour": text_colour, "text_size": text_size}

        self.click = False
        self.released = False
        self.pressed = False
        self.mouse_pos = (0, 0)

    def draw(self):
        """Display the button on the surface"""
        if self.click and self.rect.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.surface, self.button_attr["colour_pressed"], self.rect,
                             border_radius=self.button_attr["rounded_corner"])
        else:
            pygame.draw.rect(self.surface, self.button_attr["colour"], self.rect,
                             border_radius=self.button_attr["rounded_corner"])
        self.surface.blit(self.text, (
            self.button_attr["button_pos"][0] + self.button_attr["button_size"][0] // 2 - self.text.get_width() // 2,
            self.button_attr["button_pos"][1] + self.button_attr["button_size"][1] // 2 - self.text.get_height() // 2))

    def update(self, event_list) -> None:
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                else:
                    self.click = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.released = True
                    self.pressed = self.rect.collidepoint(self.mouse_pos)
                    self.click = False
            else:
                self.released = False
        self.draw()


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, default_text=""):
        super().__init__()
        self.text_colour = WHITE
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.tick = 0
        self.flash = False
        self.backspace = {"pressed": False, "pressed_start_time": 0.0}
        self.arrows = {"left_pressed": False, "right_pressed": False, "left_s_time": 0.0, "right_s_time": 0.0}
        self.delete = {"pressed": False, "pressed_start_time": 0.0}
        self.default_text = default_text
        self.text_widths = {"current": 0}
        self.t_surf = None
        self.cursor_index = -1
        self.margin = 0
        # render default text
        self.render_text()

    def update_t_surf(self, character=""):
        """Updates the text surface with the self.text and add to a dictionary of width for the individual characters"""
        self.t_surf = self.font.render(self.text, True, self.text_colour, self.backcolor)
        if character:
            self.text_widths[character] = self.t_surf.get_width() - self.text_widths["current"]
        self.text_widths["current"] = self.t_surf.get_width()

    def find_cursor_pos(self):
        """Convert the cursor index into x position for the cursor"""
        running_width = 0
        if self.cursor_index == -2:
            return 0
        for ind, character in enumerate(self.text):
            running_width += self.text_widths[character]
            if ind == self.cursor_index:
                return running_width

    def find_the_index(self, mouse_pos_x):
        """Find the cursor index when clicking within the text field"""
        mouse_pos_x = mouse_pos_x - self.pos[0] - 5
        running_width = 0
        for ind, character in enumerate(self.text):
            current_ind_width = round(self.text_widths[character] / 2)
            if current_ind_width > mouse_pos_x and ind == 0:
                self.cursor_index = -2
                break
            running_width += self.text_widths[character]
            if mouse_pos_x < running_width:
                if mouse_pos_x < running_width - current_ind_width:
                    self.cursor_index = ind - 1
                    break
                if mouse_pos_x > running_width - current_ind_width:
                    self.cursor_index = ind
                    break
            else:
                self.cursor_index = -1
        self.cursor_end_check()

    def cursor_blink(self, speed):
        """Works out when to blink the cursor based on speed(the amount of frames)"""
        if self.tick > speed:
            self.tick = 0
            if self.flash:
                self.flash = False
            else:
                self.flash = True
        else:
            self.tick += 1

    def cont_press(self, delay):
        """When the backspace key is pressed for longer than the delay. delete from self.text once a frame"""
        if time.time() - self.backspace["pressed_start_time"] > delay and self.backspace["pressed"]:
            self.backspace_pressed()
        elif self.arrows["left_pressed"] and self.arrows["right_pressed"]:
            pass
        elif self.arrows["left_pressed"] and time.time() - self.arrows["left_s_time"] > delay:
            self.move_cursor_with_arrows("left")
        elif self.arrows["right_pressed"] and time.time() - self.arrows["right_s_time"] > delay:
            self.move_cursor_with_arrows("right")
        elif self.delete["pressed"] and time.time() - self.delete["pressed_start_time"] > delay:
            self.del_key_pressed()
        self.update_t_surf()

    def text_input(self, character):
        """updates the self.text when an input key is pressed"""
        if self.cursor_index == -1:
            self.text += character
        elif self.cursor_index == -2:
            self.text = character + self.text
            self.cursor_index = 0
        else:
            first_half = self.text[:self.cursor_index + 1]
            second_half = self.text[self.cursor_index + 1:]
            first_half += character
            self.cursor_index += 1
            self.text = first_half + second_half
        self.update_t_surf(character)

    def move_cursor_with_arrows(self, direction):
        """Move the cursor left or right with the left and right arrows"""
        if direction == "left":
            if self.cursor_index == -2:
                pass
            elif self.cursor_index == -1:
                self.cursor_index = len(self.text) - 2
            else:
                self.cursor_index -= 1
                if self.cursor_index == -1:
                    self.cursor_index = -2
        else:
            if self.cursor_index == -1:
                pass
            elif self.cursor_index == -2:
                self.cursor_index = 0
            else:
                self.cursor_index += 1
                self.cursor_end_check()

    def backspace_pressed(self):
        if self.cursor_index == -1:
            self.text = self.text[:-1]
        elif self.cursor_index == -2:
            return
        else:
            first_half = self.text[:self.cursor_index]
            second_half = self.text[self.cursor_index + 1:]
            self.text = first_half + second_half
            self.cursor_index -= 1
            if self.cursor_index == -1:
                self.cursor_index = -2

    def del_key_pressed(self):
        if self.cursor_index == -1:
            return
        elif self.cursor_index == -2:
            self.text = self.text[1:]
        else:
            first_half = self.text[:self.cursor_index + 1]
            second_half = self.text[self.cursor_index + 2:]
            self.text = first_half + second_half
            self.cursor_end_check()

    def cursor_end_check(self):
        """Checks if the cursor is at the end of the self.text string and changes the cursor_ind to -1"""
        if self.cursor_index == len(self.text) - 1:
            self.cursor_index = -1

    def render_text(self):
        if not self.text and not self.active:
            self.t_surf = self.font.render(self.default_text, True, self.text_colour, self.backcolor)
        self.margin = int(self.t_surf.get_height() * 0.1)
        if self.cursor_index == -1:
            curs_pos_x = self.text_widths["current"] + 5
        else:
            curs_pos_x = self.find_cursor_pos() + 4
        self.image = pygame.Surface((max(self.width, self.text_widths["current"] + self.margin * 2),
                                     self.t_surf.get_height() + self.margin),
                                    pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(self.t_surf, (5, 0))
        if self.active:
            outline_colour = WHITE
            # draw the cursor
            if self.flash:
                pygame.draw.rect(self.image, WHITE, pygame.Rect((curs_pos_x, int(self.margin * 2)),
                                                                (2, self.image.get_height() - int(self.margin * 4))))
            else:
                pygame.draw.rect(self.image, GREY, pygame.Rect((curs_pos_x, int(self.margin * 2)),
                                                               (2, self.image.get_height() - int(self.margin * 4))))
        else:
            outline_colour = GREY
        # Draw text box outline
        pygame.draw.rect(self.image, outline_colour, self.image.get_rect().inflate(-2, -2), 2)

        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        self.cursor_blink(40)
        self.cont_press(0.5)

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = bool(self.rect.collidepoint(event.pos))
                self.update_t_surf()
                self.render_text()
                if self.active:
                    mouse_pos_x = event.pos[0]
                    self.find_the_index(mouse_pos_x)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace["pressed"] = False
                elif event.key == pygame.K_LEFT:
                    self.arrows["left_pressed"] = False
                elif event.key == pygame.K_RIGHT:
                    self.arrows["right_pressed"] = False
                elif event.key == pygame.K_DELETE:
                    self.delete["pressed"] = False
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_LEFT:
                    self.move_cursor_with_arrows("left")
                    self.arrows["left_pressed"] = True
                    self.arrows["left_s_time"] = time.time()
                elif event.key == pygame.K_RIGHT:
                    self.move_cursor_with_arrows("right")
                    self.arrows["right_pressed"] = True
                    self.arrows["right_s_time"] = time.time()
                elif event.key == pygame.K_RETURN:
                    self.active = False
                    self.update_t_surf()
                elif event.key == pygame.K_BACKSPACE:
                    self.backspace["pressed_start_time"] = time.time()
                    self.backspace["pressed"] = True
                    self.backspace_pressed()
                    self.update_t_surf()
                elif event.key == pygame.K_DELETE:
                    self.delete["pressed_start_time"] = time.time()
                    self.delete["pressed"] = True
                    self.del_key_pressed()
                    self.update_t_surf()
            if event.type == pygame.TEXTINPUT and self.active:
                self.text_input(event.text)

        if self.active:
            self.render_text()
