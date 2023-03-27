import entity_list as el

FLAGS = {
	# flag: True/False,
	"test_flag": False,
	"test_clock_flag": False,
	"test_loc_flag": False,
}

class Flagger:
	def __init__(
		self,
		clock,
		player,
	):
		self.clock  = clock
		self.player = player

	def location_triggered_flags(self):
		# Note that this function updates flags based on where the player is.
		# Since the player is the one that instigates dialog and other effects
		# that require flags, this should not be an issue. (E.g., a flag that
		# triggers because an NPC is in a certain place can be coded to trigger
		# when the player is in that place, since the effect depends on the player
		# being able to talk to the NPC, and thus the NPC is there too.)
		if self.player.x == -60 and self.player.y == -70:
			FLAGS["test_loc_flag"] = True
		else:
			FLAGS["test_loc_flag"] = False

	def run(self):
		for entity in el.LIST_OF_ENTITIES:
			entity.update_from_flags()
		self.time_triggered_flags()
		self.location_triggered_flags()

	def time_triggered_flags(self):
		if self.clock.current_minute > 30:
			FLAGS["test_clock_flag"] = True
		else:
			FLAGS["test_clock_flag"] = False