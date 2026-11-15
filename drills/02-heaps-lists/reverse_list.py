"""Drill 02-1: turn a linked list around, in place.

A linked list is a chain of Node objects. Each node holds a value and a link to the next node; the
last node's link is None. You are given the first node, the head, or None for an empty list. Turn
the chain around so that every link points the other way, and return the new head: the node that
was last.

    1 -> 2 -> 3 -> None     becomes     3 -> 2 -> 1 -> None
    reverse_list(None)  ->  None

Change the links of the nodes you were given. Make no new Node and no second list: a few variables
are enough. The tests check that the nodes are the same objects, and they give you a chain of
100,000 nodes, which is too long for a function that calls itself once per node.

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


def reverse_list(head: Node | None) -> Node | None:
    raise NotImplementedError("TODO(you)")
