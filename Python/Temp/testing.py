from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host='sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com',
        user=input('enter username: '),
        password=getpass('enter password: '),
        database='sumerianDB'
    ) as connection:
        show_db_query = "SHOW DATABASES"
        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)
except Error as e:
    print(e)