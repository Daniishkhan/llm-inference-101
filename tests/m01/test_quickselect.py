"""M3: quickselect. Run: uv run pytest tests/m01/test_quickselect.py"""

import ast
import inspect
import math
import random
import time

import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.bench import stats
from llm101.bench.stats import quickselect


def test_quickselect_the_docstring_examples():
    assert quickselect([7, 1, 5, 3], 0) == 1
    assert quickselect([7, 1, 5, 3], 2) == 5
    assert quickselect([2, 2, 1], 1) == 2


def test_quickselect_a_single_value():
    assert quickselect([4.5], 0) == 4.5


def test_quickselect_the_largest():
    assert quickselect([3, 9, 1], 2) == 9


def test_quickselect_all_values_equal():
    assert quickselect([5] * 10, 7) == 5


def test_quickselect_negative_and_fractional_values():
    assert quickselect([-1.5, 2.25, -7.0, 0.0], 1) == -1.5


def test_quickselect_works_on_a_tuple():
    assert quickselect((3, 1, 2), 1) == 2


def test_quickselect_does_not_change_its_input():
    values = [9, 4, 7, 1, 8]
    quickselect(values, 2)
    assert values == [9, 4, 7, 1, 8]


def test_quickselect_rejects_an_empty_list():
    with pytest.raises(ValueError):
        quickselect([], 0)


@pytest.mark.parametrize("k", [-1, 3, 10])
def test_quickselect_rejects_a_k_out_of_range(k):
    with pytest.raises(IndexError):
        quickselect([1, 2, 3], k)


def test_stats_does_not_sort():
    tree = ast.parse(inspect.getsource(stats))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            assert name not in {"sorted", "sort"}, "stats.py selects; it never sorts"


@given(data=st.data())
def test_quickselect_agrees_with_sorting(data):
    values = data.draw(st.lists(st.floats(-1e9, 1e9, allow_nan=False), min_size=1, max_size=300))
    k = data.draw(st.integers(0, len(values) - 1))
    assert quickselect(values, k) == sorted(values)[k]


@given(st.lists(st.integers(-5, 5), min_size=1, max_size=200))
def test_quickselect_with_many_repeats(values):
    in_order = sorted(values)
    for k in {0, len(values) // 2, len(values) - 1}:
        assert quickselect(values, k) == in_order[k]


def test_quickselect_ordered_input_is_not_the_worst_case():
    n = 4_000
    ordered = list(range(n))
    shuffled = ordered[:]
    random.Random(1).shuffle(shuffled)

    def best_of_three(values):
        best = math.inf
        for _ in range(3):
            start = time.perf_counter()
            try:
                quickselect(values, n // 2)
            except RecursionError:
                pytest.fail(
                    "quickselect went more than 1,000 calls deep on 4,000 ordered numbers: "
                    "which pivot does an ordered list give you? (book chapter 3)"
                )
            best = min(best, time.perf_counter() - start)
        return best

    t_shuffled = best_of_three(shuffled)
    t_rising = best_of_three(ordered)
    t_falling = best_of_three(ordered[::-1])
    for order, took in (("rising", t_rising), ("falling", t_falling)):
        assert took < 10 * t_shuffled + 0.005, (
            f"input in {order} order took {took * 1e3:.1f} ms against {t_shuffled * 1e3:.1f} ms "
            f"shuffled: which pivot does a list in {order} order give you? (book chapter 3)"
        )
