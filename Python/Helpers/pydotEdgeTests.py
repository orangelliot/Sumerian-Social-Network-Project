import pydot as pd

g = pd.Dot()

g.set_edge_defaults(weight=1)

g.add_node(pd.Node('a'))
g.add_node(pd.Node('b'))

test_edge = pd.Edge('a', 'b', weight=3, fontsize=3)
g.add_edge(test_edge)

print(test_edge.get_attributes().get('weight'))