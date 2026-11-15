"""Diagnostic 1: run-length encoding.

Squeeze a text by replacing each run of the same letter with the letter followed by the length of
the run.

    encode("aaabcc")  ->  "a3b1c2"
    encode("x")       ->  "x1"
    encode("")        ->  ""

The text contains letters only. Upper and lower case are different letters: "aA" is two runs.

Time box: 15 minutes.
"""


def encode(text: str) -> str:
    raise NotImplementedError("TODO(you)")
