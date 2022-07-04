import networkx as nx
import os
from Database.SQLfuncs import SQLfuncs

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

tablets = db.execute_query("select distinct tabid from tabids;")
for i in range(len(tablets)):
    tablets[i] = tablets[i][0]
tablet_network = nx.Graph()
tablet_network.add_nodes_from(tablets)

names = db.execute_query("select distinct name from rawnames;")
for i in range(len(names)):
    names[i] = names[i][0]
name_progress = 0
num_names = len(names)
for cur_name in names:
    cur_name = db.sanitizeInput(cur_name)
    tabs_with_name = db.execute_query("select distinct tabid from rawnames where name=\'" + cur_name + "\';")
    generated_edges = list()
    for i in range(len(tabs_with_name)):
        cur_tab = tabs_with_name.pop()[0]
        for tuple in tabs_with_name:
            cur_pair = [cur_tab, tuple[0]]
            generated_edges.append(cur_pair)
    edge_progress = 0
    num_edges = len(generated_edges)
    for edge in generated_edges:
        print("%d/%d   %d/%d" % (name_progress, num_names, edge_progress, num_edges), end='\r')
        try:
            tablet_network.edges[edge]["weight"] = tablet_network.edges[edge]["weight"] + 1
        except:
            tablet_network.add_edge(edge[0], edge[1], weight=1)
        edge_progress += 1
    name_progress += 1
