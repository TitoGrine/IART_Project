import pygame
import zhed_board
from run import run_puzzle
import math
import puzzle_reader
import random

size = 80

def bot_playing(puzzle):
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 35, 1, 0)
    level = puzzle_reader.get_puzzle(puzzle)
    boards = run_puzzle(level)

    side = len(level)
    window = pygame.display.set_mode((side * size, side * size))

    run = True

    index = 0

    while run:
        pygame.time.delay(70)

        board = boards[index]

        for i in range(side):
            y_pos = i * size
            for j in range(side):
                x_pos = j * size
                tile = board[i][j]
                deviance = random.randint(170, 190)      

                if tile == zhed_board.BoardState.GOAL:
                    text = font.render('⊛', True, (0, 0, 0))
                    pygame.draw.rect(window, (255, 102,   0), (x_pos, y_pos, size, size))
                    window.blit(text, (x_pos + round((size - text.get_width())/2), y_pos + round((size - text.get_height())/2)))
                elif tile == zhed_board.BoardState.EMPTY:
                    pygame.draw.rect(window, (deviance, deviance, deviance), (x_pos, y_pos, size, size))
                elif tile == zhed_board.BoardState.FILLED:
                    text = font.render('·', True, (205, 174,   0))
                    pygame.draw.rect(window, (255, 204,   0), (x_pos, y_pos, size, size))
                    window.blit(text, (x_pos + round((size - text.get_width())/2), y_pos + round((size - text.get_height())/2)))
                else:
                    text = font.render(str(tile), True, (0, 0, 0))
                    pygame.draw.rect(window, (255, 255, 255), (x_pos, y_pos, size, size))
                    window.blit(text, (x_pos + round((size - text.get_width())/2), y_pos + round((size - text.get_height())/2)))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and index != len(boards) - 1:
                    index += 1
                elif event.key == pygame.K_LEFT and index != 0:
                    index -= 1

        pygame.display.update()

    pygame.quit()


bot_playing(4)
