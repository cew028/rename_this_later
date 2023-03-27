import entity_list as el

FLAGS = {
	# flag: True/False,
	"test_flag": False,
	"test_clock_flag": False,
}

class Flagger:
	def __init__(
		self,
		clock,
	):
		self.clock = clock

	def run(self):
		for entity in el.LIST_OF_ENTITIES:
			entity.update_from_flags()
		self.time_triggered_flags()

	def time_triggered_flags(self):
		if self.clock.current_minute > 30:
			FLAGS["test_clock_flag"] = True
		else:
			FLAGS["test_clock_flag"] = False