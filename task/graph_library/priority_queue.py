import heapq


class PriorityQueue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item, priority):

        heapq.heappush(self.items, (item, priority))

    def get(self):
        return heapq.heappop(self.items)
