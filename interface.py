import pygame
import zhed_board
from graph.graph import Graph
from run import run_puzzle
import puzzle_reader
import random
import threading

size = 70
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
    HINT = (255, 244, 79)

    BACKGROUND = (97, 200, 188)

    WHITE = (255, 255, 255)


class BoardSettings:
    def __init__(self, window, font):
        self.window = window
        self.font = font


class Hint:
    NO_HINT = -1
    HINT = -2

    def __init__(self, hint, path, block=None):
        self.path = path
        self.hint = hint
        self.block = block


class Tile(pygame.sprite.Sprite):
    def __init__(self, font, symbol, text_color, window, tile_color, x_pos, y_pos, x=-1, y=-1):
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.Surface([size, size])
        self.image.fill(GameColors.WHITE)
        self.image.set_colorkey(GameColors.WHITE)

        self.tile = pygame.Rect((x_pos, y_pos, size, size))
        text = font.render(symbol, True, text_color)
        pygame.draw.rect(window, tile_color, self.tile)
        window.blit(text, (x_pos + round((size - text.get_width()) / 2),
                           y_pos + round((size - text.get_height()) / 2)))

        self.rect = self.image.get_rect()


def draw_board(settings, board, side, index, last, expandables=[], hints=Hint(Hint.NO_HINT, [])):
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
            build_tile(settings, sprites, tile, GameColors.COMPLETED, GameColors.empty_color(), '∙')

    if hints.hint is Hint.HINT:
        for hint in hints.path:
            build_tile(settings, sprites, hint, GameColors.HINT, GameColors.empty_color(), '∙')
            build_tile(settings, sprites, hints.block, GameColors.TILE_TEXT,
                       GameColors.HINT, str(board[hints.block[0]][hints.block[1]]))

    sprites.draw(settings.window)

    return interactable_sprites


def build_tile(settings, sprites, tile, foreground_color, background_color, symbol):
    x_pos = tile[1] * size + 10
    y_pos = tile[0] * size + 10
    sprites.add(Tile(settings.font, symbol, foreground_color, settings.window,
                     background_color, x_pos, y_pos))


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
            else:
                key_press = False

        counter = (counter + 1) % 5
        pygame.display.flip()

    pygame.quit()


def process_mouse(board, interactable, pos):
    clicked_sprites = [s for s in interactable if s.tile.collidepoint(pos)]
    clicked_pos = None
    expandables = []

    if len(clicked_sprites) != 0:
        clicked_pos = (clicked_sprites[0].y, clicked_sprites[0].x)
        expandables = zhed_board.ZhedBoard.get_all_expandables(board, clicked_pos)

    return expandables, clicked_pos


def get_hint(board_state, hints):
    graph = Graph(lambda node: node.is_goal, lambda node: zhed_board.ZhedBoard.get_all_operators(node.state))
    moves = puzzle_reader.get_boards_list(graph.a_star(board_state))
    if moves is None or len(moves) > 1:
        hints.path.extend(moves[1].move.placed_blocks)
        hints.block = moves[1].move.starting_block
        hints.hint = Hint.HINT
    else:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

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
    hints = Hint(Hint.NO_HINT, [])

    while run:
        pygame.time.delay(50)

        if key_press or counter == 0:
            interactable = draw_board(settings, board_state.board_state, side, index, False, expandables=expandables,
                                      hints=hints)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                expandables, clicked_pos = process_mouse(board_state, interactable, pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                key_press = True

                if event.key == pygame.K_r:
                    board_state = initial_board_state
                elif event.key == pygame.K_SPACE:
                    threading.Thread(target=get_hint, args=(board_state, hints)).start()

                if clicked_pos != None:
                    if event.key == pygame.K_UP:
                        board_state = board_state.up(clicked_pos)
                    elif event.key == pygame.K_DOWN:
                        board_state = board_state.down(clicked_pos)
                    elif event.key == pygame.K_RIGHT:
                        board_state = board_state.right(clicked_pos)
                    elif event.key == pygame.K_LEFT:
                        board_state = board_state.left(clicked_pos)
                    hints.hint = hints.NO_HINT
                    hints.block = None
                    hints.path = []

                    clicked_pos = None
                    expandables = []
            else:
                key_press = False

        if board_state.is_goal:
            pygame.time.delay(50)
            run = False

        counter = (counter + 1) % 5
        pygame.display.update()

    pygame.quit()


player_playing(5)
