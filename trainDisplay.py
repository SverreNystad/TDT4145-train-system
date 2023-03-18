occupiedSign = "X"
nonOccupiedSign = "O"

def displayTrain():
	pass

def displayWagon(wagonName: str, wagonType: str, wagonGroups: int, placesPerGroup: int):
	print("Wagon name: " + wagonName)

	if (wagonType == "Sittevogn"):
		displaySittingWagon(wagonGroups, placesPerGroup)
	elif (wagonType == "Sovevogn"):
		displaySleepingWagon(wagonGroups, placesPerGroup)


def displaySleepingWagon(rooms: int, bedPerRoom: int):
	wagonLength = (bedPerRoom-1) + (rooms+2)
	print("+" + "-"*wagonLength + "+")
	
	for room in range(rooms):
		for bed in range(bedPerRoom):
			bedOccupationSign = nonOccupiedSign
			if placeIsOccupied(room, bed):
				bedOccupationSign = occupiedSign
			bedSign = bedOccupationSign + " " + str(bed + room*bedPerRoom)
			print("|" + "   |" + " "*(wagonLength - len(bedSign) - 4) + bedSign + "|")

		print("-" + "-"*wagonLength + "-")

	print("+" + "-"*wagonLength + "+")

def displaySittingWagon(rows, seatsPerRow):
	# Print the top border of the wagon
    print("+" + "-"*(seatsPerRow-1) + "-"*(rows+2)*(seatsPerRow) + "+")
    # Print the seats in each row
    for row in range(rows):
        print("|", end="")
        for seat in range(seatsPerRow):
            seat_num = str(row*seatsPerRow + seat + 1)
            seatOccupationSign = nonOccupiedSign
            if placeIsOccupied(row, seat):
                seatOccupationSign = occupiedSign
            print(seatOccupationSign + " "*(rows - len(seat_num)) + seat_num + " |", end="")
        print()
    # Print the bottom border of the wagon
    print("+" + "-"*(seatsPerRow-1) + "-"*(rows+2)*(seatsPerRow) + "+")

def placeIsOccupied(row, seat):
	# TODO: Check if the place is occupied
	return False

if __name__ == "__main__":
	displayWagon("SJ-Sittevogn-1", "Sittevogn", 3, 4)
	displayWagon("SJ-Sovevogn-1", "Sovevogn", 3, 5)
	# displayTrain(10, 7)