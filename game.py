# import numpy as np


class Board:
    def __init__(self, b):
        self.board = b

    def __str__(self):
        s = '--'
        for i in self.board[0]:
            s += '{:>3}'.format(i)
        s += '--\n' + '{:>2}'.format(self.board[1][0]) + ' | ' * 6 + '{:<2}'.format(self.board[1][1]) + '\n--'
        for i in self.board[2]:
            s += '{:>3}'.format(i)
        s+='--'
        return s

    def move(self, pos):



if __name__ == "__main__":
    startboard = [[4] * 6, [0] * 2, [4] * 6]
    b = Board(startboard)


