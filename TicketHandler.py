
from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, dayAfterTomorrow, previewWithSpecialCharacters, translateWeekDayToNorwegian
import sqlite3
from TrainTrips import getAllStationsForTrip

DATABASE: str = DATABASE_NAME

def getWagonTypes(tripId: int) -> list:
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	cursor.execute("""SELECT * FROM Billett NATURAL JOIN VognForekomst NATURAL JOIN Vogn
	WHERE TurID =:tripId;""", {"tripId": tripId})
	results = cursor.fetchall()
	connection.close()
	return results

def getCompartmentOwner(tripId: int, wagonNr: int, groupNr: int, placeNr: int) -> int:
    pass

def buyTicket(tripId: int, wagonNr: int, groupNr: int, placeNr: int, customerId: int) -> None:
	pass

def canBuyTicket(tripId: int, wagonNr: int, groupNr: int, placeNr: int) -> bool:
	pass

def seetingIsOccupied(tripId: int, wagonNr: int, groupNr: int, placeNr: int) -> bool:
	pass

def getSoldTickets(tripId: int, startStation: str, endStation: str) -> list:

	pass

if __name__ == "__main__":
	print(getWagonTypes(1))