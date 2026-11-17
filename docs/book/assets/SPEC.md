# The book: author spec (read all of it before writing a chapter)

The course has one book per module, in `docs/book/NN-slug/`, sharing `docs/book/assets/`. This file
holds the rules that every book follows. A module may add a short section at the end ("Module N") for
its own table of mechanisms; where the two disagree, that section wins for its module.

## Who reads this

Danish: about seven years of Python, the last two in applied AI work (open models, fine-tuning, serving
with vLLM). Typing code by hand is the skill being rebuilt, alongside data structures and algorithms.
Matrices and probability get a physical picture before a formula. Wants first principles, analogies that say where they
break, and no assumed knowledge of anything the chapter needs. Machine: MacBook, Apple M5 (4 performance
and 6 efficiency cores), macOS 26, Python 3.13 with uv. Each program is read, covered, typed into `scratch/` from
memory, compared with the page and run with `uv run python scratch/NAME.py`.

## The one rule (from CLAUDE.md)

Danish types every solution. The book may **teach** every mechanism with complete worked examples, but
it must **never** contain a working implementation, a sketch, pseudo-code or a "fixed" version of:

- a contract function of any module (Module 1: `time_calls`, `summarise`, `quickselect`, `percentile`,
  `histogram`, `render_report`, `slowest_lines`, and the `main` of `python -m llm101.bench`);
- a drill (`drills/`: `encode`, `top_endpoints`, `pair_with_sum`, `is_balanced`, `merge`,
  `MovingAverage`, `group_anagrams`, `longest_streak`, `sort_colours`, `count_stretches`, `tidy_path`,
  `free_slots`).

Teach each mechanism on a **different problem**, one step away, with its own names. Each module's
section at the end of this file has a table: *Mechanism, Teach it with, Never*. `tools/book-check.py`
refuses any code block that defines a stub's function or class name, and that check is a floor, not
the rule: a block that solves the same problem under another name breaks the rule too. The
"Never" column governs the teaching: the chapters, their worked examples and every rung 4. The folded
rungs 2 and 3 of the build chapter and of the drills chapter describe their own problem's idea in
words, as the ladder in CLAUDE.md says they do, and never in code.

## Voice

- **First principles.** Every idea is motivated by a problem before it is named. Say what the machine
  does (the interpreter, the clock, memory). No magic, no "just".
- **One idea at a time.** A new idea gets the smallest complete program that shows it, then its exact
  output, then a wider version.
- **Analogies say where they break**, in the same callout or the next sentence.
- **Plain English.** Short sentences. "You", not "we". A term in bold the first time it is used, and
  explained right there. No jokes that need programmer culture.
- **Concrete numbers.** Show `sys.getsizeof(1.0)` printing 24, not "floats are big". Times come from the
  M5 and say so.
- **Maths gets a picture first**: a ruler, a queue, a hand of cards, a thermometer. The formula comes
  after, in words before symbols.
- **British spelling**: colour, neighbour, initialise, behaviour, centre, summarise. Technical names keep
  their own spelling (`tokenizer`, `quantization` in a quoted name).
- **"In a real engine"** appears only where the link to vLLM, nano-vLLM or SGLang is genuine, and says
  where in that engine.

## Shape of a concept chapter

1. `p.chapter-kicker` ("Chapter N"), the `h1`, and a `p.lede`: one or two sentences on what you can do
   at the end.
2. An "In this chapter" `div.callout.note` with 4 to 7 bullets, in order.
3. **The problem first**: the first `h2` is a problem, not a name ("The problem: one timing lies").
4. A "First principle" callout early (what the machine does), and an "Analogy" callout with where it
   breaks.
5. Sections, one idea each: a small complete program, its output, a wider version. 2 to 4 "Try it"
   callouts per chapter, each followed by `details.hint` or `details.answer`. "Trap" callouts sit where
   the mistake happens.
6. A worked example on a different problem from the module's contract.
7. From Module 2 on, one **"Write it"** near the end (a `div.callout.try` with that label): a function
   of about ten lines, written from an empty file in ten minutes, on the chapter's mechanism and on a
   problem that is neither a contract function nor a drill. Its stub and three to five tests go in
   `drills/<set>/warmups/`, its name goes in `guarded` in `pyproject.toml`, and it gets one ledger row
   and no redos. A chapter with a "Write it" has at most three "Try it" callouts.
8. One "In a real engine" callout (class `twin`), where it is genuine.
9. "Check yourself": a `div.quiz` with 5 to 8 questions (explain, predict, or work out a number), each
   answer in a `details.answer`.
10. "What you can do now": 4 to 8 bullets that mirror "In this chapter".

**Length:** 2,000 to 3,500 words of prose per concept chapter, code not counted. A chapter is one read
block (90 minutes), with its programs rebuilt from memory. From Module 2 on a concept chapter has at
most eight complete programs: Module 1's chapters have ten to seventeen, which is more than the block
holds when each one is covered and retyped. **Python you need** boxes (`div.callout.note` with that
label) refresh a construct in a few lines where a chapter first leans on it (closures, `nonlocal`,
`try`/`finally`, dataclasses, f-string formats such as `:,` and `.2f`, `python -m`).

## Special chapters

- **00 Start here**: what the module builds and why; "Done when"; the day-by-day table (day, read,
  drill, milestone); the session's blocks; first-time setup (`uv sync`, the hook, reading the red); how
  to read the book; how to get unstuck. No new code beyond shell commands.
- **Drills**: one `h3` per drill (the tutor panel puts its rung box after each `h3`), with: the
  pattern in one sentence, a link to the stub, the time box, and rungs 1 to 3 of the ladder as
  `details.hint` blocks ("Rung 1: where to look", "Rung 2: the idea in words", "Rung 3: the shape").
  A review drill names its pattern only inside rung 2: its pattern line says that it is not said, and
  rungs 1 and 3 do not name it either.
  No solution in any form, folded or not. Before the drills, one `h2` per pattern that teaches the
  pattern on a different problem, with a complete worked example.
- **Build**: "The spec, restated" (short, linking the README), "Setup: read the red", then one `h2` per
  milestone whose text starts **"Milestone N"** ("Milestone 1: time_calls"; the tutor panel looks for
  that), each with these bold-labelled parts in order: **Goal**, **Re-read** (links to the exact
  sections), **Turns green** (the command), **The hint ladder** (four `details.hint`: "Rung 1: where to
  look", "Rung 2: the idea in words", "Rung 3: the shape", "Rung 4: the same mechanism on a different
  problem"; rung 4 may hold a complete program on the different problem), **Common bugs** (symptom,
  then cause), **Done when**, **Commit** (the message). Then "Make it yours" (stretch), the review
  ritual, and the log.
- **Appendix**: reading a traceback; the errors of this module as tables (message, cause, fix,
  chapter); cheat sheets (pytest, hypothesis, uv, the module's library calls); a glossary as a `dl`;
  what the next module brings.

## HTML contract

- One file per chapter: `NN-slug.html`, with `<title>NN · Title — Book title</title>`. Headings are `h2`
  and `h3` only below the `h1`. Anchors are made from the heading text by `book.js`; link to a section of
  another chapter as `05-where-the-time-goes.html#the-call-event`. The rule: lower case, and every run
  of characters other than a to z and 0 to 9 becomes one hyphen, with none at the ends ("Python's
  clocks" becomes `python-s-clocks`, "time_calls" becomes `time-calls`).
- The `head` loads the shared assets and the book's own config, in this order:

```html
<link rel="stylesheet" href="../assets/book.css?v=1">
<link rel="stylesheet" href="../assets/tutor.css?v=1">
<script src="../assets/theme.js?v=1"></script>
<script defer src="book-config.js?v=1"></script>
<script defer src="../assets/book.js?v=1"></script>
<script defer src="../assets/tutor.js?v=1"></script>
```

- `<nav class="sidebar" aria-label="Chapters"></nav>` and `<main>` are the whole body; `book.js` builds
  the top bar, the sidebar, the outline, prev and next, and the "done" box from `book-config.js`.
- No CDN, no inline `<style>` or `<script>`, no images that need a server. Escape `<`, `>` and `&` in
  code (`&lt;`, `&gt;`, `&amp;`).
- Paths in prose are relative to the repository root: `src/llm101/bench/stats.py`. Links to repository
  files from a chapter go up three levels: `../../../modules/01-measure/README.md`.

**Callouts:** `<div class="callout KIND"><span class="label">LABEL</span>…</div>` with KIND one of
`principle` (First principle), `analogy` (Analogy), `twin` (In a real engine), `trap` (Trap), `try`
(Try it), `note` (In this chapter, Python you need, or any other label).

**Stepped figures:** a picture that changes in a few steps, each with one sentence or two of
narration. `book.js` shows one step at a time, with a numbered track and Back and Next; without it
the steps appear one under the other.

```html
<figure class="steps" aria-label="What the figure shows">
<div class="step" data-label="One run each">
<svg class="viz" viewBox="0 0 720 180" role="img" aria-label="The step, in words">…</svg>
<p>What this step shows.</p>
</div>
…
<figcaption>Where the numbers come from.</figcaption>
</figure>
```

Two to five steps, each `data-label` of one to three words. The `svg` is inline and takes its
colours from the classes in `book.css` (`viz-a`, `viz-b`, `viz-c`, `viz-band`, `viz-axis`,
`viz-work`, `viz-wait`, `viz-small`), never from a colour written in the page, so that every
theme works. Every number in a figure is a number printed by a program of the same chapter. A figure
shows measurements or a mechanism on the chapter's teaching problem; it never draws the steps of a
contract function or a drill. At most two stepped figures per chapter.

**Hints and answers:** `<details class="hint"><summary>…</summary>…</details>` and
`<details class="answer"><summary>…</summary>…</details>`.

**Quiz:** `<div class="quiz"><div class="q"><p>Question</p><details class="answer"><summary>Answer</summary><p>…</p></details></div>…</div>`.

**Code:**

- `<pre class="code" data-lang="python" data-file="two_clocks.py" data-check="run"><code>…</code></pre>`
  is a complete program. `data-check` is one of:
  - `run` (the default): book-check runs it with the project's Python (`.venv/bin/python -I`), with no
    input and a 10-second limit; it must exit with 0.
  - `error`: it must exit with an error. If a `pre.output` follows, its last line must equal the last
    line the program printed to stderr (the exception line, such as `ValueError: k is out of range`).
  - `fragment`: a piece that does not run on its own (a signature, two lines in the middle of
    something). Not run. Keep fragments rare.
- `<pre class="output" data-for="two_clocks.py"><code>…</code></pre>` right after a `run` block is its
  exact output; book-check compares it, ignoring trailing spaces. **A program that prints something
  different on every run** (anything that prints a time) gets a `pre.output` **without** `data-for`,
  introduced as "one run on the M5; yours will differ". Run the program yourself and paste what it
  printed, so the numbers are real.
- File names in `data-file` are unique within a chapter; they are also the names the reader types in
  `scratch/`.
- `<pre class="shell"><code>$ uv run python scratch/two_clocks.py</code></pre>` for commands: the copy
  button copies only the `$ ` lines, without the `$ `.
- `data-lang="text"` for anything that is neither Python nor shell.

**Check your chapter:** `uv run python tools/book-check.py docs/book/NN-slug/NN-file.html` reports 0
problems (the code runs, outputs match, links and anchors resolve, and no block defines a contract or
drill name).

---

## Module 1: Measure first

Book title: **Measure first**. Files in `docs/book/01-measure/`:

| File | Chapter | Feeds |
|---|---|---|
| `index.html` | the book's front page | |
| `00-start-here.html` | 00 Start here | the week |
| `01-two-clocks.html` | 01 Two clocks | M1 `time_calls` |
| `02-tails-and-percentiles.html` | 02 Tails and percentiles | M2 `histogram`, M4 `percentile` |
| `03-partition-and-select.html` | 03 Partition and select | M3 `quickselect`, M4 |
| `04-pictures-in-the-terminal.html` | 04 Pictures in the terminal | M5 `summarise`, `render_report`, `main` |
| `05-where-the-time-goes.html` | 05 Where the time goes | M6 `slowest_lines` |
| `06-boxes-and-arrays.html` | 06 Boxes and arrays | M7 the Experiment |
| `07-drills.html` | 07 Drills | sets 00 and 01 |
| `08-build-the-harness.html` | 08 Build the harness | M1 to M7 |
| `09-appendix.html` | 09 Appendix | |

The spec is `modules/01-measure/README.md`; the contract is the stubs in `src/llm101/bench/` (their
docstrings are part of the spec); the tests are in `tests/m01/`.

| Mechanism | Teach it with | Never |
|---|---|---|
| Timing with two clocks | a kettle that you wait for against sums that you do: `time.sleep` against a busy loop, each timed once with `time.perf_counter_ns` and `time.process_time_ns`; the clocks' resolution (`time.get_clock_info`); why `time.time` is the wrong clock; warm-up shown on a function that builds a cache the first time it runs | a function that takes another function and a count and records a list of per-call times, with or without warm-up (that is `time_calls`) |
| Percentiles, tails, interpolation | commute times, the heights of a class, a queue at a café; reading a temperature between two hourly readings (linear interpolation in general); `numpy.percentile` and `statistics.quantiles` used to *look at* data | a function that computes a percentile of a list by numpy's linear method, sorted or not (that is `percentile`) |
| Histograms | counting words by length; which hour of the day a timestamp falls in (whole-number bins); `numpy.histogram` used to *look at* data; floating-point surprises such as `0.1 + 0.2` and `int(0.3 / 0.1)` | a function that returns counts and edges for equal-width bins of floats (that is `histogram`) |
| Partition and selection | a hand of cards split around a chosen card (in prose, tables and drawings); splitting a list of words around a pivot word into new lists with comprehensions (not in place); `random.choice` for a pivot; expected value with dice; binary search as the cousin that throws half away | an in-place partition of a list around a pivot (two- or three-way: that is the `sort_colours` drill), and any function that returns the k-th smallest (that is `quickselect`) |
| rich | a weather report: a `Table` of rainfall by month, and a bar chart of it drawn with `#` or `▇`; `Console(record=True)` and `export_text`; markup, and `rich.markup.escape` and `Text` for text with square brackets; `Group` | a function that renders a latency report, or a histogram of timings with `█` bars (that is `render_report`) |
| Profiling, `sys.settrace` | cProfile and pstats on a toy (a slow recursive Fibonacci and a fast one); a tracer that *prints* every event it sees (`call`, `line`, `return`) for a three-line function; a tracer that counts *calls* per function name with the `call` event; frames (`f_code.co_name`, `f_lineno`); `sys.gettrace`; `try`/`finally` to put things back; tracing against sampling | a tracer that counts or times anything line by line, and any explanation of how to turn events into time per line (that is `slowest_lines`) |
| Why numpy is fast; object sizes | `sys.getsizeof` of ints, floats, lists and tuples; a thousand floats in a list, in `array.array` and in numpy; a Python loop against numpy on *the sum* or *the mean* of a list, timed once with `time.perf_counter_ns`; boxes and pallets | the M7 Experiment itself (the sum of the squares of a million numbers, both ways, with the harness) |
| argparse | a tiny unit converter (`--km 5` prints miles) | the argument parser of `python -m llm101.bench` |

Do not define any of these names in an example: `time_calls`, `summarise`, `quickselect`, `percentile`,
`histogram`, `render_report`, `slowest_lines`, `Timings`, `Report`, nor the drill names. Do not write a
`main` that times a function many times and prints a report.

---

## Module 2: Tokenizer

Book title: **Tokenizer**. Files in `docs/book/02-tokenizer/`. The spec is
`modules/02-tokenizer/README.md`; the contract is the stubs in `src/llm101/tokenizer/` (their
docstrings are part of the spec); the tests are in `tests/m02/`; the drills are set 02 in
`drills/02-heaps-lists/`, and each concept chapter's **Write it** is in its `warmups/` folder.

| File | Chapter | Feeds | Write it |
|---|---|---|---|
| `index.html` | the book's front page | | |
| `00-start-here.html` | 00 Start here | the week | |
| `01-bytes-and-utf8.html` | 01 Bytes and UTF-8 | M1 `utf8_encode` | `count_characters` |
| `02-pairs-and-merges.html` | 02 Pairs and merges | M2 `count_pairs`, `merge_pair`; M3 `train_bpe` | `busiest_hour` |
| `03-encoding-by-rank.html` | 03 Encoding by rank | M4 `pretokenize`, `apply_merges`, `Tokenizer` | `invert_table` |
| `04-gpt2s-tokenizer.html` | 04 GPT-2's tokenizer | M5 `bytes_to_unicode`, `load_gpt2`, `main` | `read_palette` |
| `05-heaps-and-linked-lists.html` | 05 Heaps and linked lists | M6 `apply_merges_fast` | `next_alive` |
| `06-tokens-as-cost.html` | 06 Tokens as cost | M7 the Experiment | `messages_that_fit` |
| `07-drills.html` | 07 Drills | set 02 | |
| `08-build-the-tokenizer.html` | 08 Build the tokenizer | M1 to M7 | |
| `09-appendix.html` | 09 Appendix | | |

### The h2 headings of each chapter

Fixed in advance, so that chapters link to each other's sections by anchor (the slug rule above). A
chapter may add `h3`s under them, and may add an `h2` only where this list says "and others".

- **00**: What you will build: a tokenizer · The rule: you type every line · Done when · The six
  days · First-time setup · A tour of the repository · How to read this book · How to get unstuck ·
  Check yourself · What you can do now
- **01**: The problem: a model reads numbers · Characters and code points · Bytes in Python · Bits,
  shifts and masks · The UTF-8 table · Reading UTF-8 by hand · Surrogates, and text that is not text ·
  When bytes are not a whole character · How many bytes a script takes · Check yourself · What you
  can do now
- **02**: The problem: 256 tokens are too few · Counting with a dict · Neighbours in a list · Ties,
  and choosing with a key · Byte-pair encoding by hand · Overlapping pairs · Count each word once ·
  What training gives you · Check yourself · What you can do now
- **03**: The problem: new text, old merges · A table of ranks · Encoding a word by hand · From ids
  back to text · Why split before merging · Regular expressions from first principles · Letters in
  every script: the regex package · GPT-2's split pattern, piece by piece · Round trips and
  hypothesis · Check yourself · What you can do now
- **04**: The problem: two files and 50,257 ids · A first look at the files · Why the files are full of
  Ġ · Reading JSON and lines of text · Ids in GPT-2's order · The token that no merge makes · tiktoken,
  the oracle · A program with exclusive arguments · Colour in rich, one piece at a time · Check
  yourself · What you can do now
- **05**: The problem: one long word takes seconds · Why the slow way is quadratic · Heaps from first
  principles · heapq, and how tuples compare · Entries that went stale · A linked list in two lists ·
  Removing from the middle in constant time · How the two fit together · Check yourself · What you
  can do now
- **06**: The problem: the same sentence, different bills · Characters per token · Paying per token ·
  Tokens and latency · How big should a vocabulary be? · Measuring a tokenizer's speed · Why
  tiktoken is fast · Check yourself · What you can do now
- **07**: How the drills work · The order of this module · Following links: a chain of nodes ·
  Walking two chains at once · A heap as a to-do list · The smallest of many · Set 02: heaps and
  linked lists · The debugging drill · Check yourself · What you can do now. Under "Set 02", one `h3`
  per drill: `reverse_list`, `merge_two_lists`, `days_to_wait`, `k_largest`, `merge_sorted_runs`,
  `longest_draw`; under "The debugging drill", one `h3`: `print_queue`.
- **08**: The spec, restated · Setup: read the red · Milestone 1: utf8_encode · Milestone 2:
  count_pairs and merge_pair · Milestone 3: train_bpe · Milestone 4: pretokenize, apply_merges and
  Tokenizer · Milestone 5: bytes_to_unicode, load_gpt2 and main · Milestone 6: apply_merges_fast ·
  Milestone 7: the Experiment · When you are stuck · Make it yours · The review and the log · Check
  yourself · What you can do now
- **09**: Reading a traceback · The errors of this module · Cheat sheets · Glossary · What Module 3
  brings · Check yourself · What you can do now

### What a chapter may use

- Book programs run with the project's Python in an empty folder (book-check). They may import the
  given names of the contract, which are data and not functions: `from llm101.tokenizer.gpt2 import
  VOCAB_PATH, MERGES_PATH` reads GPT-2's real files from `data/gpt2/`. They may build tiktoken's GPT-2
  encoding from those two files to *look at* tokens, as `tests/m02/conftest.py` does, never from the
  network. They may never call a contract function or a drill: those are stubs and raise.
- `GPT2_PATTERN` may be printed and taken apart one alternative at a time; no example calls
  `findall`, `finditer` or `split` with the whole pattern (that call is `pretokenize`). Tables may
  show how the pattern splits sample strings.
- Numbers about GPT-2 (ids, token counts) come from running the oracle, and the chapter says so.
- **The oracle's setup is taught once**, in chapter 4's "tiktoken, the oracle". Chapters 1 to 3 show
  the oracle's answers as tables ("From the oracle") instead of programs. A later program that needs
  the setup says that its first lines may be typed with the page open; no chapter has more than two
  such programs.
- **Each idea is taught in one place.** Chapter 7's pattern sections are read before chapter 5
  (block 5 of the day before each drill), so chapter 5 builds on them and does not teach a heap's
  shape, `heapq` or a chain of nodes again. The book has one "In a real engine" box on vLLM's free
  block queue (chapter 5).

### Mechanisms

| Mechanism | Teach it with | Never |
|---|---|---|
| Code points, bytes, UTF-8 | `ord`, `chr`, `len` of a str against `len` of its bytes; `bytes` and `bytearray` literals, indexing that gives an int, `hex()`, `f"{b:08b}"`; `str.encode` and `bytes.decode` used to *look*; shifts and masks on a different problem (an RGB colour packed into one int and taken apart, flags in a permissions byte); the UTF-8 table as boxes of bits; *decoding* one character by hand, bytes to code point, in a table | any code that turns a code point or a string into UTF-8 bytes with shifts and masks, for any number of bytes (that is `utf8_encode`); counting characters in UTF-8 bytes in code (that is the Write it `count_characters`) |
| Counting and choosing | `dict.get`, `collections.Counter` on the words of a text; neighbours with `zip(xs, xs[1:])` on a different question (day-to-day changes in temperature); `max` and `min` with a key that is a tuple, to break ties (students by score, then name); `str.replace` to show the left-to-right, no-overlap rule on strings ("aaa".replace("aa", "X")) | a function or loop that counts the neighbouring pairs of a sequence, or replaces a pair of neighbours with one item, on ids, letters or words (that is `count_pairs` and `merge_pair`); the busiest hour (the Write it) |
| Training BPE | by hand, in prose and tables: a corpus of a few words, round by round (counts, the winner, the new token); why each distinct word is counted once and weighed by its frequency, shown with `Counter` on a text | a training loop in code, on any data (that is `train_bpe`) |
| Encoding by rank, decoding | a dict of ranks and `.get(pair, math.inf)`; encoding one word by hand in a table, round by round; `bytes.decode` with `errors="strict"`, `"replace"` and `"ignore"` on broken bytes; `b"".join` | a loop that repeatedly finds the lowest-ranked pair and merges it (that is `apply_merges`); a class or function that turns text into ids or ids into text through merges (that is `Tokenizer`); inverting a dict in code (the Write it `invert_table`) |
| Regular expressions | `re.findall` and `re.fullmatch`; character classes, `+`, `?`, alternation (the first alternative that matches wins), groups and `(?:...)`, the lookahead `(?!...)`; `re.compile(r"\p{L}")` failing in `re` (an `error` block), and `regex` with `\p{L}` and `\p{N}`; each alternative of GPT-2's pattern on its own, on sample strings | a call of `findall`, `finditer` or `split` with the whole of GPT-2's pattern (that is `pretokenize`) |
| Property tests of a round trip | hypothesis `st.text()` and `st.characters(codec="utf-8")`; a round trip of something else (`json.dumps` and `json.loads`, `base64`) | a round-trip test of a tokenizer |
| GPT-2's files | `head` and `wc -l` on the real files (shell blocks); `json.loads` and `Path.read_text(encoding="utf-8")` on a small JSON of your own and then on `vocab.json`, looking up a few tokens; `str.split("\n")` and its empty last piece; the idea of a byte-to-character map, in words and a table of a few rows, with the rule stated as the docstring's three ranges (`str.isprintable()` may explain why the ranges have gaps, for a byte or two, never as a test over all 256) | code that builds GPT-2's map from 256 bytes to printable characters, or a predicate over all 256 bytes that picks the ones it keeps (that is `bytes_to_unicode`); parsing `merges.txt` into pairs of ids, or anything that builds a tokenizer from the two files (that is `load_gpt2`); reading a JSON palette into hex codes (the Write it `read_palette`) |
| tiktoken | building GPT-2's encoding from `data/gpt2/` and calling `encode_ordinary`, `decode_single_token_bytes` and `decode` to look at tokens | counting the tokens of the six sentences in `modules/02-tokenizer/BENCH.md`, or timing encoders on `argparse`'s source (that is the M7 Experiment) |
| argparse, rich | a mutually exclusive group on a different program (a temperature converter that takes `--celsius` or `--fahrenheit`); `rich.text.Text` with `append(text, style=...)` and background styles on a different problem (marking the numbers in a log line) | a `main` that tokenizes a text and prints its tokens on alternating colours, its ids or its count (that is `main`) |
| Heaps | `heapq` on a different problem (a hospital's triage queue, events in a simulation by time); a heap drawn as a tree in a list, parent `(i - 1) // 2`; tuples compared item by item; stale entries recognised by a version number (a delivery whose time was changed) | the drills (`k_largest`, `merge_sorted_runs`), and popping past entries that are no longer in a set (the Write it `next_alive`); a heap of pairs of neighbours, or any merge of neighbouring items driven by a heap (that is `apply_merges_fast`); the fault of the debugging drill `print_queue` (unorderable items reached when priorities tie) or its fix, anywhere in the book before chapter 7's rungs |
| Linked lists | `Node` objects with `next`: build, walk, insert at the front, remove the node after a given one (chapter 7); a list kept in two lists of indices, `prev` and `next`, on a different problem (people leaving a queue, a playlist with songs removed) (chapter 5) | reversing a linked list or merging two sorted ones (the drills `reverse_list`, `merge_two_lists`); merging two neighbours of a linked list into one item (part of `apply_merges_fast`) |
| Heap over a linked list | in words in chapter 5 ("How the two fit together"); as a complete program only in rung 4 of Milestone 6, on a different problem: simplifying a line by removing, again and again, the point whose triangle with its neighbours has the smallest area (Visvalingam's algorithm). It removes points; it never merges two items into a new one | a program that merges neighbouring pairs by rank or by any priority |
| Cost and speed | prices in dollars per million tokens, input against output; tokens per character on sentences of your own (not BENCH.md's); `time.perf_counter_ns` around a call (the harness is the reader's, and it is a stub while the book is written) | how many of the newest messages fit in a window (the Write it `messages_that_fit`); the M7 Experiment itself, and any claim about which of `apply_merges` and `apply_merges_fast` is faster on ordinary text |

Do not define any guarded name in an example (`pyproject.toml`, `[tool.llm101] guarded`), and do not
write a `main` that tokenizes a text and prints its tokens.
