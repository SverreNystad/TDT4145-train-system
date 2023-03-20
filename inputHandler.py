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
	if (userInput.lower().find("select") != -1 or userInput.lower().find("drop") != -1 or userInput.lower().find("from") != -1):
		return True

def inputSQLData(message: str) -> str:
	userInput: str = input(message)
	if isSQLInjection(userInput):
		print("Possible SQL Injection detected")
		print("Please do not do this again :)")
		return ""
	else:
		return userInput
