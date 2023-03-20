import sqlite3
from database_config import DATABASE_NAME
from inputHandler import previewWithSpecialCharacters


DATABASE: str = DATABASE_NAME
STATION_NAME_INDEX: int = 0
MOH_INDEX: int = 1


def getStations() -> list:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Stasjon;")
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

def printStations() -> None:
	stations: list = getStations()
	print("Stasjoner: ")
	for station in stations:
		print("Stasjonsnavn: " + previewWithSpecialCharacters(station[STATION_NAME_INDEX]) + " Moh: " + str(station[MOH_INDEX]))

if __name__ == "__main__":
	printStations()