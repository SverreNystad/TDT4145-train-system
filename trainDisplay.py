from TrainTrips import getTrainSetup;
occupiedSign = "X"
nonOccupiedSign = "O"

def displayTrain(tripID: int, soldTickets: list):
	# soldTickets = (plass nummer, vognnummer)
	print("Displaying train for tour with id: " + str(tripID))
	train = getTrainSetup(tripID)
	# soldTickets = getSoldTickets(tripID, stoppID) # TODO: Must create method
	for wagon in train:
		displayWagon(soldTickets, wagon[0], wagon[1], wagon[2], wagon[3], wagon[4])


def displayWagon(soldTickets: list, wagonNr: int, wagonName: str, wagonType: str, wagonGroups: int, placesPerGroup: int):
	print("Wagon name: " + wagonName +" is the " + str(wagonNr) + "th in the train")

	if (wagonType == "Sittevogn"):
		displaySittingWagon(soldTickets, wagonNr, wagonGroups, placesPerGroup) # TODO: correct to wagonNummer
	elif (wagonType == "Sovevogn"):
		displaySleepingWagon(soldTickets, wagonNr, wagonGroups, placesPerGroup) # TODO: correct to wagonNummer

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
            print(seatOccupationSign + " "*(rows - len(seat_num)) + seat_num + " |", end="")
        print()
    # Print the bottom border of the wagon
    print("+" + "-"*(seatsPerRow-1) + "-"*(rows+2)*(seatsPerRow) + "+")


def placeIsOccupied(soldTickets: list, wagonNr: int, placeMentsPerGroup: int , placementInGroup: int, group: int):
	# TODO: Check if the place is occupied
	for ticket in soldTickets:
		# ticket -> [wagon, placement]
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

if __name__ == "__main__":
	# displayWagon([(1,1), (1,3), (1, 5), (1,8), (1,16)], 1, "SJ-Sittevogn-1", "Sittevogn", 4, 4)
	# displayWagon([(1,4)], 1, "SJ-Sittevogn-1", "Sittevogn", 4, 4)

	# displayWagon([(2,1), (2,2), (2, 3), (2,4), (2,8)], 2, "SJ-Sovevogn-1", "Sovevogn", 4, 2)
	# displayWagon([(1,5), (1,1), (1, 3), (1,8)], 3, "SJ-Sovevogn-2", "Sovevogn", 3, 1)

	displayTrain(1, [(1,1), (1,3), (1, 5), (1,8), (1,16), (2,1), (2,2), (2, 3), (2,4), (2,8)])
	displayTrain(2, [(1,1), (1,3), (1, 5), (1,8), (1,16), (2,1), (2,2), (2, 3), (2,4), (2,8)])
	displayTrain(3, [(1,1), (1,3), (1, 5), (1,8), (1,16), (2,1), (2,2), (2, 3), (2,4), (2,8)])
