"""Training byte-pair encoding: count the pairs, merge the most frequent, repeat.

Milestones M2 (count_pairs, merge_pair) and M3 (train_bpe).
"""

from collections.abc import Iterable, Sequence

Pair = tuple[int, int]
"""Two token ids that sit next to each other, left first."""


def count_pairs(ids: Sequence[int]) -> dict[Pair, int]:
    """How many times each pair of neighbouring ids occurs in ids, reading from left to right.

    Every position counts, so pairs may overlap:

        count_pairs([1, 2, 3, 1, 2])  ->  {(1, 2): 2, (2, 3): 1, (3, 1): 1}
        count_pairs([7, 7, 7])        ->  {(7, 7): 2}      positions 0 and 1, and 1 and 2
        count_pairs([5])              ->  {}
        count_pairs([])               ->  {}

    The order of the keys is not part of the answer. The sequence you were given is not changed.
    """
    raise NotImplementedError("TODO(you)")


def merge_pair(ids: Sequence[int], pair: Pair, new_id: int) -> list[int]:
    """A new list in which every occurrence of pair is replaced by new_id, scanning from left to
    right.

    When two occurrences overlap, the left one wins and the scan goes on after it:

        merge_pair([1, 2, 3, 1, 2], (1, 2), 9)   ->  [9, 3, 9]
        merge_pair([7, 7, 7], (7, 7), 9)          ->  [9, 7]
        merge_pair([7, 7, 7, 7], (7, 7), 9)       ->  [9, 9]
        merge_pair([1, 2], (2, 1), 9)             ->  [1, 2]      not there: an equal copy

    The sequence you were given is not changed.
    """
    raise NotImplementedError("TODO(you)")


def train_bpe(chunks: Iterable[str], vocab_size: int) -> list[Pair]:
    """Learn byte-pair merges from chunks of text, until the vocabulary has vocab_size tokens.

    The vocabulary starts with the 256 single bytes: byte b is the token with id b. Each chunk
    becomes the list of its UTF-8 bytes. Then, one round per merge:

    1. Count every pair of neighbouring ids in every chunk, as count_pairs does. A chunk that
       appears five times among the chunks counts five times.
    2. Choose the most frequent pair. When several pairs are equally frequent, choose the smallest
       of them, compared as tuples: (32, 116) before (101, 114), and (97, 98) before (97, 99).
    3. Give it the next free id: 256 for the first merge, 257 for the second, and so on. Replace the
       pair with that id in every chunk, as merge_pair does.

    Merges never join the end of one chunk to the start of the next. Training stops early, with
    fewer merges, when no chunk has two tokens left. Returns the merges in the order they were
    learned: merges[r] is the pair that became token 256 + r.

        train_bpe(["abab", "ab"], 258)  ->  [(97, 98), (256, 256)]
            "ab" occurs three times, so (97, 98) becomes 256; then "abab" is [256, 256], and the
            only pair left, (256, 256), becomes 257.
        train_bpe(["ba", "ab"], 257)    ->  [(97, 98)]       a tie: (97, 98) is the smaller pair
        train_bpe(["hello"], 256)       ->  []               no room for a merge

    Chunks repeat a lot in real text ("the" may be a twentieth of all words), and the tests train
    300 merges on a million characters in ten seconds. Count each distinct chunk once and weigh it
    by how often it appears.

    Raises ValueError if vocab_size is below 256.
    """
    raise NotImplementedError("TODO(you)")
