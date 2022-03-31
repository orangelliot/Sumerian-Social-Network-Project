from getpass import getpass
from mysql.connector import connect, Error
import os

try:
    with connect(
        host='localhost',
        user=input('enter username: '),
        password=getpass('enter password: '),
    ) as connection:
        createCDLIyears = '''CREATE TABLE cdliyears (
            cdliname varchar(255) not null,
            kingnum varchar(63) not null,
            seqnum int not null,
            PRIMARY KEY (kingnum)
            );'''
        createTabids = '''CREATE TABLE tabids (
            tabid char(128) not null,
            simmetric float,
            numnames int,
            numyears int,
            kingnum varchar(63),
            PRIMARY KEY (tabid),
            FOREIGN KEY (kingnum) REFERENCES cdliyears (kingnum)
            );'''
        createRawnames = '''CREATE TABLE rawnames (
            name varchar(255) not null,
            tabid char(128) not null,
            FOREIGN KEY (tabid) REFERENCES tabids (tabid)
            );'''
        createRawyears = '''CREATE TABLE rawyears (
            year varchar(255) not null,
            tabid char(128) not null,
            FOREIGN KEY (tabid) REFERENCES tabids (tabid)
            );'''
        with connection.cursor() as cursor:
            cursor.execute('DROP DATABASE sumeriantabdb;')
            cursor.execute('CREATE DATABASE sumeriantabdb;')
            cursor.execute('USE sumeriantabdb;')
            cursor.execute(createCDLIyears)
            cursor.execute(createTabids)
            tablets = os.listdir(os.getcwd() + '/Translated/')
            numTablets = len(tablets)
            currentTablet = 0
            for tabid in tablets:
                currentTablet += 1
                print("%d/%d" % (currentTablet, numTablets), end="\r")
                cursor.execute('INSERT INTO tabids (tabid) VALUES (\'' + tabid[0:7] + '\')')
            print("%d/%d" % (currentTablet, numTablets))
            cursor.execute(createRawnames)
            cursor.execute(createRawyears)
        

except Error as e:
    print(e)