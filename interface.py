import pygame
import zhed_board
from run import run_puzzle
import puzzle_reader
import random

size = 65
deviance = 0


class GameColors:
    @staticmethod
    def empty_color():
        deviance = random.randint(-10, 10)
        return 117 + deviance, 230 + deviance, 218 + deviance

    TILE = (12, 97, 112)
    TILE_TEXT = (190, 218, 221)

    GOAL_TEXT = (125, 24, 13)
    GOAL = (227, 66, 52)

    COMPLETED = (33, 182, 168)
    COMPLETED_TEXT = (163, 235, 177)

    BACKGROUND = (97, 200, 188)

    WHITE = (255, 255, 255)


class BoardSettings:
    def __init__(self, window, font):
        self.window = window
        self.font = font


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

    def __init__(self, text, text_color, size):
        font = pygame.font.SysFont('Hack', size, 1, 0)

        self.text_display = font.render(text, True, text_color)

    def draw(self, window, x0, y0, x1, y1):
        window.blit(self.text_display, (x0 + round((x1 - x0 - self.text_display.get_width()
                                                    ) / 2), y0 + round((y1 - y0 - self.text_display.get_height()) / 2)))


class Button(pygame.sprite.Sprite):
    def __init__(self, font, text, text_color, window, background_color, width, height, x_pos, y_pos, action, arguments=[]):
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


def process_mouse(board, interactable, pos):
    clicked_sprites = [s for s in interactable if s.tile.collidepoint(pos)]
    clicked_pos = None
    expandables = []

    if len(clicked_sprites) != 0:
        clicked_pos = (clicked_sprites[0].y, clicked_sprites[0].x)
        expandables = zhed_board.ZhedBoard.get_all_expandables(
            board, clicked_pos)

    return expandables, clicked_pos


def draw_board(settings, board, side, index, last, expandables=[]):
    sprites = pygame.sprite.Group()
    interactable_sprites = []

    for i in range(side):
        y_pos = i * size + 10
        for j in range(side):
            x_pos = j * size + 10
            tile = board[i][j]

            if tile == zhed_board.BoardState.GOAL:
                if last:
                    sprites.add(Tile(settings.font, '◈', GameColors.COMPLETED_TEXT,
                                     settings.window, GameColors.COMPLETED, x_pos, y_pos))
                else:
                    sprites.add(Tile(settings.font, '◈', GameColors.GOAL_TEXT,
                                     settings.window, GameColors.GOAL, x_pos, y_pos))
            elif tile == zhed_board.BoardState.EMPTY:
                empty_color = GameColors.empty_color()
                sprites.add(Tile(settings.font, ' ', empty_color, settings.window,
                                 empty_color, x_pos, y_pos))
            elif tile == zhed_board.BoardState.FILLED:
                sprites.add(Tile(settings.font, '∙', GameColors.TILE_TEXT,
                                 settings.window, GameColors.TILE, x_pos, y_pos))
            else:
                tile = Tile(settings.font, str(tile), GameColors.TILE_TEXT,
                            settings.window, GameColors.TILE, x_pos, y_pos, x=j, y=i)
                sprites.add(tile)
                interactable_sprites.append(tile)

    for expandable in expandables:
        for tile in expandable:
            empty_color = GameColors.empty_color()
            x_pos = tile[1] * size + 10
            y_pos = tile[0] * size + 10
            sprites.add(Tile(settings.font, '∙', GameColors.COMPLETED, settings.window,
                             empty_color, x_pos, y_pos))

    sprites.draw(settings.window)

    return interactable_sprites


def draw_menu(settings):
    sprites = pygame.sprite.Group()

    side_y = round((settings.window.get_width() - 20) / size)
    side_x = round((settings.window.get_height() - 20) / size)

    for i in range(side_y):
        y_pos = i * size + 10
        for j in range(side_x):
            x_pos = j * size + 10
            empty_color = GameColors.empty_color()
            sprites.add(Tile(settings.font, ' ', empty_color, settings.window, empty_color, x_pos, y_pos))

    sprites.draw(settings.window)


def draw_buttons(settings, button_objs):
    buttons = pygame.sprite.Group()

    for button in button_objs:
        buttons.add(button)
        button.draw(settings.window, GameColors.GOAL_TEXT)

    buttons.draw(settings.window)


def check_button_clicks(buttons, pos, condition=True):
    clicked_buttons = [s for s in buttons if s.tile.collidepoint(pos)]

    if len(clicked_buttons) != 0 and condition:
        clicked_buttons[0].trigger()


def level_menu(game_mode):
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 37, 1, 0)
    window = pygame.display.set_mode((size * 8 + 20, size * 8 + 20))

    window.fill(GameColors.BACKGROUND)

    value = ""

    title = Title("CHOOSE LEVEL", GameColors.TILE, 70)
    settings = BoardSettings(window, font)
    buttons = []
    run = True
    counter = 0

    while run:
        pygame.time.delay(50)

        if counter == 0:
            draw_menu(settings)

        title.draw(window, 0, 0, size * 8 + 20, size * 3.5 + 10)

        TextField(font, "Level: " + value, GameColors.TILE_TEXT,
                            settings.window, GameColors.TILE, size * 6, round(size * 1.5), size + 10, round(size * 3.5) + 10)

        buttons.clear()
        buttons.append(Button(settings.font, "∙  START  ∙", GameColors.GOAL_TEXT,
                            settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10, round(size * 5.5) + 10, game_mode, arguments=[1 if len(value) == 0 else int(value)]))

        draw_buttons(settings, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP and len(value) != 0:
                check_button_clicks(buttons, pygame.mouse.get_pos(), condition=bool(int(value) > 0 and int(value) <= 101))
            elif event.type == pygame.KEYDOWN:
                if len(value) < 3:
                    if event.key == pygame.K_0:
                        value += "0"
                    if event.key == pygame.K_1:
                        value += "1"
                    if event.key == pygame.K_2:
                        value += "2"
                    if event.key == pygame.K_3:
                        value += "3"
                    if event.key == pygame.K_4:
                        value += "4"
                    if event.key == pygame.K_5:
                        value += "5"
                    if event.key == pygame.K_6:
                        value += "6"
                    if event.key == pygame.K_7:
                        value += "7"
                    if event.key == pygame.K_8:
                        value += "8"
                    if event.key == pygame.K_9:
                        value += "9"

                if len(value) > 0:
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        value = value[:-1]

        counter = (counter + 1) % 5
        pygame.display.update()

    pygame.quit()

    return


def mode_menu():
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 30, 1, 0)
    window = pygame.display.set_mode((size * 8 + 20, size * 8 + 20))

    window.fill(GameColors.BACKGROUND)

    title = Title("CHOOSE MODE", GameColors.TILE, 70)
    settings = BoardSettings(window, font)
    buttons = []
    run = True
    counter = 0

    while run:
        pygame.time.delay(50)

        if counter == 0:
            draw_menu(settings)

        title.draw(window, 0, 0, size * 8 + 20, size * 3.5 + 10)

        buttons.append(Button(settings.font, "∙  PLAYER MODE  ∙", GameColors.GOAL_TEXT,
                            settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10, round(size * 3.5) + 10, level_menu, arguments=[player_playing]))
                            
        buttons.append(Button(settings.font, "∙  BOT SOLUTION  ∙", GameColors.GOAL_TEXT,
                            settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10, round(size * 5.5) + 10, level_menu, arguments=[bot_playing]))

        draw_buttons(settings, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                check_button_clicks(buttons, pygame.mouse.get_pos())

        counter = (counter + 1) % 5
        pygame.display.update()

    pygame.quit()


def main_menu():
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 30, 1, 0)
    window = pygame.display.set_mode((size * 8 + 20, size * 8 + 20))

    window.fill(GameColors.BACKGROUND)

    title = Title("ZHED", GameColors.TILE, 120)
    settings = BoardSettings(window, font)
    buttons = []
    run = True
    counter = 0

    while run:
        pygame.time.delay(50)

        if counter == 0:
            draw_menu(settings)

        title.draw(window, 0, 0, size * 8 + 20, size * 3.5 + 10)

        buttons.append(Button(settings.font, "∙  PLAY  ∙", GameColors.GOAL_TEXT,
                            settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10, round(size * 3.5) + 10, mode_menu))
                            
        buttons.append(Button(settings.font, "∙  QUIT  ∙", GameColors.GOAL_TEXT,
                            settings.window, GameColors.GOAL, size * 6, round(size * 1.5), size + 10, round(size * 5.5) + 10, lambda: pygame.quit()))

        draw_buttons(settings, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                check_button_clicks(buttons, pygame.mouse.get_pos())

        counter = (counter + 1) % 5
        pygame.display.update()

    pygame.quit()


def bot_playing(puzzle):
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 37, 0, 0)
    level = puzzle_reader.read_file(puzzle)
    boards = run_puzzle(level)

    boards = list(map(lambda board: puzzle_reader.padd_board(board), boards))

    side = len(boards[0])

    window = pygame.display.set_mode((side * size + 20, side * size + 20))
    window.fill(GameColors.BACKGROUND)
    run = True
    index = 0
    counter = 0
    key_press = True

    settings = BoardSettings(window, font)

    while run:
        pygame.time.delay(50)

        board = boards[index]

        if key_press or counter == 0:
            draw_board(settings, board, side, index, index == len(boards) - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                key_press = True
                if event.key == pygame.K_RIGHT and index != len(boards) - 1:
                    index += 1
                elif event.key == pygame.K_LEFT and index != 0:
                    index -= 1
                elif event.key == pygame.K_ESCAPE:
                    run = False
            else:
                key_press = False

        counter = (counter + 1) % 5
        pygame.display.flip()

    main_menu()


def player_playing(puzzle):
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 37, 0, 0)
    level = puzzle_reader.padd_raw_board(puzzle_reader.read_file(puzzle))
    board_state = zhed_board.ZhedBoard.build_from_file(level)
    initial_board_state = board_state

    side = len(board_state.board_state)

    window = pygame.display.set_mode((side * size + 20, side * size + 20))
    window.fill(GameColors.BACKGROUND)
    run = True
    index = 0
    counter = 0
    key_press = True

    settings = BoardSettings(window, font)
    expandables = []
    clicked_pos = None
    interactable = []

    while run:
        pygame.time.delay(50)

        if key_press or counter == 0:
            interactable = draw_board(
                settings, board_state.board_state, side, index, False, expandables=expandables)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                expandables, clicked_pos = process_mouse(
                    board_state, interactable, pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                key_press = True

                if event.key == pygame.K_r:
                    board_state = initial_board_state
                elif event.key == pygame.K_ESCAPE:
                    run = False

                if clicked_pos != None:
                    if event.key == pygame.K_UP:
                        board_state = board_state.up(clicked_pos)
                    elif event.key == pygame.K_DOWN:
                        board_state = board_state.down(clicked_pos)
                    elif event.key == pygame.K_RIGHT:
                        board_state = board_state.right(clicked_pos)
                    elif event.key == pygame.K_LEFT:
                        board_state = board_state.left(clicked_pos)
                    

                    clicked_pos = None
                    expandables = []
            else:
                key_press = False

        if board_state.is_goal:
            pygame.time.delay(50)
            run = False

        counter = (counter + 1) % 5
        pygame.display.update()

    main_menu()


main_menu()
