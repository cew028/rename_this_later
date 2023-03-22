from pygame.locals import *

FPS = 60
GRIDSIZE = 10
WINWIDTH, WINHEIGHT = 48 * GRIDSIZE, 24 * GRIDSIZE
HALFWINWIDTH, HALFWINHEIGHT = WINWIDTH/2, WINHEIGHT/2

CLOCK_SPEED = FPS # When CLOCK_SPEED = FPS, an in-game minute is a real-life second.
				  # Make CLOCK_SPEED smaller to cause in-game time to pass faster.

BLACK = (000, 000, 000)
WHITE = (255, 255, 255)
RED   = (255, 000, 000)

A = K_z
B = K_x
UP = K_UP
DOWN = K_DOWN
LEFT = K_LEFT
RIGHT = K_RIGHT