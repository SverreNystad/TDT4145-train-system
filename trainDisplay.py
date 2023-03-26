from TrainTrips import getTrainSetup;
occupiedSign = "X"
nonOccupiedSign = " "

def displayTrain(tripID: int, soldTickets: list):
    print("Displaying train for trip with id: " + str(tripID))
    train = getTrainSetup(tripID)
    for wagon in train:
        displayWagon(soldTickets, wagon[0], wagon[1], wagon[2], wagon[3], wagon[4])


def displayWagon(soldTickets: list, wagonNr: int, wagonName: str, wagonType: str, wagonGroups: int, placesPerGroup: int):
    print("Wagon name: " + wagonName +" is wagon number " + str(wagonNr) + " in the train")

    if (wagonType == "Sittevogn"):
        displaySittingWagon(soldTickets, wagonNr, wagonGroups, placesPerGroup)
    elif (wagonType == "Sovevogn"):
        displaySleepingWagon(soldTickets, wagonNr, wagonGroups, placesPerGroup)

def displaySleepingWagon(soldTickets, wagonNr: int, rooms: int, bedPerRoom: int):
    wallsSize = 2
    maxRoomSize = len(str(rooms*bedPerRoom)) + wallsSize
    corridor = "|   |"
    print("+" + "-"*(maxRoomSize + len(corridor)) + "+")
    
    for room in range(1, rooms+1):
        for bed in range(1, bedPerRoom+1):
            bedOccupationSign = nonOccupiedSign
            if placeIsOccupied(soldTickets, wagonNr, bedPerRoom, bed, room):
                bedOccupationSign = occupiedSign
            bedPlacement = str(bed + (room-1)*bedPerRoom)
            if bedOccupationSign == occupiedSign:
                occupationAndPlacement = " "*(maxRoomSize-len(bedPlacement) + 1) + bedOccupationSign
            else:
                occupationAndPlacement = bedOccupationSign + " "*(maxRoomSize-len(bedPlacement)) + bedPlacement
            print("|" + "   |"  + occupationAndPlacement + "|")

        if (room != rooms):
            print(corridor + "-"*(len(occupationAndPlacement)) + "|")

    print("+" + "-"*(maxRoomSize + len(corridor)) + "+")

def displaySittingWagon(soldTickets, wagonNr: int, rows: int, seatsPerRow: int):
    # Print the top border of the wagon
    print("+" + "-"*(seatsPerRow-1) + "-"*(rows+2)*(seatsPerRow) + "+")
    # Print the seats in each row
    for row in range(1, rows +1):
        print("|", end="")
        for seat in range(1, seatsPerRow+1):
            seat_num = str(((row-1)*seatsPerRow) + seat)
            seatOccupationSign = nonOccupiedSign
            if placeIsOccupied(soldTickets, wagonNr, seatsPerRow, seat, row):
                seatOccupationSign = occupiedSign
            if seatOccupationSign == occupiedSign:
                print(" "*(rows - len(seat_num) + 1) + seatOccupationSign + " |", end="")
            else:
                print(seatOccupationSign + " "*(rows - len(seat_num)) + seat_num + " |", end="")
        print()
    # Print the bottom border of the wagon
    print("+" + "-"*(seatsPerRow-1) + "-"*(rows+2)*(seatsPerRow) + "+")


def placeIsOccupied(soldTickets: list, wagonNr: int, placeMentsPerGroup: int , placementInGroup: int, group: int):
    for ticket in soldTickets:
        if (ticket[0] == wagonNr and convertPlacementToGroupAndSeat(ticket[1], placeMentsPerGroup) == (group, placementInGroup) ):
            return True
    return False

def convertPlacementToGroupAndSeat(placement: int, placesInGroups: int):
    group = placement // placesInGroups + 1
    seat = placement % placesInGroups
    if seat == 0:
        seat = placesInGroups
        group -= 1
    return (group, seat)
