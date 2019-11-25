import unittest
from task.graph_library.graph import Graph
from task.graph_library.planarity_testing import PlanarTest


class PlanarTestingTest(unittest.TestCase):
    def test_k5_graph(self):
        g = Graph(
            5, [[None, 1, 1, 1, 1], [1, None, 1, 1, 1], [1, 1, None, 1, 1],
                [1, 1, 1, None, 1], [1, 1, 1, 1, None]])
        self.assertFalse(PlanarTest(g).lr_planarity())

    def test_k33_graph(self):
        g = Graph(
            6, [[None, None, None, 1, 1, 1], [None, None, None, 1, 1, 1],
                [None, None, None, 1, 1, 1], [1, 1, 1, None, None, None],
                [1, 1, 1, None, None, None], [1, 1, 1, None, None, None]])
        self.assertFalse(PlanarTest(g).lr_planarity())

    def test_full_graph_less_than_5_nodes(self):
        g = Graph(3, [[None, 1, 1], [1, None, 1], [1, 1, None]])
        self.assertTrue(PlanarTest(g).lr_planarity())

    def test_full_graph_more_than_5_nodes(self):
        g = Graph(6, [[None, 1, 1, 1, 1, 1], [1, None, 1, 1, 1, 1],
                      [1, 1, None, 1, 1, 1], [1, 1, 1, None, 1, 1],
                      [1, 1, 1, 1, None, 1], [1, 1, 1, 1, 1, None]])
        self.assertFalse(PlanarTest(g).lr_planarity())

    def test_simple_planar_graph(self):
        g = Graph(5, [[None, 1, None, None, None], [1, None, 1, None, None],
                      [None, 1, None, 1, None], [None, None, 1, None, 1],
                      [None, None, None, 1, None]])
        self.assertTrue(PlanarTest(g).lr_planarity())

    def test_Petersen_graph(self):
        g = Graph(10, [[None, 1, None, None, 1, None, 1, None, None, None],
                  [1, None, 1, None, None, None, None, 1, None, None],
                  [None, 1, None, 1, None, None, None, None, 1, None],
                  [None, None, 1, None, 1, None, None, None, None, 1],
                  [1, None, None, 1, None, 1, None, None, None, None],
                  [None, None, None, None, 1, None, 1, 1, 1, 1],
                  [1, None, None, None, None, 1, None, 1, 1, 1],
                  [None, 1, None, None, None, 1, 1, None, 1, 1],
                  [None, None, 1, None, None, 1, 1, 1, None, 1],
                  [None, None, None, 1, None, 1, 1, 1, 1, None]])
        self.assertFalse(PlanarTest(g).lr_planarity())

    def test_no_simple_planar_graph(self):
        g = Graph(8, [
            [None, 1, None, None, None, None, None, None],
            [None, None, 1, 1, None, None, None, None],
            [None, 1, None, None, 1, None, None, None],
            [None, 1, None, None, None, 1, None, 1],
            [None, None, 1, None, None, 1, 1, None],
            [None, None, None, 1, 1, None, 1, None],
            [None, None, None, None, 1, 1, None, 1],
            [None, None, None, 1, None, None, 1, None]])
        self.assertTrue(PlanarTest(g).lr_planarity())


if __name__ == '__main__':
    unittest.main()
