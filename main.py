import pygame
import sys
from pygame.locals import *

import clock_manager as cm
import entity_list as el
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
		"test_entity":  ss.spritesheet(image_file).image_at((50,  0, 10, 10), colorkey = 0),
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
	clock = cm.Clock()
	question_box = tm.QuestionBox(
		DISPLAYSURF = DISPLAYSURF,
	)

	while True:
		camerax, cameray = player.x, player.y 
		DISPLAYSURF.fill(gc.BLACK)
		for block in wm.BLOCKS:
			camera_controller(
				DISPLAYSURF, \
				get_sprite_from("spritesheet.png")["block"], \
				block[0], block[1],\
				camerax, cameray
			)
		for entity in el.LIST_OF_ENTITIES:
			camera_controller(
				DISPLAYSURF, \
				get_sprite_from("spritesheet.png")["test_entity"], \
				entity.x, entity.y, \
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
		clock.run()
		question_box.run()
		# print(clock.format_date_and_time())
		# print(en.guy3.list_of_choices()) # For debugging for now.

		if dialog_box.message is not None or question_box.list_of_choices != []:
			player.can_move = False
			clock.can_run   = False
		else:
			player.can_move = True
			clock.can_run   = True
			for entity in el.LIST_OF_ENTITIES:
				entity.in_conversation = False

		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()
				if event.key == gc.A:
					dialog_target = player.attempt_dialog()
					if question_box.list_of_choices != []:
						question_box.make_selection(dialog_target)
					if dialog_target is not None and not dialog_target.in_conversation:
						dialog_target.start_conversation(
							dialog_box = dialog_box,
						)
					if dialog_box.ready_for_input:
						dialog_box.continue_inputted = True
						if len(dialog_box.list_of_lines) < dialog_box.height//gc.GRIDSIZE-1:
							dialog_target.generate_next_message(question_box)
				if event.key == gc.LEFT:
					if question_box.list_of_choices != []:
						question_box.selected_choice -= 1
						question_box.selected_choice = question_box.selected_choice % len(question_box.list_of_choices)
						question_box.list_of_lines = []
				if event.key == gc.RIGHT:
					if question_box.list_of_choices != []:
						question_box.selected_choice += 1
						question_box.selected_choice = question_box.selected_choice % len(question_box.list_of_choices)
						question_box.list_of_lines = []

		pygame.display.update()
		FPSCLOCK.tick(gc.FPS)

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()