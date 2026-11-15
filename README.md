# llm-inference-101: LLM inference in Python, typed by hand

A self-paced course in 18 modules. It goes from a benchmark harness to a tokenizer, GPT-2 small in
numpy, sampling and a KV cache; then to a mini serving engine with continuous batching, a paged KV
cache, prefix caching, chunked prefill, speculative decoding and structured output; then to reading,
tuning, quantising and fine-tuning for vLLM; and finally to serving open models behind a router, with
retrieval, on more than one kind of hardware. Data structures and algorithms are learned where the
engine needs them: quickselect for percentiles, a heap for top-k, a doubly linked list for free KV
blocks, a radix tree for shared prefixes.

> **Every line in `src/llm101/` and `drills/` is typed by hand.** Claude writes the specs, the tests and
> the book, and reviews finished code, but never writes the solution (see [CLAUDE.md](CLAUDE.md)).
> Early code is a learner's code on purpose: judge the trajectory, the tests and the measurements.

## Where things are

| | |
|---|---|
| [goal.md](goal.md) | The spine: the goal, the ground rules, the 18 modules, the patterns table, the reading |
| [docs/methodology.md](docs/methodology.md) | How a day and a module run: blocks, the spec ritual, drills and the ledger, reviews |
| [docs/setup.md](docs/setup.md) | This Mac, the first-time steps, and what arrives with which module |
| [CLAUDE.md](CLAUDE.md) | The tutor rules Claude follows in this repo |
| [CONCEPTS.md](CONCEPTS.md) | The concept graph: every pattern and inference concept, where it is introduced and reused |
| [docs/book/index.html](docs/book/index.html) | **The book**: one per module ([online](https://daniishkhan.github.io/llm-inference-101/)) |
| [modules/01-measure/README.md](modules/01-measure/README.md) | The current module's spec: Measure first |
| [drills/](drills/) | Classic problems by pattern, a stub and its tests each, typed against the clock |
| [ledger.md](ledger.md) | Every drill attempt: minutes, hints, lookups, the two redo dates |
| [log.md](log.md) | Five lines a session, and a measurement at the end of each module |
| [docs/parking-lot.md](docs/parking-lot.md) | Ideas waiting for a decision date |

## Quick start

```sh
uv sync                        # Python 3.13 and the dependencies, into .venv
tools/install-hooks.sh         # the pre-commit hook: ruff format and lint checks
uv run pytest tests/m01        # Module 1's tests: all red on day one; that is the starting line
```

Then read [the Module 1 spec](modules/01-measure/README.md) and start at
[chapter 0 of its book](docs/book/01-measure/00-start-here.html).

### Reading the book

**Online:** [daniishkhan.github.io/llm-inference-101](https://daniishkhan.github.io/llm-inference-101/),
published from `main` whenever the book changes and its check passes.

**Locally:** the book is plain HTML with no build step. Open `docs/book/index.html`, or serve it with
`uv run python tools/serve-book.py` and visit <http://localhost:8767>. There is no live tutor: the
tutor panel composes a prompt for you to paste into Claude Code in the terminal, where
[CLAUDE.md](CLAUDE.md) applies.

## Modules

A module takes about a week and is done when its "Done when" passes ([goal.md](goal.md)).

| # | Module | You build | Pattern | Status |
|---|---|---|---|---|
| | **Phase 1: one model, one request (Mac)** | | | |
| 1 | Measure first | A benchmark harness: p50, p95, p99, throughput, a terminal histogram, a line timer | Arrays and hashing; quickselect | **In progress** (from Mon 16 Nov 2026) |
| 2 | Tokenizer | BPE: train, encode, decode; GPT-2's tokenizer reproduced | Hash maps, heaps, linked lists | Not started |
| 3 | Forward pass | GPT-2 small in numpy from its safetensors file, with greedy generation | Matrix shapes; complexity | Not started |
| 4 | Sampling | Temperature, top-k, top-p, repetition penalty, stop strings; a live probability chart | Heaps, quickselect, prefix sums, binary search, sliding window | Not started |
| 5 | KV cache | The cache, and tokens per second with and without it | Dynamic arrays, ring buffers | Not started |
| | **Phase 2: many requests, a mini engine (Mac)** | | | |
| 6 | Serving loop | An async server for `/v1/completions` and `/v1/chat/completions` that streams | Queues, state machines | Not started |
| 7 | Continuous batching | A step-level scheduler and an animation of batch slots | Greedy, intervals | Not started |
| 8 | Paged KV cache | A block allocator with alloc, free and fork, and a live block map | Doubly linked lists | Not started |
| 9 | Prefix caching | Chained block hashes and a radix tree, compared on a chat workload | Hashing, LRU, tries | Not started |
| 10 | Scheduling and chunked prefill | Decode-first scheduling with chunked prefill and priorities | Heaps, greedy, sliding windows | Not started |
| 11 | Speculative decoding and structured output | N-gram drafts, and a JSON mode from token masks | Hashing, two pointers, stacks, graphs, tries | Not started |
| | **Phase 3: real vLLM (GPU)** | | | |
| 12 | Read nano-vLLM, then vLLM | One request traced end to end, and a one-page map | Reading code | Not started |
| 13 | Performance and tuning | A load generator and a tuning report | Binary search on the answer; streaming percentiles | Not started |
| 14 | Quantization | One model served at three precisions; int4 packing | Bit manipulation | Not started |
| 15 | Fine-tuning and multi-LoRA serving | A LoRA, served beside three others on one base model | Hashing, LRU | Not started |
| | **Phase 4: serving open models for real** | | | |
| 16 | The front door | A router that routes by prefix, with a terminal dashboard | Consistent hashing, heaps, a token bucket | Not started |
| 17 | RAG serving | Exact and IVF top-k search, served behind the router | Heaps, k-means, graph search | Not started |
| 18 | Other hardware | One model on four kinds of hardware: cost per million tokens and latency | Careful measurement | Not started |
| | **Capstone** | One repo: the engine, the router, the RAG pipeline, the hardware report, a write-up | | Not started |

## Measurements

Each module keeps its numbers in its own `BENCH.md`, with the machine, the date and an Experiment
(the prediction is written before the run). This table collects the headline number of each.

| Module | Headline number | Source |
|---|---|---|
| 1 | *not yet measured* | [modules/01-measure/BENCH.md](modules/01-measure/BENCH.md) |

## Layout

```
README.md           the map (this file)
goal.md             the spine
CLAUDE.md           tutor rules: explain, set problems, test, review; never solve
CONCEPTS.md         concept graph
ledger.md, log.md   your drill ledger and your log
pyproject.toml      the uv project; [tool.llm101] done lists the finished modules
src/llm101/         the engine you type, one subpackage per module
tests/mNN/          each module's tests (the spec)
modules/NN-slug/    each module's README (the frozen spec) and BENCH.md
drills/             classic problems by pattern
docs/               methodology, setup, parking lot, the book
scratch/            your folder for the book's examples
tools/              book check, book server, Pages build, CI helper, hook installer
```

Toolchain, decided once: Python 3.13 with uv; numpy and rich; pytest, hypothesis and ruff. Everything
else arrives with the module that needs it ([docs/setup.md](docs/setup.md)).
