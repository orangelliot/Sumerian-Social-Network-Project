import pydot
import graphviz
from Database.SQLfuncs import SQLfuncs

tablet_net = pydot.Dot('tablet_net', graph_type='graph',bgcolor='yellow')

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

tablet_counter = 0
tablets = db.execute_select('select distinct tabid from tabids;')
for i in range(len(tablets)):
    tablets[i] = [tablet_counter, tablets[i][0]]
    temp_node = pydot.Node(tablet_counter,label=tablets[i])
    tablet_net.add_node(temp_node)
    tablet_counter += 1

names = db.execute_select('select distinct name from rawnames where name !=\'...\' limit 4;')

for i in range(len(names)):
    names[i] = names[i][0]

edges = [list()]*tablet_counter

######################## FUNCS ########################
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
###################### END FUNCS ######################

name_progress = 0
num_names = len(names)

for cur_name in names:
    name_progress += 1
    cur_name = db.sanitizeInput(cur_name)
    tabs_with_name = db.execute_select('select distinct tabid from rawnames where name=\'' + cur_name + '\';')

    tablet_counter = 0
    for i in range(len(tabs_with_name)):
        tabs_with_name[i] = [tablet_counter, tabs_with_name[i][0]]
        tablet_counter += 1

    while len(tabs_with_name) > 1:
        edge_progress = 0
        cur_tab = tabs_with_name.pop()
        for sub_tab in tabs_with_name:
            edge_progress += 1
            print("%d/%d   %d   %d" % (name_progress, num_names, len(tabs_with_name), edge_progress), end='\r')
            cur_edge = [cur_tab, sub_tab, 1]
            if cur_tab[0] > sub_tab[0]:
                cur_edge = [sub_tab, cur_tab, 1]
            edge_candidate = searchForEdge(cur_edge, edges[cur_tab[0]])
            if edge_candidate != None:
                edge_candidate[2] += 1
            else:
                edges[cur_tab[0]].append(cur_edge)