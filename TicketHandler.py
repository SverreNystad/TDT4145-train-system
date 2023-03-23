
from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, dayAfterTomorrow, previewWithSpecialCharacters, translateWeekDayToNorwegian
import sqlite3
from TrainTrips import getStationsForTrip, getTrainSetup

DATABASE: str = DATABASE_NAME

# def getWagonTypes(tripId: int) -> list:
# 	wagonTypes = [(wagon[0], wagon[2]) for wagon in getTrainSetup(tripId)]
# 	return wagonTypes

def getOccupiedPlaces(tripId: int, startStation: str, endStation: str) -> list:
	"""
	(vognnummer, plass)
	"""
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	wagons = getTrainSetup(tripId)
	stations = getStationsForTrip(tripId, startStation, endStation)

	for wagon in wagons:
		wagonType = wagon[2]
		wagonNumber = wagon[0]
		if wagonType == "Sittevogn":
			getOccupiedSeats(tripId, stations, wagonNumber)
		if wagonType == "Sovevogn":
			getOccupiedBeds(tripId, wagonNumber)

	occupiedPlaces = cursor.fetchall()
	return occupiedPlaces

def getOccupiedSeats(tripId: int, stations: list, wagonNumber: int) -> list:
	
	return

def getOccupiedBeds(tripId: int, wagonNumber: int) -> list:

	return

def getTicketEndStation(tripId: int, ticketId: int) -> str:
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	cursor.execute("")
	results = cursor.fetchall()
	connection.close()
	return results

def buyTicket(tripId: int, wagonNr: int, groupNr: int, placeNr: int, customerId: int) -> None:
	pass

def canBuyTicket(tripId: int, wagonNr: int, groupNr: int, placeNr: int) -> bool:
	pass

def placeIsOccupied(tripId: int, wagonNr: int, groupNr: int, placeNr: int) -> bool:
	pass

def getSoldTickets(tripId: int, startStation: str, endStation: str) -> list:

	pass

if __name__ == "__main__":
	print(getOccupiedPlaces(1, "Mosjoeen", "Bodoe"))