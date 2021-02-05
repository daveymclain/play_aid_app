import pygame, time, math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)


class Button:
    def __init__(self, surface, name="button", colour=(255, 0, 0), colour_pressed=(100, 0, 0),
                 pos=(50, 100), size=(200, 50), rounded_corner=5, text_colour=(0, 0, 0), text_size=32):
        self.font = pygame.font.SysFont('Comic Sans MS', 32)
        self.text = self.font.render(name, True, text_colour)
        self.rect = pygame.Rect(pos, size)
        self.mouse_over = False
        self.surface = surface
        self.button_attr = {"colour": colour, "colour_pressed": colour_pressed, "rounded_corner": rounded_corner,
                            "button_pos": pos, "button_size": size}
        self.button_text_attr = {"name": name, "text_colour": text_colour, "text_size": text_size}

    def draw(self, pressed=False):
        if pressed and self.mouse_over:
            pygame.draw.rect(self.surface, self.button_attr["colour_pressed"], self.rect,
                             border_radius=self.button_attr["rounded_corner"])
        else:
            pygame.draw.rect(self.surface, self.button_attr["colour"], self.rect,
                             border_radius=self.button_attr["rounded_corner"])
        self.surface.blit(self.text, (
            self.button_attr["button_pos"][0] + self.button_attr["button_size"][0] // 2 - self.text.get_width() // 2,
            self.button_attr["button_pos"][1] + self.button_attr["button_size"][1] // 2 - self.text.get_height() // 2))

    def collide_point(self, pos):
        self.mouse_over = self.rect.collidepoint(pos)


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
        if len(self.text) == self.cursor_index + 1:
            self.cursor_index = -1

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

    def backspace_cont_press(self, delay):
        """When the backspace key is pressed for longer than the delay. delete from self.text once a frame"""
        if time.time() - self.backspace["pressed_start_time"] > delay and self.backspace["pressed"]:

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
        self.update_t_surf()


    def render_text(self):
        if not self.text and not self.active:
            self.t_surf = self.font.render(self.default_text, True, self.text_colour, self.backcolor)
        self.margin = int(self.t_surf.get_height() * 0.1)
        if self.cursor_index == -1:
            curs_pos_x = self.text_widths["current"] + 5
        else:
            curs_pos_x = self.find_cursor_pos() + 5
        self.image = pygame.Surface((max(self.width, self.text_widths["current"] + self.margin * 2),
                                     self.t_surf.get_height() + self.margin),
                                    pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(self.t_surf, (5, 0))
        if self.active:
            outline_colour = WHITE
            if self.flash:
                pygame.draw.rect(self.image, WHITE, pygame.Rect((curs_pos_x, int(self.margin * 2)),
                                                                (2, self.image.get_height() - int(self.margin * 4))))
            else:
                pygame.draw.rect(self.image, GREY, pygame.Rect((curs_pos_x, int(self.margin * 2)),
                                                               (2, self.image.get_height() - int(self.margin * 4))))
        else:
            outline_colour = GREY
        pygame.draw.rect(self.image, outline_colour, self.image.get_rect().inflate(-2, -2), 2)

        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        self.cursor_blink(40)
        self.backspace_cont_press(0.5)

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
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.update_t_surf()
                    self.render_text()
                elif event.key == pygame.K_BACKSPACE:
                    if self.cursor_index == -2:
                        continue
                    self.backspace["pressed_start_time"] = time.time()
                    self.backspace["pressed"] = True

                    if self.cursor_index != -1:
                        first_half = self.text[:self.cursor_index ]
                        second_half = self.text[self.cursor_index + 1:]
                        self.text = first_half + second_half
                        self.cursor_index -= 1
                        if self.cursor_index == -1:
                            print("set cursor to start pos")
                            self.cursor_index = -2
                    else:
                        self.text = self.text[:-1]
                    self.update_t_surf()
            if event.type == pygame.TEXTINPUT and self.active:
                if self.cursor_index == -1:
                    self.text += event.text
                elif self.cursor_index == -2:
                    self.text = event.text + self.text
                else:
                    first_half = self.text[:self.cursor_index + 1]
                    second_half = self.text[self.cursor_index + 1:]
                    first_half += event.text
                    self.cursor_index += 1
                    self.text = first_half + second_half
                self.update_t_surf(event.text)

        if self.active:
            self.render_text()
