import pygame
import zhed_board
from run import run_puzzle
import puzzle_reader
import random

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

    BACKGROUND = (97, 200, 188)

class BoardSettings:
    def __init__(self, window, font):
        self.window = window
        self.font = font



def draw_tile(font, symbol, text_color, window, tile_color, x_pos, y_pos):
    text = font.render(symbol, True, text_color)
    pygame.draw.rect(window, tile_color, (x_pos, y_pos, size, size))
    window.blit(text, (x_pos + round((size - text.get_width())/2),
                       y_pos + round((size - text.get_height())/2)))

def draw_board(settings, board, side, index, last) :
    for i in range(side):
                y_pos = i * size + 10
                for j in range(side):
                    x_pos = j * size + 10
                    tile = board[i][j]

                    if tile == zhed_board.BoardState.GOAL:
                        if last:
                            draw_tile(settings.font, '◈', GameColors.COMPLETED_TEXT,
                                      settings.window, GameColors.COMPLETED, x_pos, y_pos)
                        else:
                            draw_tile(settings.font, '◈', GameColors.GOAL_TEXT,
                                      settings.window, GameColors.GOAL, x_pos, y_pos)
                    elif tile == zhed_board.BoardState.EMPTY:
                        empty_color = GameColors.empty_color()
                        draw_tile(settings.font, ' ', empty_color, settings.window,
                                  empty_color, x_pos, y_pos)
                    elif tile == zhed_board.BoardState.FILLED:
                        draw_tile(settings.font, '∙', GameColors.TILE_TEXT,
                                  settings.window, GameColors.TILE, x_pos, y_pos)
                    else:
                        draw_tile(settings.font, str(tile), GameColors.TILE_TEXT,
                                  settings.window, GameColors.TILE, x_pos, y_pos)

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
        pygame.display.update()

    pygame.quit()

def process_mouse(board, pos):


def player_playing(puzzle):
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
            draw_board(settings, board, side, index, len(boards) - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                board = process_mouse(board, pygame.mouse.get_pos())
            else:
                key_press = False

        counter = (counter + 1) % 5
        pygame.display.update()

    pygame.quit()

bot_playing(16)
