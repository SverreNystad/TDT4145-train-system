import sqlite3

from database_config import DATABASE_NAME;

DATABASE: str = DATABASE_NAME

def getAllTrainRoutesForTrip(startStation: str, endStation: str, date: str) -> list:
	# Get all routes that match the start and end station
	trips: list = findRoutesByTrip(startStation, endStation)
	
	# Get all routes from trips that match the date and the next day
	
	
	return 

def findRoutesByTrip(startStation: str, endStation: str) -> list: # Could also be done by sql query
	# Get all routes that match the start and end station
	allRoutesWithStartStation = getAllRoutesWithStation(startStation)
	allRoutesWithEndStation = getAllRoutesWithStation(endStation)

	# find the intersection of the two lists
	result = list(set(allRoutesWithStartStation) & set(allRoutesWithEndStation))
	return result

def getAllRoutesWithStation(station: str) -> list:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()

	cursor.execute("SELECT RuteID FROM Rutestopp WHERE Stasjonsnavn =:station", {"station": station})
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

def getAllTrainRoutesOnDay(stationName: str, weekDay: str) -> list:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT RuteID FROM RuteTider WHERE Stasjonsnavn =:stationName AND Ukedag =:weekDay", {"stationName": stationName, "weekDay": weekDay})
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

def getAllAvalibleTicketsBy(startStation: str, endStation: str, date: str) -> list:
	pass