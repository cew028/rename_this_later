import pygame
import sys
from pygame.locals import *

import spritesheet

FPS = 30 
WINWIDTH = 640
WINHEIGHT = 480

WHITE = (255, 255, 255)

def build_sprites(image_file):
	SPRITES = spritesheet.spritesheet(image_file)
	PLAYERSPRITE = {
		"left":  SPRITES.image_at(( 0,  0, 16, 16), colorkey = 0),
		"up":    SPRITES.image_at((16,  0, 16, 16), colorkey = 0),
		"right": SPRITES.image_at((32,  0, 16, 16), colorkey = 0),
		"down":  SPRITES.image_at((48,  0, 16, 16), colorkey = 0),
	}
	return PLAYERSPRITE

def main():
	global FPSCLOCK, DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	# pygame.display.set_icon(pygame.image.load(".png")) TODO
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	pygame.display.set_caption("Title")
	# BASICFONT = pygame.font.Font("freesansbold.ttf", 32)
	while True:
		runGame()

def runGame():
	camerax          = 0 # x-coordinate of the center of the camera
	cameray          = 0 # y-coordinate of the center of the camera
	playerx          = WINWIDTH/2 # x-coordinate of the player
	playery          = WINHEIGHT/2 # y-coordinate of the player
	targetx          = playerx # x-coordinate of the destination
	targety          = playery # y-coordinate of the destination
	moving           = False
	move_delay       = 5 # Number of frames to wait before moving. If you tap, you don't move; you have to hold the button.
	move_delay_count = 0
	player_direction = "left"
	while True:
		# current_time = FPSCLOCK.get_time()
		DISPLAYSURF.fill(WHITE)
		DISPLAYSURF.blit(build_sprites("arrow.png")[player_direction], (playerx,playery))

		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()

		keys = pygame.key.get_pressed()

		if keys[K_UP] and not moving:
			player_direction = "up"
			move_delay_count += 1
			if move_delay_count >= move_delay:
				moving = True
				targety -= 16
		if keys[K_DOWN] and not moving:
			player_direction = "down"
			move_delay_count += 1
			if move_delay_count >= move_delay:
				moving = True
				targety += 16
		if keys[K_LEFT] and not moving:
			player_direction = "left"
			move_delay_count += 1
			if move_delay_count >= move_delay:
				moving = True
				targetx -= 16
		if keys[K_RIGHT] and not moving:
			player_direction = "right"
			move_delay_count += 1
			if move_delay_count >= move_delay:
				moving = True
				targetx += 16

		if targetx > playerx: # Target to the right
			playerx += 2 
		if targetx < playerx: # Target to the left
			playerx -= 2
		if targety > playery: # Target below
			playery += 2 
		if targety < playery: # Target above
			playery -= 2

		if not (keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]):
			move_delay_count = 0

		if moving and targetx == playerx and targety == playery:
			moving = False


		pygame.display.update()
		FPSCLOCK.tick(FPS)

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()