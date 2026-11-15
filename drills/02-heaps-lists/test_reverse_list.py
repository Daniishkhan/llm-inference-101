from hypothesis import given
from hypothesis import strategies as st

from reverse_list import Node, reverse_list


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
        assert len(nodes) <= limit, "the list goes round in a loop: a link points backwards"
        head = head.next
    return nodes


def values_of(head):
    return [node.value for node in nodes_of(head)]


def test_an_empty_list():
    assert reverse_list(None) is None


def test_a_single_node():
    head = Node(7)
    assert reverse_list(head) is head
    assert head.next is None


def test_the_example():
    assert values_of(reverse_list(chain([1, 2, 3]))) == [3, 2, 1]


def test_two_nodes():
    assert values_of(reverse_list(chain([1, 2]))) == [2, 1]


def test_the_new_head_is_the_old_last_node():
    head = chain([1, 2, 3])
    last = head.next.next
    assert reverse_list(head) is last


def test_the_same_nodes_are_used():
    head = chain([4, 5, 6, 7])
    before = nodes_of(head)
    after = nodes_of(reverse_list(head))
    assert [id(node) for node in after] == [id(node) for node in reversed(before)], (
        "change the links of the nodes you were given; make no new Node"
    )


def test_the_old_head_is_now_the_end():
    head = chain([1, 2, 3])
    reverse_list(head)
    assert head.next is None


@given(st.lists(st.integers(), max_size=50))
def test_any_list(values):
    assert values_of(reverse_list(chain(values))) == values[::-1]


@given(st.lists(st.integers(), max_size=50))
def test_reversing_twice_gives_the_list_back(values):
    assert values_of(reverse_list(reverse_list(chain(values)))) == values


def test_a_chain_of_one_hundred_thousand_nodes():
    values = list(range(100_000))
    assert values_of(reverse_list(chain(values))) == values[::-1]
