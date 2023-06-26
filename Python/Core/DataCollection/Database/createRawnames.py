from Database.SQLfuncs import SQLfuncs
import os
import pandas as pd
import numpy as np

cdliyears = pd.read_csv(os.getcwd()+'/rawnames.csv')
cdliyears = cdliyears.values.tolist()
db = SQLfuncs('localhost', 'root', 'admin2019')

for tuple in cdliyears:
    db.execute_insert('INSERT INTO rawnames (tabid, name) values (\'' + tuple[1] + '\', \'' + tuple[0] + '\')')