import ast
import inspect
import random
import signal

import pytest
from hypothesis import given
from hypothesis import strategies as st

import merge_sorted_runs as module
from merge_sorted_runs import merge_sorted_runs


def test_the_examples():
    assert merge_sorted_runs([[1, 4, 9], [2, 3], [], [5]]) == [1, 2, 3, 4, 5, 9]
    assert merge_sorted_runs([]) == []


def test_only_empty_runs():
    assert merge_sorted_runs([[], [], []]) == []


def test_one_run():
    assert merge_sorted_runs([[1, 2, 3]]) == [1, 2, 3]


def test_repeats_across_runs():
    assert merge_sorted_runs([[1, 2, 2], [2, 3], [1]]) == [1, 1, 2, 2, 2, 3]


def test_runs_of_different_lengths():
    assert merge_sorted_runs([[10], [1, 2, 3, 4, 5, 11], [6]]) == [1, 2, 3, 4, 5, 6, 10, 11]


def test_the_runs_you_were_given_are_not_changed():
    runs = [[1, 3], [2]]
    merge_sorted_runs(runs)
    assert runs == [[1, 3], [2]]


@given(st.lists(st.lists(st.integers(-20, 20), max_size=10), max_size=8))
def test_any_runs(runs):
    runs = [sorted(run) for run in runs]
    assert merge_sorted_runs(runs) == sorted(value for run in runs for value in run)


def test_it_does_not_sort_or_hand_the_work_to_heapq_merge():
    assert merge_sorted_runs([[1, 3], [2]]) == [1, 2, 3], "first it must work"
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            assert name not in {"sorted", "sort"}, "merge the runs yourself, without sorting"
            if isinstance(node.func, ast.Attribute) and node.func.attr == "merge":
                owner = getattr(node.func.value, "id", None)
                assert owner != "heapq", "heapq.merge does the whole drill: merge the runs yourself"
        if isinstance(node, ast.ImportFrom) and node.module == "heapq":
            assert all(alias.name != "merge" for alias in node.names), (
                "heapq.merge does the whole drill: merge the runs yourself"
            )


class StillRunning(Exception):
    pass


def stop_the_run(signum, frame):
    raise StillRunning


def test_five_hundred_runs_of_four_hundred_in_two_seconds():
    rng = random.Random(3)
    runs = [sorted(rng.randrange(10**6) for _ in range(400)) for _ in range(500)]
    before = signal.signal(signal.SIGALRM, stop_the_run)
    signal.setitimer(signal.ITIMER_REAL, 2.0)
    try:
        result = merge_sorted_runs(runs)
    except StillRunning:
        pytest.fail(
            "still running after 2 s: looking at the head of every run for every number costs "
            "n * k steps"
        )
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, before)
    assert result == sorted(value for run in runs for value in run)
