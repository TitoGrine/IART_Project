import math
import sys
from copy import deepcopy
from functools import reduce

import heuristics as hs
# Class to save state of Zhed Board
from zhed.model import *


class ZhedBoard:
    """" Constructor
    :param board_state: list of lists with the state of the board
    :param goals: list of tuples with coordinates to the goals
    :param numbered: list of tuples with coordinates to the numbered blocks
    """
    types = {
        ".": BoardState.EMPTY,
        "X": BoardState.GOAL
    }

    heuristics_function = None

    def __init__(self, board_state, goals, numbered, align_numbered, is_goal=False, move=None):
        self.align_numbered = align_numbered
        self.is_goal = is_goal
        self.numbered = numbered
        self.goals = goals
        self.board_state = board_state
        self.move = move
        if move is not None:
            goal = self.get_nearest(self.move.starting_block, self.goals)
            self.heuristics_value = self.heuristics_function(goal)
            self.cost_value = self.cost()

    # Build from list of list of strings the state of the board
    @staticmethod
    def build_from_file(board_state):
        goals = []
        numbered = []
        board = []
        for i in range(0, len(board_state)):
            row = []
            for j in range(0, len(board_state[i])):
                current_piece = board_state[i][j]
                piece = ZhedBoard.types.get(current_piece,
                                            int(current_piece) if current_piece.isdigit() else current_piece)
                if piece == BoardState.GOAL:
                    goals.append((i, j))
                elif piece != BoardState.EMPTY and piece > 0:
                    numbered.append((i, j))
                row.append(piece)
            board.append(row)

        aligned_numbered = list(filter(
            lambda x: len(list(filter(lambda y: y[0] == x[0] or x[1] == y[1], goals))) > 0, numbered))

        return ZhedBoard(board, goals, numbered, aligned_numbered)

    @staticmethod
    def get_coordinates(numbered_block):
        y = numbered_block[0]
        x = numbered_block[1]
        return x, y

    # Builds the board state if the left operator is chosen on a given numbered blocks coordinate
    def left(self, numbered_block):
        x, y = self.get_coordinates(numbered_block)
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x]
        used_blocks = num_blocks + 0 if self.move is None else self.move.used_blocks
        row = board_state[y]
        placed_blocks = []
        goal = self.is_goal
        row[x] = BoardState.FILLED
        while num_blocks > 0 and x > 0:
            x -= 1
            if row[x] == BoardState.GOAL:
                goal = True
                break
            if row[x] == BoardState.EMPTY:
                row[x] = BoardState.FILLED
                placed_blocks.append((y, x))
                num_blocks -= 1
        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, self.align_numbered, is_goal=goal,
                         move=Move(BoardMove.LEFT, numbered_block, (y, x), placed_blocks, used_blocks))

    # Builds the board state if the right operator is chosen on a given numbered blocks coordinate
    def right(self, numbered_block):
        x, y = self.get_coordinates(numbered_block)
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x]
        used_blocks = num_blocks + 0 if self.move is None else self.move.used_blocks
        row = board_state[y]
        placed_blocks = []
        goal = self.is_goal
        row[x] = BoardState.FILLED
        while num_blocks > 0 and x < len(row) - 1:
            x += 1
            if row[x] == BoardState.GOAL:
                goal = True
                break
            if row[x] == BoardState.EMPTY:
                row[x] = BoardState.FILLED
                placed_blocks.append((y, x))
                num_blocks -= 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, self.align_numbered, is_goal=goal,
                         move=Move(BoardMove.RIGHT, numbered_block, (y, x), placed_blocks, used_blocks))

    # Builds the board state if the up operator is chosen on a given numbered blocks coordinate
    def up(self, numbered_block):
        x, y = self.get_coordinates(numbered_block)
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x]
        used_blocks = num_blocks + 0 if self.move is None else self.move.used_blocks
        placed_blocks = []
        goal = self.is_goal
        board_state[y][x] = BoardState.FILLED
        while num_blocks > 0 and y > 0:
            y -= 1
            if board_state[y][x] == BoardState.GOAL:
                goal = True
                break
            if board_state[y][x] == BoardState.EMPTY:
                board_state[y][x] = BoardState.FILLED
                placed_blocks.append((y, x))
                num_blocks -= 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, self.align_numbered, is_goal=goal,
                         move=Move(BoardMove.UP, numbered_block, (y, x), placed_blocks, used_blocks))

    # Builds the board state if the down operator is chosen on a given numbered blocks coordinate
    def down(self, numbered_block):
        x, y = self.get_coordinates(numbered_block)
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x]
        used_blocks = num_blocks + 0 if self.move is None else self.move.used_blocks
        placed_blocks = []
        goal = self.is_goal
        board_state[y][x] = BoardState.FILLED
        while num_blocks > 0 and y < len(board_state) - 1:
            y += 1
            if board_state[y][x] == BoardState.GOAL:
                goal = True
                break
            if board_state[y][x] == BoardState.EMPTY:
                board_state[y][x] = BoardState.FILLED
                placed_blocks.append((y, x))
                num_blocks -= 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, self.align_numbered, is_goal=goal,
                         move=Move(BoardMove.DOWN, numbered_block, (y, x), placed_blocks, used_blocks))

    # Gets all the operators from the current board state
    @staticmethod
    def get_all_operators(self):
        operators = []
        for i in self.numbered:
            if i[1] > 0:
                operators.append(self.left(i))
            if i[1] < (len(self.board_state[i[0]])) - 1:
                operators.append(self.right(i))
            if i[0] < (len(self.board_state)) - 1:
                operators.append(self.down(i))
            if i[0] > 0:
                operators.append(self.up(i))
        return operators

    # Gets all the operators from the current board state
    @staticmethod
    def get_all_expandables(self, coords):
        placed = []

        if coords[1] > 0:
            placed.append(self.left(coords).move.placed_blocks)
        if coords[1] < (len(self.board_state[coords[0]])) - 1:
            placed.append(self.right(coords).move.placed_blocks)
        if coords[0] < (len(self.board_state)) - 1:
            placed.append(self.down(coords).move.placed_blocks)
        if coords[0] > 0:
            placed.append(self.up(coords).move.placed_blocks)

        return placed

    @staticmethod
    def manhattan(self, other):
        return abs(self[0] - other[0]) + abs(self[1] - other[1])

    def heuristics(self):
        value = 0
        nearest_goal = self.get_nearest(self.move.starting_block, self.goals)
        nearest_dist = hs.nearest_dist(self,)
        goal_dist = hs.nearest_goal(self, nearest_goal)
        value += hs.in_direction_of_goal(self)
        value += hs.punish_bad_expansions(self, nearest_goal)
        value += hs.benefit_outered_blocks(self, nearest_goal)
        return value + goal_dist + nearest_dist

    def get_nearest(self, coordinates, coordinates_list):
        return reduce(
            lambda curr, nxt: curr if self.manhattan(curr, coordinates) <
                                      self.manhattan(nxt, coordinates) else nxt, coordinates_list)

    def is_the_same_quadrant(self):
        nearest_goal = self.get_nearest(self.move.starting_block, self.goals)
        x_quadrant = len(self.board_state[0]) / 2
        y_quadrant = len(self.board_state) / 2
        goal_quadrant = (math.ceil(nearest_goal[0] / y_quadrant), math.ceil(nearest_goal[1] / x_quadrant))
        finish_quadrant = (math.ceil(self.move.finish_block[0] / y_quadrant),
                           math.ceil(self.move.finish_block[1] / x_quadrant))
        return goal_quadrant == finish_quadrant

    def cost(self):
        if self.is_goal:
            return -sys.maxsize

        return self.move.used_blocks
