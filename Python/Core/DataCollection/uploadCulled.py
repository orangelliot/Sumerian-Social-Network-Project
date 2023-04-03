# Uploaded Culled 
# October 2022
# Elliot Fisk
# ---------------
# TODO synopsis and comments v below v

import pandas as pd
import multiprocessing as mp
from Database.SQLfuncs import SQLfuncs

CULLING_SIZE = 1000

culled_set_df = pd.read_csv(f'tablets_culled_{CULLING_SIZE}.csv')
culled_set = culled_set_df.Tabid.values.tolist()
db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

progress = 1
set_size = len(culled_set)
for tabid in culled_set:
    db.execute_insert(f'insert into tabids{CULLING_SIZE} values (' + str(progress) + ', \'' + tabid + '\');')
    print("%d/%d" % (progress, set_size), end='\r')
    progress += 1