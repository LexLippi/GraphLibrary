import unittest
from task.graph_library.priority_queue import PriorityQueue


class PriorityQueueTest(unittest.TestCase):
    def test_priority_queue_push(self):
        q = PriorityQueue()
        q.push(0, 1)
        self.assertEqual([(0, 1)], q.items)

    def test_priority_queue_get(self):
        q = PriorityQueue()
        q.push(1, 0)
        q.push(11, 2)
        q.push(3, -1)
        self.assertEqual((1, 0), q.get())

    def test_priority_queue_init(self):
        q = PriorityQueue()
        self.assertEqual([], q.items)

    def test_priority_queue_is_empty(self):
        q = PriorityQueue()
        self.assertTrue(q.is_empty())
        q.push(7, 5)
        self.assertFalse(q.is_empty())


if __name__ == '__main__':
    unittest.main()
