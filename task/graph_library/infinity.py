import functools


@functools.total_ordering
class Infinity:
    def __eq__(self, other):
        return isinstance(other, Infinity)

    def __ge__(self, other):
        return isinstance(other, (Infinity, int, float))
