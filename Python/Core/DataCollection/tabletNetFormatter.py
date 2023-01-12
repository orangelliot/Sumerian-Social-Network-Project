# Tablet Net Formatter
# October 2022
# Elliot Fisk
# ---------------
# TODO synopsis and comments v below v

import csv
from Database.SQLfuncs import SQLfuncs

CULLING_SIZE=1000

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

net_csv = open(f'tablet_net{CULLING_SIZE}f.csv', 'w', newline='')
net_writer = csv.writer(net_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

num_tabs = db.execute_select(f'select count(tabid) from tabids{CULLING_SIZE};')[0][0]

for i in range(num_tabs):
    for j in range((i + 1), num_tabs):
        net_writer.writerow([(i + 1), (j + 1), 0, -1])
    print("%d/%d" % (i, num_tabs), end='\r')