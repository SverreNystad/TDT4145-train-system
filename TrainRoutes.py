import sqlite3

from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters

DATABASE: str = DATABASE_NAME

def findRoutesDrivingBetween(startStation: str, endStation: str) -> list: 
    """
    Find all routes that has the start and end station in its stops in correct order.
    return [routeID, routeID, ...]
    """
    # Create a connection to the database
    connection = sqlite3.connect(DATABASE)
    # Create a cursor to execute SQL commands
    cursor = connection.cursor()
    cursor.execute("""
    SELECT DISTINCT rs1.RuteID
    FROM Rutestopp rs1
    JOIN Rutestopp rs2 ON rs1.RuteID = rs2.RuteID
    WHERE rs1.Stasjonsnavn =:startStation
        AND rs2.Stasjonsnavn =:endStation
        AND rs1.StoppNr < rs2.StoppNr;
    """, {"startStation": startStation, "endStation": endStation})
    routesInCorrectOrder = cursor.fetchall()
    connection.commit()
    connection.close()
    # Change the list of tuples to a list of integers [(1,), (2,)] -> [1, 2]
    routesInCorrectOrder = [RouteId[0] for RouteId in routesInCorrectOrder]
    return routesInCorrectOrder


def getAllTrainRoutesOnDay(stationName: str, weekDay: str) -> list:
    correctedStation = convertSpecialCharacters(stationName)
    convertedWeekDay = convertSpecialCharacters(weekDay)
    # Create a connection to the database
    connection = sqlite3.connect(DATABASE)
    # Create a cursor to execute SQL commands
    cursor = connection.cursor()
    cursor.execute("SELECT RuteID, Ankomst, Avgang FROM RuteTider WHERE Stasjonsnavn =:stationName AND Ukedag =:weekDay", {
                   "stationName": correctedStation, "weekDay": convertedWeekDay})
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result

if __name__ == "__main__":
    print ("Test findRoutesDrivingBetween:" )
    print("Find routes driving between Trondheim and Fauske " + str(findRoutesDrivingBetween("Trondheim", "Fauske")))
    print("Find routes driving between Bodoe and Trondheim " + str(findRoutesDrivingBetween("Bodoe", "Trondheim")))
    print("Find routes driving between Mosjoeen and Trondheim " + str(findRoutesDrivingBetween("Mosjoeen", "Trondheim")))
    print("Find routes driving between Trondheim and Mosjoeen " + str(findRoutesDrivingBetween("Trondheim", "Mosjoeen")))
    print("Test getAllTrainRoutesOnDay:" )
    print("Get all train routes on day Trondheim and Monday " + str(getAllTrainRoutesOnDay("Trondheim", "Mandag")))
    print("Get all train routes on day Trondheim and Tuesday " + str(getAllTrainRoutesOnDay("Trondheim", "Tirsdag")))
    print("Get all train routes on day Trondheim and Sunday " + str(getAllTrainRoutesOnDay("Trondheim", "Soendag")))
