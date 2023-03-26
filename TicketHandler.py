from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, previewWithSpecialCharacters, translateWeekdayToNorwegian
import sqlite3
from TrainTrips import getStationsForTrip, getTrainSetup
from datetime import datetime

DATABASE: str = DATABASE_NAME
WAGON_NUMBER_INDEX: int = 0
WAGON_TYPE_INDEX: int = 2
WAGON_PLACES_PER_GROUP_INDEX: int = 4

def getOccupiedPlaces(tripID: int, startStation: str, endStation: str) -> list:
    """
    Using a trip, start station, and end station, returns all places (seats/beds) in all
    wagons that are not available during the trip.
    Returns [(VognNummer, PlassNummer), ...]
    """
    # get wagons for trip, including type and number
    wagons = getTrainSetup(tripID)
    # get all stations between the start and end station for the trip, except the end station
    stations = getStationsForTrip(tripID, startStation, endStation)
    # check if stations are valid
    if len(stations) == 0:
        return ["Invalid"]

    occupiedPlaces = []

    for wagon in wagons:
        wagonNumber = wagon[WAGON_NUMBER_INDEX]
        wagonType = wagon[WAGON_TYPE_INDEX]
        placesPerGroup = wagon[WAGON_PLACES_PER_GROUP_INDEX]
        # call different methods based on wagon type
        if wagonType == "Sittevogn":
            occupiedSeats = getOccupiedSeats(tripID, stations, wagonNumber)
            occupiedPlaces += occupiedSeats
        elif wagonType == "Sovevogn":
            occupiedBeds = getOccupiedBeds(tripID, wagonNumber, placesPerGroup)
            occupiedPlaces += occupiedBeds
    return occupiedPlaces

def getOccupiedPlacesInWagon(tripID: int, startStation: str, endStation: str, wagonNumber: int) -> list:
    """
    Using a trip, start station, end station, and wagonNumber, get all places (seats/beds)
    in the given wagon that are not available during the trip.
    Returns [(VognNummer, PlassNummer), ...]
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # get stations for trip
    stations = getStationsForTrip(tripID, startStation, endStation)
    
    # get wagonType and placesPerGroup for this wagon
    wagonInfo = cursor.execute("""
        SELECT VognType, PlasserPerGruppering FROM Togtur 
        NATURAL JOIN Togrute
        NATURAL JOIN VognForekomst
        NATURAL JOIN Vogn
        WHERE TurID = :tripID AND VognNummer = :wagonNumber;""",
        {"tripID": tripID, "wagonNumber": wagonNumber})
    wagonInfo = cursor.fetchone()
    wagonType = wagonInfo[0]
    placesPerGroup = wagonInfo[1]

    occupiedPlaces = []
    if wagonType == "Sittevogn":
        occupiedSeats = getOccupiedSeats(tripID, stations, wagonNumber)
        occupiedPlaces += occupiedSeats
    elif wagonType == "Sovevogn":
        occupiedBeds = getOccupiedBeds(tripID, wagonNumber, placesPerGroup)
        occupiedPlaces += occupiedBeds
    return occupiedPlaces

def getOccupiedSeats(tripID: int, stations: list, wagonNumber: int) -> list:
    """
    Get all seats that are not available for a given trip and wagon number over certain stations.
    Returns [(VognNummer, PlassNummer), ...]
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
    occupiedSeats = cursor.execute(f"""
    SELECT VognNummer, PlassNummer FROM Billett AS B
    WHERE EXISTS
        (SELECT * FROM BillettStopperVed AS BSV
        WHERE B.TurID = BSV.TurID
            AND B.BillettID = BSV.BillettID
            AND Stasjonsnavn {operator} {stations}
            AND Stasjonsnavn <>
                (SELECT Stasjonsnavn FROM BillettStopperVed
                WHERE TurID = B.TurID
                    AND BillettID = B.BillettID
                GROUP BY BillettID
                HAVING MAX(StasjonsNummer))
        AND B.VognNummer = {wagonNumber});""")

    # fetch data and close connection
    occupiedSeats = cursor.fetchall()
    connection.close()
    return occupiedSeats

def getOccupiedBeds(tripID: int, wagonNumber: int, bedsPerGroup: int) -> list:
    """
    Get all beds that are not available for a given trip and wagon number.
    Returns [(VognNummer, PlassNummer), ...]
    """
    # connect to database
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(f"""SELECT VognNummer, PlassNummer FROM Billett
    WHERE VognNummer = :wagonNumber AND TurID = :tripID;""",
    {"wagonNumber": wagonNumber, "tripID": tripID})
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

def containsDuplicateTickets(places: list) -> bool:
    return len(places) == len(set(places))

def buyTickets(tripID: int, startStation: str, endStation: str, places: list, customerID: int) -> None:
    """
    Try to buy tickets for a trip, given a list of places (seats/beds) and a customerID.

    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # check if stations are valid for this trip
    stations = getStationsForTrip(tripID, startStation, endStation)
    if len(stations) == 0:
        print("Invalid stations. Please try again with different start and end station.")
        return
    
    # check for each requested ticket if it is the same ticket
    if not containsDuplicateTickets(places):
        print("Could not buy tickets. Remove duplicate seats/beds, you cannot buy the same seat/bed twice.")
        return
    
    # get train setup for trips
    wagons = getTrainSetup(tripID)

    # check for each requested ticket if it is possible to buy it, and add ticket row to list of tickets
    tickets = []
    for place in places:
        wagonNumber = place[0]
        placeNumber = place[1]
        # check if wagon number exists
        if wagonNumber - 1 > len(wagons):
            print(f"No such wagon on this train trip. Amount of wagons is {len(wagons)}.")
            return
        # check if seat/bed exists in given wagon with wagon number as index for list
        groups: int = wagons[wagonNumber][3]
        placesPerGroup: int = wagons[wagonNumber][4]
        if placeNumber > groups * placesPerGroup:
            print(f"No such seat in this given wagon. Last seat number is {groups * placesPerGroup}.")
            return
        # check if seat/bed is available
        if not canBuyTicket(tripID, startStation, endStation, wagonNumber, placeNumber):
            print(f"Could not buy tickets. Ticket for wagon {wagonNumber} and seat/bed {placeNumber} is not available.")
            return
        else:
            tickets.append([tripID, 0, 0, placeNumber, wagonNumber])
    
    # get datetime now
    purchaseTime = datetime.now()
    # insert new order for now
    cursor.execute(f"""INSERT INTO KundeOrdre (KjoepsTidspunkt, Kundenummer)
    VALUES ('{purchaseTime}', '{customerID}')""")
    # get newly created order number
    orderNumber = cursor.lastrowid

    # get next ticket ID for this trip
    cursor.execute(f"""SELECT MAX(BillettID) FROM Billett
    WHERE TurID = {tripID}""")
    ticketID = cursor.fetchall()
    if len(ticketID) == 0 or ticketID[0][0] == None:
        ticketID = 1
    else:
        ticketID = ticketID[0][0] + 1
    # add order number to all tickets and format rows for insertion
    ticketsFormatted = []
    for i in range(len(tickets)):
        tickets[i][1] = ticketID + i
        tickets[i][2] = orderNumber
        ticketsFormatted.append(tuple(tickets[i]))
    if len(tickets) == 1:
        ticketsFormatted = str(tuple(ticketsFormatted))[1:-2]
    else:
        ticketsFormatted = str(tuple(ticketsFormatted))[1:-1]
    # add all tickets
    cursor.execute(f"""INSERT INTO Billett (TurID, BillettID, OrdreNummer, PlassNummer, VognNummer)
    VALUES {ticketsFormatted}""")

    # get all stations for tickets
    stations = getStationsForTrip(tripID, startStation, endStation)
    stations.append((endStation,))
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
    return not (wagonNumber, placeNumber) in occupiedPlaces
