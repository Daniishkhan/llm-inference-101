"""Write it, chapter 1: count the characters in UTF-8 bytes, without decoding them.

You are given valid UTF-8: the bytes of some text. Return how many characters the text has. The
UTF-8 table of chapter 1 is all you need: look at what each kind of byte looks like in binary.

    count_characters(b"hello")                 ->  5
    count_characters("é€🙂".encode("utf-8"))    ->  3     2 + 3 + 4 = 9 bytes
    count_characters(b"")                      ->  0

Use bit masks on the bytes; do not decode them (the tests read your file). Ten minutes.
"""


def count_characters(data: bytes) -> int:
    raise NotImplementedError("TODO(you)")
