import pygame

from pygame.locals import *

import global_constants as gc


class Entity:
	def __init__(
		self,
		name,
		x,
		y,
		list_of_messages,
		schedule,
	):
		self.name             = name
		self.x                = x
		self.y                = y
		self.list_of_messages = list_of_messages
		self.schedule         = schedule

	def start_conversation(self, dialog_box):
		keys = pygame.key.get_pressed()

		dialog_box.speaker = self.name
		dialog_box.message = self.list_of_messages[0]

		if keys[K_z] and dialog_box.ready_for_input:
		 	dialog_box.continue_inputted = True
		if keys[K_BACKSPACE]:
		 	dialog_box.turn_off()


guy1 = Entity(
	name = "Guy1", 
	x = 0, 
	y = 20,
	list_of_messages = [
		"Hello. This is message 1.",
		"Welcome back. This is message 2.",
		"Now this is message 3.",
	],
	schedule = None,
)
guy2 = Entity(
	name = "Guy2", 
	x = -20, 
	y = -10,
	list_of_messages = [
		"This is guy2.",
	],
	schedule = None,
)

LIST_OF_ENTITIES = [
	guy1,
	guy2,
]