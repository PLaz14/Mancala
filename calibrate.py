from gameagent import Agent
from game import Board
import math as m
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")

SHOW_EVERY = 100

class Simulate:
    def __init__(self):
        self.total_reward = []

    def __str__(self):
        moving_avg = np.convolve(self.total_reward, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode='valid')
        plt.plot([i for i in range(len(moving_avg))], moving_avg)
        plt.ylabel(f"Reward {SHOW_EVERY}ma")
        plt.xlabel("episode #")
        plt.show()


if __name__ == "__main__":
    s = Simulate()
    agent = Agent()

    for i in range(1000):
        startboard = np.array([[4] * 6, [0] * 2, [4] * 6])
        b = Board(startboard)
        c, player = np.random.randint(1, 3), 0
        empty = [0] * 6  # used to check if one side of the board is empty
        while b.board[0] != empty and b.board[2] != empty:
            if c % 2 == 1:
                player = 1
            elif c % 2 == 0:
                player = 2

            if player == 1:
                agent.game_reward += agent.runtime(b, player)
                while b.goagainp1:
                    #print('agentI went again...')
                    agent.game_reward += agent.runtime(b, player)
                agent.epsilon *= agent.EPS_DECAY
            elif player == 2:
                agent.game_reward += agent.runtime(b, player)
                while b.goagainp2:
                    #print('agentI went again...')
                    agent.game_reward += agent.runtime(b, player)
                agent.epsilon *= agent.EPS_DECAY

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
        #print(b)
        agent.game_reward += (b.board[1][0] - b.board[1][1])
        #if not i%100:
        print('Game {}: '.format(i), end='')
        if winner == 0:
            print("It's a draw! Final score " + score)
        else:
            print("Player {} won! Final score ".format(winner) + score)
        s.total_reward.append(agent.game_reward)
    print(s)