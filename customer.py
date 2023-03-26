from datetime import datetime
import sqlite3

from database_config import DATABASE_NAME
from inputHandler import inputSQLData;

DATABASE: str = DATABASE_NAME
ORDERID_INDEX = 0
ORDER_DATE_INDEX = 1

def registerCustomerInfo() -> int:
	customerName = inputSQLData("Enter customer name: ")
	customerEmail = inputSQLData("Enter customer email: ")
	customerPhone = inputSQLData("Enter customer phone: ")
	if (canCreateCustomer(customerEmail, customerPhone)):
		return postCustomer(customerName, customerEmail, customerPhone)
	else:
		print("Customer already exists")


def legalInput(customerName: str, customerEmail: str, customerPhone: str) -> bool:
    if (customerName == "" or customerEmail == "" or customerPhone == ""):
        print("Illegal input due to: blank input")
        return False
    if all(not char.isalpha() and not char.isspace() for char in customerName):
        print("Illegal input due to: Name must be alphabetic or space")
        return False
    if (customerPhone.isdigit() == False):
        print("Illegal input due to: Name must be alphabetic and phone number must be numeric")
        return False
    if (customerEmail.find("@") == -1 or customerEmail.find(".") == -1):
        print("Illegal input due to: Email must contain @ and .")
        return False
    if (len(customerPhone) < 8):
        print("Illegal input due to: Phone number must be at least 8 digits")
        return False
    return True

def postCustomer(customerName: str, customerEmail: str, customerPhone: str) -> int:
	if (legalInput(customerName, customerEmail, customerPhone) == False or canCreateCustomer(customerEmail, customerPhone) == False):
		print("Registration failed!")
		return
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("INSERT INTO Kunde (Navn, Email, TlfNr) VALUES (?,?,?)", (customerName, customerEmail, customerPhone))
	connection.commit()
	connection.close()
	print("Registration successful!")
	return getCustomer(customerEmail)

def canCreateCustomer(customerEmail: str, customerPhone: str) -> bool:
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Kunde WHERE Epost =:customerEmail OR TlfNr =:customerPhone;", {"customerEmail": customerEmail, "customerPhone": customerPhone})
	result = cursor.fetchall()
	connection.close()
	return len(result) == 0

def login() -> int:
	customerEmail = inputSQLData("Enter email to login: ")
	return getCustomer(customerEmail)

def getCustomer(customerEmail: str) -> int:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT Kundenummer FROM Kunde WHERE Epost =:customerEmail", {"customerEmail": customerEmail})
	result = cursor.fetchone()
	connection.close()
	return result


def printFutureOrdersAndTickets(identificator) -> None:
	# Get all orders
	CustomerID = getCustomerNrByMailOrPhone(identificator)
	if CustomerID == -1:
		print("We couldn't find a user with this mail or phone number")
	history: list = getCustomerHistory(CustomerID)
	orderToTicket: dict = {}

	for order in history:
		orderToTicket[order] = getCustomerTicketBy(order[ORDERID_INDEX])


	for order in orderToTicket:
		tickets: list = orderToTicket[order]
		futureTickets: list = []

		# Check for each ticket that it is in the ticket is in the future
		for ticket in tickets:
			if (getDateOfTicket(ticket[ORDER_DATE_INDEX]) > datetime.now()): #I do not know if it is possible to compare a datetime object with a string
				futureTickets.append(ticket)
		print("Ordernummer: " + str(order[ORDERID_INDEX]) + " Order date: " + str(order[ORDER_DATE_INDEX]))

		for futureTicket in futureTickets:
			printTicket(futureTicket)

def getCustomerHistory(CustomerID: str) -> list:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM KundeOrdre WHERE Kundenummer =:CustomerID", {"CustomerID": CustomerID})
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

def getCustomerTicketBy(CustomerOrderID: str) -> list:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Billett WHERE OrdreNummer =:CustomerOrderID", {"CustomerOrderID": CustomerOrderID})
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

def getDateOfTicket(tripID: str) -> datetime:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT TurDato FROM Togtur WHERE TurID =:tripID", {"tripID": tripID})
	result = cursor.fetchone()
	connection.commit()
	connection.close()
	date: str = result[0]
	return datetime.strptime(date, "%Y-%m-%d")

def printTicket(ticket: list) -> None:
	print("Ticket with id " + str(ticket[1]) + " for trip with id: " + str(ticket[0]) + " going the " + str(getDateOfTicket(ticket[0])) + " with seat number: " + str(ticket[3]) + " and wagon number: " + str(ticket[4]))

def insertOrder():
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	postCustomer("Sverre", "sverre.nystad@gmail.com", "12345678")
	cursor.execute("INSERT INTO KundeOrdre (Ordrenummer, KjoepsTidspunkt, Kundenummer) VALUES (1, '2023-5-1', 1)")
	cursor.execute("INSERT INTO Billett (TurID, BillettID, OrdreNummer, PlassNummer, VognNummer) VALUES (1,1,1,2,2)")
	cursor.execute("SELECT * FROM KundeOrdre")
	connection.commit()
	connection.close()
#insertOrder()

def getCustomerNrByMailOrPhone(identificator: str) -> int:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	#Har vi check slik at email må ha @ og tlf nr ikke kan ha @? Er bra å ha for denne spørringen
	cursor.execute("SELECT Kundenummer FROM Kunde WHERE Kunde.Email=:id OR Kunde.TlfNr=:id", {"id": identificator})
	a=cursor.fetchone()
	if a==None:
		return -1
	return a[0]
if __name__ == "__main__":
	# print(canCreateCustomer("sverre.nystad@gmail.com", "12345678"))
	# postCustomer("Sverre", "sverre.nystad@gmail.com", "12345678")
	# print(canCreateCustomer("sverre.nystad@gmail.com", "12345678"))
	printFutureOrdersAndTickets("sverre.nystad@gmail.com")



