"""Drill 01-3: sort three colours in place, in one pass.

A list holds only the values 0, 1 and 2 (think red, white and blue). Rearrange it in place so that
all the 0s come first, then all the 1s, then all the 2s. Return nothing: change the list you were
given.

    colours = [2, 0, 2, 1, 1, 0]
    sort_colours(colours)
    colours  ->  [0, 0, 1, 1, 2, 2]

The rules: one pass over the list, swapping elements, with a few variables and no second list.
Counting the 0s, 1s and 2s and then writing them back takes two passes, so it does not count. The
tests read your function and fail if it calls sorted() or .sort().

This move is the heart of quickselect: smaller than a pivot to the left, larger to the right, equal
in the middle. Module 1's quickselect milestone (M3) uses it, so do this drill first.

Time box: 25 minutes.
"""


def sort_colours(colours: list[int]) -> None:
    raise NotImplementedError("TODO(you)")
