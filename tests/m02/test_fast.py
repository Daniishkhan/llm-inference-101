"""M6: apply_merges_fast, and Tokenizer.encode on a long chunk.

Run: uv run pytest tests/m02/test_fast.py
"""

import ast
import inspect
import random
import signal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.tokenizer import fast
from llm101.tokenizer.bpe import apply_merges
from llm101.tokenizer.fast import apply_merges_fast
from llm101.tokenizer.gpt2 import load_gpt2

# A merge table built for speed tests: every pair of twenty letters (400 merges), then 3,000 pairs
# of those pairs. A long chunk of these letters needs thousands of rounds of merging.
LETTERS = b"etaoinshrdlucmfwypgb"
LONG_MERGES = [(a, b) for a in LETTERS for b in LETTERS]
LONG_MERGES += [
    (256 + i, 256 + j) for i in range(400) for j in range(400) if (i * 7 + j * 3) % 23 == 0
][:3000]
LONG_RANKS = {pair: rank for rank, pair in enumerate(LONG_MERGES)}


class StillRunning(Exception):
    pass


def stop_the_run(signum, frame):
    raise StillRunning


def within(seconds, work, message):
    before = signal.signal(signal.SIGALRM, stop_the_run)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        return work()
    except StillRunning:
        pytest.fail(message)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, before)


def test_apply_merges_fast_the_examples_of_apply_merges():
    ranks = {(98, 99): 0, (97, 98): 1}
    assert apply_merges_fast([97, 98, 99], ranks) == [97, 256]
    assert apply_merges_fast([97, 98], ranks) == [257]
    assert apply_merges_fast([99, 97], ranks) == [99, 97]
    assert apply_merges_fast([97, 98, 99], {(97, 98): 0, (256, 99): 1}) == [257]


def test_apply_merges_fast_overlapping_occurrences_go_left_first():
    assert apply_merges_fast([97, 97, 97], {(97, 97): 0}) == [256, 97]
    assert apply_merges_fast([97, 97, 97, 97], {(97, 97): 0}) == [256, 256]
    assert apply_merges_fast([97, 97, 97, 97], {(97, 97): 0, (256, 256): 1}) == [257]


def test_apply_merges_fast_empty_and_single():
    assert apply_merges_fast([], LONG_RANKS) == []
    assert apply_merges_fast([101], LONG_RANKS) == [101]


def test_apply_merges_fast_does_not_change_its_input():
    ids = list(b"eetaoe")
    apply_merges_fast(ids, LONG_RANKS)
    assert ids == list(b"eetaoe")


@st.composite
def merge_tables(draw):
    """Random merges over the ids 0, 1 and 2: merge r may use any id below 256 + r that exists."""
    existing = [0, 1, 2]
    ranks = {}
    for _ in range(draw(st.integers(0, 12))):
        pair = (draw(st.sampled_from(existing)), draw(st.sampled_from(existing)))
        if pair not in ranks:
            ranks[pair] = len(ranks)
            existing.append(256 + ranks[pair])
    return ranks


@given(ranks=merge_tables(), ids=st.lists(st.integers(0, 2), max_size=60))
def test_apply_merges_fast_agrees_with_apply_merges(ranks, ids):
    assert apply_merges_fast(ids, ranks) == apply_merges(ids, ranks)


@given(ids=st.lists(st.sampled_from(list(LETTERS)), max_size=200))
def test_apply_merges_fast_agrees_with_apply_merges_on_the_long_table(ids):
    assert apply_merges_fast(ids, LONG_RANKS) == apply_merges(ids, LONG_RANKS)


def test_apply_merges_fast_one_hundred_thousand_letters_in_two_seconds():
    rng = random.Random(0)
    ids = list(bytes(rng.choice(LETTERS) for _ in range(100_000)))
    merged = within(
        2.0,
        lambda: apply_merges_fast(ids, LONG_RANKS),
        "still merging after 2 s: does each merge look at every pair again? (book chapter 5)",
    )
    # The answer of a reference run: its length, its sum and its first eight ids.
    assert (len(merged), sum(merged), merged[:8]) == (
        55_915,
        19_520_616,
        [509, 284, 121, 568, 451, 494, 3025, 105],
    )


def test_apply_merges_fast_does_not_hand_the_work_to_apply_merges():
    # First it must work; a stub that does nothing proves nothing.
    assert apply_merges_fast([97, 98, 99], {(98, 99): 0, (97, 98): 1}) == [97, 256]
    tree = ast.parse(inspect.getsource(fast))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            assert name != "apply_merges", "fast.py finds the answer itself"


def test_gpt2_encodes_a_long_word_in_two_seconds(oracle):
    # 50,000 letters with no space: one chunk. Tokenizer.encode must use apply_merges_fast now.
    tokenizer = load_gpt2()
    rng = random.Random(1)
    word = "".join(rng.choice("etaoinshrdlu") for _ in range(50_000))
    ids = within(
        2.0,
        lambda: tokenizer.encode(word),
        "GPT-2 still encoding one long word after 2 s: does Tokenizer.encode use "
        "apply_merges_fast yet?",
    )
    assert ids == oracle.encode_ordinary(word)
