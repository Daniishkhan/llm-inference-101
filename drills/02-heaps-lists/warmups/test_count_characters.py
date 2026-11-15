import ast
import inspect

from hypothesis import given
from hypothesis import strategies as st

import count_characters as module
from count_characters import count_characters


def test_the_examples():
    assert count_characters(b"hello") == 5
    assert count_characters("é€🙂".encode()) == 3
    assert count_characters(b"") == 0


def test_a_hindi_word():
    assert count_characters("नमस्ते".encode()) == 6


@given(st.text())
def test_any_text(text):
    assert count_characters(text.encode()) == len(text)


def test_it_does_not_decode():
    assert count_characters("€".encode()) == 1, "first it must work"
    tree = ast.parse(inspect.getsource(module))
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            assert node.attr != "decode", "count with masks, without decoding"
        if isinstance(node, ast.Call):
            assert getattr(node.func, "id", None) != "str", "str(data, ...) decodes too"
