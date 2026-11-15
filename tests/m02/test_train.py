"""M2 (count_pairs, merge_pair) and M3 (train_bpe).

One milestone at a time:
    uv run pytest tests/m02 -k "count_pairs or merge_pair"
    uv run pytest tests/m02 -k train_bpe
"""

import argparse
import inspect
import signal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.tokenizer.train import count_pairs, merge_pair, train_bpe

# Written for these tests: 560 characters of English in which a few words repeat a lot.
TRAINING_TEXT = (
    "A tokenizer turns text into numbers. It reads the bytes of the text, counts the pairs "
    "that sit next to each other, and merges the most frequent pair into a new token. Then it "
    "counts again, and merges again. After a few hundred rounds the common words are single "
    "tokens, the rare words are a few tokens each, and every text, in any language, can still be "
    "written down, because the 256 single bytes never leave the vocabulary. The tokens the model "
    "sees are the tokens the tokenizer learned, and the tokens it learned are the tokens of the "
    "text it was trained on."
)

small_ids = st.lists(st.integers(0, 4), max_size=40)

# ------------------------------------------------------------------ M2: count_pairs, merge_pair


def test_count_pairs_the_docstring_examples():
    assert count_pairs([1, 2, 3, 1, 2]) == {(1, 2): 2, (2, 3): 1, (3, 1): 1}
    assert count_pairs([7, 7, 7]) == {(7, 7): 2}
    assert count_pairs([5]) == {}
    assert count_pairs([]) == {}


def test_count_pairs_works_on_a_tuple():
    assert count_pairs((4, 5, 4, 5)) == {(4, 5): 2, (5, 4): 1}


def test_count_pairs_does_not_change_its_input():
    ids = [3, 1, 3, 1]
    count_pairs(ids)
    assert ids == [3, 1, 3, 1]


@given(small_ids)
def test_count_pairs_counts_every_position_once(ids):
    assert sum(count_pairs(ids).values()) == max(len(ids) - 1, 0)


@given(small_ids, small_ids)
def test_count_pairs_of_two_lists_joined(left, right):
    # Joining two lists adds exactly one pair: the last of the left with the first of the right.
    expected = dict(count_pairs(left))
    for pair, count in count_pairs(right).items():
        expected[pair] = expected.get(pair, 0) + count
    if left and right:
        seam = (left[-1], right[0])
        expected[seam] = expected.get(seam, 0) + 1
    assert count_pairs(left + right) == expected


def test_merge_pair_the_docstring_examples():
    assert merge_pair([1, 2, 3, 1, 2], (1, 2), 9) == [9, 3, 9]
    assert merge_pair([7, 7, 7], (7, 7), 9) == [9, 7]
    assert merge_pair([7, 7, 7, 7], (7, 7), 9) == [9, 9]
    assert merge_pair([1, 2], (2, 1), 9) == [1, 2]


def test_merge_pair_returns_a_new_list():
    ids = [1, 2, 3]
    merged = merge_pair(ids, (8, 8), 9)
    assert merged == [1, 2, 3]
    assert merged is not ids, "return a new list, even when nothing changes"
    assert type(merge_pair((1, 2), (1, 2), 9)) is list


def test_merge_pair_does_not_change_its_input():
    ids = [1, 2, 1, 2]
    merge_pair(ids, (1, 2), 9)
    assert ids == [1, 2, 1, 2]


def test_merge_pair_an_empty_list_and_a_single_id():
    assert merge_pair([], (1, 2), 9) == []
    assert merge_pair([1], (1, 2), 9) == [1]


@given(small_ids, st.integers(0, 4), st.integers(0, 4))
def test_merge_pair_can_be_undone(ids, left, right):
    # 99 is not among the ids, so every 99 in the answer is one merge: put the pair back.
    merged = merge_pair(ids, (left, right), 99)
    undone = []
    for token in merged:
        undone.extend([left, right] if token == 99 else [token])
    assert undone == ids


@given(small_ids, st.integers(0, 4), st.integers(0, 4))
def test_merge_pair_leaves_no_occurrence_behind(ids, left, right):
    merged = merge_pair(ids, (left, right), 99)
    assert (left, right) not in count_pairs(merged)


# --------------------------------------------------------------------------- M3: train_bpe


def test_train_bpe_the_docstring_examples():
    assert train_bpe(["abab", "ab"], 258) == [(97, 98), (256, 256)]
    assert train_bpe(["ba", "ab"], 257) == [(97, 98)]
    assert train_bpe(["hello"], 256) == []


def test_train_bpe_rejects_a_vocabulary_below_256():
    with pytest.raises(ValueError):
        train_bpe(["hello"], 255)


def test_train_bpe_stops_when_nothing_is_left_to_merge():
    assert train_bpe(["ab"], 1000) == [(97, 98)]
    assert train_bpe(["a", "b", ""], 300) == []


def test_train_bpe_a_chunk_that_repeats_counts_each_time():
    # (99, 100) occurs twice, (97, 98) once. Counting each distinct chunk only once, with no weight,
    # would make them equal, and the tie would go to (97, 98).
    assert train_bpe(["ab", "cd", "cd"], 257) == [(99, 100)]


def test_train_bpe_merges_never_cross_from_one_chunk_to_the_next():
    # Joined, "ab" + "ab" would hold (98, 97); as two chunks, it never occurs.
    assert train_bpe(["ab", "ab"], 300) == [(97, 98)]


def test_train_bpe_works_on_utf8_bytes():
    # é is the two bytes 195 169; "éé" is 195 169 195 169.
    assert train_bpe(["éé"], 258) == [(195, 169), (256, 256)]


def test_train_bpe_accepts_any_iterable_of_chunks():
    assert train_bpe(iter(["abab", "ab"]), 258) == [(97, 98), (256, 256)]


def test_train_bpe_on_a_paragraph_learns_these_merges():
    expected = [
        (104, 101),  # "he"
        (116, 256),  # "t" + "he"
        (116, 111),  # "to"
        (101, 110),  # "en"
        (107, 259),  # "k" + "en"
        (258, 260),  # "to" + "ken"
        (97, 114),  # "ar"
        (101, 114),  # "er"
        (105, 110),  # "in"
        (97, 110),  # "an"
        (116, 101),  # "te"
        (261, 115),  # "token" + "s"
        (105, 116),  # "it"
        (108, 101),  # "le"
        (110, 101),  # "ne"
    ]
    assert train_bpe(TRAINING_TEXT.split(), 256 + 15) == expected


@given(st.lists(st.text(alphabet="abcé ", max_size=12), max_size=8), st.integers(256, 300))
def test_train_bpe_each_merge_uses_tokens_that_already_exist(chunks, vocab_size):
    merges = train_bpe(chunks, vocab_size)
    assert len(merges) <= vocab_size - 256
    assert len(set(merges)) == len(merges), "a pair is merged once"
    for rank, (left, right) in enumerate(merges):
        assert left < 256 + rank and right < 256 + rank


class StillRunning(Exception):
    pass


def stop_the_run(signum, frame):
    raise StillRunning


def test_train_bpe_three_hundred_merges_on_a_million_characters_in_ten_seconds():
    # argparse's source, ten times over: about 92,000 words, but only about 2,600 distinct ones.
    # Counting each distinct word once takes about a second; counting every word, about 35.
    words = (inspect.getsource(argparse) * 10).split()
    before = signal.signal(signal.SIGALRM, stop_the_run)
    signal.setitimer(signal.ITIMER_REAL, 10.0)
    try:
        merges = train_bpe(words, 256 + 300)
    except StillRunning:
        pytest.fail(
            "still training after 10 s: count each distinct chunk once, and weigh its pairs by how "
            "often the chunk appears (see the docstring)"
        )
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, before)
    assert len(merges) == 300
