import datetime
import sqlite3

from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, previewWithSpecialCharacters;

DATABASE: str = DATABASE_NAME

def printAllTrainRoutesForTrip(startStation: str, endStation: str, date: str, time: str) -> None:
	routes: list = getAllTrainRoutesForTrip(startStation, endStation, date, time)
	print(routes)
	# sort routes by day and time
	sortRoutesByDayAndTime(routes)

	for i in range(0, len(routes), 2):
		startStation: str = previewWithSpecialCharacters(routes[i][0][1])
		endStation: str = previewWithSpecialCharacters(routes[i+1][0][1])
		start: str = f"Route {str(routes[i][0][0])} starts on station {startStation} and departs {routes[i][0][4]}, {routes[i][0][2]} {routes[i][1]}"
		end: str = f" arrives at {endStation} at {routes[i+1][0][3]}."
		print(start + ", and" + end)

def sortRoutesByDayAndTime(routes: list) -> list:
	# Sort routes by day and time
	weekdays =	[
		"Mandag",
		"Tirsdag",
		"Onsdag",
		"Torsdag",
		"Fredag",
		"Lørdag",
		"Søndag"
	]
	if len(routes) > 0:
		routes.sort(key=lambda route: weekdays.index(route[0][2]))
	return routes

def routeToString(inputRoute: list) -> str:
	isStartStation: bool = False
	route: list = inputRoute[0]
	station = previewWithSpecialCharacters(route[1])
	if (route[3] == None):
		isStartStation = True
	if isStartStation:
		return "Route: " + str(route[0]) + " starts on station " + station + " and departs " + route[4] + " on " + route[2] + "."
	else:
		return "Route: " + str(route[0]) + " ends on station " + station + " and arrives " + route[3] + "."

def getAllTrainRoutesForTrip(startStation: str, endStation: str, date: str, time: str) -> list:
	convertedStartStation = convertSpecialCharacters(startStation)
	convertedEndStation = convertSpecialCharacters(endStation)
	# Get all routes that match the start and end station
	trips: list = findRoutesByTrip(convertedStartStation, convertedEndStation)
	# Get all routes from trips that match the date and the next day
	tripDay: str = convertDateToWeekDay(date)
	dayAfterTripDay: str = dayAfterTomorrow(tripDay)
	dateAfter: str = nextDate(date)

	routesForTrip: list = []
	for trip in trips:
		startFirst: list = getAllRouteDrivingOn(trip, convertedStartStation, tripDay, time)
		endFirst: list = getAllRouteDrivingOn(trip, convertedEndStation, tripDay, time)
		startSecond: list = getAllRouteDrivingOn(trip, convertedStartStation, dayAfterTripDay, time)
		endSecond: list = getAllRouteDrivingOn(trip, convertedEndStation, dayAfterTripDay, time)
		if len(startFirst) == 0 or len(endFirst) == 0 or len(startSecond) == 0 or len(endSecond) == 0:
			continue
	
		startFirst.append(date)
		routesForTrip.append(startFirst)
		routesForTrip.append(endFirst)

		startSecond.append(dateAfter)
		routesForTrip.append(startSecond)
		routesForTrip.append(endSecond)
	return routesForTrip

def convertDateToWeekDay(date: str) -> str:
	# Convert the date to a weekday
	# DD.MM.YYYY -> Monday
	day, month, year = date.split(".")
	datetime_object = datetime.datetime(int(year), int(month), int(day))
	weekday = datetime_object.strftime("%A")
	return translateWeekDayToNorwegian(weekday)

def nextDate(date: str) -> str:
	# Get date after date
	# DD.MM.YYYY -> DD.MM.YYYY
	day, month, year = date.split(".")
	datetime_object = datetime.datetime(int(year), int(month), int(day))
	datetime_next_day = datetime_object + datetime.timedelta(days=1)
	next_day = datetime_next_day.strftime("%d.%m.%Y")
	return next_day

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

def getAllRouteDrivingOn(routeID: int, station: str, day: str, time: str) -> list:
	RUTETIDER_ARRIVAL_INDEX = 3
	RUTETIDER_PARTING_INDEX = 4

	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Rutetider WHERE RuteID =:routeId AND Stasjonsnavn =:station AND Ukedag =:day ", {"routeId": routeID, "station": station, "day": day})
	routeTimes = cursor.fetchall()
	connection.close()
	
	allRoutesAfterTime = []
	for routetime in routeTimes:
		arrival = routetime[RUTETIDER_ARRIVAL_INDEX]
		parting = routetime[RUTETIDER_PARTING_INDEX]
		if arrival == None:
			arrival = parting
		elif parting == None:
			parting = arrival
			
		if arrival > time and parting > time:
			allRoutesAfterTime.append(routetime)
	return allRoutesAfterTime


def findRoutesByTrip(startStation: str, endStation: str) -> list: # Could also be done by sql query
	# Get all routes that match the start and end station
	allRoutesWithStartStation = getAllRoutesWithStation(startStation)
	allRoutesWithEndStation = getAllRoutesWithStation(endStation)

	# find the intersection of the two lists, could also be done by sql query
	result = list(set(allRoutesWithStartStation) & set(allRoutesWithEndStation))

	# Get all routes that have startstop before endstop
	connection = sqlite3.connect(DATABASE)

	routesInCorrectOrder = []
	# for each routID find the startstopnr and endstopnr and compare them. 
	# If startstopnr < endstopnr then the route is in the correct order and should be added to the list
	for route in result:
		routeID = route[0]
		cursor = connection.cursor()
		cursor.execute("SELECT StoppNr FROM Rutestopp WHERE RuteID =:routeID AND Stasjonsnavn =:stationName", {"routeID": str(routeID), "stationName": startStation})
		startStationStoppNr = cursor.fetchone()
		connection.commit()

		cursor.execute("SELECT StoppNr FROM Rutestopp WHERE RuteID =:routeID AND Stasjonsnavn =:stationName", {"routeID": str(routeID), "stationName": endStation})
		endStationStoppNr = cursor.fetchone()
		connection.commit()

		if startStationStoppNr[0] < endStationStoppNr[0]:
			routesInCorrectOrder.append(route[0])
	connection.close()
	return routesInCorrectOrder


def getAllRoutesWithStation(station: str) -> list:
	correctedStation = convertSpecialCharacters(station)
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()

	cursor.execute("SELECT RuteID FROM Rutestopp WHERE Stasjonsnavn =:station", {"station": correctedStation})
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

def getAllTrainRoutesOnDay(stationName: str, weekDay: str) -> list:
	correctedStation = convertSpecialCharacters(stationName)
	convertedWeekDay = convertSpecialCharacters(weekDay)
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT RuteID, Ankomst, Avgang FROM RuteTider WHERE Stasjonsnavn =:stationName AND Ukedag =:weekDay", {"stationName": correctedStation, "weekDay": convertedWeekDay})
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result


if __name__ == "__main__":
	# print(getAllTrainRoutesForTrip("Trondheim", "Bodø", "21.03.2023", "07:00"))

	# print(findRoutesByTrip("Trondheim", "Fauske"))
	# print(findRoutesByTrip("Mosjøen", "Trondheim"))

	# print("Trondheim-" + "Bodø: " + str(findRoutesByTrip("Trondheim", "Bodoe")) + " should be  1, 2") 
	# print("Bodø-" + "Mosjøen: " + str(findRoutesByTrip("Trondheim", "Mosjoeen")) + " should be  1, 2") 
	# print("Mo i Rana-" + "Mosjøen: " + str(findRoutesByTrip("Mo i Rana", "Mosjoeen")) + " should be  3") 
	# print("Bodø-" + "Trondheim: " + str(findRoutesByTrip("Bodoe", "Trondheim")) + " should be  0") 
	printAllTrainRoutesForTrip("Trondheim", "Bodø", "21.03.2023", "07:00")
	printAllTrainRoutesForTrip("Mosjøen", "Bodø", "21.03.2023", "07:00")
	printAllTrainRoutesForTrip("Mo i Rana", "Mosjoeen", "21.03.2023", "07:00")


	# convertDateToWeekDay("21.03.2023")
	# print(sortRoutesByDayAndTime(getAllTrainRoutesForTrip("Trondheim", "Bodø", "21.03.2023", "07:00")))


