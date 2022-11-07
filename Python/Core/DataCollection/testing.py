from Database.SQLfuncs import SQLfuncs

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

entries = db.execute_select("select distinct tabids1000.tabid, ambig.year from tabids1000 join (rawnames join (select tabid, year from bestyears where bestyears.year in ('amar-sin 6a', 'amar-sin 6b', 'sulgi 42a', 'sulgi 42b')) as ambig on rawnames.tabid = ambig.tabid) on tabids1000.tabid = rawnames.tabid;")
for i in range(len(entries)):
    db.execute_insert(f"insert into ambigtabs1000 values ({i + 1}, '{entries[i][0]}', '{entries[i][1]}');")