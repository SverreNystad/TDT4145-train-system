




from Station import printStations
from TrainRoutes import getAllTrainRoutesForTrip, getAllTrainRoutesOnDay
from customer import login, printFutureOrdersAndTickets, registerCustomerInfo
from database_config import setup
from inputHandler import inputSQLData


def main():
	# Setup the database with all tables and data
	setup()

	isLoggedIn: bool = False
	userID: int

	print("Welcome to the Train App")
	print("Want to see the list of commands? Type 'help'")

	while True:
		userInput: str = inputSQLData("\nEnter a command: ")

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

		if userInput == "exit":
			break

		if userInput == "register":
			registerCustomerInfo()
			# TODO login as the new customer

		if userInput == "login":
			customerId = login()
			if (customerId):
				userID = customerId[0]
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
			if (len(temp) == 3):
				weekday = temp[1]
				correctedWeekday = weekday[0].upper() + weekday[1:].lower()
				station = temp[2]
				allRoutes = getAllTrainRoutesOnDay(station, correctedWeekday)
				print("All train routes for that stops at " + station + " on " + correctedWeekday + ": ")
				for route in allRoutes:
					routID = route[0]
					print("Route: " + str(routID))

			if (len(temp) == 4):
				date = temp[1]
				startStation = temp[2]
				endStation = temp[3]
				print("All train routes for " + startStation + " to " + endStation + " on " + date + ": ")
				allRoutes = getAllTrainRoutesForTrip(startStation, endStation, date)
				for route in allRoutes:
					print("Route: " + str(route))

if __name__ == "__main__":
	main()