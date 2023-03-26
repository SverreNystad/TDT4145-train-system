from datetime import datetime
import sqlite3

from database_config import DATABASE_NAME
from inputHandler import inputSQLData, previewDate;

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
        print("Customer already exists.")


def legalInput(customerName: str, customerEmail: str, customerPhone: str) -> bool:
    if (customerName == "" or customerEmail == "" or customerPhone == ""):
        print("Illegal input due to: blank input")
        return False
    if all(not char.isalpha() and not char.isspace() for char in customerName):
        print("Illegal input due to: Name must only contain letters or spaces")
        return False
    if (customerPhone.isdigit() == False):
        print("Illegal input due to: Phone number must only contain numbers")
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
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Kunde (Navn, Epost, TlfNr) VALUES (?,?,?)", (customerName, customerEmail, customerPhone))
    connection.commit()
    connection.close()
    print("Registration successful!")
    return getCustomer(customerEmail)

def canCreateCustomer(customerEmail: str, customerPhone: str) -> bool:
    """
    Checks if a customer with the given email or phone number already exists.
    """
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Kunde
    WHERE Epost =:customerEmail OR TlfNr =:customerPhone;""",
    {"customerEmail": customerEmail, "customerPhone": customerPhone})
    customerExists = cursor.fetchall()
    connection.close()
    return len(customerExists) == 0

def login() -> int:
    customerEmail = inputSQLData("Enter email to login: ")
    return getCustomer(customerEmail)

def getCustomer(customerEmail: str) -> int:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT Kundenummer FROM Kunde
    WHERE Epost =:customerEmail""",
    {"customerEmail": customerEmail})
    customer = cursor.fetchone()
    connection.close()
    return customer

def printFutureOrdersAndTickets(CustomerID) -> None:
    # Get all orders
    history: list = getCustomerOrderHistory(CustomerID)
    orderToTicket: dict = {}

    for order in history:
        orderToTicket[order] = getCustomerTicketByOrder(order[ORDERID_INDEX])

    for order in orderToTicket:
        tickets: list = orderToTicket[order]
        futureTickets: list = []

        # Check each ticket that it is in the future
        for ticket in tickets:
            if (getDateOfTicket(ticket[ORDER_DATE_INDEX]) > datetime.now()):
                futureTickets.append(ticket)
        print("Ordernumber: " + str(order[ORDERID_INDEX]) + ", Order date: " + str(order[ORDER_DATE_INDEX]))

        for futureTicket in futureTickets:
            printTicket(futureTicket)
        
        print()

def getCustomerOrderHistory(CustomerID: str) -> list:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM KundeOrdre
    WHERE Kundenummer =:CustomerID""",
    {"CustomerID": CustomerID})
    allOrders = cursor.fetchall()
    connection.close()
    return allOrders

def getCustomerTicketByOrder(CustomerOrderID: str) -> list:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Billett
    WHERE OrdreNummer =:CustomerOrderID""", {"CustomerOrderID": CustomerOrderID})
    allTickets = cursor.fetchall()
    connection.close()
    return allTickets

def getDateOfTicket(tripID: str) -> datetime:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT TurDato FROM Togtur
    WHERE TurID =:tripID""", {"tripID": tripID})
    ticketDate = cursor.fetchone()
    connection.close()
    date: str = ticketDate[0]
    return datetime.strptime(date, "%Y-%m-%d")

def printTicket(ticket: list) -> None:
    startStation, endStation = getStartAndStopStation(ticket[0], ticket[1])
    print(f"Ticket for trip {ticket[0]} going from {startStation} to {endStation} the {previewDate(str(getDateOfTicket(ticket[0])))} with seat number {ticket[3]} and wagon number {ticket[4]}")

def getStartAndStopStation(tripID, ticketID):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""SELECT Stasjonsnavn FROM BillettStopperVed
    WHERE TurID =:TripID AND BillettID =:TicketID
    ORDER BY StasjonsNummer""", {"TripID": tripID, "TicketID": ticketID})
    stations = cursor.fetchall()
    connection.close()
    return stations[0][0], stations[-1][0]
