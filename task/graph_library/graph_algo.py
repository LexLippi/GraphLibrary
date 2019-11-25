from collections import deque
from task.graph_library.infinity import Infinity
from task.graph_library.priority_queue import PriorityQueue
from task.graph_library.graph_types import (UnweightedUnorderedGraph,
                                            UnweightedOrderedGraph,
                                            WeightedOrderedGraph,
                                            WeightedPlanarUnorderedGraph,
                                            WeightedPlanarOrderedGraph,
                                            WeightedUnorderedGraph)


class BaseGraphAlgorithms:
    @staticmethod
    def _get_path(start_node, finish_node, track):
        """
        Функция, которая принимает на вход начальную и конечную вершину, а
        также словарь, в котором каждому ключу(вершине) соответствует родитель
        и вес ребра из родителя до этой вершины. Эта функция возвращает список
        переходов от начальной до конечной вершины
        """
        if finish_node not in track:
            return
        path = [finish_node + 1]
        while finish_node != start_node:
            finish_node = track[finish_node][0]
            path.append(finish_node + 1)
        path.reverse()
        return path


class Dfs(BaseGraphAlgorithms):
    def find_path(self, graph, start_node, finish_node):
        """
        Функция возвращает путь в графе от стартовой вершины до конечной,
        найденный с помощью алгоритма DFS, если такого пути нет, то
        возвращается None
        """
        exp_types = (UnweightedUnorderedGraph, UnweightedOrderedGraph)
        if type(graph) not in exp_types:
            raise TypeError('This type is not expected for this algorithm')
        stack = [start_node]
        used = {start_node}
        track = {start_node: (None, 0)}
        while stack:
            current_start_node = stack.pop()
            for j in graph.adjacency_list[current_start_node]:
                current_finish_node = j
                if current_finish_node not in used:
                    stack.append(current_finish_node)
                    used.add(current_finish_node)
                    track[current_finish_node] = (
                        current_start_node, track[current_start_node][1] + 1)
        return self._get_path(start_node, finish_node, track)


class Bfs(BaseGraphAlgorithms):
    def find_path(self, graph, start_node, finish_node):
        """
        Функция возвращает путь в графе от стартовой вершины до конечной,
        найденный с помощью алгоритма BFS, если такого пути нет, то
        возвращается None
        """
        exp_types = (UnweightedUnorderedGraph, UnweightedOrderedGraph)
        if type(graph) not in exp_types:
            raise TypeError('This type is not expected for this algorithm')
        queue = deque()
        queue.append(start_node)
        used = set()
        used.add(start_node)
        track = {start_node: (None, 0)}
        while queue:
            current_start_node = queue.popleft()
            for j in graph.adjacency_list[current_start_node]:
                current_finish_node = j
                if current_finish_node not in used:
                    used.add(current_finish_node)
                    queue.append(current_finish_node)
                    track[current_finish_node] = (
                        current_start_node, track[current_start_node][1] + 1)
        return self._get_path(start_node, finish_node, track)


class Dijkstra(BaseGraphAlgorithms):
    def find_path(self, graph, start_node, finish_node):
        """
        Функция возвращает путь в графе от стартовой вершины до конечной,
        найденный с помощью алгоритма Дейкстры, если такого пути нет, то
        возвращается None
        """
        exp_types = (WeightedOrderedGraph, WeightedPlanarOrderedGraph,
                     WeightedPlanarUnorderedGraph, WeightedUnorderedGraph)
        if not isinstance(graph, exp_types) or graph.negative_weight:
            raise TypeError('This type is not expected for this algorithm')
        track = {start_node: (None, 0)}
        not_visited = graph.adjacency_vertices
        while True:
            to_open = None
            best_price = Infinity()
            for point in not_visited:
                if point in track and track[point][1] < best_price:
                    best_price = track[point][1]
                    to_open = point
            if to_open is None or to_open == finish_node:
                break
            for next_node in graph.adjacency_list[to_open]:
                current_price = (
                        track[to_open][1] + graph.weights[to_open, next_node])
                if next_node not in track or (
                        track[next_node][1] > current_price):
                    track[next_node] = (to_open, current_price)
            not_visited.pop(not_visited.index(to_open))
        return self._get_path(start_node, finish_node, track)


class FordBellman(BaseGraphAlgorithms):
    def find_path(self, graph, start_node, finish_node):
        """
        Функция возвращает путь в графе от стартовой вершины до конечной,
        найденный с помощью алгоритма Форда-Беллмана, если такого пути нет, то
        возвращается None
        """
        exp_types = (WeightedOrderedGraph, WeightedPlanarOrderedGraph)
        if not isinstance(graph, exp_types):
            raise TypeError('This type is not expected for this algorithm')
        track = {start_node: [None, 0]}
        for i in range(graph.node_count):
            for j in range(graph.edge_count):
                u, v = graph.edge_list[j]
                if u in track:
                    if v in track:
                        weight = min(track[v][1],
                                     track[u][1] + graph.weights[(u, v)])
                        prev = track[v][0] if track[v][1] == weight else u
                    else:
                        weight = track[u][1] + graph.weights[(u, v)]
                        prev = u
                    track[v] = [prev, weight]
        for u, v in graph.edge_list:
            if u in track and (
                    track[u][1] + graph.weights[(u, v)] < track[v][1]):
                return
        return self._get_path(start_node, finish_node, track)


class AStar(BaseGraphAlgorithms):
    def find_path(self, graph, start_node, finish_node):
        """
        Функция возвращает путь в графе от стартовой вершины до конечной,
        найденный с помощью алгоритма А* (А - стар), если такого пути нет, то
        возвращается None
        """
        exp_types = (WeightedPlanarOrderedGraph, WeightedPlanarUnorderedGraph)
        if not isinstance(graph, exp_types):
            raise TypeError('This type is not expected for this algorithm')
        self.get_dfs_heights(graph)
        if graph.node_count <= finish_node or start_node < 0:
            return None
        frontier = PriorityQueue()
        frontier.push(start_node, 0)
        track = {start_node: (None, 0)}
        while not frontier.is_empty():
            to_open = frontier.get()
            if to_open[0] == finish_node:
                break
            for next_node in graph.adjacency_list[to_open[0]]:
                if (to_open[0], next_node) not in graph.weights:
                    continue
                current_price = (
                        to_open[1] + graph.weights[to_open[0], next_node])
                if next_node not in track or (
                        current_price < track[next_node][1]):
                    track[next_node] = (to_open[0], current_price)
                    priority = (current_price + self.heuristic[to_open[0]] +
                                self.heuristic[finish_node])
                    frontier.push(next_node, priority)
        return self._get_path(start_node, finish_node, track)

    def get_dfs_heights(self, graph):
        self.heuristic = [0 for _ in range(graph.node_count)]
        start_node = 0
        stack = [start_node]
        used = {start_node}
        self.heuristic[start_node] = 0
        while stack:
            current_start_node = stack.pop()
            for j in graph.adjacency_list[current_start_node]:
                current_finish_node = j
                if current_finish_node not in used:
                    stack.append(current_finish_node)
                    self.heuristic[current_finish_node] = (
                            self.heuristic[current_start_node] + 1)
                    used.add(current_finish_node)
