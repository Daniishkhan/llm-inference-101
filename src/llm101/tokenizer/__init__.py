"""Module 2, tokenizer: text to token ids and back, by byte-pair encoding, as GPT-2 does it.

The contract (see modules/02-tokenizer/README.md). Names, signatures, docstrings, the Pair alias,
GPT-2's split pattern and the paths of GPT-2's files are given; the bodies are yours.

    utf8.py      utf8_encode
    train.py     count_pairs, merge_pair, train_bpe; Pair
    bpe.py       pretokenize, apply_merges, Tokenizer; GPT2_PATTERN
    gpt2.py      bytes_to_unicode, load_gpt2; VOCAB_PATH, MERGES_PATH
    fast.py      apply_merges_fast
    __main__.py  main: `uv run python -m llm101.tokenizer "some text"`
"""

from llm101.tokenizer.bpe import GPT2_PATTERN, Tokenizer, apply_merges, pretokenize
from llm101.tokenizer.fast import apply_merges_fast
from llm101.tokenizer.gpt2 import MERGES_PATH, VOCAB_PATH, bytes_to_unicode, load_gpt2
from llm101.tokenizer.train import Pair, count_pairs, merge_pair, train_bpe
from llm101.tokenizer.utf8 import utf8_encode

__all__ = [
    "GPT2_PATTERN",
    "MERGES_PATH",
    "VOCAB_PATH",
    "Pair",
    "Tokenizer",
    "apply_merges",
    "apply_merges_fast",
    "bytes_to_unicode",
    "count_pairs",
    "load_gpt2",
    "merge_pair",
    "pretokenize",
    "train_bpe",
    "utf8_encode",
]
