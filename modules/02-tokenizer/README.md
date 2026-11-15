# 02-tokenizer: Tokenizer

**Module 2** (planned from Mon 23 Nov 2026, once Module 1 is done) · Phase 1, one model, one request ·
Book: [docs/book/02-tokenizer](../../docs/book/02-tokenizer/index.html), build chapter:
[8 Build the tokenizer](../../docs/book/02-tokenizer/08-build-the-tokenizer.html)

> **A draft for the spec ritual.** Before day 1, in one sitting of about an hour: read it, with the
> book's chapter 00 (Start here) and chapter 7's "How the drills work" and "Following links", which
> day 1's drill needs; then settle the decisions at the end (the ritual's usual twenty minutes), and
> freeze it with a commit (`Module 2: spec frozen`). After that, a requirement can only move to
> "Stretch", in writing, with the date. The stubs, the tests and the book are written to this draft
> already; whatever the ritual changes, Claude changes in them the same morning.

## Concept

A model does not read letters. It reads **token ids**: whole numbers from 0 to 50,256 for GPT-2, each
standing for a short run of bytes. The **tokenizer** turns text into ids and ids back into text, and
it is the first and the last thing every request passes through.

Text is first **bytes**: UTF-8 writes each character as one to four bytes, so any text at all, in any
script, becomes a list of numbers from 0 to 255. **Byte-pair encoding (BPE)** then learns, from a body
of text, which neighbouring pairs to glue together: it counts every adjacent pair, merges the most
frequent one into a new token, and repeats. The list of merges, in the order they were learned, *is*
the tokenizer. Encoding replays those merges on new text, earliest first; decoding glues the bytes
back together. GPT-2 does exactly this, after splitting the text into words with one regular
expression, and its 50,000 merges are a text file you can read.

A token is also the unit of **cost**. Prompts are billed per token, the KV cache stores per token, and
a reply streams one token at a time. The same sentence can take several times as many GPT-2 tokens in
one language as in another, so the tokenizer decides what a request costs before the model sees it.

The Python you meet this module: `bytes` and `bytearray`, `ord` and `chr`, bit shifts and masks,
`str.encode` and `bytes.decode` with `errors=`, dicts as counters, `max` and `min` with a `key`,
regular expressions with the `regex` package, `json`, reading files with `pathlib`, `heapq`, and a
linked list kept in two lists of indices.

## The pattern

- **Hash maps.** Training is counting: a dict from a pair of ids to how often it occurs, and a dict
  from each distinct word to how often *it* occurs, so that a word seen a thousand times is counted
  once and weighed a thousand times. A merge table is a dict from a pair to its rank.
- **Heaps.** Encoding asks, again and again, "which pair here was learned earliest?" A scan answers
  it in n steps each time; a heap of candidate pairs answers it in log n, if you can recognise the
  entries that went stale.
- **Linked lists.** Merging two neighbours in a Python list shifts everything after them. A linked
  list, kept as two lists of neighbour indices, merges in place in constant time.
- [CONCEPTS.md](../../CONCEPTS.md) rows introduced here: every row whose "Introduced" column says M2.
  Reused: arrays and hashing (M1 drills), Big-O, and the harness (`time_calls`, `summarise`), which
  measures this module's Experiment.

## In a real engine

- vLLM tokenizes every prompt before scheduling it, with the model's Hugging Face tokenizer, and turns
  the ids it generates back into text a few at a time while it streams. A token can end in the middle
  of a character, so the detokenizer holds back bytes that do not yet make a whole character: the
  `errors="replace"` question of chapter 3, in a server.
- tiktoken, OpenAI's tokenizer, does GPT-2's split and merges in Rust. Your tests check your ids
  against it, built from the same two files you load.
- Prefix caching (Module 11) hashes blocks of token ids, and the token budget of a batch (Module 9) is
  counted in tokens. Both start here.

## Spec

The program is `python -m llm101.tokenizer`.

| Argument | Meaning | Default |
|---|---|---|
| `TEXT` | the text to tokenize | |
| `--file PATH` | tokenize the text of this file instead | |
| `--train PATH` | train a tokenizer on the text of this file, and use it instead of GPT-2's | off: GPT-2's |
| `--vocab-size N` | with `--train`, the size of the vocabulary to train | 512 |

Give exactly one of `TEXT` and `--file`. Behaviour:

- Without `--train` it loads GPT-2's tokenizer from `data/gpt2/` (committed; the files and their
  checksums are in `tools/fetch-gpt2-tokenizer.py`).
- With rich, it prints the text token by token, each token on a background colour that alternates
  between two, so that you can see where one token ends and the next begins. A token is shown as its own bytes,
  decoded on their own with `errors="replace"`.
- Under it, the ids, separated by spaces.
- Last, one line: `N tokens, C characters, B bytes`.

Example: `uv run python -m llm101.tokenizer "Grüße aus München! 你好"`

## The contract

The package is `src/llm101/tokenizer/`. The names, signatures and docstrings are given, and so are the
`Pair` alias, GPT-2's split pattern `GPT2_PATTERN` and the paths of GPT-2's files; the tests call
these exact names. **Every docstring is part of the spec**: it says what to return, what to raise, and
what the tests check.

One rule holds for every tokenizer in this module: ids 0 to 255 are the single bytes, in some order,
and **merge number r makes the token whose id is 256 + r**. For a tokenizer you train, byte b has id b.
For GPT-2 the bytes have other ids (`!` is 0), and its 50,000 merges make ids 256 to 50,255; 50,256 is
`<|endoftext|>`, which no merge makes.

| Function | File | One line |
|---|---|---|
| `utf8_encode(text) -> bytes` | `utf8.py` | UTF-8 by hand, with shifts and masks |
| `count_pairs(ids) -> {pair: count}` | `train.py` | How often each adjacent pair occurs |
| `merge_pair(ids, pair, new_id) -> list` | `train.py` | Replace every occurrence of a pair, left to right |
| `train_bpe(chunks, vocab_size) -> [pair]` | `train.py` | Learn the merges, most frequent pair first |
| `pretokenize(text) -> [str]` | `bpe.py` | Split text into chunks with GPT-2's pattern |
| `apply_merges(ids, ranks) -> list` | `bpe.py` | Replay the merges on one chunk, earliest first |
| `Tokenizer(byte_ids, merges, special_tokens)` | `bpe.py` | `encode`, `decode`, `token_bytes` |
| `bytes_to_unicode() -> {byte: char}` | `gpt2.py` | GPT-2's map from a byte to a printable character |
| `load_gpt2(vocab_path, merges_path) -> Tokenizer` | `gpt2.py` | GPT-2's tokenizer, from its two files |
| `apply_merges_fast(ids, ranks) -> list` | `fast.py` | The same answer with a heap and a linked list |
| `main(argv=None)` | `__main__.py` | The program |

`utf8.py` may not call `.encode()` or `.decode()`, import `codecs`, or hand a string and an encoding
to `bytes()` or `bytearray()`; `gpt2.py` may not import tiktoken; `fast.py` may not call `apply_merges`. The tests read
the files to check. tiktoken is the tests' oracle, not your tool.

### Milestones

Do them in order. Each milestone has a book chapter that comes first, so a day is: read the chapter,
then turn its milestone green. The days are a guide, not a deadline.

| Day | | Milestone | Read first | Turns green |
|---|---|---|---|---|
| 1 | **M1** | `utf8_encode` | ch. 1, Bytes and UTF-8 | `uv run pytest tests/m02/test_utf8.py` |
| 2 | **M2** | `count_pairs`, `merge_pair` | ch. 2, Pairs and merges | `uv run pytest tests/m02 -k "count_pairs or merge_pair"` |
| 2 | **M3** | `train_bpe` | ch. 2 | `uv run pytest tests/m02 -k train_bpe` |
| 3 | **M4** | `pretokenize`, `apply_merges`, `Tokenizer` | ch. 3, Encoding by rank | `uv run pytest tests/m02/test_bpe.py`: the first half of "Done when" |
| 4 | **M5** | `bytes_to_unicode`, `load_gpt2` and `main` | ch. 4, GPT-2's tokenizer | `uv run pytest tests/m02/test_gpt2.py`: the second half of "Done when"; then run the program |
| 5 | **M6** | `apply_merges_fast`, and `Tokenizer` uses it | ch. 5, Heaps and linked lists | `uv run pytest tests/m02/test_fast.py` |
| 6 | **M7** | The Experiment in [BENCH.md](BENCH.md) | ch. 6, Tokens as cost | BENCH.md has its prediction, measurement and explanation |

Commit after each one: `M1: utf8_encode green`. Stuck? The hint ladders are in book chapter 8, folded
away. Ask Claude for one rung at a time.

No test in `tests/m02` passes before you type anything. The tests that read your code (for `.encode`
in `utf8.py`, tiktoken in `gpt2.py`, `apply_merges` in `fast.py`) call your function first, so they
stay red until it works.

## Done when

goal.md: *round trips are exact on arbitrary Unicode, and token IDs match GPT-2's tokenizer on the
test set.*

- [ ] `test_done_when_round_trips_are_exact_on_arbitrary_unicode` and the rest of `test_bpe.py` are
      green.
- [ ] `test_done_when_ids_match_gpt2_on_the_test_set` and the rest of `test_gpt2.py` are green.
- [ ] `uv run pytest tests/m02` is green from end to end.
- [ ] `uv run python -m llm101.tokenizer "Grüße aus München! 你好"` prints the coloured tokens, the
      ids and the count.
- [ ] [BENCH.md](BENCH.md) has its Experiment: a prediction written before the run, the measurement,
      and two sentences on why. Its headline number is in the Measurements table of the top-level
      [README](../../README.md).
- [ ] One commit per milestone (M1 to M7), each through the pre-commit hook, and one more for M7's
      prediction, made before its measurement.
- [ ] A review of the whole module has been run, and its three questions are answered in
      [log.md](../../log.md).
- [ ] Five lines in log.md, and `"m02"` added to `done` under `[tool.llm101]` in `pyproject.toml`.

## Drills this module

Set 02, [heaps and linked lists](../../drills/02-heaps-lists/README.md): six problems and a debugging
drill. Four are on this module's pattern: `reverse_list` and `merge_two_lists` (linked lists),
`k_largest` and `merge_sorted_runs` (heaps). `days_to_wait` and `longest_draw` are review: they do not
say which pattern they need. `print_queue` is the debugging drill: a short program with a failing test,
to find, explain and fix in 20 minutes. Each concept chapter also has one **Write it**: a function of
about ten lines on that chapter's mechanism, in `drills/02-heaps-lists/warmups/`, with one ledger row
and no redos.

Redos come first every day, and set 01's +7 redos and the eight that Module 1's week leaves fall in
this week's first days. A new problem that does not fit in the hour waits for the next drill block.

| Day | Drill block |
|---|---|
| 1 | The redos that fall due (eight from Module 1's week), then `reverse_list` if the hour allows |
| 2 | Redos, then `merge_two_lists` and `days_to_wait` |
| 3 | Redos, then `k_largest` |
| 4 | Redos, then `merge_sorted_runs` |
| 5 | Redos, then `print_queue`, then `longest_draw` if the hour allows (otherwise it waits for the next drill block) |
| 6 | Redos, then the mock round (an engine kata from Module 1) |

## Stretch goals (only after "Done when")

1. **A cache of chunks.** GPT-2's own encoder keeps a dict from each chunk it has seen to its ids.
   Add one to `Tokenizer`, and measure what it saves on a long English text with your harness.
2. **Training that updates its counts.** `train_bpe` counts every pair again after each merge. Update
   only the counts that a merge changes, and measure the speed-up on 2,000 merges.
3. **`utf8_decode` by hand**, with Python's `errors="replace"` behaviour: one `�` for each maximal
   piece of a broken sequence. Check it against `bytes.decode` with hypothesis.
4. **Unigram segmentation** (goal.md's stretch): split a word into vocabulary pieces so that the sum
   of their log-probabilities is highest, with dynamic programming. It is Word Break with scores.

## Decisions for the spec ritual

Each has a default. Change what you want here, then freeze.

1. **Milestone order**: as above. Default: keep.
2. **UTF-8 by hand (M1).** Keep it, or use `str.encode` and start at M2. Default: keep. It is the
   one place this module makes you look at bits, and chapter 6's cost of a sentence in another script
   starts there.
3. **Ties in training.** When two pairs are equally frequent, the smaller pair wins (compared as
   tuples). The other choice is the pair seen first, which is what some trainers do. Default: the
   smaller pair; it does not depend on the order of a dict.
4. **The Experiment (M7)**: "the same sentence in six languages and scripts: how many tokens each, and
   how much faster is tiktoken than your encoder on a long text?", or a question of your own. Default:
   as drafted.
5. **`--train` in the program.** Keep it, or move it to stretch. Default: keep. It is how you see
   your own merges at work.
6. **GPT-2's files in the repository** (1.5 MB in `data/gpt2/`), or fetched by
   `tools/fetch-gpt2-tokenizer.py` before the tests run. Default: committed, so the tests and CI never
   need the network.

## How to run

```sh
uv run pytest tests/m02/test_utf8.py -x       # one milestone's file, stopping at the first failure
uv run pytest tests/m02 -k train_bpe          # one milestone, by name
uv run pytest tests/m02                       # everything, once M6 is green
uv run python -m llm101.tokenizer "Hello, wörld!"   # the program, once M5 is green
uv run python tools/fetch-gpt2-tokenizer.py --check  # GPT-2's files are present and unchanged
```

## Files

```
modules/02-tokenizer/README.md   this file: the spec
modules/02-tokenizer/BENCH.md    your numbers (M7)
src/llm101/tokenizer/utf8.py     utf8_encode
src/llm101/tokenizer/train.py    count_pairs, merge_pair, train_bpe; Pair (given)
src/llm101/tokenizer/bpe.py      pretokenize, apply_merges, Tokenizer; GPT2_PATTERN (given)
src/llm101/tokenizer/gpt2.py     bytes_to_unicode, load_gpt2; the paths of GPT-2's files (given)
src/llm101/tokenizer/fast.py     apply_merges_fast
src/llm101/tokenizer/__main__.py main
data/gpt2/                       GPT-2's vocab.json and merges.txt (given)
tests/m02/                       the tests (given): the spec, in code
```

Every function body in `src/llm101/tokenizer/` is yours. Everything else in this list is given.
