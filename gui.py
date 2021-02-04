import pygame, time


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
    def __init__(self, x, y, w, font):
        super().__init__()
        self.text_colour = WHITE
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()
        self.tick = 0
        self.flash = False
        self.backspace = {"pressed": False, "pressed_start_time": 0.0}

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.text_colour, self.backcolor)
        margin = int(t_surf.get_height() * 0.1)
        curs_pos_x = t_surf.get_width() + 5
        self.image = pygame.Surface((max(self.width, t_surf.get_width() + margin * 2),
                                     t_surf.get_height() + margin),
                                    pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 0))
        if self.active:
            outline_colour = WHITE
            if self.flash:
                pygame.draw.rect(self.image, WHITE, pygame.Rect((curs_pos_x, int(margin * 2)),
                                                                (2, self.image.get_height() - int(margin * 4))))
            else:
                pygame.draw.rect(self.image, GREY, pygame.Rect((curs_pos_x, int(margin * 2)),
                                                               (2, self.image.get_height() - int(margin * 4))))
        else:
            outline_colour = GREY
        pygame.draw.rect(self.image, outline_colour, self.image.get_rect().inflate(-2, -2), 2)

        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        if time.time() - self.backspace["pressed_start_time"] > 0.5 and self.backspace["pressed"]:
            self.text = self.text[:-1]
        if self.tick > 40:
            self.tick = 0
            if self.flash:
                self.flash = False
            else:
                self.flash = True
        else:
            self.tick += 1
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = bool(self.rect.collidepoint(event.pos))
                self.render_text()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace["pressed"] = False
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.render_text()
                elif event.key == pygame.K_BACKSPACE:
                    self.backspace["pressed_start_time"] = time.time()
                    self.backspace["pressed"] = True
                    self.text = self.text[:-1]
                # else:
                #     self.text += event.unicode
            if event.type == pygame.TEXTINPUT and self.active:
                self.text += event.text

        if self.active:
            self.render_text()
