import pygame

import global_constants as g
import spritesheet

# The image file for the font is 160x160 pixels and contains 
# 16 characters per row, and 16 columns.
IMAGE_WIDTH, IMAGE_HEIGHT = 160, 160
COLUMNS, ROWS = 16, 16
CHARACTER_WIDTH, CHARACTER_HEIGHT = int(IMAGE_WIDTH / COLUMNS), int(IMAGE_HEIGHT / ROWS)
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
																					 # but this matches the image file.
]


class DialogBox:
	def __init__(
			self, 
			DISPLAYSURF = None,
		):
		self.text_counter 			= 0
		self.frames_between_letters = 1 # Make this value larger to cause text to write more slowly.
		self.message_done 			= False
		self.message 				= None
		self.CHARACTERS 			= self.get_font_from("font.png")
		self.DISPLAYSURF 			= DISPLAYSURF
		self.topleftx 				= 0
		self.toplefty 				= g.WINHEIGHT - 6*g.GRIDSIZE
		self.width 					= g.WINWIDTH
		self.height 				= 5*g.GRIDSIZE
		self.list_of_lines          = []
		self.buffer_message         = ""

	def break_message_to_fit_textbox(self):
		"""Input a message and the width (in pixels) of the dialog box.
		Outputs a list of text lines that will fit in that width."""
		list_of_words = self.message.split()
		for i, word in enumerate(list_of_words):
			list_of_words[i] = word + " "
		current_line = ""
		while list_of_words != []:
			if len(current_line) + len(list_of_words[0]) < self.width/g.GRIDSIZE - 2:
				current_line += list_of_words[0]
				del list_of_words[0]
			else:
				self.list_of_lines.append(current_line)
				current_line = ""
		self.list_of_lines.append(current_line)

	def buffer_text(self, line):
		if self.text_counter <= self.frames_between_letters * len(line) and not self.message_done:
			self.buffer_message = line[0:self.text_counter//self.frames_between_letters]
			self.text_counter += 1
		else:
			self.message_done = True
			self.text_counter = 0
			self.buffer_message = line
		return line

	def draw_dialog_box(self):
		# Draw the background of the box.
		pygame.draw.rect(self.DISPLAYSURF, g.WHITE, (self.topleftx, self.toplefty, self.width, self.height+g.GRIDSIZE))

		# Draw the four corners of the frame.
		self.write_message(input_message="╔", x=self.topleftx,                       y=self.toplefty)
		self.write_message(input_message="╗", x=self.topleftx+self.width-g.GRIDSIZE, y=self.toplefty)
		self.write_message(input_message="╚", x=self.topleftx,                       y=self.toplefty+self.height)
		self.write_message(input_message="╝", x=self.topleftx+self.width-g.GRIDSIZE, y=self.toplefty+self.height)

		# Draw the top and bottom of the frame.
		for gridx in range(self.width//g.GRIDSIZE-2):
			self.write_message(input_message="═", x=self.topleftx+(gridx+1)*g.GRIDSIZE, y=self.toplefty)
			self.write_message(input_message="═", x=self.topleftx+(gridx+1)*g.GRIDSIZE, y=self.toplefty+self.height)

		# Draw the sides of the frame.
		for gridy in range(self.height//g.GRIDSIZE-1):
			self.write_message(input_message="║", x=self.topleftx,                       y=self.toplefty+(gridy+1)*g.GRIDSIZE)
			self.write_message(input_message="║", x=self.topleftx+self.width-g.GRIDSIZE, y=self.toplefty+(gridy+1)*g.GRIDSIZE)

		# Draw the text.
		line_counter = 1
		self.break_message_to_fit_textbox()
		line = self.buffer_text(self.list_of_lines[0])
		self.write_message(line, x=self.topleftx+g.GRIDSIZE, y=self.toplefty+g.GRIDSIZE*line_counter)
		if self.message_done:
			line_counter += 1
			self.message_done = False

	def get_font_from(self, image_file):
		CHARACTERS = {}
		for i, char in enumerate(CHARACTER_LIST):
			column = i % COLUMNS
			row = i // COLUMNS
			CHARACTERS[char] = spritesheet.spritesheet(image_file).image_at(
				(column*CHARACTER_WIDTH, row*CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT),
				colorkey = -1
			)
		return CHARACTERS

	def write_message(self, input_message, x, y):
		"""Input a character dictionary, a message, and a coordinate (x,y).
		Outputs the message drawn in the character set starting at the specified coordinate."""
		list_of_letters = [letter for letter in input_message]
		letter_count = 0
		for letter in list_of_letters:
			self.DISPLAYSURF.blit(self.CHARACTERS[letter], (x + letter_count*CHARACTER_WIDTH, y))
			letter_count += 1







