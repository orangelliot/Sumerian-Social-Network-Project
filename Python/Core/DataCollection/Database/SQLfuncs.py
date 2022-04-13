from getpass import getpass
from mysql.connector import connect, Error

class SQLfuncs(object):
    connection = None

    def __init__(self, hostname, username, userpassword):
        try:
            self.connection = connect(
                host=hostname,
                user=username,
                password=userpassword,
                database='sumerianDB'
            )
            print('Connection to sumerian-social-network successful')
        except Error as e:
            print(f"The error '{e}' occurred")

    def addNameToTab(self, name, tabid):
        cursor = self.connection.cursor()
        addNameQuery = 'INSERT INTO rawnames (name, tabid) VALUES (\'' + name + '\', \'' + tabid + '\');'
        try:
            cursor.execute(addNameQuery)
            self.connection.commit()
            #print('Added name successfuly')
        except Error as e:
            print(f"The error '{e}' occurred")

    def addYearToTab(self, year, tabid):
        cursor = self.connection.cursor()
        addYearQuery = 'INSERT INTO rawyears (year, tabid) VALUES (' + year + ', ' + tabid + ');'
        try:
            cursor.execute(addYearQuery)
            self.connection.commit()
            #print('Added year successfuly')
        except Error as e:
            print(f"The error '{e}' occurred")

    def getAttribute(self, relation, attribute):
        cursor = self.connection.cursor()
        getAttributeQuery = 'SELECT ' + attribute + ' FROM ' + relation + ';'
        try:
            data = cursor.execute(getAttributeQuery)
            print('Fetched data successfuly')
            return data
        except Error as e:
            print(f"The error '{e}' occurred")