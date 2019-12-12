import numpy as np


class Board:
    def __init__(self, b):
        self.board = b
        self.goagainp1 = True
        self.goagainp2 = True

    def __str__(self):
        s = '--'
        for i in self.board[0]:
            s += '{:>3}'.format(i)
        s += '--\n' + '{:>2}'.format(self.board[1][0]) + ' | ' * 6 + '{:<2}'.format(self.board[1][1]) + '\n--'
        for i in self.board[2]:
            s += '{:>3}'.format(i)
        s+='--'
        return s

    def movep1(self, pos):
        self.goagainp1 = False
        row = 2
        stones = self.board[row][pos]
        self.board[row][pos] = 0
        while stones != 0:
            while pos+1 != len(self.board[row]):
                self.board[row][pos+1]+=1
                pos+=1
                stones-=1
                if stones == 0:
                    return

            self.board[1][1]+=1
            stones-=1
            if stones == 0:
                self.goagainp1 = True
                return

            row = 0
            pos = 6
            while pos-1 != -1:
                self.board[row][pos-1]+=1
                pos-=1
                stones-=1
                if stones == 0:
                    return
            pos = -1
            row = 2

    def movep2(self, pos):
        self.goagainp2 = False
        row = 0
        stones = self.board[row][pos]
        self.board[row][pos] = 0
        while stones != 0:
            while pos-1 != -1:
                self.board[row][pos-1]+=1
                pos-=1
                stones-=1
                if stones == 0:
                    return

            self.board[1][0]+=1
            stones-=1
            if stones == 0:
                self.goagainp2 = True
                return

            row = 2
            pos = -1
            while pos+1 != len(self.board[row]):
                self.board[row][pos+1]+=1
                pos+=1
                stones-=1
                if stones == 0:
                    return
            pos = 6
            row = 0
            


if __name__ == "__main__":
    startboard = np.array([[4] * 6, [0] * 2, [4] * 6])
    b = Board(startboard)
    print(b)

    c = 1
    empty = [0]*6
    while b.board[0]!=empty and b.board[2]!=empty:
        pos = 0
        if c%2 == 1:
            player = 1
        elif c%2 == 0:
            player = 2

        try:
            pos = input("Player {}, choose your space to move from...".format(player)) 
        except:
            pass
        while not -1<pos-1<6:
            try:
                pos = input("Player {}, choose your space to move from...".format(player))
            except:
                continue

        if player == 1:
            b.movep1(pos-1) 
            print(b)
            while b.goagainp1:
                try:
                    pos = input("Player 1, go again...")
                except:
                    continue
                b.movep1(pos-1)
                print(b)
        elif player == 2:
            b.movep2(pos-1)
            print(b)
            while b.goagainp2:
                try:
                    pos = input("Player 2, go again...")
                except:
                    continue
                b.movep2(pos-1)
                print(b)


        c+=1
    if b.board[0] == empty: 
        b.board[1][1]+=sum(b.board[2])
        b.board[2]=empty
    elif b.board[2] == empty: 
        b.board[1][0]+=sum(b.board[0])
        b.board[0]=empty
    score = '{}-{}'.format(max(b.board[1]), min(b.board[1]))
    if b.board[1].index(max(b.board[1])) == 0: winner = 2
    else: winner = 1
    print(b)
    print("Player {} won! Final score ".format(winner)+score)
