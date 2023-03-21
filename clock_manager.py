MINUTES_IN_AN_HOUR = 60
HOURS_IN_A_DAY     = 24
DAYS_IN_A_YEAR     = 365
MINUTES_IN_A_DAY   = MINUTES_IN_AN_HOUR * HOURS_IN_A_DAY
MINUTES_IN_A_YEAR  = MINUTES_IN_A_DAY * DAYS_IN_A_YEAR
HOURS_IN_A_YEAR    = HOURS_IN_A_DAY * DAYS_IN_A_YEAR

DAYS_IN_JAN = 31
DAYS_IN_FEB = 28
DAYS_IN_MAR = 31
DAYS_IN_APR = 30
DAYS_IN_MAY = 31
DAYS_IN_JUN = 30
DAYS_IN_JUL = 31
DAYS_IN_AUG = 31
DAYS_IN_SEP = 30
DAYS_IN_OCT = 31
DAYS_IN_NOV = 30
DAYS_IN_DEC = 31

DAYS_THRU_JAN = DAYS_IN_JAN
DAYS_THRU_FEB = DAYS_THRU_JAN + DAYS_IN_FEB
DAYS_THRU_MAR = DAYS_THRU_FEB + DAYS_IN_MAR
DAYS_THRU_APR = DAYS_THRU_MAR + DAYS_IN_APR
DAYS_THRU_MAY = DAYS_THRU_APR + DAYS_IN_MAY
DAYS_THRU_JUN = DAYS_THRU_MAY + DAYS_IN_JUN
DAYS_THRU_JUL = DAYS_THRU_JUN + DAYS_IN_JUL
DAYS_THRU_AUG = DAYS_THRU_JUL + DAYS_IN_AUG
DAYS_THRU_SEP = DAYS_THRU_AUG + DAYS_IN_SEP
DAYS_THRU_OCT = DAYS_THRU_SEP + DAYS_IN_OCT
DAYS_THRU_NOV = DAYS_THRU_OCT + DAYS_IN_NOV
DAYS_THRU_DEC = DAYS_THRU_NOV + DAYS_IN_DEC


class Clock:
	def __init__(self):
		self.time_counter   = 0 # In minutes. 0 is "12:00 midnight, Jan 1, year 0."
		self.current_year   = 0 # Unbounded.
		self.current_month  = 0 # 0 through 11.
		self.current_day    = 0 # 1 through 365.
		self.current_hour   = 0 # 0 through 23.
		self.current_minute = 0 # 0 through 59.

	def add_minutes(self, minutes):
		self.time_counter += minutes
		self.get_date()
		self.get_time()

	def format_date_and_time(self):
		"""Returns a string of date and time."""
		if self.current_hour <= 9:
			reformatted_hour = "0" + str(self.current_hour)
		else:
			reformatted_hour = str(self.current_hour)
		if self.current_minute <= 9:
			reformatted_minute = "0" + str(self.current_minute)
		else:
			reformatted_minute = str(self.current_minute)

		match self.current_month:
			case 0:
				date = "January " + str(self.current_day)
			case 1:
				date = "February " + str(self.current_day - DAYS_THRU_JAN)
			case 2:
				date = "March " + str(self.current_day - DAYS_THRU_FEB)
			case 3:
				date = "April " + str(self.current_day - DAYS_THRU_MAR)
			case 4:
				date = "May " + str(self.current_day - DAYS_THRU_APR)
			case 5:
				date = "June " + str(self.current_day - DAYS_THRU_MAY)
			case 6:
				date = "July " + str(self.current_day - DAYS_THRU_JUN)
			case 7:
				date = "August " + str(self.current_day - DAYS_THRU_JUL)
			case 8:
				date = "September " + str(self.current_day - DAYS_THRU_AUG)
			case 9:
				date = "October " + str(self.current_day - DAYS_THRU_SEP)
			case 10:
				date = "November " + str(self.current_day - DAYS_THRU_OCT)
			case 11:
				date = "December " + str(self.current_day - DAYS_THRU_NOV)
		return "Year " + str(self.current_year) + ", " + date + ", " + reformatted_hour + ":" + reformatted_minute

	def get_date(self):
		self.current_day  = (self.time_counter // MINUTES_IN_A_DAY) % DAYS_IN_A_YEAR + 1
		self.current_year = (self.time_counter // MINUTES_IN_A_YEAR) % MINUTES_IN_A_YEAR
		if 0 <= self.current_day <= DAYS_THRU_JAN:
			self.current_month = 0
		elif DAYS_THRU_JAN < self.current_day <= DAYS_THRU_FEB:
			self.current_month = 1
		elif DAYS_THRU_FEB < self.current_day <= DAYS_THRU_MAR:
			self.current_month = 2
		elif DAYS_THRU_MAR < self.current_day <= DAYS_THRU_APR:
			self.current_month = 3
		elif DAYS_THRU_APR < self.current_day <= DAYS_THRU_MAY:
			self.current_month = 4
		elif DAYS_THRU_MAY < self.current_day <= DAYS_THRU_JUN:
			self.current_month = 5
		elif DAYS_THRU_JUN < self.current_day <= DAYS_THRU_JUL:
			self.current_month = 6
		elif DAYS_THRU_JUL < self.current_day <= DAYS_THRU_AUG:
			self.current_month = 7
		elif DAYS_THRU_AUG < self.current_day <= DAYS_THRU_SEP:
			self.current_month = 8
		elif DAYS_THRU_SEP < self.current_day <= DAYS_THRU_OCT:
			self.current_month = 9
		elif DAYS_THRU_OCT < self.current_day <= DAYS_THRU_NOV:
			self.current_month = 10
		elif DAYS_THRU_NOV < self.current_day <= DAYS_THRU_DEC:
			self.current_month = 11

	def get_time(self):
		self.current_minute = self.time_counter % MINUTES_IN_AN_HOUR
		self.current_hour   = (self.time_counter // MINUTES_IN_AN_HOUR) % HOURS_IN_A_DAY
	
	