import sqlite3


DATABASE_NAME: str = 'Nordlandsbanen.db'

def setup() -> None:
    # Create all tables
    createTablesSql: str = ''
    with open('DB2Nordlandsbanen.sql', 'r') as file:
        createTablesSql = file.read()

    insertDataSql: str = ''
    with open('allDataForUserStories.sql', 'r') as file:
        insertDataSql = file.read()
    
    # Create a connection to the database
    connection = sqlite3.connect(DATABASE_NAME)
    # Create a cursor to execute SQL commands
    cursor = connection.cursor()
    cursor.executescript(createTablesSql)

    if (isEmpty()):
        cursor.executescript(insertDataSql)

    connection.commit()
    connection.close()

def isEmpty() -> bool:
    # Create a connection to the database
    connection = sqlite3.connect(DATABASE_NAME)
    # Create a cursor to execute SQL commands
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Stasjon")
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return len(result) == 0

if (__name__ == '__main__'):
    setup()