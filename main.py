import pygame
import sys
from pygame.locals import *

import global_constants as gc
import player_manager as pm
import spritesheet as ss
import text_manager as tm
import world_map as wm


def camera_controller(DISPLAYSURF, object, objectx, objecty, camerax, cameray):
	DISPLAYSURF.blit(object, (objectx-camerax+gc.HALFWINWIDTH, objecty-cameray+gc.HALFWINHEIGHT))

def get_sprite_from(image_file):
	SPRITESHEET = {
		"player_left":  ss.spritesheet(image_file).image_at(( 0,  0, 10, 10), colorkey = 0),
		"player_up":    ss.spritesheet(image_file).image_at((10,  0, 10, 10), colorkey = 0),
		"player_right": ss.spritesheet(image_file).image_at((20,  0, 10, 10), colorkey = 0),
		"player_down":  ss.spritesheet(image_file).image_at((30,  0, 10, 10), colorkey = 0),
		"block":        ss.spritesheet(image_file).image_at((40,  0, 10, 10), colorkey = 0),
		"test_thing":   ss.spritesheet(image_file).image_at((50,  0, 10, 10), colorkey = 0),
	}
	return SPRITESHEET

def main():
	global FPSCLOCK, DISPLAYSURF # These can't go in global_constants because you need to pygame.init() first.
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	# pygame.display.set_icon(pygame.image.load(".png")) TODO
	DISPLAYSURF = pygame.display.set_mode((gc.WINWIDTH, gc.WINHEIGHT), SCALED)
	pygame.display.set_caption("Title")

	while True:
		run_game()

def run_game():
	player = pm.Player(
		DISPLAYSURF = DISPLAYSURF,
		SPRITESHEET = get_sprite_from("spritesheet.png"),
	)
	dialog_box = tm.DialogBox(
		DISPLAYSURF = DISPLAYSURF,
	)

	while True:
		# current_time = FPSCLOCK.get_time()
		camerax, cameray = player.x, player.y 
		DISPLAYSURF.fill(gc.BLACK)
		for block in wm.BLOCKS:
			camera_controller(
				DISPLAYSURF, \
				get_sprite_from("spritesheet.png")["block"], \
				block[0], block[1],\
				camerax, cameray
			)
		for thing in wm.THINGS_TO_TALK_TO:
			camera_controller(
				DISPLAYSURF, \
				get_sprite_from("spritesheet.png")["test_thing"], \
				thing[0], thing[1], \
				camerax, cameray
			)
		camera_controller( # Draw the player last so it's always on top.
			DISPLAYSURF, \
			player.sprite, \
			player.x, player.y, \
			camerax, cameray
		)

		player.run()
		dialog_box.run()

		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()
				if event.key == K_z:
					player.start_conversation(dialog_box = dialog_box)

		pygame.display.update()
		FPSCLOCK.tick(gc.FPS)

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()