import networkx as nx
from retiming.RetimingGraph import RetimingGraph
import numpy as np


class RetimingGraphRandom(RetimingGraph):
    def __init__(self, n_vertices=10, edge_probability=0.25, max_weight=1, max_delay=10, weights="positive", positive_cycle_check=None, verbose=False):
        G = nx.fast_gnp_random_graph(n_vertices, edge_probability, seed=np.random, directed=True)

        nodes, edges = list(G.nodes), list(G.edges)
        # print(nodes, edges)
        if weights == "positive":
            weight = np.ones(len(edges), dtype=int)
        elif weights == "random":
            weight = np.random.randint(0, max_weight, size=len(edges), dtype=int)
        else:
            AttributeError("weights can be either 'positive' or 'random'")

        if positive_cycle_check is None:
            # If weights is not random a positive cycle check is always useless since cycles at most have 1 weight cycle
            positive_cycle_check = (weights == "random")
        delay = np.random.randint(0, max_delay, size=(len(nodes) - 1))
        # Insert 0 as delay of first node v(h) for a retiming to be lega;
        delay = np.insert(delay, 0, 0)
        # print(nodes, edges, list(weight), list(delay))
        super().__init__(nodes, edges, delay, weight, positive_cycle_check=positive_cycle_check, remove_clockwise_edges=True, verbose=verbose)

    def tester(self):
        try:
            self.opt1_algorithm()
            self.opt2_algorithm()
        except:
            AttributeError("Random generated graph is not correct")

if __name__ == "__main__":
    g = RetimingGraphRandom(10)

    # g.draw_graph(g.graph)
    # g.wd_algorithm(verbose=True)
    g.opt1_algorithm()
    print("-------------------------------------------------------------------------------")
    g.opt2_algorithm()
