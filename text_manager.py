import pygame

import global_constants as gc
import spritesheet as ss

# The image file for the font is 160x160 pixels and contains 
# 16 characters per row, and 16 columns.
IMAGE_WIDTH, IMAGE_HEIGHT = 160, 160
COLUMNS, ROWS = 16, 16
CHARACTER_WIDTH, CHARACTER_HEIGHT = int(IMAGE_WIDTH / COLUMNS), int(IMAGE_HEIGHT / ROWS)
# CHARACTER_WIDTH and CHARACTER_HEIGHT really should be the same as gc.GRIDSIZE. 
# If that ever changes things may need refactoring.

# These are the characters from code page 437: https://en.wikipedia.org/wiki/Code_page_437
CHARACTER_LIST = [ 
	 "", "☺", "☻", "♥", "♦", "♣", "♠", "•", "◘", "○", "◙", "♂", "♀", "♪", "♫", "☼", # Using "" for the NUL character.
	"►", "◄", "↕", "‼", "¶", "§", "▬", "↨", "↑", "↓", "→", "←", "∟", "↔", "▲", "▼",
	" ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
	"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
	"@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
	"P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", # Need to escape \
	"`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
	"p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "⌂",
	"Ç", "ü", "é", "â", "ä", "à", "å", "ç", "ê", "ë", "è", "ï", "î", "ì", "Ä", "Å",
	"É", "æ", "Æ", "ô", "ö", "ò", "û", "ù", "ÿ", "Ö", "Ü", "¢", "£", "¥", "₧", "ƒ",
	"á", "í", "ó", "ú", "ñ", "Ñ", "ª", "º", "¿", "⌐", "¬", "½", "¼", "¡", "«", "»",
	"░", "▒", "▓", "│", "┤", "╡", "╢", "╖", "╕", "╣", "║", "╗", "╝", "╜", "╛", "┐",
	"└", "┴", "┬", "├", "─", "┼", "╞", "╟", "╚", "╔", "╩", "╦", "╠", "═", "╬", "╧",
	"╨", "╤", "╥", "╙", "╘", "╒", "╓", "╫", "╪", "┘", "┌", "█", "▄", "▌", "▐", "▀",
	"α", "ß", "Γ", "π", "Σ", "σ", "µ", "τ", "Φ", "Θ", "Ω", "δ", "∞", "φ", "ε", "∩",
	"≡", "±", "≥", "≤", "⌠", "⌡", "÷", "≈", "°", "∙", "·", "√", "ⁿ", "²", "■", "□",  # □ is supposed to be a non-
																					 # breaking space in code 437, 
																					 # but □ matches the image file.
]


class DialogBox:
	def __init__(
			self, 
			DISPLAYSURF = None,
		):
		self.text_counter 			= 0
		self.frames_between_letters = 1 # Make this value larger to write more slowly.
		self.message_done 			= False
		self.line_done              = False
		self.message 				= None
		self.CHARACTERS 			= self.get_font_from("font.png")
		self.DISPLAYSURF 			= DISPLAYSURF
		self.topleftx 				= 0
		self.toplefty 				= gc.WINHEIGHT - 6*gc.GRIDSIZE
		self.width 					= gc.WINWIDTH
		self.height 				= 5*gc.GRIDSIZE
		self.list_of_lines          = []
		self.line_counter           = 0
		self.is_too_short           = False
		self.flash_counter          = 0
		self.ready_for_input        = False
		self.continue_inputted      = False

	def break_message_to_fit_box(self):
		"""Takes self.message, splits it into substrings, and
		places those substrings in self.list_of_lines, where
		the substrings are short enough to fit in the dialog box."""
		list_of_words = self.message.split()
		for i, word in enumerate(list_of_words):
			list_of_words[i] = word + " "
		current_line = ""
		while list_of_words != []:
			if len(current_line) + len(list_of_words[0]) <= self.width/gc.GRIDSIZE - 2:
				current_line += list_of_words[0]
				del list_of_words[0]
			else:
				self.list_of_lines.append(current_line)
				current_line = ""
		self.list_of_lines.append(current_line)

	def buffer_text(self, line):
		if (
			self.text_counter <= self.frames_between_letters * len(line) \
			and not self.line_done \
			and not self.message_done
		):
			buffer_message = line[0:self.text_counter//self.frames_between_letters]
			self.text_counter += 1
		else:
			self.line_done = True
			self.text_counter = 0
			buffer_message = line
		return buffer_message

	def check_if_box_is_too_short(self):
		if len(self.list_of_lines) >= self.height//gc.GRIDSIZE:
			self.is_too_short = True

	def draw_dialog_box(self):
		self.draw_dialog_frame()
		self.draw_dialog_text()

	def draw_dialog_frame(self):
		# Draw the background of the box.
		pygame.draw.rect(
			self.DISPLAYSURF, gc.WHITE, \
			(self.topleftx, self.toplefty, self.width, self.height+gc.GRIDSIZE)
		)

		# Draw the four corners of the frame.
		self.write_message(
			input_message="╔", x=self.topleftx, y=self.toplefty
		)
		self.write_message(
			input_message="╗", x=self.topleftx+self.width-gc.GRIDSIZE, y=self.toplefty
		)
		self.write_message(
			input_message="╚", x=self.topleftx, y=self.toplefty+self.height
		)
		self.write_message(
			input_message="╝", x=self.topleftx+self.width-gc.GRIDSIZE, y=self.toplefty+self.height
		)

		# Draw the top and bottom of the frame.
		for gridx in range(self.width//gc.GRIDSIZE-2):
			self.write_message(
				input_message="═", x=self.topleftx+(gridx+1)*gc.GRIDSIZE, y=self.toplefty
			)
			self.write_message(
				input_message="═", x=self.topleftx+(gridx+1)*gc.GRIDSIZE, y=self.toplefty+self.height
			)

		# Draw the sides of the frame.
		for gridy in range(self.height//gc.GRIDSIZE-1):
			self.write_message(
				input_message="║", x=self.topleftx, y=self.toplefty+(gridy+1)*gc.GRIDSIZE
			)
			self.write_message(
				input_message="║", x=self.topleftx+self.width-gc.GRIDSIZE, y=self.toplefty+(gridy+1)*gc.GRIDSIZE
			)

	def draw_dialog_text(self):
		# First we generate the list_of_lines.
		if self.list_of_lines == []:
			self.break_message_to_fit_box() 

		self.check_if_box_is_too_short()

		# Next we typewriter out the lines in list_of_lines, one at a time.
		if self.line_counter < min(len(self.list_of_lines), self.height//gc.GRIDSIZE-1):
			buff = self.buffer_text(self.list_of_lines[self.line_counter])
			self.write_message(
				input_message=buff, x=self.topleftx+gc.GRIDSIZE, y=self.toplefty+gc.GRIDSIZE*(self.line_counter+1)
			)
			if self.line_done and not self.message_done:
				self.line_counter += 1
				self.line_done = False
		else:
			self.message_done = True

		# This code writes the lines that we've already typewritered, so that they don't disappear.
		for line in range(self.line_counter):
			self.write_message(
				input_message=self.list_of_lines[line], x=self.topleftx+gc.GRIDSIZE, y=self.toplefty+gc.GRIDSIZE*(line+1)
			)
		if self.message_done:
			self.waiting_for_input()

	def get_font_from(self, image_file):
		CHARACTERS = {}
		for i, char in enumerate(CHARACTER_LIST):
			column = i % COLUMNS
			row = i // COLUMNS
			CHARACTERS[char] = ss.spritesheet(image_file).image_at(
				(column*CHARACTER_WIDTH, row*CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT),
				colorkey = -1
			)
		return CHARACTERS

	def run(self):
		if self.message is not None:
			self.draw_dialog_box()
		else:
			self.turn_off()

	def turn_off(self):
		self.text_counter  	   = 0
		self.message_done  	   = False
		self.line_done     	   = False
		self.message 	   	   = None
		self.list_of_lines 	   = []
		self.line_counter 	   = 0
		self.is_too_short      = False
		self.flash_counter     = 0
		self.ready_for_input   = False
		self.continue_inputted = False

	def waiting_for_input(self):
		self.ready_for_input = True

		# This value is the number of times per second the "▼" flashes.
		flash_freq_sec = 2

		# This converts flash_freq_sec to a number of frames.
		flash_freq_frames   = gc.FPS // flash_freq_sec 

		# Tick up the counter.
		self.flash_counter += 1 

		# Roll over the counter if you reach flash_freq_frames.
		self.flash_counter  = self.flash_counter % flash_freq_frames 

		if self.flash_counter < flash_freq_frames // 2: # Alternate on/off.
			self.write_message(
				input_message="▼", x=self.topleftx+self.width-gc.GRIDSIZE*2, y=self.toplefty+self.height-gc.GRIDSIZE
			)
		if self.continue_inputted:
			for _ in range(self.height//gc.GRIDSIZE-1):
				if self.list_of_lines != []:
					del self.list_of_lines[0]
					if self.list_of_lines == []:
						self.message = None
				else:
					self.message = None
			self.line_counter = 0
			self.message_done = False
			self.ready_for_input = False
			self.continue_inputted = False

	def write_message(self, input_message, x, y):
		"""Input a message and a coordinate (x,y).
		Outputs the message drawn starting at the specified coordinate."""
		list_of_letters = [letter for letter in input_message]
		letter_count = 0
		for letter in list_of_letters:
			self.DISPLAYSURF.blit(self.CHARACTERS[letter], (x + letter_count*CHARACTER_WIDTH, y))
			letter_count += 1

