import networkx as nx
import matplotlib.pyplot as plt


def draw_retiming_graph(graph):
    """
    Draws retiming graph alongside edges weights and node delay
    :param graph: graph to draw
    """
    pos = nx.shell_layout(graph)

    delay = nx.get_node_attributes(graph, 'delay')

    weights = nx.get_edge_attributes(graph, 'weight')

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights)
    nx.draw_shell(graph, labels=delay, with_labels=True, font_weight='bold')
    plt.show()


def plot_dictionary(dictionary):
    """
    Plots a dictionary {n_nodes: value}. Used for memory and time profiling
    :param dictionary: {n_nodes: memory_usage} or {n_nodes: delta_time}
    """
    x, y = zip(*sorted(dictionary.items()))  # unpack a list of pairs into two tuples

    plt.plot(x, y)
    plt.show()


def compute_retimed_graph(graph, retiming, draw=False):
    """
    Computes retimed graph by applying retiming found to graph
    :param graph: Directed graph on which retiming will be applied
    :param retiming: retiming dictionary
    :param draw: if True, draw retiming graph
    :return: retimed graph
    """
    # Instantiate new graph
    G_r = nx.DiGraph()
    edge_attributes = nx.get_edge_attributes(graph, "weight")
    delays = nx.get_node_attributes(graph, "delay")
    G_r.add_weighted_edges_from([(u, v, edge_attributes[u, v] + retiming[v] - retiming[u]) for u, v in graph.edges])
    G_r.add_nodes_from([(v, {"delay": delays[v]}) for v in graph.nodes])
    if draw:
        draw_retiming_graph(G_r)
    return G_r
