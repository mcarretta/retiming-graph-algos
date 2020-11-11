from tests.paper_test_graphs import get_paper_graphs
from algorithms.opt1 import opt1_algorithm
from algorithms.opt2 import opt2_algorithm
from retiming.RetimingGraphRandom import RetimingGraphRandom


def random_test_opt1_opt2(n_tests=1, n_nodes_list=[10, 20, 50, 100, 200, 500], weights="random", verbose=True):
    """
    Generates n_tests tests over the list of nodes n_nodes_list, instantiates random graph accordingly and tests algorithms
    opt1 and opt2 on them (result is correct if they have the same optimal clock)
    :param n_tests: number of test to be executed
    :param n_nodes_list: list of number of nodes that will correspond to an execution of the algorithm
    :param weights: random | positive
    :return:
    """
    for _ in range(n_tests):
        for n_nodes in n_nodes_list:

            valid_graph = False
            while not valid_graph:
                try:
                    g = RetimingGraphRandom(n_nodes, edge_probability=0.6, weights=weights, verbose=verbose)
                    valid_graph = True
                except:
                    pass
            cp_1 = opt1_algorithm(g.graph)[1]
            cp_2 = opt2_algorithm(g.graph)[1]
            if verbose:
                print(f"OPT1 and OPT2 optimal clocks for random graph of {n_nodes} nodes: {cp_1}, {cp_2}")
            assert cp_1 == cp_2


def test_opt1_2(verbose=False, draw=False):
    """
    Tests algorithms opt1 and opt2 on graphs on Leierson - Saxe paper and on ,
    National Taiwan University
    http://recipe.ee.ntu.edu.tw/LabWebsite/miniworkshop_Opt+App/Session%204-1%20JHJiang%20%5B%E7%9B%B8%E5%AE%B9%E6%A8%A1%E5%BC%8F%5D.pdf
    :param draw: True if we want to draw the retimed graph
    :param verbose: True  [False] to enable [disable] verbosity
    """
    g1, test1, g2, test2 = get_paper_graphs()

    print("Testing opt1 and opt2 on paper graph")
    _, optimal_clock1_opt1 = opt1_algorithm(g1.graph, draw=draw, verbose=verbose)
    _, optimal_clock1_opt2 = opt2_algorithm(g1.graph, draw=draw, verbose=verbose)

    assert optimal_clock1_opt1 == test1["opt1"]
    assert optimal_clock1_opt2 == test1["opt2"]

    print("Testing opt1 and opt2 on Jiang's slides")
    _, optimal_clock2_opt1 = opt1_algorithm(g2.graph, draw=draw, verbose=verbose)
    _, optimal_clock2_opt2 = opt2_algorithm(g2.graph, draw=draw, verbose=verbose)
    assert optimal_clock2_opt1 == test2["opt1"]
    assert optimal_clock2_opt2 == test2["opt2"]
