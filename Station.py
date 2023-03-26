import sqlite3
from database_config import DATABASE_NAME
from inputHandler import previewWithSpecialCharacters

DATABASE: str = DATABASE_NAME
STATION_NAME_INDEX: int = 0
MOH_INDEX: int = 1

def getStations() -> list:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Stasjon;")
    stations = cursor.fetchall()
    connection.close()
    return stations

def printStations() -> None:
    stations: list = getStations()
    print("Stasjoner")
    longest_name = (max(len(x[0]) for x in stations))
    for station in stations:
        print("Navn: " + previewWithSpecialCharacters(station[STATION_NAME_INDEX]).ljust(longest_name + 5) + "moh: " + str(station[MOH_INDEX]) + "m")
