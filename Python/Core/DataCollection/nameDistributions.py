import matplotlib.pyplot as plt
import os
from Database.SQLfuncs import SQLfuncs

db = SQLfuncs('localhost', 'root', 'admin2019')

namexyear = db.execute_select('select a.name, metayears.bestyear from (((select * from metanames order by count desc limit 250) as a left join rawnames on a.name = rawnames.name) left join rawyears on rawnames.tabid = rawyears.tabid) left join metayears on rawyears.year = metayears.year order by name;')

cdliyears = db.execute_select('select kingid from cdliyears order by seqid asc;')
for i in range(len(cdliyears)):
    cdliyears[i] = cdliyears[i][0]

yearcounts = {}
for key in cdliyears:
    yearcounts[key] = 0

index = 0
lastname = 'start'
for tuple in namexyear:
    currentname = tuple[0]
    if lastname != 'start' and currentname != lastname:
        print(f'finished processing {lastname}                          ')
        vals = list(yearcounts.values())
        vals = str(vals).replace('[','').replace(']','')
        db.execute_insert(f'insert into namedists values (\'{currentname}\', {vals});')
        for key in cdliyears:
            yearcounts[key] = 0
        index += 1
    if tuple[1] != None:
        try:
            yearcounts[tuple[1]] += 1
        except:
            print(f'error occured for {tuple[1]}')
    lastname = currentname