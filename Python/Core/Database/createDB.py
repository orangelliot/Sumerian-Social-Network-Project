#Elliot Fisk, generate SQL database

from getpass import getpass
from mysql.connector import connect, Error
import os

try:
    with connect(
        host='sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com',
        user=input('enter username: '),
        password='2b928S#%',
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
            cursor.execute('DROP DATABASE sumerianDB;')
            cursor.execute('CREATE DATABASE sumerianDB;')
            cursor.execute('USE sumerianDB;')
            cursor.execute(createCDLIyears)
            cursor.execute(createTabids)
            tablets = os.listdir(os.getcwd() + '/Dataset/Translated/')
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