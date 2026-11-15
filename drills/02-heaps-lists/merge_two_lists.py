"""Drill 02-2: merge two sorted linked lists into one.

You are given the heads of two linked lists, each already in rising order of value (either may be
None, an empty list). Join their nodes into one linked list in rising order, and return its head.

    1 -> 4 -> 6     and     2 -> 4 -> 5     become     1 -> 2 -> 4 -> 4 -> 5 -> 6
    merge_two_lists(None, None)  ->  None

When two values are equal, the node from the first list comes first. Use the nodes you were given
by changing their links: no node of the answer may be new, and every node of both lists must be in
it. The tests check this, and give you two lists of 100,000 nodes each.

Time box: 20 minutes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(eq=False, repr=False)
class Node:
    """One link of the chain. Given: compare nodes with `is`, and print one with repr()."""

    value: int
    next: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.value})"


def merge_two_lists(first: Node | None, second: Node | None) -> Node | None:
    raise NotImplementedError("TODO(you)")
