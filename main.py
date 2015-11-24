import threading
import sys

import pygame

from pygame.locals import *

from eeglogger import EEGLogger
from foblogger import FobLogger

# standard pygame setup code
pygame.init()
play_clock = pygame.time.Clock()
screen = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN | pygame.NOFRAME, 32)
pygame.display.set_caption('symtop')
coordinate = (0, 0)
coordlock = threading.Lock()

if __name__ == '__main__':
    motion_tracker = FobLogger(coordlock)
    eeg_logger = EEGLogger()
    motion_tracker.start()
    eeg_logger.start()

    ypos = 0
    while True:
        # event handling loop for quit events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # fill the screen to draw from a blank state
        screen.fill((255, 255, 255))

        # draw a red tracking ball
        coordlock.acquire()
        pygame.draw.circle(screen, (255, 0, 0), (int((coordinate[0] + 58) * 10), int((coordinate[1] + 71) * 10)), 40)
        coordlock.release()

        # draw target ball
        pygame.draw.circle(screen, (0, 50, 255), (int(800), int(ypos)), 40)

        pygame.display.update()
        play_clock.tick(60)
        ypos += 1
        ypos %= 1600
