from dataclasses import dataclass
from enum import Enum
import sys
from copy import deepcopy


class BoardState(Enum):
    GOAL = -2
    EMPTY = -1
    FILLED = 0


class BoardMove(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


@dataclass
class Move:
    move: BoardMove
    starting_block: tuple
    num_blocks: int
    placed_blocks: list


# Class to save state of Zhed Board
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

    def __init__(self, board_state, goals, numbered, is_goal=False, move=None):
        self.is_goal = is_goal
        self.numbered = numbered
        self.goals = goals
        self.board_state = board_state
        self.move = move

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
        return ZhedBoard(board, goals, numbered)

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
                placed_blocks.append((y,x))
                num_blocks -= 1
        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, is_goal=goal,
                         move=Move(BoardMove.LEFT, numbered_block, num_blocks, placed_blocks))

    # Builds the board state if the right operator is chosen on a given numbered blocks coordinate
    def right(self, numbered_block):
        x, y = self.get_coordinates(numbered_block)
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x]
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
                placed_blocks.append((y,x))
                num_blocks -= 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, is_goal=goal,
                         move=Move(BoardMove.RIGHT, numbered_block, num_blocks, placed_blocks))

    # Builds the board state if the up operator is chosen on a given numbered blocks coordinate
    def up(self, numbered_block):
        x, y = self.get_coordinates(numbered_block)
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x]
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
                placed_blocks.append((y,x))
                num_blocks -= 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, is_goal=goal,
                         move=Move(BoardMove.UP, numbered_block, num_blocks, placed_blocks))

    # Builds the board state if the down operator is chosen on a given numbered blocks coordinate
    def down(self, numbered_block):
        x, y = self.get_coordinates(numbered_block)
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x]
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
                placed_blocks.append((y,x))
                num_blocks -= 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, is_goal=goal,
                         move=Move(BoardMove.DOWN, numbered_block, num_blocks, placed_blocks))

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

    def heuristics(self):
        value = 0
        nearest_goal = self.goals[0]
        x, y = self.get_coordinates(self.move.starting_block)
        nearest_dist = abs(x - nearest_goal[1]) + abs( y - nearest_goal[0])
        #find nearest goal
        for i in self.goals:
            if abs(x - i[1]) + abs( y - i[0]) < nearest_dist:
                nearest_goal = i
                nearest_dist = abs(x - i[1]) + abs( y - i[0])
        #if in same row or column as goal, lessen priority
        if x == nearest_goal[1] or y == nearest_goal[0]:
            value += 10  #value subject to change
        #if expanding away from goal, lessen priority
        if self.move.move == BoardMove.LEFT and x < nearest_goal[1]:
            value += 1
        if self.move.move == BoardMove.RIGHT and x > nearest_goal[1]:
            value += 1
        if self.move.move == BoardMove.DOWN and y > nearest_goal[0]:
            value += 1
        if self.move.move == BoardMove.UP and y < nearest_goal[0]:
            value += 1
        value += nearest_dist

        return value

    def cost(self):
        cost = 0
        for block in self.move.placed_blocks:
            x = block[1]
            y = block[0]
            for i in self.numbered:
                if i[0] == y:
                    if abs(i[1] - x) <= self.board_state[i[0]][i[1]]:
                        cost -= 1
                if i[1] == x:
                    if abs(i[0] - y) <= self.board_state[i[0]][i[1]]:
                        cost -= 1

        return cost
