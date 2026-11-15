"""Diagnostic 4: balanced brackets.

A text is balanced when every opening bracket is closed by a bracket of the same kind, in the
right order. The three kinds are ( ), [ ] and { }. Every other character is ignored.

    is_balanced("a(b[c]{d})e")  ->  True
    is_balanced("([)]")         ->  False     closed in the wrong order
    is_balanced("((")           ->  False     never closed
    is_balanced("")             ->  True

Time box: 15 minutes.
"""


def is_balanced(text: str) -> bool:
    raise NotImplementedError("TODO(you)")
