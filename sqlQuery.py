
from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, dayAfterTomorrow, previewWithSpecialCharacters, translateWeekDayToNorwegian
import sqlite3

DATABASE: str = DATABASE_NAME

def doQuery(query: str):
    # Connect to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor
	cursor = connection.cursor()
	# Execute the query
	cursor.execute(query)
	# Fetch the results
	results = cursor.fetchall()
	# Close the connection
	connection.close()
	# Return the results
	return results

if __name__ == "__main__":
	print("THE SQL QUERY MODULE IS NOT INTENDED TO BE RUN AS A SCRIPT.")
	print("===============================================")

	print(doQuery("SELECT VognOppsettID FROM Togrute NATURAL JOIN Togtur WHERE TurID = 3"))

	print(doQuery("""SELECT Stasjonsnavn FROM Rutestopp
	WHERE StoppNr BETWEEN (SELECT StoppNr AS startStopp FROM Rutestopp WHERE Stasjonsnavn = 'Trondheim' AND RuteID = (SELECT RuteID FROM Togtur WHERE TurID = 1)) + 1
	AND (SELECT StoppNr AS endeStopp FROM Rutestopp WHERE Stasjonsnavn = 'Bodoe' AND RuteID = (SELECT RuteID FROM Togtur WHERE TurID = 1)) - 1 AND
	RuteID = (SELECT RuteID FROM Togtur WHERE TurID = 1);"""))

	# print(doQuery("""SELECT B.Plassnummer, B.Vognnummer FROM BillettStopperVed AS BSV NATURAL JOIN Billett AS B
	# WHERE BSV.Stasjonsnavn IN
	# (SELECT Stasjonsnavn FROM Rutestopp WHERE StoppNr BETWEEN
	# (SELECT StoppNr AS startStopp FROM Rutestopp WHERE Stasjonsnavn = 'Steinkjer' AND RuteID = 1) + 1 AND
	# (SELECT StoppNr AS endeStopp FROM Rutestopp WHERE Stasjonsnavn = 'Fauske' AND RuteID = 1) - 1 AND RuteID = 1);"""))
