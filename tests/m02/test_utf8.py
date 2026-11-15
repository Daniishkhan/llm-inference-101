"""M1: utf8_encode. Run: uv run pytest tests/m02/test_utf8.py"""

import ast
import inspect

import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.tokenizer import utf8
from llm101.tokenizer.utf8 import utf8_encode


def test_utf8_encode_the_docstring_examples():
    assert utf8_encode("A") == b"A"
    assert utf8_encode("é") == b"\xc3\xa9"
    assert utf8_encode("€") == b"\xe2\x82\xac"
    assert utf8_encode("") == b""


def test_utf8_encode_returns_bytes():
    assert type(utf8_encode("abc")) is bytes, "return bytes, not a list or a bytearray"


@pytest.mark.parametrize(
    ("code_point", "length"),
    [
        (0x00, 1),
        (0x7F, 1),
        (0x80, 2),
        (0x7FF, 2),
        (0x800, 3),
        (0xD7FF, 3),
        (0xE000, 3),
        (0xFFFF, 3),
        (0x10000, 4),
        (0x10FFFF, 4),
    ],
)
def test_utf8_encode_each_length_at_its_edges(code_point, length):
    character = chr(code_point)
    got = utf8_encode(character)
    assert len(got) == length, f"U+{code_point:04X} takes {length} bytes"
    assert got == character.encode("utf-8")


def test_utf8_encode_four_bytes_for_an_emoji():
    assert utf8_encode("🙂") == b"\xf0\x9f\x99\x82"


def test_utf8_encode_a_sentence_in_three_scripts():
    sentence = "Grüße, 你好, नमस्ते 🙂"
    assert utf8_encode(sentence) == sentence.encode("utf-8")


@pytest.mark.parametrize("code_point", [0xD800, 0xDBFF, 0xDC00, 0xDFFF])
def test_utf8_encode_rejects_a_surrogate(code_point):
    with pytest.raises(ValueError):
        utf8_encode("a" + chr(code_point) + "b")


@given(st.text())
def test_utf8_encode_matches_python_on_any_text(text):
    assert utf8_encode(text) == text.encode("utf-8")


def test_utf8_encode_is_done_by_hand():
    # First the function must work; a stub that does nothing proves nothing.
    assert utf8_encode("é€") == b"\xc3\xa9\xe2\x82\xac"
    tree = ast.parse(inspect.getsource(utf8))
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            assert node.attr not in {"encode", "decode"}, "work the bytes out yourself"
        if isinstance(node, ast.Import):
            assert all(alias.name != "codecs" for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            assert node.module != "codecs"
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) in {"bytes", "bytearray"}:
            assert len(node.args) < 2 and not node.keywords, (
                "bytes(text, 'utf-8') is str.encode under another name"
            )
