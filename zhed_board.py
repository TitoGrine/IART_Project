from enum import Enum
import sys
from copy import deepcopy


class BoardState(Enum):
    GOAL = -2
    EMPTY = -1
    FILLED = 0


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

    def __init__(self, board_state, goals, numbered, is_goal=False):
        self.is_goal = is_goal
        self.numbered = numbered
        self.goals = goals
        self.board_state = board_state

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

    # Builds the board state if the left operator is chosen on a given numbered blocks coordinate
    def left(self, numbered_block):
        y = numbered_block[0]
        x = numbered_block[1] - 1
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x + 1]
        row = board_state[y]
        goal = self.is_goal
        while num_blocks > 0 and x >= 0:
            if row[x] == BoardState.GOAL:
                goal = True
                break
            if row[x] != BoardState.EMPTY:
                row[x] = BoardState.EMPTY
                num_blocks -= 1
            x -= 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, is_goal=goal)

    # Builds the board state if the right operator is chosen on a given numbered blocks coordinate
    def right(self, numbered_block):
        y = numbered_block[0]
        x = numbered_block[1] + 1
        board_state = deepcopy(self.board_state)
        num_blocks = board_state[y][x - 1]
        row = board_state[y]
        goal = self.is_goal
        while num_blocks > 0 and x <= len(row):
            if row[x] == BoardState.GOAL:
                goal = True
                break
            if row[x] != BoardState.EMPTY:
                row[x] = BoardState.EMPTY
                num_blocks -= 1
            x += 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, is_goal=goal)

    # Builds the board state if the up operator is chosen on a given numbered blocks coordinate
    def up(self, numbered_block):
        y = numbered_block[0] - 1
        x = numbered_block[1]
        board_state = self.board_state.copy()
        num_blocks = board_state[y + 1][x]
        goal = self.is_goal
        while num_blocks > 0 and y >= 0:
            if board_state[y][x] == BoardState.GOAL:
                goal = True
                break
            if board_state[y][x] != BoardState.EMPTY:
                board_state[y][x] = BoardState.EMPTY
                num_blocks -= 1
            y -= 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, is_goal=goal)

    # Builds the board state if the down operator is chosen on a given numbered blocks coordinate
    def down(self, numbered_block):
        y = numbered_block[0] + 1
        x = numbered_block[1]
        board_state = self.board_state.copy()
        num_blocks = board_state[y - 1][x]
        goal = self.is_goal
        while num_blocks > 0 and y <= len(board_state):
            if board_state[y][x] == BoardState.GOAL:
                goal = True
                break
            if board_state[y][x] != BoardState.EMPTY:
                board_state[y][x] = BoardState.EMPTY
                num_blocks -= 1
            y += 1

        numbered = self.numbered.copy()
        numbered.remove(numbered_block)
        return ZhedBoard(board_state, self.goals.copy(), numbered, is_goal=goal)

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
        # TODO: Add heuristic to compare states
        return 0

    def cost(self):
        return -sys.maxsize if self.is_goal else 0
