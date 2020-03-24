import array

class Levels:
    level1 = [-1, -1, -1, -1, -1, -1, -1, -1,
              -1, -1, -1, -1, -2, -1, -1, -1,
              -1, -1, -1, -1, -1, -1, -1, -1,
              -1, -1, -1, -1, -1, -1, -1, -1,
              -1, -1,  2, -1, -1, -1, -1, -1,
              -1, -1, -1, -1,  2, -1, -1, -1,
              -1, -1, -1, -1, -1, -1, -1, -1,
              -1, -1, -1, -1, -1, -1, -1, -1,]

    levels = [level1]

    def get_level(self, i):
        if i < 1:
            i = 1
        elif i > len(self.levels):
            i = len(self.levels)

        return self.levels[i - 1]