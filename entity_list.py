import entities as en

# dict_of_messages is formatted as follows:
#	{
# 		key: ["message", "option1", targetkey1, "option2", targetkey2, ... ],
#	}

guy1 = en.Entity(
	name = "Guy1", 
	x = 0, 
	y = 20,
	dict_of_messages = {
		0: ["Hello. This is message 0.", 1],
		1: ["Welcome back. This is message 1.", 2],
		2: ["Now this is message 2.", 0],
	},
	message_index = 0,
	schedule = None,
	in_conversation = False
)
guy2 = en.Entity(
	name = "Guy2", 
	x = -20, 
	y = -10,
	dict_of_messages = {
		0: ["This is message 0.", 2],
		1: ["This is message 1.", 0],
		2: ["We skipped to message 2. You'll go to 1 next.", 1],
	},
	message_index = 0,
	schedule = None,
	in_conversation = False
)
guy3 = en.Entity(
	name = "Guy3", 
	x = 0, 
	y = -30,
	dict_of_messages = {
		0: ["Yes or No?", "Yes.", 1, "No.", 2],
		1: ["You said yes.", 0],
		2: ["You said no.", 0],
	},
	message_index = 0,
	schedule = None,
	in_conversation = False
)

LIST_OF_ENTITIES = [
	guy1,
	guy2,
	guy3,
]