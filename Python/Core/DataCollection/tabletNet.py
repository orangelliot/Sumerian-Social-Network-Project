import networkx as nx
import os
import plotly.graph_objects as go
from Database.SQLfuncs import SQLfuncs

db = SQLfuncs('sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com', 'root', '2b928S#%')

tablets = db.execute_query("select distinct tabid from tabids;")
for i in range(len(tablets)):
    tablets[i] = tablets[i][0]
tablet_network = nx.Graph()
tablet_network.add_nodes_from(tablets)

#############################################################################################
G = tablet_network

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()

#############################################################################################

names = db.execute_query("select distinct name from rawnames where name !='...' limit 50;")
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