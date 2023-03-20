




from Station import printStations
from TrainRoutes import getAllTrainRutesForTrip, getAllTrainRutesOnDay
from customer import getFutureOrders, login, printFutureOrdersAndTickets, registerCustomerInfo


def main():

	setup()

	isLoggedIn: bool = False
	userID: int

	print("Welcome to the Train App")
	print("Want to see the list of commands? Type 'help'")

	while True:
		userInput: str = input("Enter a command: ")

		if userInput == "help":
			print("=========================================")

			print("Commands: ")
			print("help - displays this message")
			print("exit - exits the app")
			print("stations - lists all stations")
			print("train routes, [weekday], [station] - lists all train routes for a specific station on a specific weekday REQUIRES 2 ARGUMENTS (weekday, station)")
			print("train routes, [date], [start station], [end station] - lists all train routes for a specific date and start and end station REQUIRES 3 ARGUMENTS (date, start station, end station)")
			print("register - registers as a Customer")
			print("login - logs in as a Customer")
			print("my tickets - lists all future tickets for the logged in Customer")
			print("=========================================")

		if (isSQLInjection(userInput)):
			print("Possible SQL Injection detected")
			print("Please do not do this again :)")
			continue
			
		if userInput == "exit":
			break

		if userInput == "register":
			registerCustomerInfo()
			# TODO login as the new customer

		if userInput == "login":
			customerId = login()
			if (customerId):
				userID = customerId
				isLoggedIn = True
				print("Logged in as Customer with ID: " + str(userID))
			else:
				print("Login failed try another epost")

		if userInput == "my tickets":
			if (isLoggedIn):
				print("Future tickets for Customer with ID: " + str(userID))
				printFutureOrdersAndTickets(userID)
			else:
				print("You are not logged in")
	
		if userInput == "stations":
			printStations()
		
		if userInput.startswith("train routes, "):
			temp = userInput.split(", ")
			if (len(temp) == 2):
				weekday = temp[1]
				stations = temp[2]
				allRoutes = getAllTrainRutesOnDay(stations, weekday)
				print("All train routes for " + stations + " on " + weekday + ": ")
				for route in allRoutes:
					print("Route: " + route)

			if (len(temp) == 3):
				date = temp[1]
				startStation = temp[2]
				endStation = temp[3]
				allRoutes = getAllTrainRutesForTrip(startStation, endStation, date)
			


def setup() -> None:
	# Create all tables
	# insert all data
	pass

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

if __name__ == "__main__":
	main()