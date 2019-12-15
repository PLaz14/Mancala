#import tensorflow as tf
import pygame as pg
import math as m
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
style.use('ggplot')
pg.init()

### PyGame variables for RL training ###
rot = 0
x1 = 150
y1 = 300
laps = 0
vel = 10

### RL variables ###
SIZE = 10
HM_EPISODES = 25000
MOVE_PENALTY = 1
WALL_PENALTY = 200
LAP_REWARD = 50
epsilon = 0.5
EPS_DECAY = 0.9999
SHOW_EVERY = 1000

start_q_table = None

LEARNING_RATE = 0.1
DISCOUNT = 0.95

### make the q-table ###
# i = left distance to closest wall
# j = forward distance to closest wall
# k = right distance to closest wall
if start_q_table is None:
    q_table = {}
    for i in range(-SIZE+1, SIZE):
        q_table[i] = [np.random.uniform(-5, 0) for t in range(2)]
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)

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

    ### main method ###
    def play(self, episode):
        run = pg.display.set_mode((800, 600))
        pg.display.set_caption("Run Game")

        while True:
            pg.time.delay(100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            # rotate based on key pressed by user
            self.testrot()
            self.move()
            self.check()

            run.fill((0, 0, 0))

            pg.draw.lines(run, (255, 255, 255), True, self.mazeout)
            pg.draw.lines(run, (255, 255, 255), True, self.mazein)
            pg.draw.line(run, (0, 255, 0), self.start[0], self.start[1])
            pg.draw.circle(run, (255, 0, 0), (int(self.x), int(self.y)), 10, 0)
            font = pg.font.Font('freesansbold.ttf', 16)
            # lap counter
            lap = font.render('Laps = {}'.format(self.laps), True, (255, 255, 255))
            lapRect = lap.get_rect()
            lapRect.center = (100, 50)
            run.blit(lap, lapRect)
            # episode counter
            ep = font.render('Episode = {}'.format(episode), True, (255, 255, 255))
            epRect = ep.get_rect()
            epRect.center = (650, 50)
            run.blit(ep, epRect)

            self.lap()

            pg.display.update()

    def action(self, choice):
        if choice==0:
            self.rot -= 0.2
        elif choice==1:
            self.rot += 0.2

    ### method for testing the class ###
    def testrot(self):
        k = pg.key.get_pressed()

        if k[pg.K_LEFT]:
            self.rot -= 0.2
        if k[pg.K_RIGHT]:
            self.rot += 0.2

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
        if 100<self.x<200 and 295<self.y<305 and not self.state:
            self.laps+=1

    ### method for finding the balls left, forward, and right distance values ###
    def finddistances(self, theta):


    def distform(self, p):
        return m.hypot(self.x-p[0], self.y-p[1])

    def detform(self, a, b, c, d):


episode_rewards = []
for episode in range(HM_EPISODES):
    game = RL()
    if episode % SHOW_EVERY == 0:
        print(f"on #{episode}, epsilon is {epsilon}")
        print(f"{SHOW_EVERY} ep mean: {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False

    episode_reward = 0
    for i in range(200):
        obj =

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
        pg.draw.circle(run, (255, 0, 0), (int(x1),int(y1)), 10, 0)
        font = pg.font.Font('freesansbold.ttf', 16)
        # lap counter
        lap = font.render('Laps = {}'.format(laps), True, (255, 255, 255))
        lapRect = lap.get_rect()
        lapRect.center = (100, 50)
        run.blit(lap, lapRect)

        if 100<x1<200 and 295<y1<305 and not state:
            laps+=1

        pg.draw.line(run, (0, 0, 255), (int(x1), int(y1)), (int(x1+(1000*m.sin(rot))), int(y1-(1000*m.cos(rot)))))

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
    if min(map(lambda p: p[0], mazein))<x1<max(map(lambda p: p[0], mazein)) and min(map(lambda p: p[1], mazein))<y1<max(map(lambda p: p[1], mazein)):
        x1, y1 = 150, 300
        rot = 0
        state = True
        laps = 0
    elif not (min(map(lambda p: p[0], mazeout))<x1<max(map(lambda p: p[0], mazeout)) and min(map(lambda p: p[1], mazeout))<y1<max(map(lambda p: p[1], mazeout))):
        x1, y1 = 150, 300
        rot = 0
        state = True
        laps = 0
    else:
        state = False
    return rot, x1, y1, state, laps

if __name__=="__main__":
    usergame()