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
            #print('Connection to sumerian-social-network successful')
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_insert(self, query):
        cursor = self.connection.cursor()
        #print(query)
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")
            return None

    def execute_select(self, query):
        cursor = self.connection.cursor()
        #print(query)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"The error '{e}' occurred")
            return None

    def sanitize_input(self, input):
        out = ""
        for i in range(len(input)):
            out += input[i]
            if input[i] == '\'':
                out += '\''
        return out

    def close(self):
        self.connection.close()