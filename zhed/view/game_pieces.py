import pygame

from zhed.model.view_state import GameColors

size = 65


class Tile(pygame.sprite.Sprite):
    def __init__(self, font, symbol, text_color, window, tile_color, x_pos, y_pos, x=-1, y=-1):
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.Surface([size, size])
        self.image.fill(GameColors.WHITE)
        self.image.set_colorkey(GameColors.WHITE)

        self.tile = pygame.Rect(x_pos, y_pos, size, size)
        text = font.render(symbol, True, text_color)
        pygame.draw.rect(window, tile_color, self.tile)
        window.blit(text, (x_pos + round((size - text.get_width()) / 2),
                           y_pos + round((size - text.get_height()) / 2)))

        self.rect = self.image.get_rect()


class Title:
    text_display: pygame.Surface

    def __init__(self, text, text_color, size, bold=1):
        font = pygame.font.SysFont('Hack', size, bold, 0)

        self.text_display = font.render(text, True, text_color)

    def draw(self, window, x0, y0, x1, y1):
        window.blit(self.text_display, (x0 + round((x1 - x0 - self.text_display.get_width()
                                                    ) / 2), y0 + round((y1 - y0 - self.text_display.get_height()) / 2)))


class Button(pygame.sprite.Sprite):
    def __init__(self, font, text, text_color, window, background_color, width, height, x_pos, y_pos, action,
                 arguments=[]):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GameColors.WHITE)
        self.image.set_colorkey(GameColors.WHITE)
        self.tile = pygame.Rect(x_pos, y_pos, width, height)
        self.action = action
        self.args = arguments

        text_display = font.render(text, True, text_color)

        pygame.draw.rect(window, background_color, self.tile)

        window.blit(text_display, (x_pos + round((width - text_display.get_width()) / 2),
                                   y_pos + round((height - text_display.get_height()) / 2)))

        self.rect = self.image.get_rect(center=(x_pos + round(width / 2), y_pos + round(height / 2)))

    def draw(self, window, border_color):
        pygame.draw.rect(window, border_color, self.rect, 3)

    def trigger(self):
        if len(self.args) == 0:
            return self.action()
        else:
            return self.action(self.args[0])


class TextField(pygame.sprite.Sprite):
    def __init__(self, font, text, text_color, window, background_color, width, height, x_pos, y_pos):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GameColors.WHITE)
        self.image.set_colorkey(GameColors.WHITE)
        self.tile = pygame.Rect(x_pos, y_pos, width, height)

        text_display = font.render(text, True, text_color)

        pygame.draw.rect(window, background_color, self.tile)

        window.blit(text_display, (x_pos + round(width / 10),
                                   y_pos + round((height - text_display.get_height()) / 2)))

        self.rect = self.image.get_rect()
