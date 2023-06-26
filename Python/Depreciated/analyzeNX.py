from Database.SQLfuncs import SQLfuncs
import networkx as nx
from CSVToNX import CSVToNX

CULLING_SIZE=1000

G = CSVToNX(f'ambig_tablet_net{CULLING_SIZE}.csv').getNX()

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

ambigtablets = db.execute_select(f'select seqid from ambigtabs{CULLING_SIZE};')
for i in range(len(ambigtablets)):
    ambigtablets[i] = ambigtablets[i][0]

years = db.execute_select(f'select seqnum from tabids join (bestyears join cdliyears on bestyears.year = cdliyears.cdliname) on tabids.tabid = bestyears.tabid')
for i in range(len(years)):
    years[i] = years[i][0]
averageyear = []

for tablet in ambigtablets:
    sum = 0
    neighbors = G[tablet]
    for node in neighbors:
        sum += years[int(node) - 1]
    averageyear[int(tablet) - 1] = sum/len(neighbors)

for i in range(len(averageyear)):
    print(f'average year for tablet {i + 1} = {averageyear[i]}')