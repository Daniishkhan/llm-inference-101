"""Drill 02-3: the k largest values, without sorting them all.

Given a list of whole numbers and a count k, return the k largest of them, largest first. Repeats
count: in [5, 5, 1] the two largest are [5, 5]. If k is more than the length of the list, return
every value, largest first.

    k_largest([3, 9, 1, 7, 9, 2], 3)  ->  [9, 9, 7]
    k_largest([4, 1], 5)              ->  [4, 1]
    k_largest([4, 1], 0)              ->  []

Sorting the whole list costs n log n steps; you only need k of them. Do it in about n log k steps.
The tests read your function and fail if it calls sorted(), .sort(), heapq.nlargest or
heapq.nsmallest, and they give it a million numbers with k = 1,000 and two seconds. The list you are
given must come back unchanged.

Raises ValueError if k is negative.

Time box: 25 minutes.
"""


def k_largest(values: list[int], k: int) -> list[int]:
    raise NotImplementedError("TODO(you)")
