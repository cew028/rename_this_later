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
	in_conversation = False,
	schedule = None,
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
	in_conversation = False,
	schedule = None,
)
guy3 = en.Entity(
	name = "Guy3", 
	x = 0, 
	y = -30,
	dict_of_messages = {
		0: ["Yes or No?", "1Yes. 2Yes. 3Yes. 4Yes. 5Yes. 6Yes. 7Yes. 8Yes. 9Yes. 10Yes. 11Yes. 12Yes. 13Yes. 14Yes. 15Yes. 16Yes. 17Yes. 18Yes. 19Yes. 20Yes.\
			1Yes. 2Yes. 3Yes. 4Yes. 5Yes. 6Yes. 7Yes. 8Yes. 9Yes. 10Yes. 11Yes. 12Yes. 13Yes. 14Yes. 15Yes. 16Yes. 17Yes. 18Yes. 19Yes. 20Yes.", 1, "No.", 2],
		1: ["You said yes.", 0],
		2: ["You said no.", 0],
	},
	message_index = 0,
	in_conversation = False,
	schedule = None,
)
guy4 = en.Entity(
	name = "Guy4", 
	x = 30, 
	y = -30,
	dict_of_messages = {
		0: ["Here's a really long message. We want to continue to confirm that wrapping the message across multiple boxes works. This message is quite long. Let's wrap it up. Here is the final sentence of the message.", 1],
		1: ["This one's short.", 0],
	},
	message_index = 0,
	in_conversation = False,
	schedule = None,
)

LIST_OF_ENTITIES = [guy1, guy2, guy3, guy4]