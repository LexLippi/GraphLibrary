import unittest
from task.graph_library.graph_factory import GraphFactory
from task.graph_library.graph_algo import (Dfs, Dijkstra, Bfs, FordBellman,
                                           AStar)


class DfsTest(unittest.TestCase):
    def test_simple_path(self):
        graph = GraphFactory.create_graph(3, [[None, 1, None], [1, None, 1],
                                          [None, 1, None]], False, False)
        self.assertListEqual(Dfs().find_path(graph, 0, 1), [1, 2])

    def test_no_path(self):
        graph = GraphFactory.create_graph(4, [[None, None, None, None],
                                          [None, None, 1, 1],
                                          [None, 1, None, None],
                                          [None, 1, None, None]], False, False)
        self.assertIsNone(Dfs().find_path(graph, 0, 3))

    def test_no_nodes(self):
        graph = GraphFactory.create_graph(2, [[None, 0], [0, None]],
                                          False, False)
        self.assertIsNone(Dfs().find_path(graph, 0, 3))

    def test_weighted_graph(self):
        graph = GraphFactory.create_graph(5, [[None, 1, 2, 3, 4],
                                              [1, None, 2, 3, 4],
                                              [2, 2, None, 3, 4],
                                              [3, 3, 3, None, 4],
                                              [4, 4, 4, 4, None]], True, False)

        with self.assertRaises(TypeError) as context:
            Dfs().find_path(graph, 0, 4)
        self.assertIsInstance(context.exception, TypeError)


class BfsTest(unittest.TestCase):
    def test_simple_path(self):
        graph = GraphFactory.create_graph(3, [[None, 1, None], [1, None, 1],
                                          [None, 1, None]], False, True)
        self.assertListEqual(Bfs().find_path(graph, 0, 2), [1, 2, 3])

    def test_no_path(self):
        graph = GraphFactory.create_graph(3, [[None, 1, None],
                                              [None, None, None],
                                              [None, 1, None]], False, True)
        self.assertIsNone(Bfs().find_path(graph, 1, 2))

    def test_no_nodes(self):
        graph = GraphFactory.create_graph(3, [[None, 1, None],
                                              [None, None, None],
                                              [None, 1, None]], False, True)
        self.assertIsNone(Bfs().find_path(graph, 1, 12))

    def test_shortest_path(self):
        graph = GraphFactory.create_graph(7, [[None, 1, 1, None, None, None,
                                               None], [None, None, None, 1,
                                                       None, None, None],
                                              [None, None, None, 1, None, None,
                                               None], [None, None, None, None,
                                                       1, None, None],
                                              [None, None, None, None, None, 1,
                                               1],
                                              [None, None, None, None, None,
                                               None, None],
                                              [None, None, None, None, None, 1,
                                               None]], False, True)
        self.assertListEqual(Bfs().find_path(graph, 0, 5), [1, 2, 4, 5, 6])

    def test_weighted_graph(self):
        graph = GraphFactory.create_graph(5, [[None, 1, 2, 3, 4],
                                              [None, None, 2, 3, 4],
                                              [None, None, None, 3, 4],
                                              [None, None, None, None, 4],
                                              [4, 4, 4, 4, None]], True, True)
        with self.assertRaises(TypeError) as context:
            Bfs().find_path(graph, 0, 4)
        self.assertIsInstance(context.exception, TypeError)


class DijkstraTest(unittest.TestCase):
    def test_unweighted_graph(self):
        graph = GraphFactory.create_graph(1, [[1]], False, False)
        with self.assertRaises(TypeError) as context:
            Dijkstra().find_path(graph, 1, 1)
        self.assertIsInstance(context.exception, TypeError)

    def test_simple_path(self):
        graph = GraphFactory.create_graph(4, [[None, 1, None, None],
                                          [1, None, 2, None],
                                          [None, 2, None, 3],
                                          [None, None, 3, None]], True, False)
        self.assertListEqual(Dijkstra().find_path(graph, 0, 2), [1, 2, 3])
        self.assertListEqual(Dijkstra().find_path(graph, 3, 1), [4, 3, 2])

    def test_little_weights_path(self):
        graph = GraphFactory.create_graph(5, [[None, 5, 1, None, None],
                                              [5, None, None, None, 1],
                                              [1, None, None, 1, None],
                                              [None, None, 1, None, 1],
                                              [None, 1, None, 1, None]],
                                          True, False)
        self.assertListEqual(Dijkstra().find_path(graph, 0, 1),
                             [1, 3, 4, 5, 2])

    def test_no_path(self):
        graph = GraphFactory.create_graph(2, [[0, None], [2, 1]], True, True)
        self.assertIsNone(Dijkstra().find_path(graph, 0, 1))

    def test_no_nodes(self):
        graph = GraphFactory.create_graph(2, [[0, 0], [0, 0]], True, False)
        self.assertIsNone(Dijkstra().find_path(graph, 0, 5))

    def test_negative_weights(self):
        graph = GraphFactory.create_graph(2, [[0, -11], [-21, 0]], True, True)
        with self.assertRaises(TypeError) as context:
            Dijkstra().find_path(graph, 0, 5)
        self.assertIsInstance(context.exception, TypeError)


class FordBellmanTest(unittest.TestCase):
    def test_unweighted_graph(self):
        graph = GraphFactory.create_graph(2, [[None, 1], [1, None]], False,
                                          True)
        with self.assertRaises(TypeError) as context:
            FordBellman().find_path(graph, 1, 2)
        self.assertIsInstance(context.exception, TypeError)

    def test_unordered_graph(self):
        graph = GraphFactory.create_graph(2, [[0, 0], [0, 0]], True, False)
        with self.assertRaises(TypeError) as context:
            FordBellman().find_path(graph, 0, 1)
        self.assertIsInstance(context.exception, TypeError)

    def test_simple_path(self):
        graph = GraphFactory.create_graph(4, [[None, 1, None, None],
                                          [None, None, -2, None],
                                          [None, None, None, 3],
                                          [None, None, None, 11]], True, True)
        self.assertListEqual(FordBellman().find_path(graph, 0, 2), [1, 2, 3])

    def test_no_nodes(self):
        graph = GraphFactory.create_graph(4, [[None, 1, None, None],
                                          [None, None, -2, None],
                                          [None, None, None, 3],
                                          [None, None, None, 0]], True, True)
        self.assertIsNone(FordBellman().find_path(graph, 0, 5))

    def test_no_path(self):
        graph = GraphFactory.create_graph(4, [[None, 1, None, None],
                                          [None, None, -2, None],
                                          [None, None, None, 3],
                                          [None, None, None, 0]], True, True)
        self.assertIsNone(FordBellman().find_path(graph, 3, 1))

    def test_little_weights_path(self):
        graph = GraphFactory.create_graph(5, [[None, 1, None, None, -1],
                                              [1, None, 1, None, None],
                                              [None, 1, None, None, None],
                                              [None, None, 1, None, None],
                                              [None, None, None, -1, None]],
                                          True, True)
        self.assertListEqual(FordBellman().find_path(graph, 0, 1),
                             [1, 5, 4, 3, 2])

    def test_negative_weight_cycle(self):
        graph = GraphFactory.create_graph(3, [[None, -1, -2], [-1, None, -4],
                                              [-1, -4, None]], True, True)
        self.assertIsNone(FordBellman().find_path(graph, 0, 2))


class AStarTest(unittest.TestCase):
    def test_no_planar_graph(self):
        g = GraphFactory.create_graph(5, [
            [None, 1, 1, 1, 1], [1, None, 1, 1, 1], [1, 1, None, 1, 1],
            [1, 1, 1, None, 1], [1, 1, 1, 1, None]], True, False)
        with self.assertRaises(TypeError) as context:
            AStar().find_path(g, 0, 1)
        self.assertIsInstance(context.exception, TypeError)

    def test_simple_path(self):
        graph = GraphFactory.create_graph(4, [
            [None, 1, None, None], [1, None, None, None],
            [None, None, None, 3], [None, None, 3, None]], True, False)
        self.assertListEqual(AStar().find_path(graph, 0, 1), [1, 2])

    def test_no_path(self):
        graph = GraphFactory.create_graph(4, [
            [None, 1, None, None], [1, None, None, None],
            [None, None, None, 3], [None, None, 3, None]], True, False)
        self.assertIsNone(AStar().find_path(graph, 0, 2))

    def test_no_nodes(self):
        graph = GraphFactory.create_graph(4, [
            [None, 1, None, None], [1, None, None, None],
            [None, None, None, 3], [None, None, 3, None]], True, False)
        self.assertIsNone(AStar().find_path(graph, 0, 5))

    def test_little_weights_path(self):
        graph = GraphFactory.create_graph(4, [
            [None, 1, 2, None], [1, None, None, 3], [2, None, None, 3],
            [None, 3, 3, None]], True, False)
        self.assertListEqual(AStar().find_path(graph, 0, 3), [1, 2, 4])


if __name__ == '__main__':
    unittest.main()
