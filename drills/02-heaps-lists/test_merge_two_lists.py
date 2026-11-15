import ast
import inspect

from hypothesis import given
from hypothesis import strategies as st

import merge_two_lists as module
from merge_two_lists import Node, merge_two_lists


def chain(values):
    """A linked list holding values, in order; its head, or None."""
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def nodes_of(head, limit=1_000_000):
    """The nodes of a linked list, in order. Stops with a clear message on a loop."""
    nodes = []
    while head is not None:
        nodes.append(head)
        assert len(nodes) <= limit, "the list goes round in a loop"
        head = head.next
    return nodes


def values_of(head):
    return [node.value for node in nodes_of(head)]


def test_two_empty_lists():
    assert merge_two_lists(None, None) is None


def test_one_empty_list():
    head = chain([1, 2])
    assert merge_two_lists(head, None) is head
    assert merge_two_lists(None, head) is head


def test_the_example():
    merged = merge_two_lists(chain([1, 4, 6]), chain([2, 4, 5]))
    assert values_of(merged) == [1, 2, 4, 4, 5, 6]


def test_one_list_entirely_before_the_other():
    assert values_of(merge_two_lists(chain([1, 2]), chain([3, 4]))) == [1, 2, 3, 4]
    assert values_of(merge_two_lists(chain([3, 4]), chain([1, 2]))) == [1, 2, 3, 4]


def test_equal_values_take_the_first_list_first():
    first = chain([4])
    second = chain([4])
    merged = nodes_of(merge_two_lists(first, second))
    assert merged[0] is first and merged[1] is second


def test_every_node_is_used_and_none_is_new():
    first = chain([1, 3, 5, 7])
    second = chain([2, 3, 8])
    given_nodes = {id(node) for node in nodes_of(first) + nodes_of(second)}
    merged = nodes_of(merge_two_lists(first, second))
    assert {id(node) for node in merged} == given_nodes, "use the nodes you were given, all of them"
    assert len(merged) == len(given_nodes)


@given(st.lists(st.integers(-50, 50)), st.lists(st.integers(-50, 50)))
def test_any_two_sorted_lists(a, b):
    a.sort()
    b.sort()
    merged = values_of(merge_two_lists(chain(a), chain(b)))
    assert merged == sorted(a + b)


def test_it_does_not_collect_and_sort():
    assert values_of(merge_two_lists(chain([1, 3]), chain([2]))) == [1, 2, 3], "first it must work"
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            assert name not in {"sorted", "sort"}, "both chains are already in order: walk them"


def test_two_lists_of_one_hundred_thousand_nodes():
    evens = list(range(0, 200_000, 2))
    odds = list(range(1, 200_000, 2))
    assert values_of(merge_two_lists(chain(evens), chain(odds))) == list(range(200_000))
