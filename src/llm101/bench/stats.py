"""Statistics without numpy: selection, percentiles and histograms.

Milestones M2 (histogram), M3 (quickselect) and M4 (percentile). The tests compare your answers
with numpy's, and they read this file: it must not import numpy, and it must not call sorted() or
.sort().
"""

from collections.abc import Sequence


def quickselect(values: Sequence[float], k: int) -> float:
    """The k-th smallest of values, counting from 0, found without sorting.

        quickselect([7, 1, 5, 3], 0)  ->  1      the smallest
        quickselect([7, 1, 5, 3], 2)  ->  5
        quickselect([2, 2, 1], 1)     ->  2      repeats count: in order, the values are 1, 2, 2

    Without sorting is the point. Sorting costs about n log n steps. Selection finds one position in
    about n steps on average, because each round throws away the part of the list that the answer is
    not in. Do not call sorted() or .sort(), and do not change the list you were given: the tests
    check both.

    The tests also time it on lists that are already in order, rising and falling, and expect each
    to take about as long as a shuffled list of the same size, so choose the pivot so that ordered
    input is not your worst case.

    Raises ValueError if values is empty, and IndexError if k is not in range(len(values)).
    """
    raise NotImplementedError("TODO(you)")


def percentile(values: Sequence[float], q: float) -> float:
    """The q-th percentile of values, by numpy's default ("linear") method. q runs from 0 to 100.

    The definition, in words. Imagine the values in order, at positions 0 to n - 1. The percentile
    sits at position h = (n - 1) * q / 100. If h is a whole number, the answer is the value at
    position h. If h falls between two positions i and i + 1, the answer lies on the straight line
    between the two values there, as far along it as h is past i:

        values in order:  10, 20, 30, 40           n = 4
        q = 50:   h = 3 * 0.50 = 1.5    halfway from 20 to 30       ->  25.0
        q = 90:   h = 3 * 0.90 = 2.7    0.7 of the way from 30 to 40 ->  37.0
        q = 0 is the smallest value; q = 100 is the largest.

    Build it on your quickselect: do not sort, and do not call numpy (the tests check both). The
    list you were given is not changed.

    Raises ValueError if values is empty or q is outside [0, 100].
    """
    raise NotImplementedError("TODO(you)")


def histogram(values: Sequence[float], bins: int) -> tuple[list[int], list[float]]:
    """Count values into `bins` bins of equal width, the way numpy.histogram(values, bins) does.

    Returns (counts, edges): `bins` counts and `bins + 1` edges.

    - The range runs from the smallest value lo to the largest value hi. If lo equals hi, the range
      is lo - 0.5 to hi + 0.5 instead.
    - The edges are lo + i * step for i = 0, 1, ..., bins, where step = (hi - lo) / bins; the last
      edge is exactly hi.
    - A value v belongs to bin i when edges[i] <= v < edges[i + 1]. The last bin also includes its
      right edge, so the largest value is counted.
    - Decide membership with the edges themselves. A division can land a value one bin away from
      where the edges put it when floating-point rounding goes against you, and the tests compare
      with numpy.

        histogram([1, 2, 2, 3, 9], 4)  ->  ([3, 1, 0, 1], [1.0, 3.0, 5.0, 7.0, 9.0])

    Raises ValueError if values is empty or bins < 1.
    """
    raise NotImplementedError("TODO(you)")
