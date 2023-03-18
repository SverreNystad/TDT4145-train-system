from datetime import datetime
import sqlite3

from database_config import DATABASE_NAME;

DATABASE: str = DATABASE_NAME
ORDER_DATE_INDEX = 1


def registerCustomerInfo():
	customerName = input("Enter customer name: ")
	customerEpost = input("Enter customer epost: ")
	customerPhone = input("Enter customer phone: ")
	postCustomer(customerName, customerEpost, customerPhone)


def legalInput(customerName: str, customerEpost: str, customerPhone: str) -> bool:
    if (customerName == "" or customerEpost == "" or customerPhone == ""):
        return False
    if (customerName.isalpha() == False or customerPhone.isdigit() == False):
        return False
    if (customerEpost.find("@") == -1 or customerEpost.find(".") == -1 or customerEpost.find("@") > customerEpost.find(".")):
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
	cursor.execute("INSERT INTO Kunde (Navn, Epost, TlfNr) VALUES (Navn =:customerName, Epost =:customerEpost, TlfNr =:customerPhone)", {"customerName": customerName, "customerEpost": customerEpost, "customerPhone": customerPhone})

	# cursor.execute("INSERT INTO Kunde (Navn, Epost, TlfNr) VALUES (?,?,?)", (customerName, customerEpost, customerPhone))
	connection.commit()
	connection.close()

def login() -> int:
	customerEpost = input("Enter epost to login: ")
	return getCustomer(customerEpost)

def getCustomer(customerEpost: str) -> int:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT KundeID FROM Kunde WHERE Epost =:customerEpost", {"customerEpost": customerEpost})
	result = cursor.fetchone()
	connection.close()
	return result


def getCustomerHistory(CustomerID: str) -> list:
	# Create a connection to the database
	connection = sqlite3.connect(DATABASE)
	# Create a cursor to execute SQL commands
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM KundeOrdre WHERE KundeID =:CustomerID", {"CustomerID": CustomerID})
	result = cursor.fetchall()
	connection.commit()
	connection.close()
	return result

def getFutureOrders(CustomerID: str) -> list:
	history: list = getCustomerHistory(CustomerID)
	futureOrders: list = []

	for order in history:
		if (order[ORDER_DATE_INDEX] > datetime.now()): # I do not know if it is possible to compare a datetime object with a string
			futureOrders.append(order)
	return futureOrders