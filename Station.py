from database_config import DATABASE_NAME


DATABASE: str = DATABASE_NAME


def getStations() -> list:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Stasjon")
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

def printStations() -> None:
	stations: list = getStations()
	for station in stations:
		print("Stasjonsnavn: " + station[0] + " Moh: " + station[1])