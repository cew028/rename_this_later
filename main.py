import pygame
import sys
from pygame.locals import *

import font_manager
import spritesheet

FPS = 30
WINWIDTH = 640
WINHEIGHT = 480
GRIDSIZE = 10

BLACK = (000, 000, 000)
WHITE = (255, 255, 255)

BLOCKS = [
	(160, 160),
	(170, 170),
	(160, 170),
]

def get_sprite_from(image_file):
	SPRITES = {
		"player_left":  spritesheet.spritesheet(image_file).image_at(( 0,  0, 10, 10), colorkey = 0),
		"player_up":    spritesheet.spritesheet(image_file).image_at((10,  0, 10, 10), colorkey = 0),
		"player_right": spritesheet.spritesheet(image_file).image_at((20,  0, 10, 10), colorkey = 0),
		"player_down":  spritesheet.spritesheet(image_file).image_at((30,  0, 10, 10), colorkey = 0),
		"block":        spritesheet.spritesheet(image_file).image_at((40,  0, 10, 10), colorkey = 0),
	}
	return SPRITES

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	# pygame.display.set_icon(pygame.image.load(".png")) TODO
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	pygame.display.set_caption("Title")
	BASICFONT = font_manager.get_font_from("font.png") # This is a dictionary whose keys are characters
													   # and whose values are sprites of those characters.
	while True:
		runGame()

def place_free(targetx, targety):
	for block in BLOCKS:
		if block == (targetx, targety):
			return False
	return True

def runGame():
	camerax          = 0 # x-coordinate of the center of the camera
	cameray          = 0 # y-coordinate of the center of the camera
	playerx          = WINWIDTH/2 # x-coordinate of the player
	playery          = WINHEIGHT/2 # y-coordinate of the player
	targetx          = playerx # x-coordinate of the destination
	targety          = playery # y-coordinate of the destination
	moving           = False
	move_delay       = 4 # Number of frames to wait before moving. If you tap, you don't move; you have to hold to move.
	move_delay_count = 0
	player_sprite    = "player_left"

	while True:
		# current_time = FPSCLOCK.get_time()
		DISPLAYSURF.fill(WHITE)
		DISPLAYSURF.blit(get_sprite_from("spritesheet.png")[player_sprite], (playerx,playery))
		for block in BLOCKS:
			DISPLAYSURF.blit(get_sprite_from("spritesheet.png")["block"], block)
		font_manager.write_message(DISPLAYSURF, BASICFONT, "Test. TEST. 01234. \\□\\\\", 160, 320)

		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()

		keys = pygame.key.get_pressed()

		if keys[K_UP] and not moving:
			player_sprite = "player_up"
			move_delay_count += 1
			if move_delay_count >= move_delay and place_free(playerx, playery - GRIDSIZE):
				moving = True
				targety -= GRIDSIZE
		if keys[K_DOWN] and not moving:
			player_sprite = "player_down"
			move_delay_count += 1
			if move_delay_count >= move_delay and place_free(playerx, playery + GRIDSIZE):
				moving = True
				targety += GRIDSIZE
		if keys[K_LEFT] and not moving:
			player_sprite = "player_left"
			move_delay_count += 1
			if move_delay_count >= move_delay and place_free(playerx - GRIDSIZE, playery):
				moving = True
				targetx -= GRIDSIZE
		if keys[K_RIGHT] and not moving:
			player_sprite = "player_right"
			move_delay_count += 1
			if move_delay_count >= move_delay and place_free(playerx + GRIDSIZE, playery):
				moving = True
				targetx += GRIDSIZE

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