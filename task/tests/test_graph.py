import unittest
from task.graph_library.graph import Graph
from task.graph_library.graph_factory import GraphFactory


class GraphTest(unittest.TestCase):
    def test_get_adjacency_list(self):
        graph = Graph(3, [[None, 1, 1], [1, None, 1], [1, 1, None]])
        self.assertEqual(graph.adjacency_list, [[1, 2], [0, 2], [0, 1]])

    def test_get_vertices(self):
        graph = Graph(3, [[None, 1, 1], [1, None, 1], [1, 1, None]])
        self.assertEqual(graph.get_adjacency_vertices(), [0, 1, 2])

    def test_get_edges(self):
        graph = Graph(3, [[None, 1, 1], [1, None, 1], [1, 1, None]])
        self.assertEqual(graph.edge_list, [(0, 1), (0, 2), (1, 2)])

    def test_empty_graph_with_not_empty_matrix(self):
        graph = Graph(0, [[None, 1, 1], [1, None, 1], [1, 1, None]])
        self.assertListEqual(graph.edge_list, [])
        self.assertListEqual(graph.adjacency_list, [])
        self.assertListEqual(graph.adjacency_vertices, [])
        self.assertListEqual(graph.adjacency_vertices, [])

    def test_edge_count(self):
        graph = Graph(
            5, [[None, 1, 1, 1, 1], [1, None, 1, 1, 1], [1, 1, None, 1, 1],
                [1, 1, 1, None, 1], [1, 1, 1, 1, None]])
        self.assertEqual(graph.edge_count, 10)

    def test_edge_count_in_ordered_graph(self):
        graph = GraphFactory().create_graph(
            3, [[None, 1, None], [None, None, 1], [None, None, None]],
            weighted=False, ordered=True)
        self.assertEqual(graph.edge_count, 2)


if __name__ == '__main__':
    unittest.main()
