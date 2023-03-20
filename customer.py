from datetime import datetime
import sqlite3

from database_config import DATABASE_NAME
from inputHandler import inputSQLData;

DATABASE: str = DATABASE_NAME
ORDERID_INDEX = 0
ORDER_DATE_INDEX = 1


def registerCustomerInfo():
	customerName = inputSQLData("Enter customer name: ")
	customerEpost = inputSQLData("Enter customer epost: ")
	customerPhone = inputSQLData("Enter customer phone: ")
	if (canCreateCustomer(customerEpost, customerPhone)):
		postCustomer(customerName, customerEpost, customerPhone)
	else:
		print("Customer already exists")


def legalInput(customerName: str, customerEpost: str, customerPhone: str) -> bool:
    if (customerName == "" or customerEpost == "" or customerPhone == ""):
        return False
    if (customerName.isalpha() == False or customerPhone.isdigit() == False):
        return False
    if (customerEpost.find("@") == -1 or customerEpost.find(".") == -1):
        return False
    return True

def postCustomer(customerName: str, customerEpost: str, customerPhone: str) -> None:
	if (legalInput(customerName, customerEpost, customerPhone) == False):
		print("Illegal input detected. Registration failed.")
		return
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	# cursor.execute("INSERT INTO Kunde (Navn, Epost, TlfNr) VALUES (customerName, customerEpost, customerPhone);", {"customerName": customerName, "customerEpost": customerEpost, "customerPhone": customerPhone})
	cursor.execute("INSERT INTO Kunde (Navn, Epost, TlfNr) VALUES (?,?,?)", (customerName, customerEpost, customerPhone))
	connection.commit()
	connection.close()

def canCreateCustomer(customerEpost: str, customerPhone: str) -> bool:
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Kunde WHERE Epost =:customerEpost OR TlfNr =:customerPhone;", {"customerEpost": customerEpost, "customerPhone": customerPhone})
	result = cursor.fetchall()
	connection.close()
	return len(result) == 0

def login() -> int:
	customerEpost = inputSQLData("Enter epost to login: ")

	return getCustomer(customerEpost)

def getCustomer(customerEpost: str) -> int:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT Kundenummer FROM Kunde WHERE Epost =:customerEpost", {"customerEpost": customerEpost})
	result = cursor.fetchone()
	connection.close()
	return result

def getFutureTickets(CustomerID: str) -> list:
	# Get all orders
	history: list = getCustomerHistory(CustomerID)
	orderToTicket: dict = {}

	for order in history:
		orderToTicket[order] = getCustomerTicketBy(order[ORDERID_INDEX])

	futureTickets: list = []

	for order in orderToTicket:
		tickets: list = orderToTicket[order]

		# Check for each ticket that it is in the ticket is in the future
		for ticket in tickets:
			if (ticket[ORDER_DATE_INDEX] > datetime.now()): # I do not know if it is possible to compare a datetime object with a string
				futureTickets.append(ticket)
	
	return futureTickets

def printFutureOrdersAndTickets(CustomerID: str) -> None:
	# Get all orders
	history: list = getCustomerHistory(CustomerID)
	orderToTicket: dict = {}

	for order in history:
		orderToTicket[order] = getCustomerTicketBy(order[ORDERID_INDEX])


	for order in orderToTicket:
		tickets: list = orderToTicket[order]
		futureTickets: list = []

		# Check for each ticket that it is in the ticket is in the future
		for ticket in tickets:
			if (ticket[ORDER_DATE_INDEX] > datetime.now()): # I do not know if it is possible to compare a datetime object with a string
				futureTickets.append(ticket)
		print("Ordernummer: " + order[ORDERID_INDEX] + " Order date: " + order[ORDER_DATE_INDEX])

		for futureTicket in futureTickets:
			print("Ticket: " + futureTicket)

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

def getCustomerTicketBy(CusomerOrderId: str) -> list:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Billett WHERE OrdreNummer =:CustomerOrderID", {"CustomerOrderID": CusomerOrderId})
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

if __name__ == "__main__":
	print(canCreateCustomer("sverre.nystad@gmail.com", "12345678"))
	postCustomer("Sverre", "sverre.nystad@gmail.com", "12345678")
	print(canCreateCustomer("sverre.nystad@gmail.com", "12345678"))



