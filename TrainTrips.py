import datetime
import sqlite3
from TrainRoutes import findRoutesDrivingBetween

from database_config import DATABASE_NAME
from inputHandler import convertDate, convertDateToWeekDay, convertSpecialCharacters, nextDate, previewDate, previewWithSpecialCharacters, translateWeekDayToNorwegian;

DATABASE: str = DATABASE_NAME

def getStationsForTrip(tripID: int, startStation: str, endStation: str) -> list:
    """
    Tar med startstasjon
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT Stasjonsnavn FROM Rutestopp
    WHERE StoppNr BETWEEN
    	(SELECT StoppNr AS startStopp FROM Rutestopp
    		WHERE Stasjonsnavn = :startStation AND RuteID =
    			(SELECT RuteID FROM Togtur WHERE TurID = :tripID)) AND
    	(SELECT StoppNr AS endeStopp FROM Rutestopp
    		WHERE Stasjonsnavn = :endStation AND RuteID =
    			(SELECT RuteID FROM Togtur WHERE TurID = :tripID)) - 1
    	AND RuteID =
    		(SELECT RuteID FROM Togtur WHERE TurID = :tripID);""",
            {"tripID": tripID, "startStation": startStation, "endStation": endStation})
    stations = cursor.fetchall()
    connection.close()
    return stations

def getTrainSetup(tripID: int) -> list:
	"""
	Will return a 2d list with each element filled with these values: 
	[(VognNummer, VognNavn, VognType, AntallGrupperinger, PlasserPerGruppering), ...]
	"""

	# Find VognOppsettID for tripID
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	cursor.execute("SELECT VognForekomst.VognNummer, VognNavn, VognType, AntallGrupperinger, PlasserPerGruppering FROM VognOppsett, Togrute, Togtur NATURAL JOIN VognForekomst NATURAL JOIN Vogn WHERE VognOppsett.VognOppsettID = Togrute.VognOppsettID  AND Togrute.RuteID = Togtur.RuteID AND Togtur.TurID =:tripID", {
	               "tripID": tripID})
	vognOppsettData = cursor.fetchall()
	connection.commit()
	connection.close()
	return vognOppsettData

def getAllTripsFor(startStation: str, endStation: str, date: str, time: str):
	"""
	Will return a 2d list with each element filled with these values:
	[(TurID, dato, RuteId, Retning, Stasjonsnavn, Ukedag, Ankomst, Avgang, StoppNr), ...]
	"""

	# Sanitize input
	startStation = convertSpecialCharacters(startStation)
	endStation = convertSpecialCharacters(endStation)
	
	# Get date and day
	day = convertDateToWeekDay(date)
	dayAfter = convertDateToWeekDay(nextDate(date))
	dateAfter = convertDate(nextDate(date))
	date = convertDate(date)

	#Create connection to database
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	cursor.execute(
		f"""
	SELECT TT.TurID, TT.TurDato, TR.RuteId, TR.BaneRetning, RS.Stasjonsnavn, RT.Ukedag, RT.Ankomst, RT.Avgang, RS.StoppNr FROM Togtur AS TT
	NATURAL JOIN Togrute  AS TR
	NATURAL JOIN Rutetider AS RT
	NATURAL JOIN Rutestopp AS RS
	WHERE (TR.RuteID IN (
		SELECT DISTINCT rs1.RuteID
		FROM Rutestopp rs1
		JOIN Rutestopp rs2 ON rs1.RuteID = rs2.RuteID
		WHERE rs1.Stasjonsnavn =:START_STATION
			AND rs2.Stasjonsnavn =:END_STATION
			AND rs1.StoppNr < rs2.StoppNr
		)
		AND (RS.Stasjonsnavn =:START_STATION OR RS.Stasjonsnavn =:END_STATION)
		AND (
				(
					TT.TurDato =:DATE AND RT.Ukedag =:DAY
					AND (
						RT.Avgang > :TIME_OF_TRAVEL
						OR (
							RS.Stasjonsnavn =:END_STATION
							AND NOT EXISTS (
								SELECT * FROM Rutetider AS RT2
								WHERE RT2.RuteID = TR.RuteID
									AND RT2.Ukedag = RT.Ukedag
									AND RT2.Stasjonsnavn =:START_STATION
									AND RT2.Avgang < :TIME_OF_TRAVEL
							)
						)
					)
				OR (
					TT.TurDato =:DATE_AFTER AND RT.Ukedag =:DAY_AFTER
				)
			)
		)
	)
	GROUP BY TT.TurID, RS.Stasjonsnavn
	ORDER BY 
		TT.TurDato ASC,
		CASE
			WHEN RT.Ukedag = 'Mandag'  THEN 1
			WHEN RT.Ukedag = 'Tirsdag' THEN 2
			WHEN RT.Ukedag = 'Onsdag'  THEN 3
			WHEN RT.Ukedag = 'Torsdag' THEN 4
			WHEN RT.Ukedag = 'Fredag'  THEN 5
			WHEN RT.Ukedag = 'Loerdag' THEN 6
			WHEN RT.Ukedag = 'Soendag' THEN 7
		END ASC,
		CASE
			WHEN RS.Stasjonsnavn =:START_STATION THEN 1
			WHEN RS.Stasjonsnavn =:END_STATION THEN 2
		END ASC,
		RT.Avgang ASC
	""", {"START_STATION": startStation, "END_STATION": endStation, "TIME_OF_TRAVEL": time, "DATE": date, "DATE_AFTER": dateAfter, "DAY": day, "DAY_AFTER": dayAfter}
	)
	allTrips = cursor.fetchall()
	connection.commit()
	connection.close()
	return allTrips


def printAllTripsFor(allTrips: list):
	"""
	Will print all trips in a nice format.
	Expects input in following format:
		allTrips = [(TurID, dato, RuteId, Retning, Stasjonsnavn, Ukedag, Ankomst, Avgang, StoppNr), ...]
	"""
	allTripsPairedStartEnd = []
	for trip in allTrips:
		start = trip
		for endtrip in allTrips:
			if endtrip[0] == start[0] and start[8] < endtrip[8]:
				allTripsPairedStartEnd.append((start, endtrip))

	for trip in allTripsPairedStartEnd:
		startOfTrip = trip[0]
		endOfTrip = trip[1]

		startStation: str = previewWithSpecialCharacters(startOfTrip[4])
		endStation: str = previewWithSpecialCharacters(endOfTrip[4])
		start: str = f"Trip {str(startOfTrip[0])} following route {str(startOfTrip[2])} departs from {startStation} at {startOfTrip[5]}, {previewDate(startOfTrip[1])} {startOfTrip[7]}"
		end: str = f" arrives at {endStation} at {endOfTrip[6]}."
		print(start + ", and" + end)


if __name__ == "__main__":
    print(getTrainSetup(1))
    # print(getStationsForTripBetweenStations(1, "Steinkjer", "Bodoe"))
    # print(getAllTripsFor("Steinkjer", "Bodoe", "2020-11-23", "12:00"))
    # print(getAllTripsFor("Trondheim", "Bodoe", "03.04.2023", "12:00"))'
    # print(getAllTripsFor("Steinkjer", "Trondheim", "03.04.2023", "00:00"))
    printAllTripsFor(getAllTripsFor("Trondheim", "Bodø", "03.04.2023", "00:00"))
    print("=====================================")
    printAllTripsFor(getAllTripsFor("Steinkjer", "Trondheim", "03.04.2023", "00:00"))
    
    
