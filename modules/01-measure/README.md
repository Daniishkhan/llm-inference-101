# 01-measure: Measure first

**Module 1** (from Mon 16 Nov 2026) · Phase 1, one model, one request · Book:
[docs/book/01-measure](../../docs/book/01-measure/index.html), build chapter:
[8 Build the harness](../../docs/book/01-measure/08-build-the-harness.html)

> **A draft for the spec ritual.** Read it on day 1, settle the decisions at the end, and freeze it
> with a commit (`Module 1: spec frozen`). After that, a requirement can only move to "Stretch", in
> writing, with the date.

## Concept

One timing is an anecdote. A benchmark calls a function many times and times every call with two
clocks: the **wall clock**, which keeps running while the function waits, and the **CPU clock**, which
runs only while it computes. Then it summarises the spread. **p50** is the typical call; **p95** and
**p99** are the slow tail, the calls a user actually notices. A **histogram** shows the shape of the
spread, and a **line timer** shows where inside a function the time goes. You build all of it by hand,
and every later module measures itself with it.

The Python you meet this module: `time.perf_counter_ns` and `time.process_time_ns`, dataclasses,
closures, `sys.settrace` and frames, `argparse`, rich, pytest and hypothesis.

## The pattern

- **Arrays and hashing.** Your line timer is a dict from line number to seconds. The drills (Group
  Anagrams, the longest streak, and Two Sum and Top K Frequent in the diagnostic) are hashing problems.
- **Selection without sorting.** A percentile is the value at one position of the sorted list, but you
  do not need the whole list sorted to know one position. Quickselect partitions around a pivot and
  throws away the side the answer is not on: about n steps on average, against n log n for sorting. The
  drill `sort_colours` is its partition step.
- [CONCEPTS.md](../../CONCEPTS.md) rows introduced here: every row whose "Introduced" column says M1.
  Reused: none yet; this is the first module.

## In a real engine

- vLLM's serving benchmark (`vllm bench serve`) reports the mean, median and p99 of time to first token
  (TTFT), time per output token and inter-token latency (ITL). Those are your p50 and p99, over a
  different set of timings. Module 12's "Done when" is a p95, and you will measure it with this harness.
- Percentiles over an endless stream (Module 8) need another trick, because you cannot keep every
  timing forever. That is where heaps come in (Find Median from Data Stream).
- Your line timer is a tracing profiler: exact, and slow. A server under load is usually watched with a
  sampling profiler (py-spy, for example), which is cheap and approximate. Chapter 5 explains the
  difference.

## Spec

The program is `python -m llm101.bench`.

| Argument | Meaning | Default |
|---|---|---|
| `--n N` | recorded calls | 1000 |
| `--warmup N` | calls made before recording starts | 50 |
| `--bins N` | histogram bins | 20 |
| `--profile` | after the report, the five slowest lines of `demo()`, with their seconds and source text | off |

Behaviour:

- It benchmarks `demo()` in `src/llm101/bench/__main__.py`, which is given: a little Python and one
  slow line.
- It prints a table: n, min, mean, p50, p95, p99, max, throughput (calls per second) and the CPU
  share, with times in a readable unit.
- Under the table, a histogram of the wall times: one line per bin, a bar of `█` characters, the
  fullest bin 40 characters wide.
- With `--profile`, the five slowest lines of `demo()`.

Example: `uv run python -m llm101.bench --n 2000 --bins 30 --profile`

## The contract

The package is `src/llm101/bench/`. The names, signatures and docstrings are given, and so are the
`Timings` and `Report` dataclasses; the tests call these exact names. **Every docstring is part of the
spec**: it says what to return, what to raise, and what the tests check.

| Function | File | One line |
|---|---|---|
| `time_calls(fn, n, warmup=0) -> Timings` | `timing.py` | Call `fn` `warmup + n` times; wall and CPU nanoseconds of each recorded call |
| `histogram(values, bins) -> (counts, edges)` | `stats.py` | Bins of equal width, exactly as `numpy.histogram` makes them |
| `quickselect(values, k) -> float` | `stats.py` | The k-th smallest value, without sorting |
| `percentile(values, q) -> float` | `stats.py` | numpy's default method, built on your quickselect |
| `summarise(timings) -> Report` | `timing.py` | p50, p95, p99, mean, min, max, throughput, CPU share |
| `render_report(report, timings, bins=20, bar_width=40)` | `report.py` | The table and the histogram, as something rich prints |
| `main(argv=None)` | `__main__.py` | The program |
| `slowest_lines(fn, *args, **kwargs) -> [(line, seconds)]` | `lines.py` | A line timer built on `sys.settrace` |

`stats.py` may not import numpy, and it may not call `sorted()` or `.sort()`; the tests read the file to
check. numpy is the tests' oracle, not your tool.

### Milestones

Do them in order. Each milestone has a book chapter that comes first, so a day is: read the chapter,
then turn its milestone green. The days are a guide, not a deadline.

| Day | | Milestone | Read first | Turns green |
|---|---|---|---|---|
| 1 | **M1** | `time_calls` | ch. 1, Two clocks | `uv run pytest tests/m01 -k time_calls` |
| 2 | **M2** | `histogram` | ch. 2, Tails and percentiles | `tests/m01/test_histogram.py` |
| 3 | **M3** | `quickselect` | ch. 3, Partition and select (drill `sort_colours` first) | `tests/m01/test_quickselect.py` |
| 3 to 4 | **M4** | `percentile` | ch. 2 and 3 | `tests/m01/test_percentile.py`: the first half of "Done when" |
| 4 | **M5** | `summarise`, `render_report` and `main`: the screen | ch. 4, Pictures in the terminal | `-k summarise` and `tests/m01/test_report.py`; then run the program |
| 5 | **M6** | `slowest_lines`, and `--profile` in `main` | ch. 5, Where the time goes | `tests/m01/test_slowest_lines.py`: the second half of "Done when" |
| 6 | **M7** | The Experiment in [BENCH.md](BENCH.md) | ch. 6, Boxes and arrays | BENCH.md has its prediction, measurement and explanation |

Commit after each one: `M1: time_calls green`. Stuck? The hint ladders are in book chapter 8, folded
away. Ask Claude for one rung at a time.

On day one, five tests pass before you type anything: the ones that read your code and check that
`stats.py` neither imports numpy nor sorts, that the two drills `longest_streak` and `sort_colours`
do not sort, and that the drill `tidy_path` does not import a path library. They pass because the
stubs do nothing; they are there to stay green.

## Done when

goal.md: *its percentiles match numpy's on random data, and its profile points to the right slow line
in a test function.*

- [ ] `test_done_when_percentiles_match_numpy_on_random_data` and the rest of `test_percentile.py` are
      green.
- [ ] `test_done_when_it_names_the_slow_line_of_a_test_function` and the rest of
      `test_slowest_lines.py` are green.
- [ ] `uv run pytest tests/m01` is green from end to end.
- [ ] `uv run python -m llm101.bench --profile` prints the table, the histogram and the slowest lines.
- [ ] [BENCH.md](BENCH.md) has its Experiment: a prediction written before the run, the measurement, and
      two sentences on why.
- [ ] One commit per milestone (M1 to M7), each through the pre-commit hook.
- [ ] A review of the whole module has been run, and its three questions are answered in
      [log.md](../../log.md).
- [ ] Five lines in log.md, and `"m01"` added to `done` under `[tool.llm101]` in `pyproject.toml`.

## Drills this module

- **Day 1:** set 00, [the diagnostic](../../drills/00-diagnostic/README.md): six problems, cold, two
  hours this once.
- **Then set 01**, [arrays and hashing](../../drills/01-arrays-hashing/README.md), six problems:
  `group_anagrams` and `tidy_path` (day 2), `sort_colours` (day 3, before M3), `longest_streak` (day 4),
  `count_stretches` and `free_slots` (day 5). `tidy_path` and `free_slots` are review: they do not say
  which pattern they need. Redos come first every day, and a new problem that does not fit in the hour
  waits for the next drill block.
- **Saturday:** the drill block is a mock round.

## Stretch goals (only after "Done when")

1. **`deep_sizeof(obj)`**: the bytes of an object and of everything it holds, counting a shared object
   once (keep a set of `id()` values). Compare a list of a million floats with a numpy array.
2. **A second line timer on `sys.monitoring`** (new in Python 3.12), and its overhead against your
   `sys.settrace` one, measured with your harness.
3. **`python -m llm101.bench module:function`**: benchmark any function by name.

## Decisions for the spec ritual

Each has a default. Change what you want here, then freeze.

1. **Milestone order**: as above, with the screen at M5. Default: keep.
2. **The quickselect speed test** (ordered input against shuffled): keep it, or move it to stretch.
   Default: keep. It is the test that shows why the pivot matters.
3. **The line timer** on `sys.settrace` (as drafted), or on `sys.monitoring`. Default: `sys.settrace`,
   which the book teaches; the tests are the same for both.
4. **The Experiment (M7)**: "a Python loop against numpy, summing the squares of a million numbers: how
   much faster, and how many bytes per number?", or a question of your own. Default: as drafted.
5. **Times in the table**: a readable unit chosen per value (default), or always milliseconds.

## How to run

```sh
uv run pytest tests/m01 -x                  # stop at the first failure
uv run pytest tests/m01 -k time_calls       # one milestone
uv run python -m llm101.bench               # the program, once M5 is green
uv run python -m llm101.bench --profile     # with the slowest lines, once M6 is green
```

## Files

```
modules/01-measure/README.md   this file: the spec
modules/01-measure/BENCH.md    your numbers (M7)
src/llm101/bench/timing.py     time_calls, summarise; Timings and Report (given)
src/llm101/bench/stats.py      quickselect, percentile, histogram
src/llm101/bench/report.py     render_report
src/llm101/bench/lines.py      slowest_lines
src/llm101/bench/__main__.py   main; demo (given)
tests/m01/                     the tests (given): the spec, in code
```

Every function body in `src/llm101/bench/` is yours. Everything else in this list is given.
