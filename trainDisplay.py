occupiedSign = "X"
nonOccupiedSign = "O"

def displayTrain(tourId: int, stoppId: int):
	print("Displaying train for tour with id: " + str(tourId) + " and stopp with id: " + str(stoppId))
	train = getTrainSetup(tourId) # TODO: Must create method
	soldTickets = getSoldTickets(tourId, stoppId) # TODO: Must create method
	for wagon in train:
		displayWagon(wagon[0], wagon[1], wagon[2], wagon[3])

def displayWagon(wagonName: str, wagonType: str, wagonGroups: int, placesPerGroup: int):
	print("Wagon name: " + wagonName)

	if (wagonType == "Sittevogn"):
		displaySittingWagon(0, wagonGroups, placesPerGroup) # TODO: correct to wagonNummer
	elif (wagonType == "Sovevogn"):
		displaySleepingWagon(0, wagonGroups, placesPerGroup) # TODO: correct to wagonNummer

def displaySleepingWagon(wagonNr: int, rooms: int, bedPerRoom: int):
	wallsSize = 2
	maxRoomSize = len(str(rooms*bedPerRoom)) + wallsSize
	corridor = "|   |"
	print("+" + "-"*(maxRoomSize + len(corridor)) + "+")
	
	for room in range(rooms):
		for bed in range(1, bedPerRoom+1):
			bedOccupationSign = nonOccupiedSign
			if placeIsOccupied(wagonNr, room, bed):
				bedOccupationSign = occupiedSign
			bedPlacement = str(bed + room*bedPerRoom)
			occupationAndPlacement = bedOccupationSign + " "*(maxRoomSize-len(bedPlacement)) + bedPlacement
			print("|" + "   |"  + occupationAndPlacement + "|")

		if (room != rooms-1):
			print(corridor + "-"*(len(occupationAndPlacement)) + "|")

	print("+" + "-"*(maxRoomSize + len(corridor)) + "+")

def displaySittingWagon(wagonNr: int, rows: int, seatsPerRow: int):
	# Print the top border of the wagon
    print("+" + "-"*(seatsPerRow-1) + "-"*(rows+2)*(seatsPerRow) + "+")
    # Print the seats in each row
    for row in range(rows):
        print("|", end="")
        for seat in range(seatsPerRow):
            seat_num = str(row*seatsPerRow + seat + 1)
            seatOccupationSign = nonOccupiedSign
            if placeIsOccupied(wagonNr, row, seat):
                seatOccupationSign = occupiedSign
            print(seatOccupationSign + " "*(rows - len(seat_num)) + seat_num + " |", end="")
        print()
    # Print the bottom border of the wagon
    print("+" + "-"*(seatsPerRow-1) + "-"*(rows+2)*(seatsPerRow) + "+")

def placeIsOccupied(wagonNr, row, seat):
	# TODO: Check if the place is occupied
	return False

if __name__ == "__main__":
	displayWagon("SJ-Sittevogn-1", "Sittevogn", 3, 4)
	displayWagon("SJ-Sovevogn-1", "Sovevogn", 3, 2)
	displayWagon("SJ-Sovevogn-2", "Sovevogn", 3, 1)

	


	# displayTrain(10, 7)