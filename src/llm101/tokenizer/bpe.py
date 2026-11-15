"""Encoding and decoding with byte-pair merges: the tokenizer itself.

Milestone M4: pretokenize, apply_merges and Tokenizer. Milestone M6 makes Tokenizer.encode use
apply_merges_fast (fast.py) instead of apply_merges; the answers stay the same.

The rule for every tokenizer in this module: ids 0 to 255 are the single bytes, in some order, and
merge number r makes the token whose id is 256 + r.
"""

from collections.abc import Iterable, Mapping, Sequence

from llm101.tokenizer.train import Pair

GPT2_PATTERN = r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
"""GPT-2's split pattern, from OpenAI's encoder.py (2019). It needs the `regex` package: Python's
own `re` does not know \\p{L} (any letter, in any script) or \\p{N} (any digit or numeral). Book
chapter 3 takes it apart, alternative by alternative."""


def pretokenize(text: str) -> list[str]:
    """Split text into chunks with GPT2_PATTERN: every match, in order. The chunks join back into
    the text.

        pretokenize("Hello world")   ->  ["Hello", " world"]
        pretokenize("I'm 42!")       ->  ["I", "'m", " 42", "!"]
        pretokenize("a   b")         ->  ["a", "  ", " b"]     the last space goes with the word
        pretokenize("")              ->  []

    A word keeps the one space in front of it, so " world" is one chunk. Merges never cross from one
    chunk into the next, so no token ever holds the end of one word and the start of another.
    """
    raise NotImplementedError("TODO(you)")


def apply_merges(ids: Sequence[int], ranks: Mapping[Pair, int]) -> list[int]:
    """Replay byte-pair merges on the ids of one chunk, the earliest learned first. A new list.

    ranks maps a pair to its rank r: the pair was the r-th merge learned, and it becomes 256 + r.
    Repeat: among the neighbouring pairs in the list, find the one with the lowest rank, and replace
    every occurrence of it with 256 + its rank, as merge_pair does. Stop when no neighbouring pair
    has a rank.

    The order is the rank, not the position:

        ranks = {(98, 99): 0, (97, 98): 1}
        apply_merges([97, 98, 99], ranks)   ->  [97, 256]     (98, 99) was learned first
        apply_merges([97, 98], ranks)       ->  [257]
        apply_merges([99, 97], ranks)       ->  [99, 97]      no pair has a rank

    This is the slow way: every round looks at every pair. Milestone M6 (fast.py) finds the same
    answer with a heap. The sequence you were given is not changed.
    """
    raise NotImplementedError("TODO(you)")


class Tokenizer:
    """A byte-level BPE tokenizer: text to ids with encode, ids to text with decode.

    byte_ids[b] is the id of the single-byte token for byte b, so byte_ids holds the numbers 0 to
    255 in some order. For a tokenizer you train, it is range(256): byte b is id b. merges[r] is the
    pair of ids that merge r joins into the token 256 + r. special_tokens maps the text of a token
    that no merge makes (GPT-2 has one, "<|endoftext|>") to its id, which comes after every merge's:
    256 + len(merges) or above (the tests do not give you any other).

        merges = train_bpe(pretokenize(text), 512)
        tokenizer = Tokenizer(range(256), merges)

    Raises ValueError if byte_ids is not the numbers 0 to 255 in some order, or if a merge uses an
    id that does not exist yet (merge r may only use ids below 256 + r).
    """

    def __init__(
        self,
        byte_ids: Sequence[int],
        merges: Sequence[Pair],
        special_tokens: Mapping[str, int] | None = None,
    ) -> None:
        raise NotImplementedError("TODO(you)")

    def encode(self, text: str) -> list[int]:
        """The ids of text: pretokenize it, turn each chunk into the ids of its UTF-8 bytes (through
        byte_ids), apply the merges to each chunk on its own, and join the results in order.

        encode never returns a special token's id. The text "<|endoftext|>" is encoded like any
        other text, as tiktoken's encode_ordinary does.
        """
        raise NotImplementedError("TODO(you)")

    def decode(self, ids: Iterable[int]) -> str:
        """The text of ids: join the bytes of every token, then decode them as UTF-8.

        Bytes that do not make a whole character (a list of ids may stop halfway through one)
        become the replacement character "�", U+FFFD, one for each broken piece, as
        bytes.decode("utf-8", errors="replace") does. So decode(encode(text)) == text for every
        text, and decode never raises on a list of valid ids.

        Raises ValueError for an id that is not in the vocabulary.
        """
        raise NotImplementedError("TODO(you)")

    def token_bytes(self, token_id: int) -> bytes:
        """The bytes that one token stands for. A special token stands for the UTF-8 bytes of its
        text.

        Raises ValueError for an id that is not in the vocabulary.
        """
        raise NotImplementedError("TODO(you)")
