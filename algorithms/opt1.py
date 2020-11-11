import numpy as np

from algorithms.wd_algorithm import wd_algorithm
from utils.retiming_utils import *


def check_legal_retiming(graph, desired_clock, w_mat, d_mat, verbose=False):
    """
    Check if a retiming is legal by solving constraints through Bellman Ford algorithm after building a constraint graph
    Constraint graph construction from Professor Jie-Hong R. Jiang's slides, National Taiwan University
    http://recipe.ee.ntu.edu.tw/LabWebsite/miniworkshop_Opt+App/Session%204-1%20JHJiang%20%5B%E7%9B%B8%E5%AE%B9%E6%A8%A1%E5%BC%8F%5D.pdf

    There are 2 different sets of constraints for a retiming to be legal for a certain desired clock (retiming <= desired_clock):
    1) retiming(u) - retiming(v) <= w(e) for every edge u->v of graph
    2) retiming(u) - retiming(v) <= W(u, v) - 1 for all verices u, v of graph such that D(u, v) > desired clock

    :param graph: directed retiming graph
    :param desired_clock: desired clock we want to achieve
    :param w_mat: W matrix from WD algorithm
    :param d_mat: D matrix from WD algorithm
    :return: retiming if valid, else None
    """
    # 1) Build constraint graph
    G_constraint = nx.DiGraph()
    w = nx.get_edge_attributes(graph, "weight")
    edge_list_r = []
    # 1.1) Constraint retiming(u) - retiming(v) <= w(e) will result in an edge  v -> u with weight w(e)
    for u, v in graph.edges:
        edge_list_r.append((v, u, w[u, v]))
    # 1.2) Constraint retiming(u) - retiming(v) <= W(u, v) - 1 will result in an edge  v -> u with weight W(u, v) - 1
    for u, v in list(np.argwhere(d_mat > desired_clock)):
        edge_list_r.append((v, u, w_mat[u, v] - 1))
    # 1.3) Add a fictitious vertex v+1 and edge v+1 -> u for every vertex u in graph with weight 0
    for u in graph.nodes:
        edge_list_r.append(("V+1", u, 0))
    # Append those edges to constraint graph
    G_constraint.add_weighted_edges_from(edge_list_r)

    # Run Bellman Ford algo
    try:
        retiming = nx.single_source_bellman_ford_path_length(G_constraint, "V+1", "weight")
        # Remove fictitious vertex V+1 from retiming dictionary
        retiming.pop("V+1")
        if verbose:
            print(f"Feasible retiming exists with clock period {desired_clock}", retiming)
        return retiming
    # If we get a NetworkXUnbounded it means some constraints are not satisfied, hence for such desired clock there's no feasible retiming
    except nx.exception.NetworkXUnbounded:
        if verbose:
            print(f"No feasible retiming exists for clock period {desired_clock}")
        return None


def _opt1_binary_search(graph, vectorized_d, w_mat, d_mat, verbose=False):
    """
    Binary search for OPT1 algorithm
    :param graph: directed retiming graph
    :param vectorized_d: array of the sorted distinct value of matrix D
    :param w_mat: matrix W obtained with WD algorithm
    :param d_mat: matrix WW obtained with WD algorithm
    :param verbose: True  [False] to enable [disable] verbosity
    :return: minimum feasible retiming obtained by solving constraints through Bellman Ford algorithm
    """
    # Initialize left and right indices for the algorithm
    left, right = 0, len(vectorized_d) - 1
    # Empty dictionary that will store the retiming values
    retiming = {}
    # Until convergence, repeat
    while left <= right:
        # Take the middle element
        mid = (left + right) // 2
        retiming[mid] = check_legal_retiming(graph, vectorized_d[mid], w_mat, d_mat, verbose)
        if retiming[mid] is None:
            left = mid + 1
        else:
            right = mid - 1
    if verbose:
        print(f"The minimum achievable clock period is {vectorized_d[left]}")
    return retiming[left], vectorized_d[left]


def opt1_algorithm(graph, draw=False, verbose=False):
    """
    Implementation of the OPT1 algorithm from Leierson - Saxe paper. It uses as key elements the WD algorithm from Leierson - Saxe,
    a binary search algorithm and the Bellman-Ford algorithm on the constraint graph to solve the inequality constraints
    and obtain the optimal retiming, that is the solution of these constraint for the smallest possible value of the D matrix
    :param graph: retiming Networkx DiGrah
    :param draw: True | False
    :param verbose: True  [False] to enable [disable] verbosity
    :return:
    """
    if verbose:
        print("Computing optimal retiming with OPT1 algorithm")
    # 1) Compute W and D using algorithm WD
    w_mat, d_mat = wd_algorithm(graph, verbose=verbose)

    # 2) Sort the elements in the range of D
    vectorized_d = np.unique(np.sort(d_mat.flatten()))
    # Remove eventual nans from vectorized_d array
    vectorized_d = vectorized_d[~np.isnan(vectorized_d)]
    # 3) Binary search among the elements of D for the minimum available clock period, chek correctness with Bellman Ford
    retiming, optimal_clock = _opt1_binary_search(graph, vectorized_d, w_mat, d_mat, verbose=verbose)

    G_r = compute_retimed_graph(graph, retiming)

    if draw:
        draw_retiming_graph(G_r)

    return G_r, optimal_clock
