import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import os

net_df = pd.read_csv(f'ambignetv3.csv')
net_df = net_df.to_numpy()

tablet = net_df[0][0]
finalvals = [[tablet,0,0]]
totalconnections = 0
samples = 0
for i in range(len(net_df)):
    if net_df[i][2] == 'ambiguous':
        continue
    if net_df[i][0] != tablet:
        finalvals[-1][1] = finalvals[-1][1]/totalconnections
        finalvals[-1][2] = samples
        print(finalvals[-1])
        tablet = net_df[i][0]
        totalconnections = 0
        samples = 0
        finalvals.append([tablet,0,0])
    mult = -1
    if net_df[i][3] < 50:
        mult = 1/(1+math.e**(-0.5*((net_df[i][3])-40)))
        #print(net_df[i][3],mult)
    else:
        mult = (-1/(1+math.e**(-0.5*((net_df[i][3])-60))))+1
        #print(net_df[i][3],mult)
    samples += net_df[i][1]
    weight = net_df[i][1]*(net_df[i][5]/100)*mult
    finalvals[-1][1] += net_df[i][3]*weight
    totalconnections += weight


avgyears = []
for i in range(len(finalvals)):
    avgyears.append(finalvals[i][1])

counts, bins = np.histogram(avgyears, bins=20, range=(38,56))
plt.hist(bins[:-1], bins, weights=counts)
path = os.getcwd() + '/GraphicRepresentations/ambighist'
plt.savefig(path)

#amar-sin 6 is ~56
#sulgi 42 is ~44