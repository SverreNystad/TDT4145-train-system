import datetime
import sqlite3

from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, dayAfterTomorrow, previewWithSpecialCharacters, translateWeekDayToNorwegian;

DATABASE: str = DATABASE_NAME

def getStationsForTrip(tripId: int, startStation: str, endStation: str) -> list:
    """
    Tar med startstasjon
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT Stasjonsnavn FROM Rutestopp
    WHERE StoppNr BETWEEN
    	(SELECT StoppNr AS startStopp FROM Rutestopp
    		WHERE Stasjonsnavn = :startStation AND RuteID =
    			(SELECT RuteID FROM Togtur WHERE TurID = :tripId)) AND
    	(SELECT StoppNr AS endeStopp FROM Rutestopp
    		WHERE Stasjonsnavn = :endStation AND RuteID =
    			(SELECT RuteID FROM Togtur WHERE TurID = :tripId)) - 1
    	AND RuteID =
    		(SELECT RuteID FROM Togtur WHERE TurID = :tripId);""",
            {"tripId": tripId, "startStation": startStation, "endStation": endStation})
    stations = cursor.fetchall()
    connection.close()
    return stations

def getTrainSetup(tripId: int) -> list:
	"""
	Will give a 2d list with each element filled with these values: 
	[VognNummer, VognNavn, VognType, AntallGrupperinger, PlasserPerGruppering]
	"""

	# Find VognOppsettID for tripId
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	cursor.execute("SELECT VognForekomst.VognNummer, VognNavn, VognType, AntallGrupperinger, PlasserPerGruppering FROM VognOppsett, Togrute, Togtur NATURAL JOIN VognForekomst NATURAL JOIN Vogn WHERE VognOppsett.VognOppsettID = Togrute.VognOppsettID  AND Togrute.RuteID = Togtur.RuteID AND Togtur.TurID =:tripId", {
	               "tripId": tripId})
	vognOppsettData = cursor.fetchall()
	connection.commit()
	connection.close()
	return vognOppsettData


if __name__ == "__main__":
    print(getTrainSetup(1))
    print(getStationsForTripBetweenStations(1, "Steinkjer", "Bodoe"))
