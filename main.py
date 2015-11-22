import threading
import sys
import time

import pygame

from pygame.locals import *

from pyfob import Fob
from pysymtop import Symtop


# set up a bunch of constants
BRIGHTBLUE = (0, 50, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BGCOLOR = WHITE

WINDOWWIDTH = 1920  # width of the program's window, in pixels
WINDOWHEIGHT = 1080  # height in pixels
WIN_CENTERX = int(WINDOWWIDTH / 2)
WIN_CENTERY = int(WINDOWHEIGHT / 2)

FPS = 60

PERIOD_INCREMENTS = 500.0
AMPLITUDE = 100

# standard pygame setup code
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Trig Bounce')

COORD = (0, 0)
MY_LOCK = threading.Lock()


class Foblogger(threading.Thread):
    def __init__(self, t_name):
        threading.Thread.__init__(self, name=t_name)
        self.fob = Fob()

    def run(self):
        global COORD
        while True:
            time.sleep(0.01)
            MY_LOCK.acquire()
            COORD = self.fob.getcord()
            MY_LOCK.release()


class EEGlogger(threading.Thread):
    def __init__(self, t_name):
        threading.Thread.__init__(self, name=t_name)
        self.symtop = Symtop()

    def run(self):
        while True:
            self.symtop.geteeg()


if __name__ == '__main__':
    motiontracker = Foblogger('fob-logger')
    eeglogger = EEGlogger('eeg-logger')
    motiontracker.start()
    eeglogger.start()
    ypos = 0
    while True:
        # event handling loop for quit events

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # fill the screen to draw from a blank state
        DISPLAYSURF.fill(BGCOLOR)

        # draw tracking ball
        MY_LOCK.acquire()
        pygame.draw.circle(DISPLAYSURF, RED, (int((COORD[0] - 58) * 10), int((COORD[1] + 71) * 10)), 40)
        MY_LOCK.release()

        # draw target ball
        pygame.draw.circle(DISPLAYSURF, BRIGHTBLUE, (int(WINDOWWIDTH * 0.333), int(ypos) + WIN_CENTERY), 40)

        # draw the border
        pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, WINDOWWIDTH, WINDOWHEIGHT), 1)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        ypos += 1
        ypos %= WINDOWHEIGHT
