"""Module 2's shared fixture: the oracle, tiktoken's GPT-2 encoding.

The oracle is built from the same two files your load_gpt2 reads, data/gpt2/vocab.json and
data/gpt2/merges.txt, so the tests never need the network. The checksums are those of
tools/fetch-gpt2-tokenizer.py: a file that has changed fails here, before any test compares ids.
"""

import pytest
import tiktoken
from tiktoken.load import data_gym_to_mergeable_bpe_ranks
from tiktoken_ext.openai_public import r50k_pat_str

from llm101.tokenizer.gpt2 import MERGES_PATH, VOCAB_PATH

MERGES_SHA256 = "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
VOCAB_SHA256 = "196139668be63f3b5d6574427317ae82f612a97c5d1cdaf36ed2256dbf636783"


@pytest.fixture(scope="session")
def oracle() -> tiktoken.Encoding:
    """GPT-2's tokenizer as tiktoken does it. Compare with encode_ordinary, which treats the text
    "<|endoftext|>" as ordinary text, as your Tokenizer.encode does."""
    ranks = data_gym_to_mergeable_bpe_ranks(
        vocab_bpe_file=str(MERGES_PATH),
        encoder_json_file=str(VOCAB_PATH),
        vocab_bpe_hash=MERGES_SHA256,
        encoder_json_hash=VOCAB_SHA256,
    )
    return tiktoken.Encoding(
        name="gpt2-from-data",
        pat_str=r50k_pat_str,
        mergeable_ranks=ranks,
        special_tokens={"<|endoftext|>": 50256},
    )
