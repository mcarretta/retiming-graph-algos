import numpy as np
from algorithms.wd_algorithm import wd_algorithm
from utils.retiming_utils import compute_retimed_graph, draw_retiming_graph
from algorithms.cp_algorithm import cp_algorithm, delta_array


def feas_algorithm(graph, desired_clock, verbose=False):
    """
    FEAS algorithm produces a retiming of a directed graph, and checks whether the clock period is less than desired_clock
    :param graph: directed retiming graph
    :param desired_clock: desired clock period, int
    :param verbose: True  [False] to enable [disable] verbosity
    :return: retiming graph
    """
    # 1) For each vertex of graph set retiming(v) = 0
    retiming = {v: 0 for v in graph.nodes}
    # 2) Repeat |V| - 1 times
    for i in range(len(graph.nodes) - 1):
        # 2.1) Compute graph G_r with the existing retiming
        G_r = compute_retimed_graph(graph, retiming)
        # 2.2) Run CP algorithm to compute delta_v array for each vertex of the graph
        delta = delta_array(G_r)
        # print(delta)
        # 2.3) For each vertex v such that delta(v), increase retiming(v) by 1
        for v, delta_v in delta.items():
            if delta_v > desired_clock:
                retiming[v] += 1
    if cp_algorithm(G_r) > desired_clock:
        if verbose:
            print(f"No feasible retiming exists for clock period {desired_clock}")
        return None
    else:
        if verbose:
            print(f"Feasible retiming exists with clock period {desired_clock}, and retiming: {retiming}")
        return retiming

def _opt2_binary_search(graph, vectorized_d, verbose=False):
    """
    Binary search to find the optimal clock period
    :param graph: directed retiming graph
    :param vectorized_d: sorted_elements in the range of matrix D
    :param verbose: True  [False] to enable [disable] verbosity
    :return: Optimal retiming
    """
    left, right = 0, len(vectorized_d) - 1
    retiming = {}
    while left <= right:
        mid = (left + right) // 2
        retiming[mid] = feas_algorithm(graph, vectorized_d[mid], verbose)
        if retiming[mid] is None:
            left = mid + 1
        else:
            right = mid - 1
    if verbose:
        print(f"The minimum achievable clock period is {vectorized_d[left]}")
    return retiming[left], vectorized_d[left]


def opt2_algorithm(graph, draw=False, verbose=False):
    """
    Optimal retiming computation for a directed graph
    :param graph: directed retiming graph
    :param draw: True if we want to draw the retimed graph
    :param verbose: True  [False] to enable [disable] verbosity
    :return: the retimed graph
    """
    if verbose:
        print("Computing optimal retiming with OPT2 algorithm")

    # 1) Compute W and D using algorithm WD
    _, d_mat = wd_algorithm(graph, verbose=verbose)
    # 2) Sort the elements in the range of D
    vectorized_d = np.unique(np.sort(d_mat.flatten()))
    vectorized_d = vectorized_d[~np.isnan(vectorized_d)]

    # 3) Binary search among the elements of D for the minimum available clock period, chek correctness with feas
    retiming, optimal_clock = _opt2_binary_search(graph, vectorized_d, verbose)

    # 4) Compute the retimed graph using the optimal solution from step 4
    G_r = compute_retimed_graph(graph, retiming)

    if draw:
        draw_retiming_graph(G_r)
    return G_r, optimal_clock
