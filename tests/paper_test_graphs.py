from retiming.RetimingGraph import RetimingGraph
from utils.retiming_utils import draw_retiming_graph


def get_paper_graphs(draw=False):
    """
    Get paper and slide graphs, alongside with a dictionary of test values we already know to be correct
    :param draw: True | False, draws the graphs
    :return: RetimingGraph objects 1 and 2 alongside with a dictionary with their tests
    """
    """
    Graph from Leierson - Saxe paper
    Minimum feasible clock period = 13
    """

    v = [0, 1, 2, 3, 4, 5, 6, 7]
    d = [0, 3, 3, 3, 3, 7, 7, 7]
    e = [[0, 1], [1, 2], [1, 7], [2, 3], [2, 6], [3, 4], [3, 5], [4, 5], [5, 6], [6, 7], [7, 0]]
    w = [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
    g1 = RetimingGraph(v, e, d, w)
    test_values1 = {"clock_period": 24, "delta": {0: 24, 1: 3, 2: 3, 3: 3, 4: 3, 5: 10, 6: 17, 7: 24}, "opt1": 13, "opt2": 13}
    if draw:
        draw_retiming_graph(g1.graph)

    """
    Graph Professor Jie-Hong R. Jiang's slides, National Taiwan University
    http://recipe.ee.ntu.edu.tw/LabWebsite/miniworkshop_Opt+App/Session%204-1%20JHJiang%20%5B%E7%9B%B8%E5%AE%B9%E6%A8%A1%E5%BC%8F%5D.pdf
    Minimum feasible clock period = 7
    """
    v = [0, 1, 2, 3]
    d = [0, 3, 3, 7]
    e = [[0, 1], [1, 2], [1, 3], [2, 3], [3, 0]]
    w = [2, 0, 0, 0, 0]
    g2 = RetimingGraph(v, e, d, w)
    test_values2 = {"clock_period": 13, "delta": {0: 13, 1: 3, 2: 6, 3: 13}, "opt1": 7, "opt2": 7}
    if draw:
        draw_retiming_graph(g2.graph)

    return g1, test_values1, g2, test_values2
