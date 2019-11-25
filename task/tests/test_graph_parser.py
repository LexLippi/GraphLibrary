import unittest
from task.graph_library.graph_parser import Parser
from task.graph_library.graph_types import (UnweightedOrderedGraph,
                                            UnweightedUnorderedGraph,
                                            WeightedOrderedGraph,
                                            WeightedUnorderedGraph)


class ParserTest(unittest.TestCase):
    def test_unweighted_adjacency_matrix_read(self):
        graph = Parser.read(['adjmat', '* 1 *', '1 * 1', '* 1 *'])
        exp_adjacency_list = [[1], [0, 2], [1]]
        self.assertIsInstance(graph, UnweightedUnorderedGraph)
        self.assertEqual(graph.node_count, 3)
        self.assertListEqual(graph.adjacency_list, exp_adjacency_list)

    def test_weighted_adjacency_matrix_read(self):
        graph = Parser.read(['adjmat w', '* 6 *', '6 * 2', '* 2 *'])
        exp_adjacency_list = [[1], [0, 2], [1]]
        exp_weights = {(0, 1): 6, (1, 0): 6, (1, 2): 2, (2, 1): 2}
        self.assertIsInstance(graph, WeightedUnorderedGraph)
        self.assertEqual(graph.node_count, 3)
        self.assertListEqual(graph.adjacency_list, exp_adjacency_list)
        self.assertDictEqual(graph.weights, exp_weights)

    def test_adjacency_list_read(self):
        graph = Parser.read(['adjlist w', '1: 3 0 4 5', '2: 4 1 5 7',
                            '3: 1 0 5 2', '4: 1 5 2 1', '5: 2 7 3 2'])
        exp_weights = {(0, 2): 0, (0, 3): 5, (1, 3): 1, (1, 4): 7, (2, 0): 0,
                       (2, 4): 2, (3, 0): 5, (3, 1): 1, (4, 1): 7, (4, 2): 2}
        exp_adjacency_list = [[2, 3], [3, 4], [0, 4], [0, 1], [1, 2]]
        self.assertIsInstance(graph, WeightedUnorderedGraph)
        self.assertEqual(graph.node_count, 5)
        self.assertListEqual(graph.adjacency_list, exp_adjacency_list)
        self.assertDictEqual(graph.weights, exp_weights)

    def test_edge_list_read(self):
        graph = Parser.read(['edlist w o', '1 2 2', '2 3 3', '1 3 1'])
        exp_adjacency_list = [[1, 2], [2], []]
        self.assertIsInstance(graph, WeightedOrderedGraph)
        self.assertEqual(graph.node_count, 3)
        self.assertListEqual(graph.adjacency_list, exp_adjacency_list)

    def test_graph_types(self):
        graph = Parser.read(['adjmat w o'])
        self.assertIsInstance(graph, WeightedOrderedGraph)
        graph = Parser.read(['adjmat o'])
        self.assertIsInstance(graph, UnweightedOrderedGraph)
        graph = Parser.read(['adjmat w'])
        self.assertIsInstance(graph, WeightedUnorderedGraph)
        graph = Parser.read(['adjmat'])
        self.assertIsInstance(graph, UnweightedUnorderedGraph)

    def test_different_case_title(self):
        graph = Parser.read(['aDJLisT w O'])
        self.assertIsInstance(graph, WeightedOrderedGraph)

    def test_incorrect_graph_type(self):
        graph = Parser.read(['bafbaekh.vba;'])
        self.assertIsNone(graph)

    def test_graph_has_no_weights_if_they_are_not_declared(self):
        graph = Parser.read(['adjmat', '* 6 *', '6 * 2', '* 2 *'])
        self.assertIsInstance(graph, UnweightedUnorderedGraph)
        self.assertFalse(hasattr(graph, 'weights'))

    def test_empty_graph(self):
        graph = Parser.read(['adjmat'])
        self.assertEqual(graph.node_count, 0)
        self.assertListEqual(graph.edge_list, [])
        self.assertListEqual(graph.adjacency_list, [])
        self.assertListEqual(graph.adjacency_vertices, [])


if __name__ == '__main__':
    unittest.main()
