from Station import printStations
from TrainRoutes import getAllTrainRoutesForTrip, getAllTrainRoutesOnDay, printAllTrainRoutesForTrip
from customer import login, printFutureOrdersAndTickets, registerCustomerInfo
from database_config import setup
from inputHandler import convertStationName, inputSQLData, isEnglishWeekDay, translateWeekDayToNorwegian

trainLogo = '''
  _______     _______     _______     _______     ___       
 /       \\   /       \\   /       \\   /       \\   /  |\_ 
|   NORD  | |  LANDS  | |  BANEN  | |   S J   | |   |____\_ 
|_________|_|_________|_|_________|_|_________|_|_  |______|
  O     O     O     O     O     O     O     O    O\/_|      
'''


def main():
	# Setup the database with all tables and data
	setup()

	isLoggedIn: bool = False
	userID: int
	print(trainLogo)
	print("Welcome to the Train App")
	print("Want to see the list of commands? Type 'help'")

	while True:
		userInput: str = inputSQLData("\nEnter a command: ").lower()
		print("")
		
		if userInput == "help":
			print("=========================================")
			print("Commands: ")
			print("help - displays this message")
			print("exit - exits the app")
			print("stations - lists all stations")
			print("train routes, <weekday>, <station> - lists all train routes for a specific station on a specific weekday REQUIRES 2 ARGUMENTS (weekday, station)")
			print("              for example, to see all routes going past station A on Monday, write 'train routes, monday, A'.")
			print("train trips, <DD.MM.YYYY>, <HH:MM>, <start station>, <end station> - lists all train trips for a specific date and start and end station REQUIRES 4 ARGUMENTS (date, time, start station, end station)")
			print("             for example, to see all trips on 01.01.2023 and 02.01.2023 after 00:00 on 01.01.2023 from station A to B, write 'train trips, 01.01.2023, 00:00, A, B'.")
			print("register - registers as a Customer")
			print("login - logs in as a Customer")
			print("tickets, <start station>, <end station>, <trip ID> - lists all available tickets between a start station and an end station for a given route")
			print("         for example, to see all available tickets from station A to B on trip 1, write 'tickets, A, B, 1'")
			print("buy ticket, <start station>, <end station>, <trip ID>, [<wagon number>, <seat/bed number>] - reserve a seat/bed in a specific wagon between a start station and an end station for a given route")
			print("            for example, to buy a two tickets from A to B on trip 1, write 'buy ticket, A, B, 1, [1, 1], [2, 1]' for seats 1 in wagons 1 and 2")
			print("my tickets - lists all future tickets for the logged in Customer")
			print("=========================================")

		elif userInput == "exit":
			break

		elif userInput == "register":
			customerId = registerCustomerInfo()
			if (customerId):
				userID = customerId[0]
				isLoggedIn = True
				print("Logged in as Customer with ID: " + str(userID))

		elif userInput == "login":
			customerId = login()
			if (customerId):
				userID = customerId[0]
				isLoggedIn = True
				print("Logged in as Customer with ID: " + str(userID))
			else:
				print("Login failed try another epost")

		elif userInput == "my tickets":
			# TODO: add order time, and fix route time
			if (isLoggedIn):
				print("Future tickets for Customer with ID: " + str(userID))
				printFutureOrdersAndTickets(userID)
			else:
				print("You are not logged in")
	
		elif userInput == "stations":
			printStations()
		
		elif userInput.startswith("train routes, "):
			temp = userInput.split(", ")
			if (len(temp) == 3):
				weekday = temp[1]
				correctedWeekday = weekday[0].upper() + weekday[1:].lower()
				if (isEnglishWeekDay(correctedWeekday)):
					correctedWeekday = translateWeekDayToNorwegian(correctedWeekday)
				
				station = temp[2]
				correctedStationName = station[0].upper() + station[1:].lower()
				allRoutes = getAllTrainRoutesOnDay(correctedStationName, correctedWeekday)
				print("All train routes that stop at " + correctedStationName + " on " + correctedWeekday + ": ")
				for route in allRoutes:
					routeID = route[0]
					arrival = route[1]
					departure = route[2]
					routeInfo: str = "Route: " + str(routeID)
					if arrival:
						routeInfo += ", Arrival: " + arrival
					else:
						routeInfo += ", the station is a start station"
					if departure:
						routeInfo += ", Departure: " + departure
					else:
						routeInfo += ", the station is an end station"
					print(routeInfo)

		elif (userInput.startswith("train trips, ")):
			temp = userInput.split(", ")
			if (len(temp) == 5):
				date = temp[1]
				time = temp[2]
				startStation = convertStationName(temp[3])
				endStation = convertStationName(temp[4])
				print("All train routes from " + startStation + " to " + endStation + " on " + date + ": ")
				printAllTrainRoutesForTrip(startStation, endStation, date, time)
		
		elif userInput.startswith("tickets, "):
			temp = userInput.split(", ")
			if (len(temp) == 5):
				startStation = convertStationName(temp[1])
				endStation = convertStationName(temp[2])
				routeID = temp[3]
				print("All available tickets from " + startStation + " to " + endStation + " on route " + routeID + ": ")
				
		elif userInput.startswith("buy ticket, "):
			temp = userInput.split(", ")
			if (len(temp) == 7):
				if (isLoggedIn):
					startStation = convertStationName(temp[1])
					endStation = convertStationName(temp[2])
					routeID = temp[3]
					seatNumber = temp[4]
					wagonNumber = temp[5]

					print("Buying ticket from " + startStation + " to " + endStation + " on route " + routeID + " in wagon " + wagonNumber + " seat " + seatNumber + " for Customer with ID: " + str(userID))
		else:
			print("Command not found. Type 'help' to see all commands")
if __name__ == "__main__":
	main()