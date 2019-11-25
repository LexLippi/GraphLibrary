from task.graph_library.graph_types import (UnweightedOrderedGraph,
                                            UnweightedUnorderedGraph,
                                            WeightedOrderedGraph,
                                            WeightedPlanarOrderedGraph,
                                            WeightedPlanarUnorderedGraph,
                                            WeightedUnorderedGraph)
from task.graph_library.graph import Graph
from task.graph_library.planarity_testing import PlanarTest


class GraphFactory:
    @staticmethod
    def create_graph(node_count, matrix, weighted, ordered):
        if not weighted and not ordered:
            return UnweightedUnorderedGraph(node_count, matrix)
        if not weighted and ordered:
            return UnweightedOrderedGraph(node_count, matrix)
        planar = PlanarTest(Graph(node_count, matrix)).lr_planarity()
        if planar and not ordered:
            return WeightedPlanarUnorderedGraph(node_count, matrix)
        if planar and ordered:
            return WeightedPlanarOrderedGraph(node_count, matrix)
        if not ordered:
            return WeightedUnorderedGraph(node_count, matrix)
        if ordered:
            return WeightedOrderedGraph(node_count, matrix)
