
from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, dayAfterTomorrow, previewWithSpecialCharacters, translateWeekDayToNorwegian
import sqlite3
from TrainTrips import getStationsForTrip, getTrainSetup
from datetime import datetime

DATABASE: str = DATABASE_NAME

def getOccupiedPlaces(tripID: int, startStation: str, endStation: str) -> list:
	"""
	Using a trip, start station, and end station, returns all places (seats/beds) in all
	wagons that are not available during the trip.
	Returns [(VognNummer, PlassNummer)]
	"""
	# get wagons for trip, including type and number
	wagons = getTrainSetup(tripID)
	# get all stations between the start and end station for the trip, except the end station
	stations = getStationsForTrip(tripID, startStation, endStation)
	occupiedPlaces = []

	for wagon in wagons:
		# get wagon type, number and places per group
		wagonType = wagon[2]
		wagonNumber = wagon[0]
		placesPerGroup = wagon[4]
		# call different methods based on wagon type
		if wagonType == "Sittevogn":
			occupiedSeats = getOccupiedSeats(tripID, stations, wagonNumber)
			occupiedPlaces += occupiedSeats
		else:
			occupiedBeds = getOccupiedBeds(tripID, wagonNumber, placesPerGroup)
			occupiedPlaces += occupiedBeds
	return occupiedPlaces

def getOccupiedPlacesInWagon(tripID: int, startStation: str, endStation: str, wagonNumber: int) -> list:
	"""
	Using a trip, start station, end station, and wagonNumber, get all places (seats/beds)
	in the given wagon that are not available during the trip.
	Returns [(VognNummer, PlassNummer)]
	"""
	# get stations for trip
	stations = getStationsForTrip(tripID, startStation, endStation)
	# connnect to database
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	# get wagonType and placesPerGroup for this wagon
	placesPerGroup = cursor.execute("""SELECT VognType, PlasserPerGruppering FROM Togtur NATURAL JOIN Togrute
	NATURAL JOIN VognForekomst NATURAL JOIN Vogn WHERE TurID = :tripID AND VognNummer = :wagonNumber;
	""", {"tripID": tripID, "wagonNumber": wagonNumber})
	wagonInfo = cursor.fetchall()
	wagonType = wagonInfo[0][0]
	placesPerGroup = wagonInfo[0][1]

	occupiedPlaces = []
	if wagonType == "Sittevogn":
		occupiedSeats = getOccupiedSeats(tripID, stations, wagonNumber)
		occupiedPlaces += occupiedSeats
	else:
		occupiedBeds = getOccupiedBeds(tripID, wagonNumber, placesPerGroup)
		occupiedPlaces += occupiedBeds
	return occupiedPlaces

def getOccupiedSeats(tripID: int, stations: list, wagonNumber: int) -> list:
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

def getOccupiedBeds(tripID: int, wagonNumber: int, bedsPerGroup: int) -> list:
	"""
	Get all beds that are not available for a given trip and wagon number.
	Returns [(VognNummer, PlassNummer)]
	"""
	# connect to database
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()

	cursor.execute(f"""SELECT VognNummer, PlassNummer FROM Billett
	WHERE VognNummer = {wagonNumber} AND TurID = {tripID}""")
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

def buyTickets(tripID: int, startStation: str, endStation: str, places: list, customerID: int) -> None:
	# check for each requested ticket if it is possible to buy it, and add row to list
	tickets = []
	for place in places:
		wagonNumber = place[0]
		placeNumber = place[1]
		if not canBuyTicket(tripID, startStation, endStation, wagonNumber, placeNumber):
			print(f"Could not buy tickets. Ticket for wagon {wagonNumber} and seat/bed {placeNumber} is not available.")
			return
		else:
			tickets.append([tripID, 0, 0, placeNumber, wagonNumber])

	# connect to database
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()

	# get datetime now
	cursor.execute(f"""SELECT datetime('now')""")
	purchaseTime = cursor.fetchall()[0][0]
	# insert new order for now
	cursor.execute(f"""INSERT INTO KundeOrdre (KjoepsTidspunkt, Kundenummer)
	VALUES ('{purchaseTime}', '{customerID}')""")
	# get newly created order number
	orderNumber = cursor.execute(f"""SELECT OrdreNummer FROM KundeOrdre
	WHERE KjoepsTidspunkt = '{purchaseTime}' AND KundeNummer = '{customerID}'""")
	orderNumber = cursor.fetchall()[0][0]

	# get next ticket ID for this trip
	cursor.execute(f"""SELECT MAX(BillettID) FROM Billett
	WHERE TurID = {tripID}""")
	ticketID = (cursor.fetchall())[0][0] + 1
	# add order number to all tickets and format rows for insertion
	ticketsFormatted = []
	for i in range(len(tickets)):
		tickets[i][1] = ticketID + i
		tickets[i][2] = orderNumber
		ticketsFormatted.append(tuple(tickets[i]))
	ticketsFormatted = str(tuple(ticketsFormatted))[1:-1]
	# add all tickets
	cursor.execute(f"""INSERT INTO Billett (TurID, BillettID, OrdreNummer, PlassNummer, VognNummer)
	VALUES {ticketsFormatted}""")

	# get all stations for tickets
	stations = getStationsForTrip(tripID, startStation, endStation)
	# create and format all rows to insert into ticket stops
	ticketStops = []
	for i in range(len(tickets)):
		for j in range(len(stations)):
			ticketStops.append((tickets[i][0], tickets[i][1], stations[j][0], j+1))
	ticketStopsFormatted = str(tuple(ticketStops))[1:-1]
		
	# add all stations for tickets
	cursor.execute(f"""INSERT INTO BillettStopperVed (TurID, BillettID, Stasjonsnavn, StasjonsNummer)
	VALUES {ticketStopsFormatted}""")

	connection.commit()

	print("Thank you for your purchase! Have a nice day :)")

def canBuyTicket(tripID: int, startStation: str, endStation: str, wagonNumber: int, placeNumber: int) -> bool:
	occupiedPlaces = getOccupiedPlacesInWagon(tripID, startStation, endStation, wagonNumber)
	if (wagonNumber, placeNumber) in occupiedPlaces:
		return False
	return True

if __name__ == "__main__":
	#print(getOccupiedPlaces(1, "Mosjoeen", "Bodoe"))
	#print(getOccupiedPlacesInWagon(1, "Mosjoeen", "Bodoe", 1))
	buyTickets(1, "Mosjoeen", "Bodoe", [(1,1), (2,2)], 1)