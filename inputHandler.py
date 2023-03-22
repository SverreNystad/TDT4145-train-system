def isSQLInjection(userInput: str) -> bool:
	# Check if the user input contains SQL injection
	if (userInput.find(";") != -1):
		return True
	if (userInput.find("--") != -1):
		return True
	if (userInput.find("\"") != -1):
		return True
	if (userInput.find("\'") != -1):
		return True
	if (userInput.find("/*") != -1):
		return True

def inputSQLData(message: str) -> str:
	userInput: str = input(message)
	if isSQLInjection(userInput):
		print("Possible SQL Injection detected")
		print("Please do not do this again :)")
		return ""
	else:
		return userInput

def convertSpecialCharacters(userInput: str) -> str:
	userInput = userInput.replace("ø", "oe")
	userInput = userInput.replace("æ", "ae")
	userInput = userInput.replace("å", "aa")
	return userInput

def previewWithSpecialCharacters(userInput: str) -> str:
	userInput = userInput.replace("oe", "ø")
	userInput = userInput.replace("ae", "æ")
	userInput = userInput.replace("aa", "å")
	return userInput

def convertStationName(stationName: str) -> str:
	# Convert the station name to a format that can be used in SQL
	convertedStationName: str = stationName[0].upper() + stationName[1:].lower()
	return convertedStationName

def isEnglishWeekDay(weekday: str) -> bool:
	# Check if the weekday is in english
	weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	return weekday in weekdays

def translateWeekDayToNorwegian(weekday: str) -> str:
	# Translate the weekday to norwegian
	weekdays = {
		"Monday": "Mandag",
		"Tuesday": "Tirsdag",
		"Wednesday": "Onsdag",
		"Thursday": "Torsdag",
		"Friday": "Fredag",
		"Saturday": "Lørdag",
		"Sunday": "Søndag"
	}
	return weekdays[weekday]

def dayAfterTomorrow(day):
	# Get the day after
	weekdays =	{
	"Mandag": "Tirsdag",
	"Tirsdag": "Onsdag",
	"Onsdag": "Torsdag",
	"Torsdag": "Fredag",
	"Fredag": "Lørdag",
	"Lørdag": "Søndag",
	"Søndag": "Mandag"
	}
	return weekdays[day]