from getpass import getpass
from mysql.connector import connect, Error

def createConnection(hostname, username, userpassword):
    connection = None
    try:
        connection = connect(
            host=hostname,
            user=username,
            password=userpassword,
            database='sumeriantabdb'
        )
        print('Connection to MySQL DB successful')
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def addNameToTab(connection, name, tabid):
    cursor = connection.cursor()
    addNameQuery = 'INSERT INTO rawnames (name, tabid) VALUES (' + name + ', ' + tabid + ');'
    try:
        cursor.execute(addNameQuery)
        connection.commit()
        print('Added name successfuly')
    except Error as e:
        print(f"The error '{e}' occurred")
