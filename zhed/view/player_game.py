import threading

import pygame

from graph.graph import Graph
from zhed.controller import zhed_board, puzzle_reader
from zhed.model.view_state import GameColors, BoardSettings, Hint
from zhed.view.draw_board import draw_board
from zhed.view.game_pieces import size, Title
import zhed.view.menus


def process_mouse(board, interactable, pos):
    """" Determines if any of the game's interactable tiles where clicked and if so, returns their possible expansion tiles and the coordinates fo the clicked tile
    :param board: ZhedBoard objetc containing all relevant information about the board
    :param interactable: list of Sprites that are interactable
    :param pos: mouse position at the moment when there was a click
    """
    clicked_sprites = [s for s in interactable if s.tile.collidepoint(pos)]
    clicked_pos = None
    expandables = []

    if len(clicked_sprites) != 0:
        clicked_pos = (clicked_sprites[0].y, clicked_sprites[0].x)
        expandables = zhed_board.ZhedBoard.get_all_expandables(
            board, clicked_pos)

    return expandables, clicked_pos

def get_hint(board_state, hints):
    """" Calculates the best possible move given the current state of the board
    :param hints: an instance of a Hint
    """

    graph = Graph(lambda node: node.is_goal, lambda node: zhed_board.ZhedBoard.get_all_operators(node.state))
    moves = puzzle_reader.get_boards_list(graph.a_star(board_state))
    if moves is None or len(moves) > 1:
        hints.path.extend(moves[1].move.placed_blocks)
        hints.block = moves[1].move.starting_block
        hints.hint = Hint.HINT
    else:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))


def player_playing(puzzle):
    """" Displays the puzzle an lets the player interact with it. The player can choose one of the numbered tiles
         using the mouse and then expand it in on of the four directions by pressing the arrow keys. in order to
         get a hint the player must press the space bar. To restart the player must press the "R" key.
    :param puzzle: the puzzle number
    """
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
            interactable = draw_board(settings, board_state.board_state, side, expandables=expandables,
                                      hints=hints)

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
            victory_screen()
            zhed.view.menus.main_menu()

        counter = (counter + 1) % 5
        pygame.display.update()

    zhed.view.menus.main_menu()


def victory_screen():
    """" Displays a victory screen for a few seconds.
    """

    pygame.init()
    pygame.display.set_caption("Zhed")

    font = pygame.font.SysFont('Arial', 30, 1, 0)
    window = pygame.display.set_mode((size * 8 + 20, size * 8 + 20))

    window.fill(GameColors.BACKGROUND)

    title = Title("CONGRATS!", GameColors.GOAL, 90)
    subtitle = Title("⋆", GameColors.HINT, 100, 0)
    settings = BoardSettings(window, font)

    counter = 0

    while counter < 18:
        counter += 1

        zhed.view.menus.draw_background(settings)

        title.draw(window, 0, 0, size * 8 + 20, size * 7 + 20)
        subtitle.draw(window, 0, 0, size * 8 + 20, size * 10 + 20)

        pygame.display.update()
        pygame.time.delay(200)

    pygame.quit()
