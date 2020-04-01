from dataclasses import dataclass
from enum import Enum


class BoardState(Enum):
    # Different states of the pieces of the board
    GOAL = -2
    EMPTY = -1
    FILLED = 0


class BoardMove(Enum):
    # Different moves of the board
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


@dataclass
class Move:
    # Different moves of the board
    move: BoardMove
    starting_block: tuple
    finish_block: tuple
    placed_blocks: list
    used_blocks: int
