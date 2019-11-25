class Graph:
    def __init__(self, node_count, matrix):
        self.node_count = node_count
        self.adjacency_list = self.get_adjacency_list(matrix)
        self.adjacency_vertices = self.get_adjacency_vertices()
        self.edge_list = self.get_edges()
        self.edge_count = len(self.edge_list)

    def add_edge(self, start, stop):
        edge = (start, stop)
        self.edge_count += 1
        self.edge_list.append(edge)
        self.adjacency_list[start].append(stop)

    def get_edges(self):
        """
        Функция вовзвращает список ребер графа
        """
        edge_list = []
        for i in range(self.node_count):
            for j in self.adjacency_list[i]:
                if (j, i) not in edge_list:
                    edge_list.append((i, j))
        return edge_list

    def get_adjacency_list(self, matrix):
        """
        Функция по матрице смежности возвращает список смежности
        """
        adjacency_list = [[] for _ in range(self.node_count)]
        for i in range(self.node_count):
            for j in range(self.node_count):
                if matrix[i][j] is not None:
                    adjacency_list[i].append(j)
        return adjacency_list

    def get_adjacency_vertices(self):
        """
        Функция возвращает список вершин в графе
        """
        return list(range(self.node_count))
