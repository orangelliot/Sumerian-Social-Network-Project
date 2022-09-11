import multiprocessing as mp
import pydot
import graphviz
import psutil
from Database.SQLfuncs import SQLfuncs

tablet_net = pydot.Dot('tablet_net', graph_type='graph',bgcolor='yellow')

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

tablet_counter = 0
tablets = db.execute_query("select distinct tabid from tabids;")
for i in range(len(tablets)):
    tablets[i] = [tablet_counter, tablets[i][0]]
    temp_node = pydot.Node(tablet_counter,label=tablets[i])
    tablet_net.add_node(temp_node)
    tablet_counter += 1

names = db.execute_query("select distinct name from rawnames where name !='...' limit 4;")

for i in range(len(names)):
    names[i] = names[i][0]

edges = [list()]*tablet_counter

######################## HELPER FUNCS ########################
def searchForEdge(edge, edge_list):
    edge_name = getEdgeName(edge)
    for cur_edge in edge_list:
        if edge_name == getEdgeName(cur_edge):
            return cur_edge
    return None

def getEdgeName(edge):
    edge_name = [edge[0][0],edge[1][0]]
    if edge_name[0] > edge_name[1]:
        temp = edge_name[0]
        edge_name[0] = edge_name[1]
        edge_name[1] = temp
    return edge_name[0]*100000+edge_name[1]
###################### END HELPER FUNCS ######################

#takes a name, collects all the tabids with that name and creates a pair for each of them,
#and then returns a list of these pairs for processing later
def tf_gather_edges(name, queue):
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
    queue.put(raw_edges)

def tf_manage_edge_collectors(names, queue):
    

if __name__ == '__main__':
    n_cpus = psutil.cpu_count()
    procs = list()
    queue = mp.Queue()