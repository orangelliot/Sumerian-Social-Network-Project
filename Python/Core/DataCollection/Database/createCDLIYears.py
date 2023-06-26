from Database.SQLfuncs import SQLfuncs
import os
import pandas as pd
import numpy as np

cdliyears = pd.read_csv(os.getcwd()+'/cdliyears.csv')
cdliyears = cdliyears.values.tolist()
db = SQLfuncs('localhost', 'root', 'admin2019')

for tuple in cdliyears:
    db.execute_insert('INSERT INTO cdliyears (seqid, kingid, year) values (' + str(tuple[2]) + ', \'' + tuple[1] + '\', \'' + tuple[0] + '\')')