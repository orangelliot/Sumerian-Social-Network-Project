from Database.SQLfuncs import SQLfuncs
import shutil
import os

path = os.getcwd() + '/Dataset/'
CULLING_SIZE = 1000

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
ambigtabs = db.execute_select(f'select tabid from ambigtabs{CULLING_SIZE};')
for i in range(len(ambigtabs)):
    ambigtabs[i] = ambigtabs[i][0] + '.conll'

for file in ambigtabs:
    shutil.copy(path + 'Translated/' + file, path + 'AmbigTablets/')