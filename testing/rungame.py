#import tensorflow as tf
import pygame as pg
import math as m

pg.init()
def game():
    run = pg.display.set_mode((800, 600))
    pg.display.set_caption("Run Game")
    maze1out = [(100, 100), (700, 100), (700, 500), (100, 500)]
    maze1in = [(200, 200), (600, 200), (600, 400), (200, 400)]
    start1 = [(100, 300), (200, 300)]

    rot = 0
    x1 = 150
    y1 = 300

    while True:
        pg.time.delay(100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        rot, x1, y1 = usermove(rot, x1, y1)
        rot, x1, y1 = check1(rot, x1, y1, maze1in, maze1out)

        run.fill((0, 0, 0))

        pg.draw.lines(run, (255, 255, 255), True, maze1out)
        pg.draw.lines(run, (255, 255, 255), True, maze1in)
        pg.draw.line(run, (0, 255, 0), start1[0], start1[1])


        pg.draw.circle(run, (255, 0, 0), (int(x1),int(y1)), 10, 0)

        pg.display.update()

def usermove(rot, x1, y1):
    vel = 10
    k = pg.key.get_pressed()

    if k[pg.K_LEFT]:
        rot -= 0.2
    if k[pg.K_RIGHT]:
        rot += 0.2

    # flipped for better start
    x1 += m.sin(rot)*vel
    y1 -= m.cos(rot)*vel

    return rot, x1, y1

def check1(rot, x1, y1, mazein, mazeout):
    if min(map(lambda p: p[0], mazein))<x1<max(map(lambda p: p[0], mazein)) and min(map(lambda p: p[1], mazein))<y1<max(map(lambda p: p[1], mazein)):
        x1, y1 = 150, 300
        rot = 0
    elif not (min(map(lambda p: p[0], mazeout))<x1<max(map(lambda p: p[0], mazeout)) and min(map(lambda p: p[1], mazeout))<y1<max(map(lambda p: p[1], mazeout))):
        x1, y1 = 150, 300
        rot = 0
    return rot, x1, y1

if __name__=="__main__":
    game()