from memory_profiler import memory_usage
from algorithms.opt1 import opt1_algorithm
from algorithms.opt2 import opt2_algorithm
from algorithms.wd_algorithm import wd_algorithm
from retiming.RetimingGraphRandom import RetimingGraphRandom
from utils.retiming_utils import plot_dictionary


def memory_random_opt1(n_nodes=20, weights="random", positive_cycle_check=None, verbose=False):
    """
    Instantiate a random retiming graph and test memory needed to compute opt1 algorithm
    :param n_nodes: number of nodes of the graph
    :param weights: random | positive
    :param positive_cycle_check: check that all cycle have positive weight
    :param verbose: True  [False] to enable [disable] verbosity
    :return: memory usage for opt1 algorithm with a random instantiated graph
    """
    print(f"Memory profiling for algorithm opt1 with {n_nodes}")
    # Generate a valid retiming graph
    valid_graph = False
    while not valid_graph:
        try:
            g = RetimingGraphRandom(n_nodes, edge_probability=0.5, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)
            valid_graph = True
        except:
            pass
    # Get max memory usage for opt1 algorithm
    # memory_usage returns a tuple (usage, retval), we're interested in the max of the first (that's why max_usage = True)

    def profile_memory(*args, **kwargs):
        mem_usage = memory_usage((opt1_algorithm, args, kwargs), retval=True, max_usage=True)[0]
        return mem_usage

    memory_usage_opt1 = profile_memory(g.graph)
    if verbose:
        print("Memory usage: ", memory_usage_opt1)
    return memory_usage_opt1



def memory_random_opt2(n_nodes=20, weights="random", positive_cycle_check=None, verbose=False):
    """
    Instantiate a random retiming graph and test memory needed to compute opt2 algorithm
    :param n_nodes: number of nodes of the graph
    :param weights: random | positive
    :param positive_cycle_check: check that all cycle have positive weight
    :param verbose: True  [False] to enable [disable] verbosity
    :return: memory usage for opt2 algorithm with a random instantiated graph
    """
    print(f"Memory profiling for algorithm opt2 with {n_nodes}")

    # Generate a valid retiming graph
    valid_graph = False
    while not valid_graph:
        try:
            g = RetimingGraphRandom(n_nodes, edge_probability=0.5, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)
            valid_graph = True
        except:
            pass
    # Get max memory usage for opt2 algorithm
    # memory_usage returns a tuple (usage, retval), we're interested in the max of the first (that's why max_usage = True)

    def profile_memory(*args, **kwargs):
        mem_usage = memory_usage((opt2_algorithm, args, kwargs), retval=True, max_usage=True)[0]
        return mem_usage

    memory_usage_opt2 = profile_memory(g.graph)
    if verbose:
        print("Memory usage: ", memory_usage_opt2)
    return memory_usage_opt2


def memory_random_wd(n_nodes=20, weights="random", positive_cycle_check=None, verbose=False):
    """
    Instantiate a random retiming graph and test memory needed to compute wd algorithm
    :param n_nodes: number of nodes of the graph
    :param weights: random | positive
    :param positive_cycle_check: check that all cycle have positive weight
    :param verbose: True  [False] to enable [disable] verbosity
    :return: memory usage for wd algorithm with a random instantiated graph
    """
    print(f"Memory profiling for algorithm wd with {n_nodes}")

    # Generate a valid retiming graph
    valid_graph = False
    while not valid_graph:
        try:
            g = RetimingGraphRandom(n_nodes, edge_probability=0.5, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)
            valid_graph = True
        except:
            pass
    # Get max memory usage for opt2 algorithm
    # memory_usage returns a tuple (usage, retval), we're interested in the max of the first (that's why max_usage = True)

    def profile_memory(*args, **kwargs):
        mem_usage = memory_usage((wd_algorithm, args, kwargs), retval=True, max_usage=True)[0]
        return mem_usage

    memory_usage_wd = profile_memory(g.graph)
    if verbose:
        print("Memory usage: ", memory_usage_wd)
    return memory_usage_wd


def random_graph_instantiation_memory(n_nodes=20, p=0.5, weights="random", positive_cycle_check=None, verbose=False):
    """
    Test memory usage to instantiate a random retiming graph
    :param n_nodes: number of nodes of the randomly generated retiming graph
    :param p: edge probability
    :param weights: random | positive
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :return: memory usage to instantiate a random retiming graph
    """
    print(f"Memory profile of an instantiation of a graph of {n_nodes} nodes with weights {weights} and positive cycle checking {positive_cycle_check}")

    # Generate a valid retiming graph
    valid_graph = False
    while not valid_graph:
        try:
            # Get max memory usage for opt2 algorithm
            # memory_usage returns a tuple (usage, retval), we're interested in the max of the first (that's why max_usage = True)

            def profile_memory(*args, **kwargs):
                mem_usage = memory_usage((RetimingGraphRandom, args, kwargs), retval=True, max_usage=True)[0]
                return mem_usage

            memory_usage_instantiation = profile_memory(n_nodes, edge_probability=p, weights="random", positive_cycle_check=positive_cycle_check ,retval=True, max_usage=True)
            if verbose:
                print("Memory usage: ", memory_usage_instantiation)
            return memory_usage_instantiation
        except:
            pass


def multiple_memory_random_opt1(node_list=[10, 20, 50, 100, 200, 500], weights="random", positive_cycle_check=None, verbose=False, plot=True):
    """
    Compute and plots memory benchmarks for algorithm opt1 with a list of graphs
    :param node_list: list of nodes of the graphs on which the benchmark will be run
    :param weights: random | positive
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :param plot: True to plot on a graph the memory usages as the number of nodes grows
    :return: dictionary {n_nodes: memory_usage} with memory usages for each different run and n_nodes as key
    """
    memory_usage_dictionary = {}
    for n in node_list:
        memory_usage_dictionary[n] = memory_random_opt1(n, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)

    if plot:
        plot_dictionary(memory_usage_dictionary)
    if verbose:
        print(memory_usage_dictionary)
    return memory_usage_dictionary


def multiple_memory_random_opt2(node_list=[10, 20, 50, 100, 200, 500], weights="random", positive_cycle_check=None, verbose=False, plot=True):
    """
    Compute and plots memory benchmarks for algorithm opt2 with a list of graphs
    :param node_list: list of nodes of the graphs on which the benchmark will be run
    :param weights: random | positive
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :param plot: True to plot on a graph the memory usages as the number of nodes grows
    :return: dictionary {n_nodes: memory_usage} with memory usages for each different run and n_nodes as key
    """
    memory_usage_dictionary = {}
    for n in node_list:
        memory_usage_dictionary[n] = memory_random_opt2(n, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)

    if plot:
        plot_dictionary(memory_usage_dictionary)

    if verbose:
        print(memory_usage_dictionary)
    return memory_usage_dictionary


def multiple_memory_random_wd(node_list=[10, 20, 50, 100, 200, 500], weights="random", positive_cycle_check=None, verbose=False, plot=True):
    """
    Compute and plots memory benchmarks for algorithm wd with a list of graphs
    :param node_list: list of nodes of the graphs on which the benchmark will be run
    :param weights: random | positive
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :param plot: True to plot on a graph the memory usages as the number of nodes grows
    :return: dictionary {n_nodes: memory_usage} with memory usages for each different run and n_nodes as key
    """
    memory_usage_dictionary = {}
    for n in node_list:
        memory_usage_dictionary[n] = memory_random_wd(n_nodes=n, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)

    if plot:
        plot_dictionary(memory_usage_dictionary)

    if verbose:
        print(memory_usage_dictionary)
    return memory_usage_dictionary


def multiple_memory_random_graph_instantiation(node_list=[10, 20, 50, 100, 200, 500], p=0.5, weights="random", positive_cycle_check=True, verbose=False, plot=True):
    """
    Compute and plots time benchmarks for algorithm opt1 with a list of graphs
    :param node_list: list of nodes of the graphs on which the benchmark will be run
    :param plot: True to plot on a graph the delta values as the number of nodes grows
    :param p: edge probability
    :param weights: random | positive
    :param positive_cycle_check: True or False, to enable or skip the check for null cycle weight
    :param verbose: True  [False] to enable [disable] verbosity
    :return: dictionary {n_nodes: memory_usage} with memory usages for each different run and n_nodes as key
    """
    assert weights == "random" or weights == "positive"
    memory_usage_dictionary = {}
    for n in node_list:
        memory_usage_dictionary[n] = random_graph_instantiation_memory(n_nodes=n, p=p, weights=weights, positive_cycle_check=positive_cycle_check, verbose=verbose)

    if plot:
        plot_dictionary(memory_usage_dictionary)

    if verbose:
        print(memory_usage_dictionary)
    return memory_usage_dictionary



