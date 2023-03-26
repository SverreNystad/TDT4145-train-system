
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
	# get wagons for trip, including type and number
	wagons = getTrainSetup(tripId)
	# get all stations between the start and end station for the trip, except the end station
	stations = getStationsForTrip(tripId, startStation, endStation)
	occupiedPlaces = []

	for wagon in wagons:
		# get wagon type, number and places per group
		wagonType = wagon[2]
		wagonNumber = wagon[0]
		placesPerGroup = wagon[4]
		# call different methods based on wagon type
		if wagonType == "Sittevogn":
			occupiedSeats = getOccupiedSeats(tripId, stations, wagonNumber)
			occupiedPlaces += occupiedSeats
		else:
			occupiedBeds = getOccupiedBeds(tripId, wagonNumber, placesPerGroup)
			occupiedPlaces += occupiedBeds
	return occupiedPlaces

# donedone!
def getOccupiedPlacesInWagon(tripId: int, startStation: str, endStation: str, wagonNumber: int) -> list:
	"""
	Using a trip, start station, end station, and wagonNumber, get all places (seats/beds)
	in the given wagon that are not available during the trip.
	Returns [(VognNummer, PlassNummer)]
	"""
	# get stations for trip
	stations = getStationsForTrip(tripId, startStation, endStation)
	# connnect to database
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	# get wagonType and placesPerGroup for this wagon
	placesPerGroup = cursor.execute("""SELECT VognType, PlasserPerGruppering FROM Togtur NATURAL JOIN Togrute
	NATURAL JOIN VognForekomst NATURAL JOIN Vogn WHERE TurID = :tripId AND VognNummer = :wagonNumber;
	""", {"tripId": tripId, "wagonNumber": wagonNumber})
	wagonInfo = cursor.fetchall()
	wagonType = wagonInfo[0][0]
	placesPerGroup = wagonInfo[0][1]

	occupiedPlaces = []
	if wagonType == "Sittevogn":
		occupiedSeats = getOccupiedSeats(tripId, stations, wagonNumber)
		occupiedPlaces += occupiedSeats
	else:
		occupiedBeds = getOccupiedBeds(tripId, wagonNumber, placesPerGroup)
		occupiedPlaces += occupiedBeds
	return occupiedPlaces

#donezo
def getOccupiedSeats(tripId: int, stations: list, wagonNumber: int) -> list:
	"""
	Get all seats that are not available for a given trip and wagon number over certain stations.
	Returns [(VognNummer, PlassNummer)]
	"""
	# connect to database
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
	
	# get info about overlapping tickets for this wagon except for end station of other tickets
	occupiedSeats = cursor.execute(f"""SELECT VognNummer, PlassNummer FROM Billett AS B
	WHERE EXISTS (SELECT * FROM BillettStopperVed AS BSV
		WHERE B.TurID = BSV.TurID AND B.BillettID = BSV.BillettID AND
			Stasjonsnavn {operator} {stations} AND Stasjonsnavn <> (
				SELECT Stasjonsnavn FROM BillettStopperVed
						WHERE TurID = B.TurID AND BillettID = B.BillettID
						GROUP BY BillettID HAVING MAX(StasjonsNummer)) AND
			B.VognNummer = {wagonNumber});""")
	
	# fetch data and close connection
	occupiedSeats = cursor.fetchall()
	connection.close()
	return occupiedSeats

#donedone!
def getOccupiedBeds(tripId: int, wagonNumber: int, bedsPerGroup: int) -> list:
	"""
	Get all beds that are not available for a given trip and wagon number.
	Returns [(VognNummer, PlassNummer)]
	"""
	# connect to database
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()

	cursor.execute(f"""SELECT VognNummer, PlassNummer FROM Billett
	WHERE VognNummer = {wagonNumber} AND TurID = {tripId}""")
	occupiedBeds = cursor.fetchall()
	connection.close()

	# get all other beds in the compartment
	allOccupiedBeds = []
	
	for bedTuple in occupiedBeds:
		compartment = (bedTuple[1] + bedsPerGroup - 1) // bedsPerGroup
		firstBed = (compartment * bedsPerGroup) - bedsPerGroup + 1
		for bed in range(firstBed, compartment * bedsPerGroup + 1):
			allOccupiedBeds.append((wagonNumber, bed))
	return set(allOccupiedBeds)

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

	return

def canBuyTicket(tripId: int, wagonNr: int, groupNr: int, placeNr: int) -> bool:
	
	return

if __name__ == "__main__":
	#print(getOccupiedPlaces(1, "Mosjoeen", "Bodoe"))
	print(getOccupiedPlacesInWagon(1, "Mosjoeen", "Bodoe", 1))