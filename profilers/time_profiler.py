from time import time
from algorithms.opt1 import opt1_algorithm
from algorithms.opt2 import opt2_algorithm
from algorithms.wd_algorithm import wd_algorithm
from retiming.RetimingGraphRandom import RetimingGraphRandom
from utils.retiming_utils import plot_dictionary


def time_random_opt1(n_nodes=20, weights="random", positive_cycle_check=None, verbose=False):
    """
    Instantiate a random retiming graph and test time needed to compute opt1 algorithm
    :param n_nodes: number of nodes of the graph
    :param weights: random | positive
    :param positive_cycle_check: check that all cycle have positive weight
    :param verbose: True  [False] to enable [disable] verbosity
    :return: time differential
    """
    # Generate a valid retiming graph
    valid_graph = False
    while not valid_graph:
        try:
            g = RetimingGraphRandom(n_nodes, edge_probability=0.5, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)
            valid_graph = True
        except:
            pass
    start_time = time()
    opt1_algorithm(g.graph)
    delta = time() - start_time
    if verbose:
        print(f"Time to execute algorithm opt1 with {n_nodes}: {delta}")
    return delta


def time_random_opt2(n_nodes=20, weights="random", positive_cycle_check=None, verbose=False):
    """
    Instantiate a random retiming graph and test time needed to compute opt2 algorithm
    :param n_nodes: nodes of the retiming graph
    :param n_nodes: number of nodes of the graph
    :param weights: random | positive
    :param positive_cycle_check: check that all cycle have positive weight
    :param verbose: True  [False] to enable [disable] verbosity
    :return: time differential
    """
    # Generate a valid retiming graph
    valid_graph = False
    while not valid_graph:
        try:
            g = RetimingGraphRandom(n_nodes, edge_probability=0.5, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)
            valid_graph = True
        except:
            pass
    start_time = time()
    opt2_algorithm(g.graph)
    delta = time() - start_time
    if verbose:
        print(f"Time to execute algorithm opt2 with {n_nodes} nodes: {delta}")
    return delta


def time_random_wd(n_nodes=20, weights="random", positive_cycle_check=None, verbose=False):
    """
    Instantiate a random retiming graph and test time needed to compute wd algorithm
    :param n_nodes: nodes of the retiming graph
    :return: time differential
    """
    # Generate a valid retiming graph
    valid_graph = False
    while not valid_graph:
        try:
            g = RetimingGraphRandom(n_nodes, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)
            valid_graph = True
        except:
            pass
    start_time = time()
    wd_algorithm(g.graph)
    delta = time() - start_time
    if verbose:
        print(f"Time to execute algorithm wd with {n_nodes} nodes: {delta}")
    return delta


def random_graph_instantiation_time(n_nodes=20, p=0.5, weights="random", positive_cycle_check=None, verbose=False):
    """
    Test time to instantiate a random retiming graph
    :param n_nodes: number of nodes of the randomly generated retiming graph
    :param p: edge probability
    :param weights: 'positive' or 'random'
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :return:
    """
    # Generate a valid retiming graph
    start_time = time()

    valid_graph = False
    while not valid_graph:
        try:
            g = RetimingGraphRandom(n_nodes, edge_probability=p, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)
            valid_graph = True
        except:
            start_time = time()
    delta = time() - start_time
    if verbose:
        print(f"Time to instantiate a graph of {n_nodes} nodes with weights {weights} and positive cycle checking {positive_cycle_check}: {delta}")
    return delta


def multiple_time_random_opt1(node_list=[10, 20, 50, 100, 200, 500], weights="random", positive_cycle_check=None, verbose=False, plot=True):
    """
    Compute and plots time benchmarks for algorithm opt1 with a list of graphs
    :param node_list: list of nodes of the graphs on which the benchmark will be run
    :param weights: random | positive
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :param plot: True to plot on a graph the memory usages as the number of nodes grows
    :return:
    """
    delta_times = {}
    for n in node_list:
        delta_times[n] = time_random_opt1(n_nodes=n, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)

    if plot:
        plot_dictionary(delta_times)

    return delta_times


def multiple_time_random_opt2(node_list=[10, 20, 50, 100, 200, 500], weights="random", positive_cycle_check=None, verbose=False, plot=True):
    """
    Compute and plots time benchmarks for algorithm opt2 with a list of graphs
    :param node_list: list of nodes of the graphs on which the benchmark will be run
    :param weights: random | positive
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :param plot: True to plot on a graph the memory usages as the number of nodes grows
    :return:
    """
    delta_times = {}
    for n in node_list:
        delta_times[n] = time_random_opt2(n_nodes=n, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)

    if plot:
        plot_dictionary(delta_times)
    return delta_times


def multiple_time_random_wd(node_list=[10, 20, 50, 100, 200, 500], weights="random", positive_cycle_check=None, verbose=False, plot=True):
    """
    Compute and plots time benchmarks for algorithm wd with a list of graphs
    :param node_list: list of nodes of the graphs on which the benchmark will be run
    :param weights: random | positive
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :param plot: True to plot on a graph the memory usages as the number of nodes grows
    :return:
    """
    delta_times = {}
    for n in node_list:
        delta_times[n] = time_random_wd(n_nodes=n, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)

    if plot:
        plot_dictionary(delta_times)

    return delta_times


def multiple_time_random_graph_instantiation(node_list=[10, 20, 50, 100, 200, 500], p=0.5, weights="random", positive_cycle_check=True, verbose=False, plot=True):
    """
    Compute and plots time benchmarks for algorithm opt1 with a list of graphs
    :param node_list: list of nodes of the graphs on which the benchmark will be run
    :param weights: random | positive
    :param p: edge probability
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :param plot: True to plot on a graph the memory usages as the number of nodes grows
    :return:
    """
    assert weights == "random" or weights == "positive"
    delta_times = {}
    for n in node_list:
        delta_times[n] = random_graph_instantiation_time(n_nodes=n, p=p, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)

    if plot:
        plot_dictionary(delta_times)

    return delta_times
