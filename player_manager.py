import pygame
from pygame.locals import *

import global_constants as gc
import text_manager as tm
import world_map as wm


class Player:
	def __init__(
			self,
			DISPLAYSURF,
			SPRITESHEET,
		):
		self.DISPLAYSURF      = DISPLAYSURF
		self.x 	 			  = 0 # x-coordinate of the player
		self.y  			  = 0 # y-coordinate of the player
		self.targetx   		  = self.x # x-coordinate of the destination when you start walking
		self.targety  		  = self.y # y-coordinate of the destination when you start walking
		self.moving    		  = False
		self.MOVE_DELAY_CONST = gc.FPS // 30 # Syntactic sugar; see move_delay.
		self.move_delay       = 4 * self.MOVE_DELAY_CONST # Number of frames to wait before moving. 
										   	   			  # If you tap, you don't move; you have to hold to move.
							 			       			  # It felt good when move_delay was 4 at 30 FPS, so the 
							 				   			  # offset ensures that no matter what gc.FPS is, 
							 			   	   			  # the move_delay is about the same.
		self.move_delay_count = 0
		self.SPRITESHEET      = SPRITESHEET
		self.sprite   		  = self.SPRITESHEET["player_down"]
		self.direction        = "down"

	def adjacent_obstruction(self):
		"""This function is syntactic sugar to run self.return_obstruction()
		on the grid cell adjacent to you in the direction you're facing."""
		match self.direction:
			case "up":
				return self.return_obstruction(self.x, self.y - gc.GRIDSIZE)
			case "down":
				return self.return_obstruction(self.x, self.y + gc.GRIDSIZE)
			case "left":
				return self.return_obstruction(self.x - gc.GRIDSIZE, self.y)
			case "right":
				return self.return_obstruction(self.x + gc.GRIDSIZE, self.y)

	def get_sprite(self):
		match self.direction:
			case "up":
				self.sprite = self.SPRITESHEET["player_up"]
			case "down":
				self.sprite = self.SPRITESHEET["player_down"]
			case "left":
				self.sprite = self.SPRITESHEET["player_left"]
			case "right":
				self.sprite = self.SPRITESHEET["player_right"]

	def movement(self):
		keys = pygame.key.get_pressed()

		if keys[K_UP] and not self.moving:
			self.direction = "up"
			self.move_delay_count += 1
			if self.move_delay_count >= self.move_delay \
			and self.adjacent_obstruction() is None:
				self.moving = True
				self.targety -= gc.GRIDSIZE
		if keys[K_DOWN] and not self.moving:
			self.direction = "down"
			self.move_delay_count += 1
			if self.move_delay_count >= self.move_delay \
			and self.adjacent_obstruction() is None:
				self.moving = True
				self.targety += gc.GRIDSIZE
		if keys[K_LEFT] and not self.moving:
			self.direction = "left"
			self.move_delay_count += 1
			if self.move_delay_count >= self.move_delay \
			and self.adjacent_obstruction() is None:
				self.moving = True
				self.targetx -= gc.GRIDSIZE
		if keys[K_RIGHT] and not self.moving:
			self.direction = "right"
			self.move_delay_count += 1
			if self.move_delay_count >= self.move_delay \
			and self.adjacent_obstruction() is None:
				self.moving = True
				self.targetx += gc.GRIDSIZE

		if self.targetx > self.x: # Target to the right
			self.x += 2 
		if self.targetx < self.x: # Target to the left
			self.x -= 2
		if self.targety > self.y: # Target below
			self.y += 2 
		if self.targety < self.y: # Target above
			self.y -= 2

		if not (keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]):
			self.move_delay_count = 0

		if self.moving and self.targetx == self.x and self.targety == self.y:
			self.moving = False

	def return_obstruction(self, x, y):
		"""Input a coordinate. 
		Output the name of an obstruction as a string.
		If there is none, return None."""
		for block in wm.BLOCKS:
			if block == (x, y):
				return "block"
		for thing in wm.THINGS_TO_TALK_TO:
			if thing == (x, y):
				return "thing"
		return None

	def run(self):
		self.get_sprite()
		self.movement()

	def start_conversation(self, dialog_box):
		keys = pygame.key.get_pressed()
		
		if self.adjacent_obstruction() == "thing":
			dialog_box.message = "□ Test. TEST. ☺ 01234. \\□\\\\ klwjer lkwjert \
				kljsl* fas ajshdflkjasdkfjaslkdjf dfhasds \
				test test 12345 TEST TEST THE QUICK BROWN FOX \
				JUMPED OVER THE LAZY DOG is this too long to \
				fit? Hooray now it works just fine. I am the \
				best. It even wraps across more than two \
				pages -- see watch this fjskaljdfj \
				jskafjklfjskl adjlk fjkljlkasdf jsadf test \
				ajksfdhjh fsd afhsadh f saf sdf asd fsdf sadf \
				blah blah bhlahas lsdfjasi \
				ajshdflkjasdkfjaslkdjf"
		if keys[K_z] and dialog_box.ready_for_input:
		 	dialog_box.continue_inputted = True
		if keys[K_BACKSPACE]:
		 	dialog_box.turn_off()