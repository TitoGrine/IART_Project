import pygame
import zhed_board
from run import run_puzzle
import puzzle_reader
import random

size = 70
deviance = 0


class GameColors():
    def empty_color(self, deviance=0):
        return (117 + deviance, 230 + deviance, 218 + deviance)

    TILE = (12, 97, 112)
    TILE_TEXT = (190, 218, 221)

    GOAL_TEXT = (125, 24, 13)
    GOAL = (227, 66, 52)

    BACKGROUND = (97, 200, 188)


def bot_playing(puzzle):
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 37, 0, 0)
    level = puzzle_reader.get_puzzle(puzzle)
    boards = run_puzzle(level)

    side = len(level)
    window = pygame.display.set_mode((side * size + 20, side * size + 20))
    window.fill(GameColors.BACKGROUND)
    run = True
    index = 0
    counter = 0
    key_press = True

    while run:
        pygame.time.delay(50)
        board = boards[index]

        if key_press or counter == 0:
            for i in range(side):
                y_pos = i * size + 10
                for j in range(side):
                    x_pos = j * size + 10
                    tile = board[i][j]

                    deviance = random.randint(-10, 10)

                    if tile == zhed_board.BoardState.GOAL:
                        text = font.render('◈', True, GameColors.GOAL_TEXT)
                        pygame.draw.rect(window, GameColors.GOAL,
                                        (x_pos, y_pos, size, size))
                        window.blit(text, (x_pos + round((size - text.get_width())/2),
                                        y_pos + round((size - text.get_height())/2)))
                    elif tile == zhed_board.BoardState.EMPTY:
                        pygame.draw.rect(window, GameColors.empty_color(
                            GameColors(), deviance), (x_pos, y_pos, size, size))
                    elif tile == zhed_board.BoardState.FILLED:
                        text = font.render('∙', True, GameColors.TILE_TEXT)
                        pygame.draw.rect(window, GameColors.TILE,
                                        (x_pos, y_pos, size, size))
                        window.blit(text, (x_pos + round((size - text.get_width())/2),
                                        y_pos + round((size - text.get_height())/2)))
                    else:
                        text = font.render(str(tile), True, GameColors.TILE_TEXT)
                        pygame.draw.rect(window, GameColors.TILE,
                                        (x_pos, y_pos, size, size))
                        window.blit(text, (x_pos + round((size - text.get_width())/2),
                                        y_pos + round((size - text.get_height())/2)))

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


bot_playing(7)
