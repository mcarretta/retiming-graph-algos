import numpy as np
import networkx as nx


def set_wd_attributes(graph):
    """
    Set attribute d(u) to compute matrix W and D
    Note that instead of -d(u) the weight was set to d(u) because Dijkstra does not accept negative weights
    """
    # Retrieve nodes and edges attributes
    node_attributes = nx.get_node_attributes(graph, "delay")
    weights = nx.get_edge_attributes(graph, "weight")

    # Instantiate a dictionary of dictionaries where the attributes will be stored in form of
    new_attributes = {}

    # Append items to dictionary of new attributes
    for e in list(graph.edges):
        new_attributes[e] = {"weight": weights[e], "d(u)": (node_attributes[e[0]])}

    # Update the graph with the new set of attributes
    nx.set_edge_attributes(graph, new_attributes)


def wd_algorithm(graph, verbose=True):
    """
    Compute the W and D matrices through Djikstra algorithm

    Let w be the shortest path weight w = w_w, w_d
    W(u, v) = w_w(u, v)
    D(u,v) = d(v) - w_d(u, v)

    :param graph: directed retiming graph
    :param verbose: True for prints, False to skip prints
    :return: W and D matrices
    """
    if verbose:
        print("Computing W and D matrices")
    # Set d(u) attribute as edge attribute
    set_wd_attributes(graph)

    # Instantiate matrices w and d
    w_mat = np.empty(shape=(len(graph.nodes), len(graph.nodes)))
    d_mat = np.empty(shape=(len(graph.nodes), len(graph.nodes)))
    w_mat[:], d_mat[:] = np.nan, np.nan
    # Run Dijkstra all pairs for weights "weight" and "d(u)"
    w = dict(nx.all_pairs_dijkstra(graph, weight="weight"))
    d = dict(nx.all_pairs_dijkstra(graph, weight="d(u)"))

    # Construct matrix W
    for row_index, data in w.items():
        w_mat[row_index, list(data[0].keys())] = list(data[0].values())

    # Construct matrix D
    for row_index, data in d.items():
        d_mat[row_index, list(data[0].keys())] = np.array(
            [graph.nodes[k]["delay"] for k in data[0].keys()]) + np.array(list(data[0].values()))

    if verbose:
        print(w_mat)
        print(d_mat)
    return w_mat, d_mat
