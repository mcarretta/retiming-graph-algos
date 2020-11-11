from algorithms.cp_algorithm import *
from tests.paper_test_graphs import get_paper_graphs


def test_delta_array():
    """
    Test delta array function over Leierson - Saxe example and Professor Jie-Hong R. Jiang's slides example
    :return:
    """
    g1, test1, g2, test2 = get_paper_graphs()
    delta_1 = delta_array(g1.graph)
    delta_2 = delta_array(g2.graph)

    assert delta_1 == test1["delta"]
    assert delta_2 == test2["delta"]


def test_cp():
    """
    Tests algorithm CP (clock period) on graphs on Leierson - Saxe paper and on ,
    National Taiwan University
    http://recipe.ee.ntu.edu.tw/LabWebsite/miniworkshop_Opt+App/Session%204-1%20JHJiang%20%5B%E7%9B%B8%E5%AE%B9%E6%A8%A1%E5%BC%8F%5D.pdf
    """
    g1, test1, g2, test2 = get_paper_graphs()

    assert cp_algorithm(g1.graph) == test1["clock_period"]
    assert cp_algorithm(g2.graph) == test2["clock_period"]
