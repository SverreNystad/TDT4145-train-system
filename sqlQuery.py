
from database_config import DATABASE_NAME
from inputHandler import convertSpecialCharacters, dayAfterTomorrow, previewWithSpecialCharacters, translateWeekDayToNorwegian
import sqlite3
from datetime import datetime
from TicketHandler import getTicketEndStation
from TrainTrips import getStationsForTrip, getTrainSetup

DATABASE: str = DATABASE_NAME

def doQuery(query: str):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    # cursor.execute("DELETE FROM BillettStopperVed WHERE TurID = 1 AND BillettID = 3")
    stations = getStationsForTrip(1, 'Steinkjer', 'Mosjoeen')
    if len(stations) > 1:
        stations = tuple([station for subtuple in stations for station in subtuple])
        operator = "IN"
    else:
        stations = f'"{stations[0][0]}"'
        operator = "="
    # connection.commit()
    #THIS MIGHT BE IT CHIEF
    cursor.execute(f"""SELECT VognNummer, PlassNummer FROM Billett AS B
    WHERE EXISTS (SELECT * FROM BillettStopperVed AS BSV
        WHERE B.TurID = BSV.TurID AND B.BillettID = BSV.BillettID AND
            Stasjonsnavn {operator} {stations} AND Stasjonsnavn <> (
                SELECT Stasjonsnavn FROM BillettStopperVed
                        WHERE TurID = B.TurID AND BillettID = B.BillettID
                        GROUP BY BillettID HAVING MAX(StasjonsNummer)) AND
            B.VognNummer = {wagonNumber}
        );""")
    # results = [getTicketEndStation(1, 1), getTicketEndStation(1, 2), getTicketEndStation(1, 3)]
    # cursor.execute("SELECT * FROM BillettStopperVed")
    results = cursor.fetchall()
    connection.close()


    # cursor.execute("INSERT INTO KundeOrdre VALUES (3, :time, 1);", {"time": datetime.now()})
    # cursor.execute("INSERT INTO Billett VALUES (3, 3, 3, 3, 3);")
    """
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 1, 'Trondheim', '1');")
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 1, 'Steinkjer', '2');")
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 1, 'Mosjoeen', '3');")

    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 2, 'Steinkjer', '1');")
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 2, 'Mosjoeen', '2');")
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 2, 'Mo i Rana', '3');")
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 2, 'Fauske', '4');")

    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 3, 'Mosjoeen', '1');")
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 3, 'Mo i Rana', '2');")
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 3, 'Fauske', '3');")
    cursor.execute("INSERT INTO BillettStopperVed VALUES (1, 3, 'Bodoe', '4');")
    """
    """
    cursor.execute("INSERT INTO Billett VALUES (1, 1, 1, 1, 1);")
    cursor.execute("INSERT INTO Billett VALUES (1, 2, 2, 3, 1);")
    cursor.execute("INSERT INTO Billett VALUES (1, 3, 3, 1, 1);")
    """
    # cursor.execute("""SELECT PlassNummer, VognNummer FROM Billett AS B
    # WHERE EXISTS (SELECT * FROM BillettStopperVed AS BSV WHERE B.BillettID = BSV.BillettID
    #     );""",
    #         {"stations": getStationsForTrip(1, 'Mo i Rana', 'Bodoe')})



    # try:
    #     cursor.execute("""SELECT PlassNummer, VognNummer FROM Billett AS B
    # WHERE EXISTS (SELECT * FROM BillettStopperVed AS BSV
    #     WHERE BSV.TurID = B.TurID AND BSV.BillettID = B.BillettID AND Stasjonsnavn IN :stations
    #         AND Stasjonsnavn <> (SELECT Stasjonsnavn, MAX(StasjonsNummer) FROM BillettStopperVed
    #                     WHERE TurID = :tripID AND BillettID = :ticketID
    #                     GROUP BY BillettID));""",
    #         {"stations": getStationsForTrip(1, )})
    # except Exception as e:
    #     print(e)
    #cursor.execute("DELETE FROM BillettStopperVed;")
    #cursor.execute("SELECT * FROM BillettStopperVed;")
    #cursor.execute("SELECT Stasjonsnavn, MAX(StasjonsNummer) FROM BillettStopperVed WHERE TurID = :tripID AND BillettID = :ticketID GROUP BY BillettID", {"tripID": 1, "ticketID": 1})
    #cursor.execute("SELECT Stasjonsnavn, MAX(StasjonsNummer) FROM BillettStopperVed WHERE BillettID = :ticketID GROUP BY BillettID", {"ticketID": 1})
    return results

if __name__ == "__main__":
    print("THE SQL QUERY MODULE IS NOT INTENDED TO BE RUN AS A SCRIPT.")
    print("===============================================")

    print(doQuery(""))

    # print(doQuery("SELECT VognOppsettID FROM Togrute NATURAL JOIN Togtur WHERE TurID = 3"))

    # print(doQuery("""SELECT Stasjonsnavn FROM Rutestopp
    # WHERE StoppNr BETWEEN (SELECT StoppNr AS startStopp FROM Rutestopp WHERE Stasjonsnavn = 'Trondheim' AND RuteID = (SELECT RuteID FROM Togtur WHERE TurID = 1)) + 1
    # AND (SELECT StoppNr AS endeStopp FROM Rutestopp WHERE Stasjonsnavn = 'Bodoe' AND RuteID = (SELECT RuteID FROM Togtur WHERE TurID = 1)) - 1 AND
    # RuteID = (SELECT RuteID FROM Togtur WHERE TurID = 1);"""))

    # print(doQuery("""SELECT B.Plassnummer, B.Vognnummer FROM BillettStopperVed AS BSV NATURAL JOIN Billett AS B
    # WHERE BSV.Stasjonsnavn IN
    # (SELECT Stasjonsnavn FROM Rutestopp WHERE StoppNr BETWEEN
    # (SELECT StoppNr AS startStopp FROM Rutestopp WHERE Stasjonsnavn = 'Steinkjer' AND RuteID = 1) + 1 AND
    # (SELECT StoppNr AS endeStopp FROM Rutestopp WHERE Stasjonsnavn = 'Fauske' AND RuteID = 1) - 1 AND RuteID = 1);"""))
