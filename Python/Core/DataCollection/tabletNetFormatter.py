import csv
from Database.SQLfuncs import SQLfuncs

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

net_csv = open('tablet_net100f.csv', 'w', newline='')
net_writer = csv.writer(net_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

num_tabs = db.execute_select('select count(tabid) from tabids100;')[0][0]
header = list(range(num_tabs))
header = list(map(str, header))
header[0] = 'seq_num'

net_writer.writerow(header)

print(num_tabs)
for i in range(num_tabs):
    i += 1
    row = list([0]) * (num_tabs)
    row[0] = i
    net_writer.writerow(row)
    print("%d/%d" % (i, num_tabs), end='\r')