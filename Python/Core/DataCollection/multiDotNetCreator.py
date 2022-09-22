import multiprocessing as mp
import pydot
import graphviz
from Database.SQLfuncs import SQLfuncs



db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

# get and clean up tablets, assign each a sequential ID
tablet_counter = 0
tablets = db.execute_query("select distinct tabid from tabids;")
for i in range(len(tablets)):
    tablets[i] = [tablet_counter, tablets[i][0]]
    tablet_counter += 1

# get and clean up names
names = db.execute_query("select distinct name from rawnames where name !='...' limit 4;")
for i in range(len(names)):
    names[i] = names[i][0]

# create DOT net and edge hash table
tablet_net = pydot.Dot('tablet_net', graph_type='graph',bgcolor='yellow')
hashed_edges = [list()]*tablet_counter

######################## HASHING FUNC ########################

def hash_to_edges(edge):
    hashing_loc = edge[0]
    for cur_edge in hashed_edges[hashing_loc]:
        if cur_edge == edge:
            cur_edge[2] +=  1
            return
    hashed_edges[hashing_loc].append(edge)
    
###################### EDGE CREATION FUNC ######################

#takes a name, collects all the tabids with that name and creates a pair for each of them,
#and then returns a list of these pairs for processing later
def tf_gather_edges(name):
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')
    query = "select distinct tabid from rawnames where name = \'" + name + "\';"
    tabs_with_name = db.execute_query(query)
    raw_edges = list()
    while len(tabs_with_name) > 1:
        edge_progress = 0
        cur_tab = tabs_with_name.pop()
        for sub_tab in tabs_with_name:
            edge_progress += 1
            print("%d   %d" % (len(tabs_with_name), edge_progress), end='\r')
            cur_edge = [cur_tab, sub_tab, 1]
            if cur_tab[0] < sub_tab[0]:
                cur_edge = [sub_tab, cur_tab, 1]
            raw_edges.append(cur_edge)
    return raw_edges

################### EDGES TO GRAPH FUNC ###################

def add_edges_from_list(my_edges):
    for edge in my_edges:
        tablet_net.add_edge(pydot.Edge(edge[0], edge[1], weight=edge[2], penwidth=edge[2]))

if __name__ == '__main__':
    with mp.Pool(mp.cpu_count) as p:
        results = p.map(tf_gather_edges, names)
    
    pre_hashing = list()
    for a in results:
        while len(a) > 0:
            pre_hashing.append(a.pop(0))
    
    with mp.Pool(mp.cpu_count) as p:
        p.map(hash_to_edges, pre_hashing)

    with mp.Pool(mp.cpu_count) as p:
        p.map(add_edges_from_list, hashed_edges)

    tablet_net.write_raw("test_raw.dot")

    