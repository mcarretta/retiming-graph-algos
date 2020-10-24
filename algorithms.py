import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_node(1, value=0)
G.add_node(2, value=7)
G.add_node(3, value=3)
G.add_node(4, value=3)
G.add_edge(2, 1, weight=0)
G.add_edge(1, 3, weight=2)
G.add_edge(3, 2, weight=0)
G.add_edge(3, 4, weight=0)
G.add_edge(4, 2, weight=0)
e = (1, 3)
print(G.get_edge_data(*e)["weight"])

print(G.nodes)

nx.draw_circular(G, with_labels=True, font_weight='bold')
plt.show()