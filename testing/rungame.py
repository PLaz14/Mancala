# import tensorflow as tf
import pygame as pg
import math as m
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use('ggplot')
pg.init()

### PyGame variables for RL training ###
rot = 0
x1 = 150
y1 = 300
laps = 0
vel = 10

### RL variables ###
SIZE = 15
HM_EPISODES = 25000
MOVE_PENALTY = 1
WALL_PENALTY = 200
LAP_REWARD = 25
epsilon = 0.9
EPS_DECAY = 0.9999
SHOW_EVERY = 1000

start_q_table = None

LEARNING_RATE = 0.1
DISCOUNT = 0.95

### make the q-table ###
# x = x-position of the ball
# y = y-position of the ball
# r = rotation of the ball
print('Building Q-Table...')
start = time.time()
if start_q_table is None:
    q_table = dict()
    for x in range(100, 701, vel):
        if not x%100:
            print('through:', x-100)
        for y in range(100, 501, vel):
            for r in range(-127, 128):
                q_table[(x, y), round(r*m.pi/16, 5)] = [np.random.uniform(-25, 0) for t in range(3)]
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)

end = time.time()
print('operation took {:.2f} seconds'.format(end-start))

### RL class and methods ###
class RL():
    def __init__(self):
        self.rot = 0
        self.x = 150
        self.y = 300
        self.vel = 10
        self.mazeout = [(100, 100), (700, 100), (700, 500), (100, 500)]
        self.mazein = [(200, 200), (600, 200), (600, 400), (200, 400)]
        self.start = [(100, 300), (200, 300)]
        self.laps = 0
        # forward distance
        self.distance = 0
        self.state = False

        self.finddistances()
        self.play(69)

    ### main method ###
    def play(self, episode):
        self.run = pg.display.set_mode((800, 600))
        pg.display.set_caption("Run Game")

        while True:
            pg.time.delay(100)
            for event in pg.event.get():
                if event.type == pg.QUIT or self.state:
                    return

            # rotate based on key pressed by user
            self.testrot()
            self.move()
            self.check()
            self.lap()

            self.run.fill((0, 0, 0))

            pg.draw.lines(self.run, (255, 255, 255), True, self.mazeout)
            pg.draw.lines(self.run, (255, 255, 255), True, self.mazein)
            pg.draw.line(self.run, (0, 255, 0), self.start[0], self.start[1])
            pg.draw.circle(self.run, (255, 0, 0), (int(self.x), int(self.y)), 10, 0)

            font = pg.font.Font('freesansbold.ttf', 16)
            # lap counter
            lap = font.render('Laps = {}'.format(self.laps), True, (255, 255, 255))
            lapRect = lap.get_rect()
            lapRect.center = (100, 50)
            self.run.blit(lap, lapRect)
            # episode counter
            ep = font.render('Episode = {}'.format(episode), True, (255, 255, 255))
            epRect = ep.get_rect()
            epRect.center = (650, 50)
            self.run.blit(ep, epRect)

            '''
            # draws guiding lines
            pg.draw.line(self.run, (0, 0, 255), (int(self.x), int(self.y)), (int(self.xn), int(self.yn)))
            pg.draw.line(self.run, (0, 0, 255), (int(self.x), int(self.y)), (int(self.xe), int(self.ye)))
            pg.draw.line(self.run, (0, 0, 255), (int(self.x), int(self.y)), (int(self.xw), int(self.yw)))
            pg.draw.line(self.run, (0, 0, 255), (int(self.x), int(self.y)), (int(self.xne), int(self.yne)))
            pg.draw.line(self.run, (0, 0, 255), (int(self.x), int(self.y)), (int(self.xnw), int(self.ynw)))

            # drawing circles of intersection with the wall
            self.finddistances()
            '''
            pg.display.update()

    def update(self):
        self.xn, self.yn = self.x + (1000 * m.sin(self.rot)), self.y - (1000 * m.cos(self.rot))
        self.xe, self.ye = self.x - (1000 * m.cos(self.rot)), self.y - (1000 * m.sin(self.rot))
        self.xw, self.yw = self.x + (1000 * m.cos(self.rot)), self.y + (1000 * m.sin(self.rot))
        self.xne, self.yne = self.x + (1000 * m.sin(self.rot - (m.pi / 4))), self.y - (
                1000 * m.cos(self.rot - (m.pi / 4)))
        self.xnw, self.ynw = self.x + (1000 * m.sin(self.rot + (m.pi / 4))), self.y - (
                1000 * m.cos(self.rot + (m.pi / 4)))

    def action(self, choice):
        if choice == 0:
            self.rot -= m.pi/16
        elif choice == 1:
            self.rot += m.pi/16
        elif choice == 2:
            self.rot = self.rot

    ### method for testing the class ###
    def testrot(self):
        k = pg.key.get_pressed()

        if k[pg.K_LEFT]:
            self.rot -= m.pi/16
        if k[pg.K_RIGHT]:
            self.rot += m.pi/16

    def move(self):
        # flipped for better start
        self.x += m.sin(self.rot) * self.vel
        self.y -= m.cos(self.rot) * self.vel

    def check(self):
        if min(map(lambda p: p[0], self.mazein)) < self.x < max(map(lambda p: p[0], self.mazein)) and min(
                map(lambda p: p[1], self.mazein)) < self.y < max(map(lambda p: p[1], self.mazein)):
            self.x, self.y = 150, 300
            self.rot = 0
            self.state = True
            self.laps = 0
        elif not (min(map(lambda p: p[0], self.mazeout)) < self.x < max(map(lambda p: p[0], self.mazeout)) and min(
                map(lambda p: p[1], self.mazeout)) < self.y < max(map(lambda p: p[1], self.mazeout))):
            self.x, self.y = 150, 300
            self.rot = 0
            self.state = True
            self.laps = 0
        else:
            self.state = False

    def lap(self):
        if 100 < self.x < 200 and 295 < self.y < 305 and not self.state:
            self.laps += 1
            return True

    ### method for finding the balls north, east, west, northeast, and northwest distance values ###
    def finddistances(self):
        self.dn, self.de, self.dw, self.dne, self.dnw = [], [], [], [], []
        for p in range(len(self.mazeout)):
            #print(self.mazeout[p], self.mazeout[p - 1])
            try:
                px, py = self.line_intersection((self.xn, self.yn), (self.mazeout[p], self.mazeout[p - 1]))
                self.dn.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.dn.append(0)
            try:
                px, py = self.line_intersection((self.xe, self.ye), (self.mazeout[p], self.mazeout[p - 1]))
                self.de.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.de.append(0)
            try:
                px, py = self.line_intersection((self.xw, self.yw), (self.mazeout[p], self.mazeout[p - 1]))
                self.dw.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.dw.append(0)
            try:
                px, py = self.line_intersection((self.xne, self.yne), (self.mazeout[p], self.mazeout[p - 1]))
                self.dne.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.dne.append(0)
            try:
                px, py = self.line_intersection((self.xnw, self.ynw), (self.mazeout[p], self.mazeout[p - 1]))
                self.dnw.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.dnw.append(0)
        for p in range(len(self.mazein)):
            #print(self.mazein[p], self.mazein[p-1])
            try:
                px, py = self.line_intersection((self.xn, self.yn), (self.mazein[p], self.mazein[p - 1]))
                self.dn.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.dn.append(0)
            try:
                px, py = self.line_intersection((self.xe, self.ye), (self.mazein[p], self.mazein[p - 1]))
                self.de.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.de.append(0)
            try:
                px, py = self.line_intersection((self.xw, self.yw), (self.mazein[p], self.mazein[p - 1]))
                self.dw.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.dw.append(0)
            try:
                px, py = self.line_intersection((self.xne, self.yne), (self.mazein[p], self.mazein[p - 1]))
                self.dne.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.dne.append(0)
            try:
                px, py = self.line_intersection((self.xnw, self.ynw), (self.mazein[p], self.mazein[p - 1]))
                self.dnw.append(self.distform((px, py)))
                pg.draw.circle(self.run, (255, 255, 255), (int(px), int(py)), 3, 0)
            except:
                self.dnw.append(0)

        self.dn, self.de, self.dw, self.dne, self.dnw = int(min(self.dn)), int(min(self.de)), int(min(self.dw)), int(min(self.dne)), int(min(self.dnw))

        return self.dn, self.de, self.dw, self.dne, self.dnw

    def distform(self, p):
        return m.hypot(self.x - p[0], self.y - p[1])

    def line_intersection(self, s, line2):
        xdiff = (self.x - s[0], line2[0][0] - line2[1][0])
        ydiff = (self.y - s[1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*((self.x, self.y), s)), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    def round(self, n):
        if n > 7:
            return int(m.ceil(n / 10.0)) * 10
        else:
            return round(n, 5)

### Inititating Q-Learning ###

episode_rewards = []
game = RL()
for episode in range(HM_EPISODES):
    #print(game.round(157.87))
    if episode % SHOW_EVERY == 0:
        print(f"on #{episode}, epsilon is {epsilon}")
        print(f"{SHOW_EVERY} ep mean: {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False

    episode_reward = 0
    for i in range(200):
        game.update()
        obs = ((game.round(game.x), game.round(game.y)), game.round(game.rot))
        #print(obs)
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 2)
        game.action(action)
        game.move()
        game.check()
        game.lap()
        '''if show:
            game.play(episode)'''

        if game.state:
            reward = -WALL_PENALTY
        elif game.laps > 0:
            reward = LAP_REWARD
        else:
            reward = -MOVE_PENALTY

        new_obs = ((game.round(game.x), game.round(game.y)), game.round(game.rot))
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]

        if reward == LAP_REWARD:
            new_q = LAP_REWARD
        else:
            # Bellman equation
            new_q = (1-LEARNING_RATE)*current_q+LEARNING_RATE*(reward+DISCOUNT*max_future_q)

        episode_reward += reward
        if reward == LAP_REWARD or reward == -WALL_PENALTY:
            break
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')
plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"q-table/qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)

#########################################################

### main game method ###
def usergame():
    run = pg.display.set_mode((800, 600))
    pg.display.set_caption("Run Game")
    maze1out = [(100, 100), (700, 100), (700, 500), (100, 500)]
    maze1in = [(200, 200), (600, 200), (600, 400), (200, 400)]
    start1 = [(100, 300), (200, 300)]

    rot = 0
    x1 = 150
    y1 = 300
    laps = 0
    vel = 10

    while True:
        pg.time.delay(100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # rotate based on key pressed by user
        rot = userrot(rot)

        x1, y1 = move(x1, y1, vel, rot)
        rot, x1, y1, state, laps = check1(rot, x1, y1, maze1in, maze1out, laps)

        run.fill((0, 0, 0))

        pg.draw.lines(run, (255, 255, 255), True, maze1out)
        pg.draw.lines(run, (255, 255, 255), True, maze1in)
        pg.draw.line(run, (0, 255, 0), start1[0], start1[1])
        pg.draw.circle(run, (255, 0, 0), (int(x1), int(y1)), 10, 0)
        font = pg.font.Font('freesansbold.ttf', 16)
        # lap counter
        lap = font.render('Laps = {}'.format(laps), True, (255, 255, 255))
        lapRect = lap.get_rect()
        lapRect.center = (100, 50)
        run.blit(lap, lapRect)

        if 100 < x1 < 200 and 295 < y1 < 305 and not state:
            laps += 1

        pg.display.update()


### user-playing methods ###
def userrot(rot):
    k = pg.key.get_pressed()

    if k[pg.K_LEFT]:
        rot -= 0.2
    if k[pg.K_RIGHT]:
        rot += 0.2

    return rot


def move(x, y, v, r):
    # flipped for better start
    x += m.sin(r) * v
    y -= m.cos(r) * v

    return x, y


def check1(rot, x1, y1, mazein, mazeout, laps):
    if min(map(lambda p: p[0], mazein)) < x1 < max(map(lambda p: p[0], mazein)) and min(
            map(lambda p: p[1], mazein)) < y1 < max(map(lambda p: p[1], mazein)):
        x1, y1 = 150, 300
        rot = 0
        state = True
        laps = 0
    elif not (min(map(lambda p: p[0], mazeout)) < x1 < max(map(lambda p: p[0], mazeout)) and min(
            map(lambda p: p[1], mazeout)) < y1 < max(map(lambda p: p[1], mazeout))):
        x1, y1 = 150, 300
        rot = 0
        state = True
        laps = 0
    else:
        state = False
    return rot, x1, y1, state, laps


if __name__ == "__main__":
    RL()
