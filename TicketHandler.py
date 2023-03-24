
from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, dayAfterTomorrow, previewWithSpecialCharacters, translateWeekDayToNorwegian
import sqlite3
from TrainTrips import getStationsForTrip, getTrainSetup

DATABASE: str = DATABASE_NAME

def getOccupiedPlaces(tripId: int, startStation: str, endStation: str) -> list:
	"""
	Using a trip, start station, and end station, returns all places (seats/beds) in all
	wagons that are not available during the trip.
	Returns [(VognNummer, PlassNummer)]
	"""
	# connect to database
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	wagons = getTrainSetup(tripId)
	stations = getStationsForTrip(tripId, startStation, endStation)
	occupiedPlaces = []

	for wagon in wagons:
		print(wagon)
		wagonType = wagon[2]
		wagonNumber = wagon[0]
		if wagonType == "Sittevogn":
			occupiedSeats = getOccupiedSeats(tripId, stations, wagonNumber)
			print("hello???" + str(occupiedSeats))
			occupiedPlaces += occupiedSeats
		if wagonType == "Sovevogn":
			occupiedBeds = getOccupiedBeds(tripId, wagonNumber)
			occupiedPlaces += occupiedBeds
	
	return occupiedPlaces

def getOccupiedSeats(tripId: int, stations: list, wagonNumber: int) -> list:
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()

	# if stations is more than one element, turn it into a tuple and use operator IN
	if len(stations) > 1:
		stations = tuple([station for subtuple in stations for station in subtuple])
		operator = "IN"
	# if stations is only one element, turn it into a single value and use equals
	else:
		stations = f'"{stations[0][0]}"'
		operator = "="
	
	occupiedSeats = cursor.execute(f"""SELECT VognNummer, PlassNummer FROM Billett AS B
	WHERE EXISTS (SELECT * FROM BillettStopperVed AS BSV
		WHERE B.TurID = BSV.TurID AND B.BillettID = BSV.BillettID AND
			Stasjonsnavn {operator} {stations} AND Stasjonsnavn <> (
				SELECT Stasjonsnavn FROM BillettStopperVed
						WHERE TurID = B.TurID AND BillettID = B.BillettID
						GROUP BY BillettID HAVING MAX(StasjonsNummer)) AND
			B.VognNummer = {wagonNumber}
		);""")
	occupiedSeats = cursor.fetchall()
	connection.close()
	return occupiedSeats

def getOccupiedCompartments(tripId: int, wagonNumber: int) -> list:
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	cursor.execute("")
	results = cursor.fetchall()
	connection.close()
	return

#done:) might not be needed though...
def getTicketEndStation(tripId: int, ticketId: int) -> str:
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	cursor.execute("""SELECT Stasjonsnavn FROM BillettStopperVed
						WHERE TurID = :tripId AND BillettID = :ticketId
						GROUP BY BillettID HAVING MAX(StasjonsNummer)""",
	{"tripId": tripId, "ticketId": ticketId})
	endStation = cursor.fetchall()
	connection.close()
	return endStation

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