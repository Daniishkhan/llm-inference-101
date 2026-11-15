import random
import signal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from group_anagrams import group_anagrams


def test_an_empty_list():
    assert group_anagrams([]) == []


def test_a_single_word():
    assert group_anagrams(["tea"]) == [["tea"]]


def test_the_example():
    words = ["stop", "cat", "pots", "act", "tops", "dog"]
    assert group_anagrams(words) == [["stop", "pots", "tops"], ["cat", "act"], ["dog"]]


def test_empty_strings_are_anagrams_of_each_other():
    assert group_anagrams(["", "a", ""]) == [["", ""], ["a"]]


def test_a_repeated_word_appears_twice_in_its_group():
    assert group_anagrams(["ab", "ba", "ab"]) == [["ab", "ba", "ab"]]


def test_no_two_words_are_anagrams():
    assert group_anagrams(["ab", "bc", "cd"]) == [["ab"], ["bc"], ["cd"]]


def test_the_same_letters_in_different_amounts_are_not_anagrams():
    # "aab" has two a's and "abb" has one: they use the same letters, but they are not anagrams.
    assert group_anagrams(["aab", "abb", "bba", "baa"]) == [["aab", "baa"], ["abb", "bba"]]


def test_groups_come_in_the_order_of_their_first_word():
    assert group_anagrams(["b", "a", "b", "a"]) == [["b", "b"], ["a", "a"]]


def test_the_list_you_were_given_is_not_changed():
    words = ["ba", "ab", "c"]
    group_anagrams(words)
    assert words == ["ba", "ab", "c"]


words = st.text(alphabet="abcdef", max_size=6)


@given(
    base=words, others=st.lists(words, max_size=20), copies=st.integers(1, 4), seed=st.integers()
)
def test_shuffled_copies_of_a_word_always_land_in_one_group(base, others, copies, seed):
    rng = random.Random(seed)
    shuffled = []
    for _ in range(copies):
        letters = list(base)
        rng.shuffle(letters)
        shuffled.append("".join(letters))
    mixed = others + shuffled
    rng.shuffle(mixed)

    groups = group_anagrams(mixed)

    # Every word comes back exactly as often as it went in.
    assert sorted(w for g in groups for w in g) == sorted(mixed)
    # All the shuffled copies of `base` sit in one and the same group.
    homes = {i for i, g in enumerate(groups) for w in g if w in shuffled}
    assert len(homes) == 1


class StillRunning(Exception):
    pass


def stop_the_run(signum, frame):
    raise StillRunning


def test_twenty_thousand_words_in_two_seconds():
    # 10,000 words, no two of them anagrams (word i has as many a's as the first digit of i, as many
    # b's as the second, and so on), then a shuffled copy of each: 10,000 groups of two.
    rng = random.Random(1)
    words = [
        "".join(letter * int(digit) for letter, digit in zip("abcde", f"{i:05d}", strict=True))
        for i in range(1, 10_001)
    ]
    copies = ["".join(rng.sample(word, len(word))) for word in words]
    before = signal.signal(signal.SIGALRM, stop_the_run)
    signal.setitimer(signal.ITIMER_REAL, 2.0)
    try:
        result = group_anagrams(words + copies)
    except StillRunning:
        pytest.fail("still running after 2 s: comparing every word with every other is too slow")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, before)
    assert result == [[word, copy] for word, copy in zip(words, copies, strict=True)]
