import pygame
import sys
from pygame.locals import *

import font_manager
import global_constants as g
import spritesheet

BLOCKS = [
	(10, 10),
	(20, 20),
	(10, 20),
	(10, 30),
	(10, 40),
	(10, 50),
	(10, 60),
	(10, 70),
	(10, 80),
	(10, 90),
]



def camera_controller(DISPLAYSURF, object, objectx, objecty, camerax, cameray):
	DISPLAYSURF.blit(object, (objectx-camerax+g.HALFWINWIDTH, objecty-cameray+g.HALFWINHEIGHT))

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
	DISPLAYSURF = pygame.display.set_mode((g.WINWIDTH, g.WINHEIGHT), SCALED)
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
	playerx          = 0 # x-coordinate of the player
	playery          = 0 # y-coordinate of the player
	targetx          = playerx # x-coordinate of the destination when you start walking
	targety          = playery # y-coordinate of the destination when you start walking
	moving           = False
	move_delay       = 4 # Number of frames to wait before moving. If you tap, you don't move; you have to hold to move.
	move_delay_count = 0
	player_sprite    = "player_left"

	text_counter = 0
	frames_between_letters = 1 # Make this value larger to cause text to write more slowly.
	message_done = False
	message = None

	while True:
		# current_time = FPSCLOCK.get_time()
		camerax = playerx # x-coordinate of the center of the camera
		cameray = playery # y-coordinate of the center of the camera
		DISPLAYSURF.fill(g.WHITE)
		camera_controller(DISPLAYSURF, get_sprite_from("spritesheet.png")[player_sprite], playerx, playery, camerax, cameray)
		for block in BLOCKS:
			camera_controller(DISPLAYSURF, get_sprite_from("spritesheet.png")["block"], block[0], block[1],camerax, cameray)

		if message is not None:
			text_counter, message_done = font_manager.draw_dialog_box(DISPLAYSURF, BASICFONT, \
																	 0, g.WINHEIGHT - 6*g.GRIDSIZE, \
																	 g.WINWIDTH, 5*g.GRIDSIZE, \
																	 message, frames_between_letters, \
																	 text_counter, message_done)

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
			if move_delay_count >= move_delay and place_free(playerx, playery - g.GRIDSIZE):
				moving = True
				targety -= g.GRIDSIZE
		if keys[K_DOWN] and not moving:
			player_sprite = "player_down"
			move_delay_count += 1
			if move_delay_count >= move_delay and place_free(playerx, playery + g.GRIDSIZE):
				moving = True
				targety += g.GRIDSIZE
		if keys[K_LEFT] and not moving:
			player_sprite = "player_left"
			move_delay_count += 1
			if move_delay_count >= move_delay and place_free(playerx - g.GRIDSIZE, playery):
				moving = True
				targetx -= g.GRIDSIZE
		if keys[K_RIGHT] and not moving:
			player_sprite = "player_right"
			move_delay_count += 1
			if move_delay_count >= move_delay and place_free(playerx + g.GRIDSIZE, playery):
				moving = True
				targetx += g.GRIDSIZE
		# Testing
		if keys[K_z]:
			message = "□ Test. TEST. ☺ 01234. \\□\\\\ klwjer lkwjert kljsl* fat ajshdflkjasdkfjaslkdjf dfhasd test test 12345"
		if not keys[K_z]:
			message = None
			text_counter = 0
			message_done = False


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
		FPSCLOCK.tick(g.FPS)

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()