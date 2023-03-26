import sqlite3

from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters

DATABASE: str = DATABASE_NAME

def getAllTrainRoutesOnDay(stationName: str, weekday: str) -> list:
    correctedStation = convertSpecialCharacters(stationName)
    convertedWeekday = convertSpecialCharacters(weekday)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT RuteID, Ankomst, Avgang FROM RuteTider
    WHERE Stasjonsnavn =:stationName
        AND Ukedag =:weekday""",
    {"stationName": correctedStation, "weekday": convertedWeekday})
    routesOnDay = cursor.fetchall()
    connection.close()
    return routesOnDay
