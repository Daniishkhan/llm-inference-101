"""Merging in n log n: a heap of candidate pairs over a linked list of tokens.

Milestone M6. The tests compare your answers with apply_merges (bpe.py), and they read this file: it
may not call apply_merges. Once it is green, make Tokenizer.encode use it.
"""

from collections.abc import Mapping, Sequence

from llm101.tokenizer.train import Pair


def apply_merges_fast(ids: Sequence[int], ranks: Mapping[Pair, int]) -> list[int]:
    """The same answer as apply_merges(ids, ranks), in time proportional to n log n for n ids.

    apply_merges looks at every pair in every round, and a long chunk can need thousands of rounds:
    20,000 letters with no space between them take one to two seconds. Keep instead:

    - the tokens as a linked list, so that merging two neighbours changes a few links and moves
      nothing else;
    - a heap of the neighbouring pairs that have a rank, so that the pair to merge next is always at
      the top.

    A merge changes the pairs on both sides of it, and the heap still holds entries for pairs that
    are gone. Recognise such an entry when it reaches the top, and skip it.

    Where the same pair occurs more than once, the leftmost goes first, as merge_pair does.

    The tests give it 100,000 letters of one chunk and two seconds, and compare its answers with
    apply_merges on random merges and random ids. The sequence you were given is not changed.
    """
    raise NotImplementedError("TODO(you)")
