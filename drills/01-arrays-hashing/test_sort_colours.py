import ast
import inspect

from hypothesis import given
from hypothesis import strategies as st

import sort_colours as module
from sort_colours import sort_colours


def sorted_in_place(colours):
    """Run sort_colours on a copy and return the copy, checking that it returns None."""
    copy = list(colours)
    assert sort_colours(copy) is None, "sort_colours changes the list and returns nothing"
    return copy


def test_the_example():
    assert sorted_in_place([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]


def test_an_empty_list():
    assert sorted_in_place([]) == []


def test_a_single_colour():
    assert sorted_in_place([1]) == [1]


def test_already_in_order():
    assert sorted_in_place([0, 1, 2]) == [0, 1, 2]


def test_in_reverse_order():
    assert sorted_in_place([2, 2, 1, 1, 0, 0]) == [0, 0, 1, 1, 2, 2]


def test_all_the_same():
    assert sorted_in_place([2, 2, 2]) == [2, 2, 2]


def test_only_two_of_the_colours():
    assert sorted_in_place([2, 0, 2, 0]) == [0, 0, 2, 2]


def test_it_changes_the_list_it_was_given():
    colours = [1, 0]
    sort_colours(colours)
    assert colours == [0, 1]


def test_it_does_not_sort():
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            assert name not in {"sorted", "sort"}, "swap elements instead (see the docstring)"


@given(st.lists(st.integers(0, 2), max_size=200))
def test_any_list_of_colours(colours):
    assert sorted_in_place(colours) == sorted(colours)
