from task.graph_library.graph import Graph


class UnweightedUnorderedGraph(Graph):
    pass


class UnweightedOrderedGraph(Graph):
    def __init__(self, node_count, matrix):
        super().__init__(node_count, matrix)
        self.edge_list = self.get_edges()
        self.edge_count = len(self.edge_list)

    def get_edges(self):
        edge_list = []
        for node in range(self.node_count):
            for connected_node in self.adjacency_list[node]:
                edge_list.append((node, connected_node))
        return edge_list


class WeightedUnorderedGraph(Graph):
    def __init__(self, node_count, matrix):
        super().__init__(node_count, matrix)
        self.weights, self.negative_weight = self.get_weights(matrix)

    def get_weights(self, matrix):
        weights = {}
        negative_weight = False
        for i in range(self.node_count):
            for j in range(self.node_count):
                if matrix[i][j] is not None:
                    weights[i, j] = matrix[i][j]
                    if matrix[i][j] < 0:
                        negative_weight = True
        return weights, negative_weight


class WeightedOrderedGraph(WeightedUnorderedGraph, UnweightedOrderedGraph):
    pass


class WeightedPlanarUnorderedGraph(WeightedUnorderedGraph):
    pass


class WeightedPlanarOrderedGraph(WeightedPlanarUnorderedGraph,
                                 WeightedOrderedGraph):
    pass
