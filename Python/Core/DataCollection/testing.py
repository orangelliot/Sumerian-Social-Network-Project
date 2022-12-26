from Database.SQLfuncs import SQLfuncs
import numpy as np
import pandas as pd

ambignet = pd.read_csv("ambignetv1.csv")
cdliyears = pd.read_csv("cdliyears.csv")

ambignet = ambignet.to_numpy()
cdliyears = cdliyears.to_numpy()
ambignet = np.hstack((ambignet, np.zeros((len(ambignet), 1))))

for i in range(len(ambignet)):
    year = ambignet[i][2]
    for j in range(len(cdliyears)):
        if year == cdliyears[j][1]:
            ambignet[i][3] = cdliyears[j][2]

df = pd.DataFrame(ambignet, columns=['tab1','count(name)','year','seqnum'])
df.to_csv('ambignetv2.csv', index=False)