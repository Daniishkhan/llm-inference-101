"""Diagnostic 5: merge overlapping intervals.

An interval is a pair (start, end) of whole numbers with start <= end, and it includes both ends.
Given a list of intervals in any order, merge the ones that overlap or touch, and return the
result sorted by start.

    merge([(1, 3), (2, 6), (8, 10)])  ->  [(1, 6), (8, 10)]
    merge([(1, 2), (2, 3)])           ->  [(1, 3)]            they touch at 2
    merge([(1, 2), (3, 4)])           ->  [(1, 2), (3, 4)]    they share no number
    merge([(5, 6), (1, 2)])           ->  [(1, 2), (5, 6)]    sorted by start
    merge([])                         ->  []

The list you are given must come back unchanged: build a new one.

Time box: 25 minutes.
"""


def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    raise NotImplementedError("TODO(you)")
