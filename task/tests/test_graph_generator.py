import unittest
from graph_generator import GraphGenerator
from task.graph_library.graph_types import (WeightedOrderedGraph,
                                            WeightedUnorderedGraph,
                                            UnweightedOrderedGraph,
                                            UnweightedUnorderedGraph,
                                            WeightedPlanarOrderedGraph,
                                            WeightedPlanarUnorderedGraph)
from task.graph_library.planarity_testing import PlanarTest


class GraphGeneratorTest(unittest.TestCase):
    def test_generate_weighted_ordered_graph(self):
        graph_generator = GraphGenerator(3, True, True)
        graph = graph_generator.generate_graph()
        self.assertIsInstance(graph, WeightedOrderedGraph)

    def test_generate_unweighted_unordered_graph(self):
        graph_generator = GraphGenerator(3, False, False)
        graph = graph_generator.generate_graph()
        self.assertIsInstance(graph, UnweightedUnorderedGraph)

    def test_generate_weighted_unordered_graph(self):
        graph_generator = GraphGenerator(3, True, False)
        graph = graph_generator.generate_graph()
        self.assertIsInstance(graph, WeightedUnorderedGraph)

    def test_generate_unweighted_ordered_graph(self):
        graph_generator = GraphGenerator(3, False, True)
        graph = graph_generator.generate_graph()
        self.assertIsInstance(graph, UnweightedOrderedGraph)

    def test_is_equal_node_count(self):
        graph_generator = GraphGenerator(15, False, True)
        graph = graph_generator.generate_graph()
        self.assertEqual(graph.node_count, 15)

    def test_generate_planar_ordered_graph(self):
        graph_generator = GraphGenerator(10, True, True, planar=True)
        graph = graph_generator.generate_graph()
        self.assertIsInstance(graph, WeightedPlanarOrderedGraph)

    def test_generate_planar_unordered_graph(self):
        graph_generator = GraphGenerator(10, True, False, planar=True)
        graph = graph_generator.generate_graph()
        self.assertIsInstance(graph, WeightedPlanarUnorderedGraph)

    def test_generate_full_graph(self):
        graph_generator = GraphGenerator(10, True, False, full_graph=True)
        graph = graph_generator.generate_graph()
        self.assertFalse(PlanarTest(graph).lr_planarity())


if __name__ == '__main__':
    unittest.main()
