import pygame


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
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width() + 10), t_surf.get_height() + 10),
                                    pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()
