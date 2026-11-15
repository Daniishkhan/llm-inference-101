"""Diagnostic 3: two numbers that add up to a target.

Given a list of whole numbers and a target, find the two positions whose numbers add up to the
target and return them as (i, j) with i < j. If no two positions do, return None.

    pair_with_sum([2, 7, 11, 15], 9)  ->  (0, 1)      because 2 + 7 == 9
    pair_with_sum([3, 3], 6)          ->  (0, 1)
    pair_with_sum([1, 2, 3], 7)       ->  None

A position cannot be used twice: in [3, 5] with target 6 there is no pair. You may assume that at
most one pair exists. The list can hold tens of thousands of numbers, and the last test checks that
the answer still comes back well inside a second.

Time box: 20 minutes.
"""


def pair_with_sum(numbers: list[int], target: int) -> tuple[int, int] | None:
    raise NotImplementedError("TODO(you)")
