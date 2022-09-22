import pydot

graph = pydot.Dot('test_net', graph_type='graph',bgcolor='yellow')

my_edge = pydot.Edge("a", "b", color="blue")
graph.add_edge(my_edge)

graph.write_raw("test_raw.dot")