#Elliot Fisk: create formatting for edgelist CSVs for ambig years

import csv
from Database.SQLfuncs import SQLfuncs

CULLING_SIZE=1000

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

net_csv = open(f'ambig_tablet_net{CULLING_SIZE}f.csv', 'w', newline='')
net_writer = csv.writer(net_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

ambig_tabs = db.execute_select(f"select tabids.seqid from ambigtabs{CULLING_SIZE} join tabids on ambigtabs{CULLING_SIZE}.tabid = tabids.tabid;")
for i in range(len(ambig_tabs)):
    ambig_tabs[i] = ambig_tabs[i][0]

num_tabs = db.execute_select(f'select count(tabid) from tabids{CULLING_SIZE};')[0][0]
years = db.execute_select(f'select seqnum from tabids{CULLING_SIZE} left join (bestyears join cdliyears on bestyears.year = cdliyears.kingnum) on tabids{CULLING_SIZE}.tabid = bestyears.tabid')

print(len(years))
print(num_tabs)

for i in ambig_tabs:
    for j in range(num_tabs):
        year = years[j][0]
        if year == None:
            year = -1
        net_writer.writerow([i, (j + 1), 0, year])
    print("%d/%d" % (i, len(ambig_tabs)), end='\r')