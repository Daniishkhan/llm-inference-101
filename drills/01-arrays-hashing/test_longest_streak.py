import ast
import inspect
import random

from hypothesis import given
from hypothesis import strategies as st

import longest_streak as module
from longest_streak import longest_streak


def test_an_empty_list():
    assert longest_streak([]) == 0


def test_a_single_number():
    assert longest_streak([7]) == 1


def test_the_first_example():
    assert longest_streak([100, 4, 200, 1, 3, 2]) == 4


def test_a_streak_with_a_repeat_inside_it():
    assert longest_streak([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9


def test_repeats_count_once():
    assert longest_streak([5, 5, 5]) == 1


def test_negative_numbers():
    assert longest_streak([-2, -1, 0, 9]) == 3


def test_no_two_numbers_are_neighbours():
    assert longest_streak([10, 20, 30]) == 1


def test_two_streaks_of_the_same_length():
    assert longest_streak([1, 2, 3, 11, 12, 13]) == 3


def test_the_list_you_were_given_is_not_changed():
    numbers = [3, 1, 2]
    longest_streak(numbers)
    assert numbers == [3, 1, 2]


def test_it_does_not_sort():
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            assert name not in {"sorted", "sort"}, "do it without sorting (see the docstring)"


@given(
    lengths=st.lists(st.integers(1, 30), min_size=1, max_size=8),
    start=st.integers(-1000, 1000),
    seed=st.integers(),
)
def test_streaks_built_with_gaps_between_them(lengths, start, seed):
    # Build streaks of known lengths with a gap of at least one missing number between them,
    # add a few repeats, shuffle, and expect the longest length back.
    numbers = []
    value = start
    for length in lengths:
        numbers.extend(range(value, value + length))
        value += length + 1 + (seed % 3)
    rng = random.Random(seed)
    numbers += rng.choices(numbers, k=len(numbers) // 3)
    rng.shuffle(numbers)
    assert longest_streak(numbers) == max(lengths)
