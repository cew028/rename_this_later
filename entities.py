import pygame

from pygame.locals import *

def start_conversation(player, dialog_box, clock):
	keys = pygame.key.get_pressed()

	match player.adjacent_obstruction():
		case "guy1":
			dialog_box.speaker = "Guy1"
			dialog_box.message = "This is guy1. I want to test how word wrapping affects the clock. \
			So this is a long message. Blah blah blah blah blah blah blah. \
			The quick brown fox jumped over the lazy dog. Here is more text. It will go on for a while. \
			Now it is finishing up. This is the second to last sentence. Finally, this is the last sentence."
		case "guy2":
			dialog_box.speaker = "Guy2 longer name test"
			dialog_box.message = "This is guy2."
	if keys[K_z] and dialog_box.ready_for_input:
	 	dialog_box.continue_inputted = True
	 	clock.add_minutes(10)
	if keys[K_BACKSPACE]:
	 	dialog_box.turn_off()

class Entity:
	def __init__(self):
		pass