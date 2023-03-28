import flag_manager as fm


class Entity:
	def __init__(
		self,
		name,
		x,
		y,
		dict_of_messages,
		dict_key,
		flag_dict,
		in_conversation,
		schedule,
	):
		self.name             = name
		self.x                = x
		self.y                = y
		self.dict_of_messages = dict_of_messages
		self.dict_key         = dict_key
		self.flag_dict        = flag_dict
		self.in_conversation  = in_conversation
		self.schedule         = schedule
		self.original_dict    = dict_of_messages.copy()

	# Syntactic sugars:
	def change_dict_key_to(self, key):
		self.dict_key = key
	def convert_choice_back_to_key(self, choice):
		return 2*(choice+1)
	def is_question(self):
		return isinstance(self.dict_of_messages[self.dict_key][0][1], int)
	def list_of_choices(self):
		number_of_choices = self.number_of_choices()
		copy_list = self.dict_of_messages[0][self.dict_key].copy()
		del copy_list[0] # Delete the question.
		i = 1
		while len(copy_list) > number_of_choices:
			del copy_list[i] # Deletes the targetkeys.
			i += 1
		return copy_list
	def message(self):
		return self.dict_of_messages[self.dict_key][0][0]
	def next_message(self):
		self.change_dict_key_to(self.dict_of_messages[self.dict_key][0][1])
	def number_of_choices(self):
		return (len(self.dict_of_messages[0][self.dict_key]) - 1) // 2 
	# Sugars completed.

	def generate_next_message(self, question_box):
		if self.is_question(): # The current message was not a question to the player.
			self.next_message()
		else: # It was a question; let's build the multiple choice.
			question_box.list_of_choices = self.list_of_choices()

	def start_conversation(self, dialog_box):
		self.in_conversation = True

		dialog_box.speaker = self.name
		dialog_box.message = self.message()

		if self.dict_of_messages[self.dict_key][1] is not None: # If this message had a flag
			flag = self.dict_of_messages[self.dict_key][1]
			fm.FLAGS[flag] = True

	def update_from_flags(self):
		for flag in fm.FLAGS:
			if fm.FLAGS[flag] is True and flag in self.flag_dict:
				if self.flag_dict[flag][1] == True: # replace_old is True (i.e., the flag overwrites the old message)
					for pair in self.flag_dict[flag][0]:
						key = pair[0]
						new_dom = pair[1]
						self.dict_of_messages[key] = new_dom
				else: # replace_old is False, so we just add to the current message
					for pair in self.flag_dict[flag][0]:
						key = pair[0]
						new_dom = pair[1]
						for arg in new_dom[0]:
							if arg not in self.dict_of_messages[key][0]:
								self.dict_of_messages[key][0].append(arg)
							
			elif fm.FLAGS[flag] is False and flag in self.flag_dict:
				# Reset only the parts of self.dict_of_messages that were changed by the flag.
				if self.flag_dict[flag][1] == True: # replace_old is True (i.e., the flag overwrote the old message)
					list_of_keys_to_revert = [pair[0] for pair in self.flag_dict[flag][0]]
					for key in list_of_keys_to_revert:
						self.dict_of_messages[key] = self.original_dict[key]
				else: # replace_old is False, so we need to remove the things that were added
					for pair in self.flag_dict[flag][0]:
						key = pair[0]
						new_dom = pair[1]
						for arg in new_dom[0]:
							if arg in self.dict_of_messages[key][0]:
								self.dict_of_messages[key][0].remove(arg)