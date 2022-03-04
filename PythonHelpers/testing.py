import networkx as nx
import matplotlib.pyplot as plt
from difflib import SequenceMatcher

print('TESTTESTTESTESTTESTTEST\n'+ str(SequenceMatcher(None, "mu ... 4(disz) ab2 mah2 6(disz) gu4-ab2 2(u) 2(disz) ab2 amar-ga 6(disz) gu4 amar-ga 3(u) 8(disz) gu4 ab2 amar-hi-a nig2-szu utu-sipa ", "mu sul-gi nita kal-ga lugal an ub-da limmu2-ba-ke4 si-mu-ur4-umki a-ra2 2-kam-as mu-hul-a mu us2-sa-bi").ratio()) + '\nTESTTESTTESTESTTESTTEST\n')

if True:
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
