import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# make a new spreadsheet where each tablet has all tablet relations on the same row
# formatted like: [tablet][relatedTablet][numRelations][relatedTablet][numRelations][...]
# use that sheet to generate an edgeList
edgeList = [(1, 2, 0.5), (2, 3, 0.8), (1, 4, 0.2), (2, 4, 0.9), (5, 3, 0.7), (3, 4, 0.3)]

G.add_weighted_edges_from(edgeList)
f = plt.figure()
subax1 = f.add_subplot(121)
nx.draw(G, ax=subax1)
f.savefig("graph.png")
