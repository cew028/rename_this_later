import pygame

from pygame.locals import *

import global_constants as gc


class Entity:
	def __init__(
		self,
		name,
		x,
		y,
		dict_of_messages,
		message_index,
		schedule,
		in_conversation,
	):
		self.name             = name
		self.x                = x
		self.y                = y
		self.dict_of_messages = dict_of_messages
		self.message_index    = message_index
		self.schedule         = schedule
		self.in_conversation  = in_conversation

	# Syntactic sugars:
	def change_message_index_to(self, choice):
		self.message_index = choice
	def is_question(self):
		return isinstance(self.dict_of_messages[self.message_index][1], int)
	def list_of_choices(self):
		number_of_choices = self.number_of_choices()
		copy_list = self.dict_of_messages[self.message_index].copy()
		del copy_list[0] # Delete the question.
		i = 1
		while len(copy_list) > number_of_choices:
			del copy_list[i] # Deletes the targetkeys.
			i += 1
		return copy_list
	def message(self):
		return self.dict_of_messages[self.message_index][0]
	def next_message(self):
		self.change_message_index_to(self.dict_of_messages[self.message_index][1])
	def number_of_choices(self):
		return (len(self.dict_of_messages[self.message_index]) - 1) // 2 

	def generate_next_message(self, dialog_box):
		if self.is_question(): # The current message was not a question to the player.
			self.next_message()
		else: # It was a question; let's build the multiple choice.
			print(self.list_of_choices())


	def start_conversation(self, dialog_box):
		self.in_conversation = True

		dialog_box.speaker = self.name
		dialog_box.message = self.message()
		self.generate_next_message(dialog_box)