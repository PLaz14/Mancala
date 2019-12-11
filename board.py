class Board:
    def __int__(self):
        self.p1goal = 0
        self.p2goal = 0
        self.p1side = [4] * 6
        self.p2side = [4] * 6

    def __str__(self):
        row1 = '--'
        for i in self.p1side:
            row1 += '{:>3}'.format(i)
        row1 += '--'
        row2 = '{:>2}' + '---'*6 + '{:>2}'.format(self.p1goal, self.p2goal)
        row3 = '--'
        for i in self.p2side:
            row3 += '{:>3}'.format(i)
        row3 += '--'
        return row1+'\n'+row2+'\n'+row3