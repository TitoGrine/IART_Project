import pygame

from zhed.model.view_state import GameColors

size = 65


class Tile(pygame.sprite.Sprite):
    # Generic tile sprite

    def __init__(self, font, symbol, text_color, window, tile_color, x_pos, y_pos, x=-1, y=-1):
        """" Constructor
        :param font: pygame font for displaying text on screen
        :param symbol: character meant to represent the tile
        :param text_color: rgb tuple for the text color
        :param window: pygame screen where the tile is displayed
        :param tile_color: rgb tuple for the tile color
        :param x_pos: horizontal coordinate in the pygame screen
        :param y_pos: vertical coordinate in the pygame screen
        :param x: horizontal coordinate of the tile in the puzzle
        :param y: vertical coordinate of the tile in the puzzle
        """
        
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
    # Sprite used for displaying titles

    text_display: pygame.Surface

    def __init__(self, text, text_color, size, bold=1):
        """" Constructor
        :param text: String to be displayed
        :param text_color: rgb tuple for the text color
        :param size: int representing the font size
        :param bold: int representing if the title should be in bold(1) or not (0)
        """

        font = pygame.font.SysFont('Hack', size, bold, 0)

        self.text_display = font.render(text, True, text_color)

    def draw(self, window, x0, y0, x1, y1):
        """" Draws the title on the screen centered around the it's square dimesions
        :param window: pygame screen where the title is displayed
        :param x0: top left corner horizontal coordinates of the title's given square space
        :param y0: top left corner vertical coordinates of the title's given square space
        :param x1: bottom right corner horizontal coordinates of the title's given square space
        :param y1: bottom right corner vertical coordinates of the title's given square space
        """
        window.blit(self.text_display, (x0 + round((x1 - x0 - self.text_display.get_width()
                                                    ) / 2), y0 + round((y1 - y0 - self.text_display.get_height()) / 2)))


class Button(pygame.sprite.Sprite):
    def __init__(self, font, text, text_color, window, background_color, width, height, x_pos, y_pos, action,
                 arguments=[]):
        """" Constructor
        :param font: pygame font for displaying text on screen
        :param text: string to be displayed in the button
        :param text_color: rgb tuple for the text color
        :param window: pygame screen where the button is displayed
        :param tile_color: rgb tuple for the tile color
        :param background_color: rgb tuple for the background color
        :param width: horizontal dimensions of the button
        :param height: vertical dimensions of the button
        :param x_pos: horizontal coordinate in the pygame screen
        :param y_pos: vertical coordinate in the pygame screen
        :param action: function to be called when the button is triggered
        :param arguments: list of arguments for the given action function
        """
        
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
        """" Draws a border around the button
        :param window: pygame screen where all objects are displayed
        :param border_color: rgb tuple for the border color
        """
        pygame.draw.rect(window, border_color, self.rect, 3)

    def trigger(self):
        """" Executes the button's trigger function
        """
        if len(self.args) == 0:
            return self.action()
        else:
            return self.action(self.args[0])


class TextField(pygame.sprite.Sprite):
    def __init__(self, font, text, text_color, window, background_color, width, height, x_pos, y_pos):
        """" Constructor
        :param font: pygame font for displaying text on screen
        :param text: string to be displayed in the textfield
        :param text_color: rgb tuple for the text color
        :param window: pygame screen where the textfield is displayed
        :param background_color: rgb tuple for the background color
        :param width: horizontal dimensions of the texfield
        :param height: vertical dimensions of the textfield
        :param x_pos: horizontal coordinate in the pygame screen
        :param y_pos: vertical coordinate in the pygame screen
        """

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
