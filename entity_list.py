import entities as en

# dict_of_messages is formatted as follows:
#	{
# 		key: [["message", "option1", targetkey1, "option2", targetkey2, ... ], flag_triggered_by_this_message],
#	}
# But that's annoying and fiddly so let's auto-format it:

def dom(*args, flag = None,):
	"""Takes the inputs and formats it as per the comment block above.
	It's called 'dom' for 'dict_of_messages'."""
	return [[arg for arg in args], flag]

# flag_dict is formatted as follows:
#	{
#		flag: [[[key1, dom1], [key2, dom2], ... ], replace_old]
#	}
# It's a list of tuples where you intend to replace the keyn with domn when the flag is made true.
# Then its a outer list, where the first entry is that aforementioned list of tuples, and the second
# entry is a boolean, default True, that indicates whether to overwrite the entire key, or just add to
# what's currently in dict_of_messages. Again, let's auto-format that.

def fd(*args, replace_old = True):
	"""Takes the inputs and formats it as per the comment block above.
	It's called 'fd' for 'flag_dict'."""
	return [[[args[i], args[i+1]] for i in range(0, len(args), 2)], replace_old]


guy1 = en.Entity(
	name = "Guy1", 
	x = 0, 
	y = 20,
	dict_of_messages = {
		0: dom("Hello. This is message 0.", 1),
		1: dom("Welcome back. This is message 1.", 2),
		2: dom("Now this is message 2.", 0),
	},
	dict_key = 0,
	flag_dict = {},
	in_conversation = False,
	schedule = None,
)
guy2 = en.Entity(
	name = "Guy2", 
	x = -20, 
	y = -10,
	dict_of_messages = {
		0: dom("This is message 0.", 2),
		1: dom("This is message 1.", 0),
		2: dom("We skipped to message 2. You'll go to 1 next.", 1),
	},
	dict_key = 0,
	flag_dict = {},
	in_conversation = False,
	schedule = None,
)
guy3 = en.Entity(
	name = "Guy3", 
	x = 0, 
	y = -30,
	dict_of_messages = {
		0: dom("Yes or No?", 
			"1Yes. 2Yes. 3Yes. 4Yes. 5Yes. \
			6Yes. 7Yes. 8Yes. 9Yes. 10Yes. \
			11Yes. 12Yes. 13Yes. 14Yes. 15Yes. \
			16Yes. 17Yes. 18Yes. 19Yes. 20Yes.\
			1Yes. 2Yes. 3Yes. 4Yes. 5Yes. \
			6Yes. 7Yes. 8Yes. 9Yes. 10Yes. \
			11Yes. 12Yes. 13Yes. 14Yes. 15Yes. \
			16Yes. 17Yes. 18Yes. 19Yes. 20Yes.", 1, 
			"No.", 2),
		1: dom("You said yes.", 0),
		2: dom("You said no.", 0),
	},
	dict_key = 0,
	flag_dict = {},
	in_conversation = False,
	schedule = None,
)
guy4 = en.Entity(
	name = "Guy4", 
	x = 30, 
	y = -30,
	dict_of_messages = {
		0: dom("Here's a really long message. \
			We want to continue to confirm that wrapping the \
			message across multiple boxes works. This message \
			is quite long. Let's wrap it up. Here is the final \
			sentence of the message.", 1),
		1: dom("This one's short.", 0),
	},
	dict_key = 0,
	flag_dict = {},
	in_conversation = False,
	schedule = None,
)
guy5 = en.Entity(
	name = "Guy5", 
	x = 50, 
	y = 50,
	dict_of_messages = {
		0: dom("You have not talked to my neighbor.", 0),
	},
	dict_key = 0,
	flag_dict = {
		"test_dialog_flag": fd(0, dom("Now you have talked to my neighbor!",0)),
	},
	in_conversation = False,
	schedule = None,
)
guy6 = en.Entity(
	name = "Guy6", 
	x = 60, 
	y = 50,
	dict_of_messages = {
		0: dom("This triggered the flag.", 0, flag="test_dialog_flag"),
	},
	dict_key = 0,
	flag_dict = {},
	in_conversation = False,
	schedule = None,
)
guy7 = en.Entity(
	name = "Guy7", 
	x = 70, 
	y = 50,
	dict_of_messages = {
		0: dom("Did you talk to my neighbor? Yes or no?", "Yes.", 1, "No.", 2),
		1: dom("Liar!", 0),
		2: dom("Well you should.", 0),
	},
	dict_key = 0,
	flag_dict = {
		"test_dialog_flag": fd(
						1, dom("Good!",0), 
						2, dom("My neighbor said you did though. Don't lie!",0),
						),
	},
	in_conversation = False,
	schedule = None,
)
guy8 = en.Entity(
	name = "Guy8", 
	x = 70, 
	y = 70,
	dict_of_messages = {
		0: dom("It's currently the first half of the hour.", 0),
	},
	dict_key = 0,
	flag_dict = {
		"test_clock_flag": fd(
							0, dom("Now it's currently the second half of the hour.", 0),
							),
	},
	in_conversation = False,
	schedule = None,
)
guy9 = en.Entity(
	name = "Guy9", 
	x = -70, 
	y = -70,
	dict_of_messages = {
		0: dom("Talk to me from the east.", 0),
	},
	dict_key = 0,
	flag_dict = {
		"test_loc_flag": fd(
							0, dom("Thank you! You're talking to me from the east, which is what I prefer.", 0),
							),
	},
	in_conversation = False,
	schedule = None,
)
guy10 = en.Entity(
	name = "Guy10", 
	x = -60, 
	y = -80,
	dict_of_messages = {
		0: dom("Multiple choice:", "No flags activated.", 1),
		1: dom("You selected no flag.", 0),
		2: dom("You selected location flag.", 0),
		3: dom("You selected dialog flag.", 0),
		4: dom("You selected clock flag.", 0),
	},
	dict_key = 0,
	flag_dict = {
		"test_loc_flag": fd(
							0, dom("Location flag activated.", 2),
							replace_old = False
							),
		"test_dialog_flag": fd(
							0, dom("Dialog flag activated.", 3),
							replace_old = False
							),
		"test_clock_flag": fd(
							0, dom("Clock flag activated.", 4),
							replace_old = False
							),
	},
	in_conversation = False,
	schedule = None,
)

LIST_OF_ENTITIES = [guy1, guy2, guy3, guy4, guy5, guy6, guy7, guy8, guy9, guy10]