from Database.SQLfuncs import SQLfuncs

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

tablets = db.execute_query("select distinct tabid from tabids;")
counter = 1
fails = 0
for i in range(len(tablets)):
    tablets[i] = int(tablets[i][0][1:])-100000
    if tablets[i] != counter:
        print('failed for tablet ', tablets[i], ' fails = ', fails)
        counter = tablets[i]
        fails += 1
    counter += 1
