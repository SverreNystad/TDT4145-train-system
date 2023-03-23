import datetime
import sqlite3

from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, dayAfterTomorrow, previewWithSpecialCharacters, translateWeekDayToNorwegian;

DATABASE: str = DATABASE_NAME

def getAllStationsForTrip(tripId: int) -> list:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT Stasjonsnavn FROM Rutestopp
    WHERE StoppNr BETWEEN
    	(SELECT StoppNr AS startStopp FROM Rutestopp
    		WHERE Stasjonsnavn = :startStasjon AND RuteID =
    			(SELECT RuteID FROM Togtur WHERE TurID = :tripId)) + 1 AND
    	(SELECT StoppNr AS endeStopp FROM Rutestopp
    		WHERE Stasjonsnavn = :endeStasjon AND RuteID =
    			(SELECT RuteID FROM Togtur WHERE TurID = :tripId)) - 1
    	AND RuteID =
    		(SELECT RuteID FROM Togtur WHERE TurID = :tripId);""")
    results = cursor.fetchall()
    connection.close()
    return results    
