import pygame
import zhed_board
import math
import puzzle_reader

pygame.init()

pygame.display.set_caption("Zhed")

level = puzzle_reader.get_puzzle(99)

board = zhed_board.ZhedBoard.build_from_file(level).board_state

side = len(level)

window = pygame.display.set_mode((side * 50, side * 50))

width = 50
heigth = 50

run = True
while run:
    pygame.time.delay(100)


    for i in range(side):
        y_pos = i * 50

        for j in range(side):
            x_pos = j * 50
            tile = board[i][j]

            if   (tile == zhed_board.BoardState.GOAL):
                pygame.draw.rect(window, (255, 102,   0), (x_pos, y_pos, width, heigth))
            elif (tile == zhed_board.BoardState.EMPTY):
                pygame.draw.rect(window, (192, 192, 192), (x_pos, y_pos, width, heigth))
            elif (tile == zhed_board.BoardState.FILLED):
                pygame.draw.rect(window, (255, 204,   0), (x_pos, y_pos, width, heigth))
            else:
                pygame.draw.rect(window, (255, 255, 255), (x_pos, y_pos, width, heigth))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()