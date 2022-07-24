import networkx as nx
import random
import math
import dash_cytoscape as cyto
from dash import Dash, html
from Database.SQLfuncs import SQLfuncs

SCALING_FACTOR = 100

if __name__ == '__main__':
    db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

    tablets = db.execute_query("select distinct tabid from tabids;")
    for i in range(len(tablets)):
        tablets[i] = tablets[i][0]
    tablet_network = nx.Graph()

    tablet_network.add_nodes_from(tablets)

    names = db.execute_query("select distinct name from rawnames where name !='...' limit 4;")
    for i in range(len(names)):
        names[i] = names[i][0]
    name_progress = 1
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

    tablet_network.remove_nodes_from(list(nx.isolates(tablet_network)))

    testnode = list(tablet_network.nodes)[math.floor((random.random()*len(tablet_network)))]
    print("")
    print(len(tablet_network.nodes))

    ego_tablet_network = nx.ego_graph(tablet_network, testnode, 2)
    print(len(ego_tablet_network.nodes))


    #############################################################################################

    app = Dash(__name__)

    pos = nx.circular_layout(ego_tablet_network, scale=1.0, center=None)

    print("check")

    cy = nx.cytoscape_data(ego_tablet_network)

    print("step 1")
    for n in cy["elements"]["nodes"]:
        for k, v in n.items():
            v["label"] = v.pop("value")

    print("step 2")

    for n, p in zip(cy["elements"]["nodes"], pos.values()):
        n["pos"] = {"x": int(p[0] * SCALING_FACTOR), "y": int(p[1] * SCALING_FACTOR)}

    print("step 3")
    elements = cy["elements"]["nodes"] + cy["elements"]["edges"]

    app.layout = html.Div(
        [
            cyto.Cytoscape(
                id="cytoscape-layout-4",
                elements=elements,
                style={"width": "100%", "height": "800px"},
                layout={"name": "preset"},  # "preset" to use the pos coords
            )
        ]
    )

    app.run_server(debug=False)