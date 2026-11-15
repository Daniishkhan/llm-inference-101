"""Drill 01-4: count the stretches that add up to a target.

You are given whole numbers in order, some of them negative, and a target. A stretch is one or more
numbers that sit next to each other in the list. Return how many stretches add up to exactly the
target. Two stretches that start or end in different places count separately, even when they hold
the same numbers. The list you are given must come back unchanged.

    count_stretches([1, 1, 1], 2)             ->  2     positions 0 to 1, and 1 to 2
    count_stretches([1, 2, 3], 3)             ->  2     [1, 2] and [3]
    count_stretches([3, 4, -7, 1, 3, 3], 7)   ->  3     [3, 4], [1, 3, 3] and the whole list
    count_stretches([1, -1, 1, -1], 0)        ->  4
    count_stretches([0, 0, 0], 0)             ->  6     every stretch there is
    count_stretches([], 0)                    ->  0     no numbers, no stretch

Trying every start with every end works and costs n * n steps. Do it in one pass, in time
proportional to n: the tests hand you 200,000 numbers and two seconds.

Time box: 35 minutes.
"""


def count_stretches(numbers: list[int], target: int) -> int:
    raise NotImplementedError("TODO(you)")
