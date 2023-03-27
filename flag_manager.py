import entity_list as el

FLAGS = {
	# flag: True/False,
	"test_flag": False,
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