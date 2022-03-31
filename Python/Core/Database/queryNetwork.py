# Simon Ellis
# Reference from Nicholas Uhlhorn's networkDisplay.py
# February 2022

from multiprocessing.connection import wait
import networkx as nx
import matplotlib.pyplot as plt
import sys
import openpyxl

print(len(sys.argv))
if len(sys.argv) < 2:
    print("Error: Incorrect number of arguments")
    print("Usage: queryNetwork.py [nameToQuery]")
    exit(0)

# Grab the tablets from file
data = openpyxl.load_workbook("out.xlsx")
data_sheet = data.worksheets[0]

edgeList = []

# add the tablets to reference eachother
current_row = 0
for name_index in range(1, len(sys.argv)):
    print("Checking for name: " + sys.argv[name_index])
    for row in data_sheet.values:
        current_row += 1
        print(str(current_row) + ":" + str(len(edgeList)), end = '\r')
        
        if row[0] == sys.argv[name_index]:
            print("Found name: " + sys.argv[name_index] + " at row " + str(current_row))
            for tablet_index_a in range(1, len(row)):
                if row[tablet_index_a] is None:
                    continue
                for tablet_index_b in range(tablet_index_a+1, len(row)):
                    if row[tablet_index_b] is None:
                        continue
                    edgeList.append((row[tablet_index_a], row[tablet_index_b], 1))
            break
        
print(str(current_row))

# make network visual

G = nx.Graph()
G.add_weighted_edges_from(edgeList)
f = plt.figure()
subax1 = f.add_subplot(121)
nx.draw(G, ax=subax1)
f.savefig("output_graph.png")

