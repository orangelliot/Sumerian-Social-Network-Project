import matplotlib.pyplot as plt
import os
from Core.DataCollection.Database.SQLfuncs import SQLfuncs

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
    print(f'processing {tuple}              ', end="\r")
    currentname = tuple[0]
    if lastname != 'start' and currentname != lastname:
        print(f'finished processing {lastname}                      ')
        plt.bar(list(yearcounts.keys()), yearcounts.values())
        path = os.getcwd() + f'/GraphicRepresentations/NameDistributions/name{tuple[0].replace(".","").replace("|","")+str(index)}'
        plt.savefig(path)
        plt.clf()
        for key in cdliyears:
            yearcounts[key] = 0
        index += 1
    if tuple[1] != None:
        try:
            yearcounts[tuple[1]] += 1
        except:
            print(f'error occured for {tuple[1]}')
    lastname = currentname