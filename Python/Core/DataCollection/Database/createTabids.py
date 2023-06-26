from Database.SQLfuncs import SQLfuncs
import os
db = SQLfuncs('localhost', 'root', 'admin2019')
tablets = os.listdir(os.getcwd() + '/Dataset/Translated/')
num_tablets = len(tablets)
cur_tab = 0

for tabid in tablets:
    cur_tab += 1
    if((cur_tab % 500) == 0):
        print("%d/%d" % (cur_tab, num_tablets), end="\r")
    db.execute_insert('INSERT INTO tabids (seqid, tabid) VALUES (' + str(cur_tab) + ', \'' + tabid[0:7] + '\')')
print("%d/%d" % (cur_tab, num_tablets))