"""M4: percentile, and the first half of "Done when".

Run: uv run pytest tests/m01/test_percentile.py
"""

import ast
import inspect
import math

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.bench.stats import percentile


def close_to_numpy(values, q):
    ours = percentile(values, q)
    theirs = float(np.percentile(values, q))
    return math.isclose(ours, theirs, rel_tol=1e-9, abs_tol=1e-9)


def test_percentile_the_docstring_examples():
    values = [40, 10, 30, 20]
    assert percentile(values, 50) == pytest.approx(25.0)
    assert percentile(values, 90) == pytest.approx(37.0)
    assert percentile(values, 0) == 10
    assert percentile(values, 100) == 40


def test_percentile_of_a_single_value():
    assert percentile([3.5], 99) == 3.5


def test_percentile_between_two_values():
    assert percentile([0, 10], 25) == pytest.approx(2.5)


def test_percentile_on_an_exact_position():
    assert percentile([5, 1, 4, 2, 3], 25) == 2


def test_percentile_with_repeats():
    for q in (50, 95, 99):
        assert close_to_numpy([1, 1, 1, 9], q)


def test_percentile_the_three_that_matter():
    values = list(range(100, 0, -1))
    for q in (50, 95, 99):
        assert close_to_numpy(values, q)


def test_percentile_does_not_change_its_input():
    values = [3, 1, 2]
    percentile(values, 50)
    assert values == [3, 1, 2]


def test_percentile_rejects_an_empty_list():
    with pytest.raises(ValueError):
        percentile([], 50)


@pytest.mark.parametrize("q", [-0.1, 100.1, 150])
def test_percentile_rejects_q_outside_0_to_100(q):
    with pytest.raises(ValueError):
        percentile([1, 2, 3], q)


def test_percentile_is_built_on_quickselect():
    tree = ast.parse(inspect.getsource(percentile))
    called = {
        getattr(node.func, "id", None) or getattr(node.func, "attr", None)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    }
    assert "quickselect" in called, "percentile finds its values with your quickselect()"


finite = st.floats(-1e6, 1e6, allow_nan=False, allow_infinity=False)


@given(values=st.lists(finite, min_size=1, max_size=400), q=st.floats(0, 100))
def test_done_when_percentiles_match_numpy_on_random_data(values, q):
    assert close_to_numpy(values, q)


@given(st.lists(st.integers(0, 10**9), min_size=1, max_size=400))
def test_percentile_p50_p95_p99_match_numpy_on_latency_like_data(values):
    for q in (50, 95, 99):
        assert close_to_numpy(values, q)
