"""Write it, chapter 3: turn a lookup table around.

Given a dict, return a new dict that maps each value back to its key. That only works when no two
keys share a value; if two do, raise ValueError and name the value in the message.

    invert_table({"a": 1, "b": 2})   ->  {1: "a", 2: "b"}
    invert_table({})                 ->  {}
    invert_table({"a": 1, "b": 1})   raises ValueError

The dict you are given must come back unchanged. Ten minutes.
"""

from collections.abc import Hashable, Mapping


def invert_table[K: Hashable, V: Hashable](table: Mapping[K, V]) -> dict[V, K]:
    raise NotImplementedError("TODO(you)")
