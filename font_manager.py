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

def break_message_to_fit_textbox(message, width):
	"""Input a message and the width (in pixels) of the dialog box.
	Outputs a list of text lines that will fit in that width."""
	list_of_lines = []
	list_of_words = message.split()
	for i, word in enumerate(list_of_words):
		list_of_words[i] = word + " "
	current_line = ""
	while list_of_words != []:
		if len(current_line) + len(list_of_words[0]) < width/g.GRIDSIZE - 2:
			current_line += list_of_words[0]
			del list_of_words[0]
		else:
			list_of_lines.append(current_line)
			current_line = ""
	list_of_lines.append(current_line)
	return list_of_lines

def buffer_text(message, frames_between_letters, text_counter, message_done, width):
	if text_counter <= frames_between_letters * len(message) and not message_done:
		buffer_message = message[0:text_counter//frames_between_letters]
		text_counter += 1
	else:
		message_done = True
		text_counter = 0
		buffer_message = message
	return buffer_message, text_counter, message_done

def draw_dialog_box(DISPLAYSURF, BASICFONT, \
	topleftx, toplefty, \
	width, height, \
	message, frames_between_letters, text_counter, message_done):

	# Draw the background of the box.
	pygame.draw.rect(DISPLAYSURF, g.WHITE, (topleftx, toplefty, width, height+g.GRIDSIZE))

	# Draw the four corners of the frame.
	write_message(DISPLAYSURF, BASICFONT, "╔", x=topleftx,                  y=toplefty)
	write_message(DISPLAYSURF, BASICFONT, "╗", x=topleftx+width-g.GRIDSIZE, y=toplefty)
	write_message(DISPLAYSURF, BASICFONT, "╚", x=topleftx,                  y=toplefty+height)
	write_message(DISPLAYSURF, BASICFONT, "╝", x=topleftx+width-g.GRIDSIZE, y=toplefty+height)

	# Draw the top and bottom of the frame.
	for gridx in range(width//g.GRIDSIZE-2):
		write_message(DISPLAYSURF, BASICFONT, "═", x=topleftx+(gridx+1)*g.GRIDSIZE, y=toplefty)
		write_message(DISPLAYSURF, BASICFONT, "═", x=topleftx+(gridx+1)*g.GRIDSIZE, y=toplefty+height)

	# Draw the sides of the frame.
	for gridy in range(height//g.GRIDSIZE-1):
		write_message(DISPLAYSURF, BASICFONT, "║", x=topleftx,                  y=toplefty+(gridy+1)*g.GRIDSIZE)
		write_message(DISPLAYSURF, BASICFONT, "║", x=topleftx+width-g.GRIDSIZE, y=toplefty+(gridy+1)*g.GRIDSIZE)

	# Draw the text.
	line_counter = 1
	list_of_lines = break_message_to_fit_textbox(message, width)
	buffer_message, text_counter, message_done = buffer_text(list_of_lines[line_counter-1], frames_between_letters, text_counter, message_done, width)
	write_message(DISPLAYSURF, BASICFONT, buffer_message, x=topleftx+g.GRIDSIZE, y=toplefty+g.GRIDSIZE*line_counter)
	if message_done:
		line_counter += 1
		message_done = False
	return text_counter, message_done

def get_font_from(image_file):
	CHARACTERS = {}
	for i, char in enumerate(CHARACTER_LIST):
		column = i % COLUMNS
		row = i // COLUMNS
		CHARACTERS[char] = spritesheet.spritesheet(image_file).image_at(
			(column*CHARACTER_WIDTH, row*CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT),
			colorkey = -1
		)
	return CHARACTERS



def write_message(DISPLAYSURF, CHARACTERS, message, x, y):
	"""Input a character dictionary, a message, and a coordinate (x,y).
	Outputs the message drawn in the character set starting at the specified coordinate."""
	list_of_letters = [letter for letter in message]
	letter_count = 0
	for letter in list_of_letters:
		DISPLAYSURF.blit(CHARACTERS[letter], (x + letter_count*CHARACTER_WIDTH, y))
		letter_count += 1

