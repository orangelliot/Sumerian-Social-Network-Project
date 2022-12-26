import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

CULLING_SIZE = 1000

net_df = pd.read_csv(f'ambignetv2.csv')
net_df = net_df.to_numpy()

tablet = net_df[0][0]
finalvals = [[tablet,0]]
totalconnections = 0
for i in range(len(net_df)):
    if net_df[i][2] == 'ambiguous':
        continue
    if net_df[i][0] != tablet:
        finalvals[-1][1] = finalvals[-1][1]/totalconnections
        #print(finalvals[-1])
        tablet = net_df[i][0]
        totalconnections = 0
        finalvals.append([tablet,0])
    finalvals[-1][1] += net_df[i][1]*net_df[i][3]
    totalconnections += net_df[i][1]

avgyears = []
for i in range(len(finalvals)):
    avgyears.append(finalvals[i][1])

counts, bins = np.histogram(avgyears, bins=20, range=(38,56))
plt.hist(bins[:-1], bins, weights=counts)
path = os.getcwd() + '/GraphicRepresentations/ambighist'
plt.savefig(path)
#amar-sin 6 is ~56
#sulgi 42 is ~44