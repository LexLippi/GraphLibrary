import unittest
from task.graph_library.infinity import Infinity


class InfinityTest(unittest.TestCase):
    def test_infinity_compare_with_number(self):
        inf = Infinity()
        a = 1000000
        b = 1e25
        self.assertTrue(inf > a)
        self.assertTrue(inf > b)
        self.assertTrue(inf >= a)
        self.assertTrue(inf >= b)
        self.assertTrue(inf != a)
        self.assertTrue(inf != b)
        self.assertFalse(inf < a)
        self.assertFalse(inf < b)
        self.assertFalse(inf <= a)
        self.assertFalse(inf <= b)

    def test_infinity_are_equal(self):
        first_inf = Infinity()
        second_inf = Infinity()
        self.assertTrue(first_inf >= second_inf)
        self.assertTrue(first_inf == second_inf)
        self.assertTrue(first_inf <= second_inf)


if __name__ == '__main__':
    unittest.main()
