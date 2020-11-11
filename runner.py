import argparse
from profilers.time_profiler import *
from profilers.mem_profiler import *
from tests.cp_tests import *
from tests.opt1_2_test import *
from retiming.RetimingGraph import RetimingGraph
from algorithms.wd_algorithm import wd_algorithm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Correctness test parsers
    parser.add_argument("--paper_test_opt", action='store_true',
                        help="Test OPT1 and OPT2 algorithms on paper and slides graph")
    parser.add_argument("--random_test_opt12", action='store_true',
                        help="Test OPT1 and OPT2 algorithms on a list of random graphs")
    parser.add_argument("--random_opt1", action='store_true', help="Test OPT1 algorithm on a random graph")
    parser.add_argument("--random_opt2", action='store_true', help="Test OPT2 algorithm on a random graph")
    parser.add_argument("--random_wd", action='store_true', help="Test wd algorithm on a random graph")

    # Performance test parsers
    parser.add_argument("--time_instantiation", action='store_true',
                        help="Test time of instantiation on a list of random graphs")
    parser.add_argument("--time_wd", action='store_true', help="Test time of WD on a list of random graphs")
    parser.add_argument("--time_opt1", action='store_true', help="Test time of OPT1 on a list of random graphs")
    parser.add_argument("--time_opt2", action='store_true', help="Test time of OPT2 on a list of random graphs")

    parser.add_argument("--memory_instantiation", action='store_true',
                        help="Test memory of instantiation on a list of random graphs")
    parser.add_argument("--memory_wd", action='store_true', help="Test memory of WD on a list of random graphs")
    parser.add_argument("--memory_opt1", action='store_true', help="Test memory of OPT1 on a list of random graphs")
    parser.add_argument("--memory_opt2", action='store_true', help="Test memory of OPT2 on a list of random graphs")

    parser.add_argument("--plot_performance", action='store_true', help="Plot performance graph")
    # General random graph parameters
    parser.add_argument('--nodes_list', default=[4, 10, 15, 20, 25, 30], nargs='+', type=int,
                        help="List of random graph number of nodes to run tests")

    parser.add_argument("--weights", default="positive", type=str, help="Set weights, random or positive")
    parser.add_argument("--cycle_check", action='store_true', help="Check for positive cycles")
    parser.add_argument("--n_tests", default=1, type=int,
                        help="How many tests for random OPT1 and OPT2 algorithms testing")

    parser.add_argument("--n_nodes", default=20, type=int, help="Number of random nodes for a random graph")
    parser.add_argument("--edge_prob", default=0.6, type=float, help="Set edge probability for a random graph")

    # General test variables
    parser.add_argument("--verbose", action='store_true', help="Set verbosity to true")
    parser.add_argument("--draw", action='store_true', help="Draw graphs")

    args = parser.parse_args()

    if args.weights == "random":
        cycle_check = True
    else:
        cycle_check = args.cycle_check
    # Graph correctness testing
    if args.random_wd:
        g = RetimingGraphRandom(n_vertices=args.n_nodes, edge_probability=args.edge_prob, weights=args.weights,
                                verbose=args.verbose)
        wd_algorithm(g.graph, draw=args.draw, verbose=args.verbose)

    if args.random_opt1:
        g = RetimingGraphRandom(n_vertices=args.n_nodes, edge_probability=args.edge_prob, weights=args.weights,
                                verbose=args.verbose)
        opt1_algorithm(g.graph, draw=args.draw, verbose=args.verbose)

    if args.random_opt2:
        g = RetimingGraphRandom(n_vertices=args.n_nodes, edge_probability=args.edge_prob, weights=args.weights,
                                verbose=args.verbose)
        opt2_algorithm(g.graph, draw=args.draw, verbose=args.verbose)

    if args.random_test_opt12:
        random_test_opt1_opt2(n_tests=args.n_tests, n_nodes_list=args.nodes_list, weights=args.weights,
                              verbose=args.verbose)

    # Algorithms performance
    # Time
    if args.time_instantiation:
        multiple_time_random_graph_instantiation(node_list=args.nodes_list, p=args.edge_prob, weights=args.weights,
                                                 positive_cycle_check=cycle_check, verbose=args.verbose,
                                                 plot=args.plot_performance)

    if args.time_wd:
        multiple_time_random_wd(node_list=args.nodes_list, weights=args.weights, positive_cycle_check=cycle_check,
                                verbose=args.verbose, plot=args.plot_performance)

    if args.time_opt1:
        multiple_time_random_opt1(node_list=args.nodes_list, weights=args.weights,
                                  positive_cycle_check=cycle_check,
                                  verbose=args.verbose, plot=args.plot_performance)

    if args.time_opt2:
        multiple_time_random_opt2(node_list=args.nodes_list, weights=args.weights,
                                  positive_cycle_check=cycle_check,
                                  verbose=args.verbose, plot=args.plot_performance)

    # Memory
    if args.memory_instantiation:
        multiple_memory_random_graph_instantiation(node_list=args.nodes_list, p=args.edge_prob, weights=args.weights,
                                                   positive_cycle_check=cycle_check, verbose=args.verbose,
                                                   plot=args.plot_performance)

    if args.memory_wd:
        multiple_memory_random_wd(node_list=args.nodes_list, weights=args.weights,
                                  positive_cycle_check=cycle_check,
                                  verbose=args.verbose, plot=args.plot_performance)

    if args.memory_opt1:
        multiple_memory_random_opt1(node_list=args.nodes_list, weights=args.weights,
                                    positive_cycle_check=cycle_check,
                                    verbose=args.verbose, plot=args.plot_performance)

    if args.memory_opt2:
        multiple_memory_random_opt2(node_list=args.nodes_list, weights=args.weights,
                                    positive_cycle_check=cycle_check,
                                    verbose=args.verbose, plot=args.plot_performance)
