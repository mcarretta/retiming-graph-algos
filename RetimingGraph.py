import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import bisect

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

    @staticmethod
    def draw_graph(graph):
        """
        Draws retiming graph alongside edges weights and node delay
        :return:
        """
        pos = nx.shell_layout(graph)

        delay = nx.get_node_attributes(graph, 'delay')

        weights = nx.get_edge_attributes(graph, 'weight')

        nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights)
        nx.draw_shell(graph, labels=delay, with_labels=True, font_weight='bold')
        plt.show()

    def set_wd_attributes(self):
        node_attributes = nx.get_node_attributes(self.graph, "delay")
        weights = nx.get_edge_attributes(self.graph, "weight")
        new_attributes = {}
        for e in list(self.graph.edges):
            new_attributes[e] = {"weight": weights[e], "d(u)": (node_attributes[e[0]])}
        nx.set_edge_attributes(self.graph, new_attributes)

    @staticmethod
    def cp_algorithm(graph, mode="clock_period", verbose=False):
        # 0) Preliminary step - instantiate needed variables
        edge_attributes = nx.get_edge_attributes(graph, "weight")
        node_delays = nx.get_node_attributes(graph, "delay")
        delta = {}  # Dictionary containing the delta value for each vertex (access will be easier next)

        # 1) Construct G_0, subgraph with each edge weight = 0
        G_0 = [e for e in edge_attributes.keys() if edge_attributes[e] == 0]

        # 2) Topological sort of its vertices
        ordered_vertices = list(nx.topological_sort(nx.DiGraph(G_0)))

        # 3) Delta v computation
        # Loop through topological sorted vertices
        for v in ordered_vertices:
            # If v has no incoming edges in G_0
            if v not in [e[1] for e in G_0]:
                # delta_v is simply node v's delay
                delta[v] = node_delays[v]
            else:
                # if v has some incoming edges in G_0 the formulation is the one below
                delta[v] = (node_delays[v] + max([delta[u] for u, v1 in G_0 if v1 == v]))

        if mode == "clock_period":
            clock_period = max(delta.values())
            if verbose:
                print(clock_period)
            return clock_period

        elif mode == "delta":
            return delta

        else:
            AttributeError("Mode can be either 'clock_period' or 'delta'")


    def wd_algorithm(self, verbose=False):
        """
        w = x, y
        D(u,v) = d(v) - y
        :return:
        """
        # Set d(u) attribute as edge attribute
        self.set_wd_attributes()

        # Instantiate matrices w and d
        w_mat = np.empty(shape=(len(self.graph.nodes), len(self.graph.nodes)))
        d_mat = np.empty(shape=(len(self.graph.nodes), len(self.graph.nodes)))

        # Run Dijkstra all pairs for weights "weight" and "d(u)"
        w = dict(nx.all_pairs_dijkstra(self.graph, weight="weight"))
        d = dict(nx.all_pairs_dijkstra(self.graph, weight="d(u)"))

        # Construct matrix w
        for row_index, data in w.items():
            w_mat[row_index, list(data[0].keys())] = list(data[0].values())

        # Construct matrix d
        for row_index, data in d.items():
            d_mat[row_index, list(data[0].keys())] = np.array([self.graph.nodes[k]["delay"] for k in data[0].keys()]) + np.array(list(data[0].values()))

        if verbose:
            print(w_mat)
            print(d_mat)
        return w_mat, d_mat


    def compute_retimed_graph(self, retiming, draw=False):
        G_r = self.graph.copy(as_view=False)
        edge_attributes = nx.get_edge_attributes(self.graph, "weight")

        for (u, v), weight in edge_attributes.items():
            G_r[u][v]["weight"] = weight + retiming[v] - retiming[u]


        if draw:
            self.draw_graph(G_r)
        return G_r


    def check_legal_retiming(self, desired_clock, w_mat, d_mat):
        retiming = nx.single_source_bellman_ford_path_length()
        G_r = self.compute_retimed_graph(retiming)
        if self.cp_algorithm(G_r) > desired_clock:
            print("No feasible retiming exists")
            return None
        else:
            print("Feasible retiming exists", retiming)
            return retiming

    def _opt1_binary_search(self, vectorized_d, w_mat, d_mat):
        left, right = 0, len(vectorized_d) - 1
        while left <= right:
            mid = (left + right) // 2
            retiming = self.check_legal_retiming(vectorized_d[mid], w_mat, d_mat)
            if retiming is None:
                left = mid + 1
            else:
                right = mid - 1
        print(f"The minimum achievable clock period is {vectorized_d[left]}")
        return retiming

    def opt1_algorithm(self, desired_clock):

        # 1) Compute W and D using algorithm WD
        w_mat, d_mat = self.wd_algorithm()

        # 2) Sort the elements in the range of D
        vectorized_d = np.unique(np.sort(d_mat.flatten()))

        # 3) Binary search among the elements of D for the minimum available clock period, chek correctness with feas
        retiming = self._opt2_binary_search(vectorized_d, w_mat, d_mat)

    def feas_algorithm(self, desired_clock):
        retiming = {n: 0 for n in self.graph.nodes}
        for _ in range(len(self.graph.nodes) - 1):
            G_r = self.compute_retimed_graph(retiming)
            #TODO check bug here
            delta = self.cp_algorithm(G_r, "delta")
            for v, delta_v in delta.items():
                if delta_v > desired_clock:
                    retiming[v] += 1

        if self.cp_algorithm(G_r) > desired_clock:
            print("No feasible retiming exists")
            return None
        else:
            print("Feasible retiming exists", retiming)
            return retiming

    def _opt2_binary_search(self, vectorized_d):
        left, right = 0, len(vectorized_d) - 1
        while left <= right:
            mid = (left + right) // 2
            retiming = self.feas_algorithm(vectorized_d[mid])
            if retiming is None:
                left = mid + 1
            else:
                right = mid - 1
        print(f"The minimum achievable clock period is {vectorized_d[left]}")
        return retiming

    def opt2_algorithm(self, draw=True):

        # 1) Compute W and D using algorithm WD
        _, d_mat = self.wd_algorithm()

        # 2) Sort the elements in the range of D
        vectorized_d = np.unique(np.sort(d_mat.flatten()))

        # 3) Binary search among the elements of D for the minimum available clock period, chek correctness with feas
        retiming = self._opt2_binary_search(vectorized_d)

        # 4) Compute the retimed graph using the optimal solution from step 4
        G_r = self.compute_retimed_graph(retiming)

        if draw:
            self.draw_graph(G_r)
        return G_r


if __name__ == "__main__":
    v = [0, 1, 2, 3, 4, 5, 6, 7]
    d = [0, 3, 3, 3, 3, 7, 7, 7]
    e = [[0, 1], [1, 2], [1, 7], [2, 3], [2, 6], [3, 4], [3, 5], [4, 5], [5, 6], [6, 7], [7, 0]]
    w = [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
    g = RetimingGraph(v, e, d, w)
    # g.wd_algorithm()
    # g.draw_graph()
    # g.cp_algorithm()
    # g.compute_retimed_graph({0: 0, 1: -1, 2: -1, 3: -2, 4: -2, 5: -2, 6: -1, 7: 0}, draw=True)
    g.feas_algorithm(13)
    # g.opt2_algorithm()

