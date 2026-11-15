"""M5: bytes_to_unicode, load_gpt2 and the program, and the second half of "Done when".

Run: uv run pytest tests/m02/test_gpt2.py

The oracle is tiktoken's GPT-2 encoding, built from the same files (conftest.py).
"""

import ast
import functools
import inspect
import os
import subprocess
import sys

import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.tokenizer import gpt2
from llm101.tokenizer.gpt2 import bytes_to_unicode, load_gpt2

# The test set: texts that each catch a different mistake.
TEST_SET = [
    "Hello world",
    "Hello, wörld!",
    "The quick brown fox jumps over the lazy dog.",
    "I'm sure they'll say we've done it, and you'd agree it's fine.",
    "IT'S LOUD and it's quiet",  # GPT-2's contractions are lower case only
    "GPT-2 has 50,257 tokens and 1,024 positions; 3.14159 is not one of them.",
    "    four spaces, then a tab\tand two newlines\n\nand trailing spaces   ",
    "def area(r: float) -> float:\n    return 3.14159 * r ** 2\n",
    '{"model": "gpt2", "max_tokens": 64, "stop": ["\\n\\n"]}',
    "https://example.com/path/to/a/page?query=tokens&limit=10#section-2",
    "Grüße aus München! Ça va? ¿Qué tal? Ελληνικά, русский язык.",
    "आज मौसम अच्छा है, इसलिए हम नदी तक पैदल जा रहे हैं।",
    "今天天气很好，所以我们要走路去河边。日本語のテキストも。",
    "مرحبا بالعالم — שלום עולם",
    "Emoji: 🙂👍🏽 and a family 👨‍👩‍👧 with joiners, and a flag 🇳🇴.",
    "e\u0301 is e with a combining accent; \u00e9 is one code point.",
    "Maths: ∀x ∈ ℝ, x² ≥ 0; ½ + ¼ = ¾; Ⅻ o'clock.",
    "!!!???... --- ***  ~~~",
    "<|endoftext|> is ordinary text when you encode it.",
    "\u00a0non-breaking\u00a0spaces\u2003and an em space",
    "",
]


@functools.cache
def gpt2_tokenizer():
    """load_gpt2(), once. Called inside each test, so that a stub that raises shows as a failure."""
    return load_gpt2()


# -------------------------------------------------------------------------- bytes_to_unicode


def test_bytes_to_unicode_the_docstring_examples():
    table = bytes_to_unicode()
    assert table[ord("A")] == "A"
    assert table[0] == "Ā"
    assert table[32] == "Ġ"
    assert table[10] == "Ċ"


def test_bytes_to_unicode_maps_every_byte_to_a_different_character():
    table = bytes_to_unicode()
    assert sorted(table) == list(range(256))
    assert len(set(table.values())) == 256
    assert all(len(character) == 1 for character in table.values())


def test_bytes_to_unicode_every_character_is_printable_and_not_a_space():
    for byte, character in bytes_to_unicode().items():
        assert character.isprintable() and not character.isspace(), f"byte {byte}"


def test_bytes_to_unicode_printable_bytes_keep_their_character():
    table = bytes_to_unicode()
    kept = [*range(33, 127), *range(161, 173), *range(174, 256)]
    assert len(kept) == 188
    for byte in kept:
        assert table[byte] == chr(byte)


def test_bytes_to_unicode_the_others_count_up_from_256():
    table = bytes_to_unicode()
    others = [*range(0, 33), *range(127, 161), 173]
    assert [table[byte] for byte in others] == [chr(256 + i) for i in range(68)]


# --------------------------------------------------------------------------------- load_gpt2


def test_load_gpt2_the_docstring_example():
    tokenizer = gpt2_tokenizer()
    assert tokenizer.encode("Hello world") == [15496, 995]
    assert tokenizer.decode([15496, 995]) == "Hello world"


def test_load_gpt2_byte_ids():
    tokenizer = gpt2_tokenizer()
    assert tokenizer.token_bytes(0) == b"!"
    assert tokenizer.token_bytes(32) == b"A"
    assert tokenizer.token_bytes(220) == b" ", "the space byte is token 220"
    assert tokenizer.token_bytes(198) == b"\n"


def test_load_gpt2_merges():
    tokenizer = gpt2_tokenizer()
    assert tokenizer.token_bytes(256) == b" t", "merges.txt's first merge, Ġ t"
    assert tokenizer.token_bytes(995) == b" world"


def test_load_gpt2_every_token_holds_the_bytes_tiktoken_gives_it(oracle):
    tokenizer = gpt2_tokenizer()
    for token_id in [*range(0, 50256, 97), 50255]:
        assert tokenizer.token_bytes(token_id) == oracle.decode_single_token_bytes(token_id)


def test_load_gpt2_end_of_text():
    tokenizer = gpt2_tokenizer()
    assert tokenizer.decode([50256]) == "<|endoftext|>"
    assert tokenizer.token_bytes(50256) == b"<|endoftext|>"
    assert 50256 not in tokenizer.encode("<|endoftext|>")


def test_load_gpt2_has_no_token_past_50256():
    tokenizer = gpt2_tokenizer()
    with pytest.raises(ValueError):
        tokenizer.token_bytes(50257)


def test_load_gpt2_takes_its_paths_as_arguments(tmp_path):
    # GPT-2's vocab.json, and its merges.txt cut down to the first 100 merges: with so few,
    # " world" can no longer become one token. A load_gpt2 that ignores its paths says [995].
    vocab = tmp_path / "v.json"
    merges = tmp_path / "m.txt"
    vocab.write_bytes(gpt2.VOCAB_PATH.read_bytes())
    lines = gpt2.MERGES_PATH.read_text(encoding="utf-8").split("\n")
    merges.write_text("\n".join(lines[:101]) + "\n", encoding="utf-8")
    small = load_gpt2(vocab, merges)
    ids = small.encode(" world")
    assert len(ids) > 1, "100 merges cannot make ' world' one token: does load_gpt2 read its paths?"
    assert all(token_id < 256 + 100 for token_id in ids)
    assert small.decode(ids) == " world"


@pytest.mark.parametrize("text", TEST_SET, ids=[f"test-set-{i}" for i in range(len(TEST_SET))])
def test_done_when_ids_match_gpt2_on_the_test_set(oracle, text):
    tokenizer = gpt2_tokenizer()
    assert tokenizer.encode(text) == oracle.encode_ordinary(text)


def test_ids_match_gpt2_on_random_text(oracle):
    # Loaded here, before hypothesis starts its clock: loading 50,000 merges inside the first
    # example would count against hypothesis's deadline of 200 ms per example.
    tokenizer = gpt2_tokenizer()

    @given(st.text())
    def ids_match(text):
        assert tokenizer.encode(text) == oracle.encode_ordinary(text)

    ids_match()


def test_gpt2_round_trips_on_arbitrary_unicode():
    tokenizer = gpt2_tokenizer()  # before hypothesis starts its clock, as above

    @given(st.text())
    def round_trips(text):
        assert tokenizer.decode(tokenizer.encode(text)) == text

    round_trips()


@pytest.mark.parametrize("text", TEST_SET[:8])
def test_gpt2_decodes_what_tiktoken_encodes(oracle, text):
    tokenizer = gpt2_tokenizer()
    assert tokenizer.decode(oracle.encode_ordinary(text)) == text


def test_gpt2_does_not_import_tiktoken():
    tokenizer = gpt2_tokenizer()
    # First it must work; a stub that does nothing proves nothing.
    assert tokenizer.encode(" world") == [995]
    tree = ast.parse(inspect.getsource(gpt2))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".")[0] != "tiktoken" for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] not in {"tiktoken", "tiktoken_ext"}


# ------------------------------------------------------------------------------- the program


def run(*args, timeout=120):
    env = {k: v for k, v in os.environ.items() if k not in {"FORCE_COLOR", "TTY_COMPATIBLE"}}
    env |= {"NO_COLOR": "1", "COLUMNS": "200"}
    command = [sys.executable, "-m", "llm101.tokenizer", *args]
    return subprocess.run(command, capture_output=True, text=True, timeout=timeout, env=env)


def test_the_program_shows_the_tokens_the_ids_and_the_count():
    result = run("Hello world")
    assert result.returncode == 0, result.stderr
    assert "Hello world" in result.stdout
    assert "15496 995" in result.stdout
    assert "2 tokens, 11 characters, 11 bytes" in result.stdout


def test_the_program_counts_characters_and_bytes_apart(oracle):
    result = run("Grüße")
    assert result.returncode == 0, result.stderr
    count = len(oracle.encode_ordinary("Grüße"))
    assert f"{count} tokens, 5 characters, 7 bytes" in result.stdout


def test_the_program_reads_a_file(tmp_path, oracle):
    text = "Tokens from a file.\nTwo lines of it.\n"
    path = tmp_path / "notes.txt"
    path.write_text(text, encoding="utf-8")
    result = run("--file", str(path))
    assert result.returncode == 0, result.stderr
    ids = oracle.encode_ordinary(text)
    assert " ".join(map(str, ids)) in result.stdout
    assert f"{len(ids)} tokens, {len(text)} characters, {len(text.encode())} bytes" in result.stdout


def test_the_program_trains_a_tokenizer_with_train(tmp_path):
    path = tmp_path / "corpus.txt"
    path.write_text("banana bandana " * 50, encoding="utf-8")
    result = run("--train", str(path), "--vocab-size", "260", "banana")
    assert result.returncode == 0, result.stderr
    lines = result.stdout.strip().splitlines()
    ids = [int(word) for word in lines[-2].split()]
    assert ids, "the ids are the line before the count"
    assert all(0 <= i < 260 for i in ids)
    assert len(ids) < 6, "four merges are enough to shorten banana"
    assert lines[-1].endswith("6 characters, 6 bytes")


@pytest.mark.parametrize("args", [(), ("hello", "--file", "x.txt")], ids=["neither", "both"])
def test_the_program_wants_exactly_one_of_text_and_file(args):
    result = run(*args)
    assert result.returncode == 2, "argparse's usage error"
