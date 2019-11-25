from task.graph_library.graph import Graph
from collections import defaultdict


class PlanarTest:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.roots = []
        self.height = defaultdict(lambda: None)
        self.low_point = {}
        self.second_low_point = {}
        self.nesting_depth = {}
        self.parent_edge = defaultdict(lambda: None)
        new_matrix = [[None for _ in range(self.graph.node_count)]
                      for _ in range(self.graph.node_count)]
        self.new_graph = Graph(self.graph.node_count, new_matrix)
        self.ordered_adj = {}
        self.S = []
        self.stack_bottom = {}
        self.low_point_edge = {}
        self.ref = defaultdict(lambda: None)
        self.side = defaultdict(lambda: 1)

    def lr_planarity(self):
        if (self.graph.node_count > 2
                and self.graph.edge_count > 3 * self.graph.node_count - 6):
            return False
        for node in self.graph.adjacency_vertices:
            if self.height[node] is None:
                self.height[node] = 0
                self.roots.append(node)
                self.dfs_orientation(node)
        for node in self.new_graph.adjacency_vertices:
            self.ordered_adj[node] = sorted(
                self.new_graph.adjacency_list[node],
                key=lambda x: self.nesting_depth[(node, x)])
        for node in self.roots:
            if not self.dfs_testing(node):
                return False
        return True

    def dfs_orientation(self, node):
        dfs_stack = [node]
        ind = defaultdict(lambda: 0)
        skip_init = defaultdict(lambda: False)
        while dfs_stack:
            node = dfs_stack.pop()
            e = self.parent_edge[node]
            for next_node in self.graph.adjacency_list[node][ind[node]:]:
                edge = (node, next_node)
                if not skip_init[edge]:
                    if (edge in self.new_graph.edge_list
                            or (next_node, node) in self.new_graph.edge_list):
                        ind[node] += 1
                        continue
                    self.new_graph.add_edge(node, next_node)
                    self.low_point[edge] = self.height[node]
                    self.second_low_point[edge] = self.height[node]
                    if self.height[next_node] is None:
                        self.parent_edge[next_node] = edge
                        self.height[next_node] = self.height[node] + 1
                        dfs_stack.append(node)
                        dfs_stack.append(next_node)
                        skip_init[edge] = True
                        break
                    else:
                        self.low_point[edge] = self.height[next_node]
                self.nesting_depth[edge] = 2 * self.low_point[edge]
                if self.second_low_point[edge] < self.height[node]:
                    self.nesting_depth[edge] += 1
                if e is not None:
                    if self.low_point[edge] < self.low_point[e]:
                        self.second_low_point[e] = min(
                            self.low_point[e], self.second_low_point[edge])
                        self.low_point[e] = self.low_point[edge]
                    elif self.low_point[edge] > self.low_point[e]:
                        self.second_low_point[e] = min(
                            self.second_low_point[e], self.low_point[edge])
                    else:
                        self.second_low_point[e] = min(
                            self.second_low_point[e],
                            self.second_low_point[edge])
                ind[node] += 1

    def dfs_testing(self, node):
        dfs_stack = [node]
        ind = defaultdict(lambda: 0)
        skip_init = defaultdict(lambda: False)
        while dfs_stack:
            node = dfs_stack.pop()
            e = self.parent_edge[node]
            skip_final = False
            for next_node in self.ordered_adj[node][ind[node]:]:
                edge = (node, next_node)
                if not skip_init[edge]:
                    self.stack_bottom[edge] = top_of_stack(self.S)
                    if edge == self.parent_edge[next_node]:
                        dfs_stack.append(node)
                        dfs_stack.append(next_node)
                        skip_init[edge] = True
                        skip_final = True
                        break
                    else:
                        self.low_point_edge[edge] = edge
                        self.S.append(ConflictPair(right=Interval(edge, edge)))
                if self.low_point[edge] < self.height[node]:
                    if next_node == self.ordered_adj[node][0]:
                        self.low_point_edge[e] = self.low_point_edge[edge]
                    else:
                        if not self.add_constraints(edge, e):
                            return False
                ind[node] += 1
            if not skip_final and e is not None:
                self.remove_back_edges(e)
        return True

    def remove_back_edges(self, e):
        u = e[0]
        while self.S and top_of_stack(self.S).lowest(self) == self.height[u]:
            pair = self.S.pop()
            if pair.left.low is not None:
                self.side[pair.left.low] = -1
        if self.S:
            pair = self.S.pop()
            while pair.left.high is not None and pair.left.high[1] == u:
                pair.left.high = self.ref[pair.left.high]
            if pair.left.high is None and pair.left.low is not None:
                self.ref[pair.left.low] = pair.right.low
                self.side[pair.left.low] = -1
                pair.left.low = None
            while pair.right.high is not None and pair.right.high[1] == u:
                pair.right.high = self.ref[pair.right.high]
            if pair.right.high is None and pair.right.low is not None:
                self.ref[pair.right.low] = pair.left.low
                self.side[pair.right.low] = -1
                pair.right.low = None
            self.S.append(pair)
        if self.low_point[e] < self.height[u]:
            hl = top_of_stack(self.S).left.high
            hr = top_of_stack(self.S).right.high
            if hl is not None and (
                    hr is None or self.low_point[hl] > self.low_point[hr]):
                self.ref[e] = hl
            else:
                self.ref[e] = hr

    def add_constraints(self, edge, e):
        pair = ConflictPair()
        while True:
            queue = self.S.pop()
            if not queue.left.empty():
                queue.swap()
            if not queue.left.empty():
                return False
            if self.low_point[queue.right.low] > self.low_point[e]:
                if pair.right.empty():
                    pair.right = queue.right.copy()
                else:
                    self.ref[pair.right.low] = queue.right.high
                pair.right.low = queue.right.low
            else:
                self.ref[queue.right.low] = self.low_point_edge[e]
            if top_of_stack(self.S) == self.stack_bottom[edge]:
                break
        while (top_of_stack(self.S).left.conflicting(edge, self) or
               top_of_stack(self.S).right.conflicting(edge, self)):
            queue = self.S.pop()
            if queue.right.conflicting(edge, self):
                queue.swap()
            if queue.right.conflicting(edge, self):
                return False
            self.ref[pair.right.low] = queue.right.high
            if queue.right.low is not None:
                pair.right.low = queue.right.low
            if pair.left.empty():
                pair.left = queue.left.copy()
            else:
                self.ref[pair.left.low] = queue.left.high
            pair.left.low = queue.left.low
        if not (pair.left.empty() and pair.right.empty()):
            self.S.append(pair)
        return True


class Interval:
    def __init__(self, low=None, high=None):
        self.low = low
        self.high = high

    def empty(self):
        return self.low is None and self.high is None

    def copy(self):
        return Interval(self.low, self.high)

    def conflicting(self, b, planarity_state):
        return (not self.empty()
                and planarity_state.low_point[self.high] >
                planarity_state.low_point[b])


class ConflictPair:
    def __init__(self, left=Interval(), right=Interval()):
        self.left = left
        self.right = right

    def swap(self):
        tmp = self.left
        self.left = self.right
        self.right = tmp

    def lowest(self, planarity_state):
        if self.left.empty():
            return planarity_state.low_point[self.right.low]
        if self.right.empty():
            return planarity_state.low_point[self.left.low]
        return min(planarity_state.low_point[self.left.low],
                   planarity_state.low_point[self.right.low])


def top_of_stack(stack):
    return stack[-1] if stack else None
