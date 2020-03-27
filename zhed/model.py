from dataclasses import dataclass
from enum import Enum


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
    finish_block: tuple
    placed_blocks: list
    used_blocks: int
