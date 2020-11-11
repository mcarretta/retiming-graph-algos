import networkx as nx


def cp_algorithm(graph):
    """
    Returns the maximum of the delta array, i.e. the optimal (minimum) clock period
    :param graph:
    :return:
    """
    return max(delta_array(graph).values())


def delta_array(graph, verbose=False):
    """
    Compute the delta array period of a synchronous circuit graph
    :param graph: graph of the synchronous circuit. Pass G.graph as parameter
    :param verbose: True  [False] to enable [disable] verbosity
    :return: Clock period or delta array of a given graph
    """

    # 0) Preliminary step - instantiate needed variables
    edge_attributes = nx.get_edge_attributes(graph, "weight")
    node_delays = nx.get_node_attributes(graph, "delay")
    delta = {}  # Dictionary containing the delta value for each vertex (access will be easier next)
    G_0 = nx.DiGraph()
    # 1) Construct G_0, subgraph with each edge weight = 0
    zero_weight_edge_list = [e for e in edge_attributes.keys() if edge_attributes[e] == 0]
    G_0.add_edges_from(zero_weight_edge_list)
    # 2) Topological sort of its vertices
    ordered_vertices = nx.topological_sort(G_0)
    # 3) Delta v computation
    # Loop through topological sorted vertices
    for v in list(ordered_vertices):
        # If v has no incoming edges in G_0
        if not [G_0.in_edges(v)]:
            # delta_v is simply node v's delay
            delta[v] = node_delays[v]
        else:
            # if v has some incoming edges in G_0 the formulation is the one below
            delta[v] = (node_delays[v] + max([delta.get(u, 0) for (u, _) in G_0.in_edges(v)], default=0))

    # For nodes that are in the set difference between the list of graph node and the one of zero nodes, the delta array
    # for those nodes is equal to the delay of those nodes
    for v in list(set.difference(set(list(graph.nodes)), set(list(G_0.nodes)))):
        delta[v] = node_delays[v]

    if verbose:
        print(delta)
    return delta

