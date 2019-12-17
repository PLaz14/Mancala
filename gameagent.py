from game import Board
import math as m
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time


class Agent:
    def __init__(self, qtable=None):
        self.PENALTY = 200
        self.REWARD = 1
        self.epsilon = 0.9
        self.EPS_DECAY = 0.9999
        self.game_reward = 0
        self.LEARNING_RATE = 0.1
        self.DISCOUNT = 0.95

        ### Initializing the Q-Table ###
        if qtable is None:
            size = 17
            self.table = {}
            print('Building randomized q-table...', end='')
            start = time.time()
            for a in range(size):
                print('through', a)
                for b in range(size):
                    for c in range(size):
                        for d in range(size):
                            for e in range(size):
                                for f in range(size):
                                    index = (a, b, c, d, e, f)
                                    self.table[index] = [np.random.uniform(-25, 0) for i in range(6)]
            end = time.time()
            print('done (took: {:.2f} seconds)'.format(end - start))
            with open("q-tables/qtable-main.pickle", "wb") as f:
                pickle.dump(self.table, f)
        else:
            with open(qtable, 'rb') as f:
                self.table = pickle.load(f)

    ### Initiate Q-Learning ###
    def runtime(self, b):
        move_reward = 0
        side = b.board[0].copy()
        obs = (side[0], side[1], side[2], side[3], side[4], side[5])
        if np.random.random() > self.epsilon:
            action = np.argmax(self.table[obs])
        else:
            action = np.random.randint(0, 5)

        b.movep2(action)  # take the move
        print('AI picked position', action+1)
        for i in range(self.game_reward, b.board[1][0]):
            move_reward += self.REWARD

        new_side = b.board[0].copy()
        new_obs = (new_side[0], new_side[1], new_side[2], new_side[3], new_side[4], new_side[5])
        max_future_q = np.max(self.table[new_obs])
        current_q = self.table[obs][action]

        if move_reward > 0:
            new_q = move_reward
        else:  # using the Bellman equation
            new_q = (1 - self.LEARNING_RATE) * current_q + self.LEARNING_RATE * (
                    move_reward + self.DISCOUNT * max_future_q)
        self.table[obs][action] = new_q  # update the q-table

        self.epsilon*=self.EPS_DECAY

        return move_reward


if __name__ == "__main__":
    A = Agent()
    startboard = np.array([[4] * 6, [0] * 2, [4] * 6])
    b = Board(startboard)
    print(b)

    c, player = 1, 0
    empty = [0] * 6  # used to check if one side of the board is empty
    while b.board[0] != empty and b.board[2] != empty:
        pos = 0
        if c % 2 == 1:
            player = 1
        elif c % 2 == 0:
            player = 2

        if player == 1:
            try:
                pos = int(input(("Player {}, choose your space to move from...\n".format(player))))
                if pos == 99:  # force exit the program
                    break
            except:
                pass
            while not -1 < pos - 1 < 6:
                try:
                    pos = int(input(("Player {}, choose your space to move from...\n".format(player))))
                    if pos == 99:  # same
                        break
                except:
                    continue

        if player == 1:
            b.movep1(pos - 1)
            print(b)
            while b.goagainp1:
                try:
                    pos = int(input("Player 1, go again...\n"))
                    if pos == 99:
                        break
                except:
                    continue
                b.movep1(pos - 1)
                print(b)
        elif player == 2:
            A.game_reward += A.runtime(b)
            print(b)
            while b.goagainp2:
                print('AI went again...')
                A.game_reward += A.runtime(b)
                print(b)

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
    print(b)
    A.game_reward+=(b.board[1][0]-b.board[[1][1]])
    if winner == 0:
        print("It's a draw! Final score " + score)
        print('AI game reward: ', A.game_reward)
    else:
        print("Player {} won! Final score ".format(winner) + score)
        print('AI game reward: ', A.game_reward)

