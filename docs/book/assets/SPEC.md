# The book: author spec (read all of it before writing a chapter)

The course has one book per module, in `docs/book/NN-slug/`, sharing `docs/book/assets/`. This file
holds the rules that every book follows. A module may add a short section at the end ("Module N") for
its own table of mechanisms; where the two disagree, that section wins for its module.

## Who reads this

Danish: about seven years of Python, the last two in applied AI work (open models, fine-tuning, serving
with vLLM). Typing code by hand is the skill being rebuilt, alongside data structures and algorithms.
Matrices and probability get a physical picture before a formula. Wants first principles, analogies that say where they
break, and no assumed knowledge of anything the chapter needs. Machine: MacBook, Apple M5 (4 performance
and 6 efficiency cores), macOS 26, Python 3.13 with uv. Examples are typed into `scratch/` and run with
`uv run python scratch/NAME.py`.

## The one rule (from CLAUDE.md)

Danish types every solution. The book may **teach** every mechanism with complete worked examples, but
it must **never** contain a working implementation, a sketch, pseudo-code or a "fixed" version of:

- a contract function of any module (Module 1: `time_calls`, `summarise`, `quickselect`, `percentile`,
  `histogram`, `render_report`, `slowest_lines`, and the `main` of `python -m llm101.bench`);
- a drill (`drills/`: `encode`, `top_endpoints`, `pair_with_sum`, `is_balanced`, `merge`,
  `MovingAverage`, `group_anagrams`, `longest_streak`, `sort_colours`).

Teach each mechanism on a **different problem**, one step away, with its own names. Each module's
section at the end of this file has a table: *Mechanism, Teach it with, Never*. `tools/book-check.py`
refuses any code block that defines a stub's function or class name, and that check is a floor, not
the rule: a block that solves the same problem under another name breaks the rule too.

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
7. One "In a real engine" callout (class `twin`), where it is genuine.
8. "Check yourself": a `div.quiz` with 5 to 8 questions (explain, predict, or work out a number), each
   answer in a `details.answer`.
9. "What you can do now": 4 to 8 bullets that mirror "In this chapter".

**Length:** 2,000 to 3,500 words of prose per concept chapter, code not counted. A chapter is one read
block (90 minutes), with its examples typed. **Python you need** boxes (`div.callout.note` with that
label) refresh a construct in a few lines where a chapter first leans on it (closures, `nonlocal`,
`try`/`finally`, dataclasses, f-string formats such as `:,` and `.2f`, `python -m`).

## Special chapters

- **00 Start here**: what the module builds and why; "Done when"; the day-by-day table (day, read,
  drill, milestone); the session's blocks; first-time setup (`uv sync`, the hook, reading the red); how
  to read the book; how to get unstuck. No new code beyond shell commands.
- **Drills**: one `h3` per drill (the tutor panel puts its rung box after each `h3`), with: the
  pattern in one sentence, a link to the stub, the time box, and rungs 1 to 3 of the ladder as
  `details.hint` blocks ("Rung 1: where to look", "Rung 2: the idea in words", "Rung 3: the shape").
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
