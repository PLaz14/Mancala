import numpy as np


class Board:
    def __int__(self):
        self.p1goal = 0
        self.p2goal = 0
        self.p1side = [4] * 6
        self.p2side = [4] * 6
        self.board = np.array(
            [[self.p1side], [self.p1goal, self.p2goal], [self.p2side]])

    def printboard(self):
        for i in self.board:
            for j in i:
                print(j)
            print()
