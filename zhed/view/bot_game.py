import pygame

import zhed.view.menus as menus
from zhed.controller import puzzle_reader
from zhed.model.view_state import GameColors, BoardSettings
from zhed.statistics import solve_puzzle
from zhed.view.draw_board import draw_board
from zhed.view.game_pieces import size


def bot_playing(puzzle):
    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 37, 0, 0)
    level = puzzle_reader.read_file(puzzle)
    boards = solve_puzzle(level)
    
    boards = map(lambda board: board.board_state, boards)

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

    menus.main_menu()



