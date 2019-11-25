import sys
import statistics
import time
from task.graph_library.graph_algo import (Bfs, Dfs, Dijkstra,
                                           FordBellman, AStar)

NUMBER_OF_LAUNCHES = 21


class Tester:
    @staticmethod
    def time_test(algorithm, graph, start_node, finish_node):
        times = []
        launch_const = 2.086
        for _ in range(2):
            algorithm(graph, start_node, finish_node)
        for i in range(NUMBER_OF_LAUNCHES):
            start_time = time.perf_counter()
            algorithm(graph, start_node, finish_node)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        delta = launch_const * statistics.stdev(times) / (
                (NUMBER_OF_LAUNCHES - 1) ** 0.5)
        return statistics.mean(times), delta

    @staticmethod
    def memory_test(algorithm, graph, start_node, finish_node):
        return (sys.getsizeof(algorithm(graph, start_node, finish_node))
                + sys.getsizeof(algorithm))

    def get_test_line(self, node_count, start_node, finish_node, graph,
                      weighted_graph, planar_graph,
                      negative_weighted_graph):
        print(node_count)
        bfs_time, bfs_delta = self.time_test(
            Bfs().find_path, graph, start_node, finish_node)
        dfs_time, dfs_delta = self.time_test(
            Dfs().find_path, graph, start_node, finish_node)
        dijkstra_time, dijkstra_delta = self.time_test(
            Dijkstra().find_path, weighted_graph, start_node, finish_node)
        ford_bellman_time, ford_bellman_delta = self.time_test(
            FordBellman().find_path, negative_weighted_graph, start_node,
            finish_node)
        a_star_time, a_star_delta_time = self.time_test(
            AStar().find_path, planar_graph, start_node, finish_node)
        bfs_memory = self.memory_test(
            Bfs().find_path, graph, start_node, finish_node)
        dfs_memory = self.memory_test(
            Dfs().find_path, graph, start_node, finish_node)
        dijkstra_memory = self.memory_test(
            Dijkstra().find_path, weighted_graph, start_node, finish_node)
        ford_bellman_memory = self.memory_test(
            FordBellman().find_path, negative_weighted_graph, start_node,
            finish_node)
        a_star_memory = self.memory_test(AStar().find_path, planar_graph,
                                         start_node, finish_node)
        test_result = {
            'Count of nodes': node_count, 'BFS average time': bfs_time,
            'BFS delta time': bfs_delta, 'DFS average time': dfs_time,
            'DFS delta time': dfs_delta,
            'Dijkstra average time': dijkstra_time,
            'Dijkstra delta time': dijkstra_delta,
            'Ford-Bellman average time': ford_bellman_time,
            'Ford-Bellman delta time': ford_bellman_delta,
            'A_Star average time': a_star_time,
            'A_Star delta time': a_star_delta_time, 'BFS memory': bfs_memory,
            'DFS memory': dfs_memory, 'Dijkstra memory': dijkstra_memory,
            'Ford-Bellman memory': ford_bellman_memory,
            'A_Star memory': a_star_memory}
        return test_result
