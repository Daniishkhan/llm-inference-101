import ast
import inspect
import random
import signal

import pytest
from hypothesis import given
from hypothesis import strategies as st

import k_largest as module
from k_largest import k_largest


def test_the_examples():
    assert k_largest([3, 9, 1, 7, 9, 2], 3) == [9, 9, 7]
    assert k_largest([4, 1], 5) == [4, 1]
    assert k_largest([4, 1], 0) == []


def test_an_empty_list():
    assert k_largest([], 3) == []


def test_repeats_count():
    assert k_largest([5, 5, 1], 2) == [5, 5]


def test_negative_numbers():
    assert k_largest([-3, -1, -2], 2) == [-1, -2]


def test_k_equal_to_the_length():
    assert k_largest([2, 3, 1], 3) == [3, 2, 1]


def test_a_negative_k_is_refused():
    with pytest.raises(ValueError):
        k_largest([1, 2], -1)


def test_the_list_you_were_given_is_not_changed():
    values = [3, 1, 2]
    k_largest(values, 2)
    assert values == [3, 1, 2]


@given(st.lists(st.integers(-100, 100), max_size=60), st.integers(0, 70))
def test_any_list(values, k):
    assert k_largest(values, k) == sorted(values, reverse=True)[:k]


def test_it_does_not_sort_or_ask_heapq_for_the_answer():
    assert k_largest([1, 3, 2], 2) == [3, 2], "first it must work"
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            assert name not in {"sorted", "sort", "nlargest", "nsmallest"}, (
                "find the k largest without sorting the whole list (see the docstring)"
            )


class StillRunning(Exception):
    pass


def stop_the_run(signum, frame):
    raise StillRunning


def test_a_million_numbers_with_k_one_thousand_in_two_seconds():
    rng = random.Random(2)
    values = [rng.randrange(10**9) for _ in range(1_000_000)]
    before = signal.signal(signal.SIGALRM, stop_the_run)
    signal.setitimer(signal.ITIMER_REAL, 2.0)
    try:
        result = k_largest(values, 1_000)
    except StillRunning:
        pytest.fail("still running after 2 s: finding the largest k times over costs n * k steps")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, before)
    assert result == sorted(values, reverse=True)[:1_000]
