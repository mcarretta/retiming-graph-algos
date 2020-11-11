import networkx as nx
import numpy as np


class RetimingGraph:
    def __init__(self, nodes, edges, delays, weights, positive_cycle_check=True, remove_clockwise_edges=True, verbose=False):
        """
        Graph initialization function to construct a RetimingGraph object
        :param nodes: list of nodes
        :param edges: list of edges
        :param delays: list of nodes' delays
        :param weights: list of edges' weights
        :param positive_cycle_check: True if we want to check for positively weighted cycles
        :param remove_clockwise_edges: True if we want to remove clockwise edges
        :param verbose: True  [False] to enable [disable] verbosity
        """
        if verbose:
            print("Instantiating graph")
        self.graph = nx.DiGraph()

        # Length of nodes array must be equal to the length of delays array
        assert (len(nodes) == len(delays))
        # Length of edges array must be equal to the length of weights array
        assert (len(edges) == len(weights))
        # Propagation delay d(v) must be non-negative for each vertex
        assert ((np.array(delays) >= 0).all())
        # Register count w(e) must be non-negative for each vertex
        assert ((np.array(weights) >= 0).all())


        # Concatenate column of weights to each corresponding edge, a weighted edge should be (u, v, weight)
        weighted_edges = np.column_stack((np.array(edges), np.array(weights)))

        # Add nodes and edges to the graph
        for node_index in range(len(nodes)):
            self.graph.add_node(nodes[node_index], delay=delays[node_index])
        self.graph.add_weighted_edges_from(weighted_edges)

        """
        Due to the nature of Correlators' functional units, there can be no edges from a subsequent node to a previous 
        node: all edges are anti-clockwise. So we remove all clockwise edges.
        """
        if remove_clockwise_edges:
            """
            Remove edges (u, v) where node u follows node v in the nodes' ordering (clockwise edges)
            """
            self.graph.remove_edges_from([(u, v) for (u, v) in self.graph.edges
                                          if u > v and (u, v) != (max(self.graph.nodes), min(self.graph.nodes))])
            """
            If there's an edge (initial_node, last_node) it won't be removed from the previous stage, so remove it; if it
            is not present it will raise a NetworkXError that will be passed for the try except statement
            """
            try:
                self.graph.remove_edge(min(self.graph.nodes), max(self.graph.nodes))
            except nx.exception.NetworkXError:
                pass

        """
        For condition W2, on the paper, each cycle must have at least one edge with positive register count (edge weight).
        This is task is computationally intense, because it requires to run nx.simple_cycles to detect elementary cycles;
        its time complexity is O((n+e)(c+1)) for n nodes, e edges and c cycles. This explodes for high values of n and e.
        One easier way would be to set all weights strictly positive, so that no negative cycle can happen
        """
        if positive_cycle_check:
            if verbose:
                print("Checking absence of null cycles")
            # Check cycles to have at least a strictly positive weighted edge in it
            edge_weights = nx.get_edge_attributes(self.graph, "weight")
            for cycle in list(nx.simple_cycles(self.graph)):
                path_weight = 0
                for edge_index in range(1, len(cycle)):
                    path_weight += edge_weights[cycle[edge_index-1], cycle[edge_index]]
                path_weight += edge_weights[cycle[edge_index], cycle[0]]
                if path_weight == 0:
                    raise AssertionError("Detected a cycle with 0 weight")





