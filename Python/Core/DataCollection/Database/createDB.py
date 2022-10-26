#Elliot Fisk, generate SQL database

from getpass import getpass
from mysql.connector import connect, Error
import os

try:
    with connect(
        host='sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com',
        user='root',
        password='2b928S#%',
    ) as connection:
        createCDLIyears = '''CREATE TABLE cdliyears (
            cdliname varchar(255) not null,
            kingnum varchar(63) not null,
            seqnum int not null,
            PRIMARY KEY (kingnum)
            );'''
        createTabids = '''CREATE TABLE tabids (
            seqid int not null,
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
        createBestyears = '''CREATE TABLE bestyears (
            year varchar(255) not null,
            tabid char(128) not null,
            similarity float(16),
            FOREIGN KEY (tabid) REFERENCES tabids (tabid)
            );'''
        createTabids10 = '''CREATE TABLE tabids10 (
            seqid int not null,
            tabid char(128) not null,
            FOREIGN KEY (tabid) REFERENCES tabids (tabid));'''
        createTabids100 = '''CREATE TABLE tabids100 (
            seqid int not null,
            tabid char(128) not null,
            FOREIGN KEY (tabid) REFERENCES tabids (tabid));'''
        createTabids1000 = '''CREATE TABLE tabids1000 (
            seqid int not null,
            tabid char(128) not null,
            FOREIGN KEY (tabid) REFERENCES tabids (tabid));'''
        with connection.cursor() as cursor:
            #cursor.execute('DROP DATABASE sumerianDB;')
            #cursor.execute('CREATE DATABASE sumerianDB;')
            cursor.execute('USE sumerianDB;')
            #cursor.execute(createCDLIyears)
            #cursor.execute(createTabids)
            #tablets = os.listdir(os.getcwd() + '/Dataset/Translated/')
            #num_tablets = len(tablets)

            #for i in range(num_tablets):
            #    cursor.execute('update tabids (seqid) values (' + str(i) + ');')

            #cur_tab = 0
            #for tabid in tablets:
            #    cur_tab += 1
            #    if((cur_tab % 500) == 0):
            #        print("%d/%d" % (cur_tab, num_tablets), end="\r")
            #    cursor.execute('INSERT INTO tabids (seqid, tabid) VALUES (' + str(cur_tab) + ', \'' + tabid[0:7] + '\')')
            #print("%d/%d" % (cur_tab, num_tablets))
            #cursor.execute(createRawnames)
            #cursor.execute(createRawyears)
            #cursor.execute(createBestyears)
            cursor.execute(createTabids10)
            cursor.execute(createTabids100)
            cursor.execute(createTabids1000)
except Error as e:
    print(e)