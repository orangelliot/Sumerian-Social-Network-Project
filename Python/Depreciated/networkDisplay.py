# Nicholas J Uhlhorn
# February 2022

from multiprocessing.connection import wait
import networkx as nx
import matplotlib.pyplot as plt
import sys
import openpyxl

# Grab the tablets from file
data = openpyxl.load_workbook("out.xlsx")
data_sheet = data.worksheets[0]

edgeList = []

# add the tablets to reference eachother
current_row = 0
for row in data_sheet.values:
    current_row += 1
    print(str(current_row) + ":" + str(len(edgeList)), end = '\r')
    for tablet_index_a in range(1, len(row)):
        if row[tablet_index_a] is None:
            continue
        for tablet_index_b in range(tablet_index_a+1, len(row)):
            if row[tablet_index_b] is None:
                continue
            edgeList.append((row[tablet_index_a], row[tablet_index_b], 1))
print(str(current_row))

# make network visual

G = nx.Graph()
G.add_weighted_edges_from(edgeList)
f = plt.figure()
subax1 = f.add_subplot(121)
nx.draw(G, ax=subax1)
f.savefig("wholeGraph.png")

