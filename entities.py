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
		message_index,
		schedule,
		in_conversation,
	):
		self.name             = name
		self.x                = x
		self.y                = y
		self.list_of_messages = list_of_messages
		self.message_index    = message_index
		self.schedule         = schedule
		self.in_conversation  = in_conversation

	def change_message_index_to(self, new_index):
		self.message_index = new_index
		if self.message_index >= len(self.list_of_messages):
			self.message_index = self.message_index % len(self.list_of_messages)

	def start_conversation(self, dialog_box):
		self.in_conversation = True

		dialog_box.speaker = self.name
		dialog_box.message = self.list_of_messages[self.message_index]

		self.change_message_index_to(self.message_index + 1)


guy1 = Entity(
	name = "Guy1", 
	x = 0, 
	y = 20,
	list_of_messages = [
		"Hello. This is message 1.",
		"Welcome back. This is message 2.",
		"Now this is message 3.",
	],
	message_index = 0,
	schedule = None,
	in_conversation = False
)
guy2 = Entity(
	name = "Guy2", 
	x = -20, 
	y = -10,
	list_of_messages = [
		"This is guy2.",
	],
	message_index = 0,
	schedule = None,
	in_conversation = False
)

LIST_OF_ENTITIES = [
	guy1,
	guy2,
]