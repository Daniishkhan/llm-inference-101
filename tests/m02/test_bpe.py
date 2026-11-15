"""M4: pretokenize, apply_merges and Tokenizer, and the first half of "Done when".

Run: uv run pytest tests/m02/test_bpe.py

These tests do not call your train_bpe: MERGES below was learned from a paragraph of English (40
merges), so that a fault in M3 cannot hide here or show up here.
"""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.tokenizer.bpe import Tokenizer, apply_merges, pretokenize

MERGES = [
    (32, 116), (104, 101), (32, 97), (256, 257), (101, 110), (256, 111), (107, 260), (261, 262),
    (101, 114), (105, 110), (114, 101), (110, 100), (263, 115), (32, 115), (101, 97), (101, 115),
    (101, 120), (105, 116), (272, 116), (32, 98), (32, 99), (32, 108), (32, 109), (32, 110),
    (32, 111), (32, 119), (256, 274), (258, 266), (258, 267), (32, 102), (32, 265), (32, 273),
    (97, 265), (100, 115), (101, 100), (101, 119), (111, 117), (114, 110), (277, 270), (32, 84),
]  # fmt: skip
RANKS = {pair: rank for rank, pair in enumerate(MERGES)}

# -------------------------------------------------------------------------------- pretokenize


def test_pretokenize_the_docstring_examples():
    assert pretokenize("Hello world") == ["Hello", " world"]
    assert pretokenize("I'm 42!") == ["I", "'m", " 42", "!"]
    assert pretokenize("a   b") == ["a", "  ", " b"]
    assert pretokenize("") == []


@pytest.mark.parametrize(
    ("text", "chunks"),
    [
        ("can't won't", ["can", "'t", " won", "'t"]),
        ("Grüße, 你好!", ["Grüße", ",", " 你好", "!"]),
        ("2,048 tokens", ["2", ",", "048", " tokens"]),
        ("x\ty", ["x", "\t", "y"]),
        ("end  ", ["end", "  "]),
        ("one\n\ntwo", ["one", "\n", "\n", "two"]),
        ("½ Ⅻ", ["½", " Ⅻ"]),
    ],
)
def test_pretokenize_splits_like_gpt2(text, chunks):
    assert pretokenize(text) == chunks


@given(st.text())
def test_pretokenize_the_chunks_join_back_into_the_text(text):
    assert "".join(pretokenize(text)) == text


@given(st.text())
def test_pretokenize_agrees_with_the_oracle(oracle, text):
    # If your chunks are GPT-2's, tiktoken encodes them one by one into the same ids as the whole.
    one_by_one = [i for chunk in pretokenize(text) for i in oracle.encode_ordinary(chunk)]
    assert one_by_one == oracle.encode_ordinary(text)


# ------------------------------------------------------------------------------- apply_merges


def test_apply_merges_the_docstring_examples():
    ranks = {(98, 99): 0, (97, 98): 1}
    assert apply_merges([97, 98, 99], ranks) == [97, 256]
    assert apply_merges([97, 98], ranks) == [257]
    assert apply_merges([99, 97], ranks) == [99, 97]


def test_apply_merges_a_merge_can_use_an_earlier_merge():
    assert apply_merges([97, 98, 99], {(97, 98): 0, (256, 99): 1}) == [257]


def test_apply_merges_every_occurrence_of_the_lowest_rank():
    assert apply_merges([97, 98, 97, 98], {(97, 98): 0}) == [256, 256]
    assert apply_merges([97, 97, 97], {(97, 97): 0}) == [256, 97], (
        "the left one wins, as merge_pair"
    )


def test_apply_merges_on_the_paragraph_merges():
    assert apply_merges(list(b" the tokens"), RANKS) == [259, 268]


def test_apply_merges_empty_and_single():
    assert apply_merges([], RANKS) == []
    assert apply_merges([116], RANKS) == [116]


def test_apply_merges_does_not_change_its_input():
    ids = list(b" the")
    apply_merges(ids, RANKS)
    assert ids == list(b" the")


@given(st.binary(max_size=30))
def test_apply_merges_leaves_no_pair_that_has_a_rank(data):
    merged = apply_merges(list(data), RANKS)
    pairs = set(zip(merged, merged[1:], strict=False))
    assert not pairs & RANKS.keys(), "stop only when no neighbouring pair has a rank"


# ---------------------------------------------------------------------------------- Tokenizer


def paragraph_tokenizer():
    return Tokenizer(range(256), MERGES)


@pytest.mark.parametrize(
    ("text", "ids"),
    [
        ("the tokens", [116, 257, 268]),
        ("The tokenizer", [84, 257, 263, 105, 122, 264]),
        ("tokens, tokens!", [116, 111, 262, 115, 44, 268, 33]),
        ("Grüße", [71, 114, 195, 188, 195, 159, 101]),
        ("", []),
    ],
)
def test_tokenizer_encode(text, ids):
    tokenizer = paragraph_tokenizer()
    assert tokenizer.encode(text) == ids


def test_tokenizer_decode():
    tokenizer = paragraph_tokenizer()
    assert tokenizer.decode([116, 257, 268]) == "the tokens"
    assert tokenizer.decode([]) == ""


def test_tokenizer_decode_takes_any_iterable():
    tokenizer = paragraph_tokenizer()
    assert tokenizer.decode(iter([116, 257, 268])) == "the tokens"


def test_tokenizer_token_bytes():
    tokenizer = paragraph_tokenizer()
    assert tokenizer.token_bytes(116) == b"t"
    assert tokenizer.token_bytes(256) == b" t"
    assert tokenizer.token_bytes(259) == b" the"
    assert tokenizer.token_bytes(268) == b" tokens"


def test_tokenizer_merges_never_cross_chunks():
    # (100, 32) is "d" followed by a space, but GPT-2's split keeps the space with the next word.
    tokenizer = Tokenizer(range(256), [(100, 32)])
    assert tokenizer.encode("d d") == [100, 32, 100]


def test_tokenizer_encode_goes_through_byte_ids():
    backwards = Tokenizer(range(255, -1, -1), [])
    assert backwards.encode("A") == [255 - 65]
    assert backwards.token_bytes(255 - 65) == b"A"
    assert backwards.decode([255 - 65, 255 - 66]) == "AB"


def test_tokenizer_decode_replaces_a_broken_character():
    bytes_only = Tokenizer(range(256), [])
    euro = list("€".encode())  # 226 130 172
    assert bytes_only.decode(euro[:2]) == "\ufffd"
    assert bytes_only.decode(euro[:2] + list(b"ok")) == b"\xe2\x82ok".decode(errors="replace")
    assert bytes_only.decode([255]) == "\ufffd"


def test_tokenizer_special_tokens():
    tokenizer = Tokenizer(range(256), [(104, 105)], {"<|end|>": 257})
    assert tokenizer.decode([256, 257]) == "hi<|end|>"
    assert tokenizer.token_bytes(257) == b"<|end|>"
    assert 257 not in tokenizer.encode("hi<|end|>"), "encode never makes a special token"


def test_tokenizer_rejects_an_unknown_id():
    tokenizer = paragraph_tokenizer()
    with pytest.raises(ValueError):
        tokenizer.decode([116, 256 + len(MERGES)])
    with pytest.raises(ValueError):
        tokenizer.token_bytes(-1)


@pytest.mark.parametrize(
    "byte_ids",
    [range(255), [0] * 256, list(range(1, 257))],
    ids=["too few", "repeats", "out of range"],
)
def test_tokenizer_rejects_bad_byte_ids(byte_ids):
    with pytest.raises(ValueError):
        Tokenizer(byte_ids, [])


def test_tokenizer_rejects_a_merge_of_tokens_that_do_not_exist_yet():
    with pytest.raises(ValueError):
        Tokenizer(range(256), [(97, 256)])  # merge 0 makes 256; it cannot use 256


@given(st.text())
def test_done_when_round_trips_are_exact_on_arbitrary_unicode(text):
    tokenizer = Tokenizer(range(256), MERGES)
    assert tokenizer.decode(tokenizer.encode(text)) == text


@given(st.text(alphabet=st.characters(codec="utf-8"), max_size=50))
def test_round_trips_with_bytes_in_another_order(text):
    tokenizer = Tokenizer(range(255, -1, -1), [(255 - 116, 255 - 104)])
    assert tokenizer.decode(tokenizer.encode(text)) == text
