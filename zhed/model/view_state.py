import random


class GameColors:
    @staticmethod
    def empty_color():
        deviance = random.randint(-10, 10)
        return 117 + deviance, 230 + deviance, 218 + deviance

    TILE = (12, 97, 112)
    TILE_TEXT = (190, 218, 221)

    GOAL_TEXT = (125, 24, 13)
    GOAL = (227, 66, 52)

    COMPLETED = (33, 182, 168)
    COMPLETED_TEXT = (163, 235, 177)

    HINT = (245, 251, 65)
    HINT_TEXT = (36, 98, 13)

    BACKGROUND = (97, 200, 188)

    WHITE = (255, 255, 255)


class BoardSettings:
    def __init__(self, window, font):
        self.window = window
        self.font = font


class Hint:
    NO_HINT = -1
    HINT = -2

    def __init__(self, hint, path, block=None):
        self.path = path
        self.hint = hint
        self.block = block
