"""M2: histogram. Run: uv run pytest tests/m01/test_histogram.py"""

import ast
import inspect
import math

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.bench import stats
from llm101.bench.stats import histogram


def assert_like_numpy(values, bins):
    counts, edges = histogram(values, bins)
    np_counts, np_edges = np.histogram(values, bins=bins)
    assert counts == [int(c) for c in np_counts]
    assert len(edges) == bins + 1
    for ours, theirs in zip(edges, np_edges, strict=True):
        assert math.isclose(ours, float(theirs), rel_tol=1e-12, abs_tol=1e-12)


def test_histogram_the_docstring_example():
    assert histogram([1, 2, 2, 3, 9], 4) == ([3, 1, 0, 1], [1.0, 3.0, 5.0, 7.0, 9.0])


def test_histogram_returns_bins_counts_and_bins_plus_one_edges():
    counts, edges = histogram([0.5, 1.5, 2.5], 7)
    assert len(counts) == 7
    assert len(edges) == 8


def test_histogram_every_value_is_counted_once():
    values = [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0]
    counts, _ = histogram(values, 3)
    assert sum(counts) == len(values)


def test_histogram_the_largest_value_goes_in_the_last_bin():
    counts, _ = histogram([0, 10], 5)
    assert counts == [1, 0, 0, 0, 1]


def test_histogram_a_value_on_an_inner_edge_goes_to_the_right():
    assert histogram([0, 1, 2, 3, 4], 4) == ([1, 1, 1, 2], [0.0, 1.0, 2.0, 3.0, 4.0])


def test_histogram_one_bin_holds_everything():
    assert histogram([5, 1, 3], 1) == ([3], [1.0, 5.0])


def test_histogram_all_values_equal():
    assert_like_numpy([2.0, 2.0, 2.0], 2)
    assert_like_numpy([7], 4)


def test_histogram_does_not_change_its_input():
    values = [3, 1, 2]
    histogram(values, 2)
    assert values == [3, 1, 2]


@pytest.mark.parametrize(("values", "bins"), [([], 3), ([1, 2], 0), ([1, 2], -1)])
def test_histogram_rejects_bad_input(values, bins):
    with pytest.raises(ValueError):
        histogram(values, bins)


def test_stats_does_not_import_numpy():
    tree = ast.parse(inspect.getsource(stats))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".")[0] != "numpy" for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] != "numpy"


finite = st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False, allow_subnormal=False)


@given(values=st.lists(finite, min_size=1, max_size=300), bins=st.integers(1, 50))
def test_histogram_matches_numpy_on_random_data(values, bins):
    assert_like_numpy(values, bins)


@given(values=st.lists(st.integers(-50, 50), min_size=1, max_size=300), bins=st.integers(1, 30))
def test_histogram_matches_numpy_on_whole_numbers(values, bins):
    # Whole numbers land exactly on edges much more often than random floats do.
    assert_like_numpy(values, bins)
