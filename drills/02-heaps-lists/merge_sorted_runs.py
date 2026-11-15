"""Drill 02-4: merge many sorted runs into one.

You are given a list of runs. Each run is a list of whole numbers in rising order, and runs may be
empty. Return one list that holds every number of every run, in rising order.

    merge_sorted_runs([[1, 4, 9], [2, 3], [], [5]])  ->  [1, 2, 3, 4, 5, 9]
    merge_sorted_runs([])                            ->  []

With k runs and n numbers in all, looking at the first number of every run to find the smallest
costs k steps for each of the n numbers. Do it in n log k. The tests read your function and fail if
it calls sorted(), .sort() or heapq.merge, and they give it 500 runs of 400 numbers and two
seconds. The runs you are given must come back unchanged.

Time box: 35 minutes.
"""


def merge_sorted_runs(runs: list[list[int]]) -> list[int]:
    raise NotImplementedError("TODO(you)")
