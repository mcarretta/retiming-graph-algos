import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class RetimingGraph:
    def __init__(self, nodes, edges, delays, weights):
        """
        Graph initialization function to construct a RetimingGraph object
        :param nodes: list of nodes
        :param edges: list of edges
        :param delays: list of nodes' delays
        :param weights: list of edges' weights
        """
        self.graph = nx.DiGraph()

        # Length of nodes array must be equal to the length of delays array
        assert (len(nodes) == len(delays))
        # Length of edges array must be equal to the length of weights array
        assert (len(edges) == len(weights))
        # Propagation delay d(v) must be non-negative for each vertex
        assert ((np.array(delays) >= 0).all())
        # Register count w(e) must be non-negative for each vertex
        assert ((np.array(weights) >= 0).all())
        # There must be some edges with strictly positive register count
        assert ((np.array(weights) > 0).any())


        # Concatenate column of weights to each corresponding edge, a weighted edge should be (u, v, weight)
        weighted_edges = np.column_stack((np.array(edges), np.array(weights)))

        # Add nodes and edges to the graph
        for node_index in range(len(nodes)):
            self.graph.add_node(nodes[node_index], delay=delays[node_index])
        self.graph.add_weighted_edges_from(weighted_edges)

    def compute_path_weight(self, path):
        path_weight = 0
        for i in range(1, len(path)):
            path_weight += self.graph.get_edge_data(path[i - 1], path[i])["weight"]
        return path_weight

    def compute_path_sum_of_delays(self, path):
        path_delay = 0
        for i in range(len(path)):
            path_delay += self.graph.get_node_data(path[i - 1], path[i])["weight"]
        return path_delay

    def draw_graph(self):
        """
        Draws retiming graph alongside edges weights and node delay
        :return:
        """
        pos = nx.shell_layout(self.graph)

        delay = nx.get_node_attributes(self.graph, 'delay')

        weights = nx.get_edge_attributes(self.graph, 'weight')

        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=weights)
        nx.draw_shell(self.graph, labels=delay, with_labels=True, font_weight='bold')
        plt.show()

    @staticmethod
    def _weight_computation(u, v, edge_attributes):
        w = (edge_attributes[u, v]["-d(u)"])
        return w

    def set_wd_attributes(self):
        node_attributes = nx.get_node_attributes(self.graph, "delay")
        weights = nx.get_edge_attributes(self.graph, "weight")
        new_attributes = {}
        for e in list(self.graph.edges):
            new_attributes[e] = {"weight": weights[e], "d(u)": (node_attributes[e[0]])}
        nx.set_edge_attributes(self.graph, new_attributes)
        return new_attributes

    def wd_algorithm(self):
        """
        w = x, y
        D(u,v) = d(v) - y
        :return:
        """
        attributes = self.set_wd_attributes()
        w_mat = np.zeros(shape=(len(self.graph.nodes), len(self.graph.nodes)))

        d_mat = np.empty(shape=(len(self.graph.nodes), len(self.graph.nodes)))
        w = dict(nx.all_pairs_dijkstra(self.graph, weight="weight"))
        d = dict(nx.all_pairs_dijkstra(self.graph, weight="d(u)"))
        for row_index, data in w.items():
            w_mat[row_index, list(data[0].keys())] = list(data[0].values())

        for row_index, data in d.items():
            d_mat[row_index, list(data[0].keys())] = np.array([self.graph.nodes[k]["delay"] for k in data[0].keys()]) + np.array(list(data[0].values()))

        print(w_mat)
        print(d_mat)
        return w_mat, d_mat

if __name__ == "__main__":
    v = [0, 1, 2, 3, 4, 5, 6, 7]
    d = [0, 3, 3, 3, 3, 7, 7, 7]
    e = [[0, 1], [1, 2], [1, 7], [2, 3], [2, 6], [3, 4], [3, 5], [4, 5], [5, 6], [6, 7], [7, 0]]
    w = [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
    g = RetimingGraph(v, e, d, w)
    g.wd_algorithm()
    # g.draw_graph()
