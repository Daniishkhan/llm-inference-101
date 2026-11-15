"""Drill 01-2: the longest streak of consecutive whole numbers.

You are given whole numbers in any order, with repeats allowed. A streak is a run of numbers that
follow each other with no gap, such as 4, 5, 6, 7 (length 4). Return the length of the longest
streak you can make from the numbers you were given. A number that appears several times still
counts once. The list you are given must come back unchanged.

    longest_streak([100, 4, 200, 1, 3, 2])           ->  4     the streak 1, 2, 3, 4
    longest_streak([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])   ->  9     0 to 8
    longest_streak([5, 5, 5])                        ->  1
    longest_streak([-2, -1, 0, 9])                   ->  3
    longest_streak([])                               ->  0

Sorting first would work and costs n log n. Do it without sorting, in time proportional to n: the
tests read your function and fail if it calls sorted() or .sort(), and they give it one streak of
200,000 numbers and two seconds.

Time box: 30 minutes.
"""


def longest_streak(numbers: list[int]) -> int:
    raise NotImplementedError("TODO(you)")
