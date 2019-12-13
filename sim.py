import numpy as np
from game import Board
import random as r


def cycle():
    startboard = np.array([[4] * 6, [0] * 2, [4] * 6])
    b = Board(startboard)

    c = 1
    player = 0
    empty = [0] * 6
    moves = 0
    while b.board[0] != empty and b.board[2] != empty:
        pos = r.randint(1, 6)
        if c % 2 == 1:
            player = 1
        elif c % 2 == 0:
            player = 2

        if player == 1:
            b.movep1(pos - 1)
            moves+=1
            while b.goagainp1:
                b.movep1(pos - 1)
                moves+=1
        elif player == 2:
            b.movep2(pos - 1)
            moves+=1
            while b.goagainp2:
                b.movep2(pos - 1)
                moves+=1

        c += 1
    if b.board[0] == empty:
        b.board[1][1] += sum(b.board[2])
        b.board[2] = empty
    elif b.board[2] == empty:
        b.board[1][0] += sum(b.board[0])
        b.board[0] = empty
    score = '{}-{}'.format(max(b.board[1]), min(b.board[1]))
    if b.board[1].index(max(b.board[1])) == 0 and not (max(b.board[1]) == min(b.board[1])):
        winner = 2
    elif b.board[1].index(max(b.board[1])) == 1 and not (max(b.board[1]) == min(b.board[1])):
        winner = 1
    else:
        winner = 0
    '''
    print(b)
    if winner == 0:
        print("It's a draw! Final score " + score)
    else:
        print("Player {} won! Final score ".format(winner) + score)
    '''
    return winner, moves


if __name__ == "__main__":
    it = 10000
    p1, p2, d, moves = 0, 0, 0, 0
    for i in range(it):
        w, m = cycle()
        if w == 1: p1 += 1
        elif w == 2: p2 += 1
        else: d += 1
        if i%(it/10)==0: print('{} iterations run'.format(i))
        moves+=m

    print()
    print('-' * 10 + 'STATS' + '-' * 10)
    print('Player 1 wins {:.3f} of the time'.format(p1 / it))
    print('Player 2 wins {:.3f} of the time'.format(p2 / it))
    print('Draw {:.3f} of the time'.format(d / it))
    print('Average number of moves per game: {}'.format(moves / it))