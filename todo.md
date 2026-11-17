# To do next

The plan is [goal.md](goal.md) and the routine is [docs/methodology.md](docs/methodology.md). This file
holds only the next steps, in order. Tick a box when it is done, and delete a section when it is empty.

## Week 1: Module 1, Mon 16 to Sat 21 Nov 2026

The day-by-day table of [chapter 0](docs/book/01-measure/00-start-here.html), as boxes. Each day runs
the five blocks in order ([docs/methodology.md](docs/methodology.md), "The day"). Block 2, the private
hour, lives outside this repository every day, so it is not listed. In every read block, cover and
retype each program, try each Try it before you open its answer, and answer Check yourself before you
open the answers. In every drill block, redos come first, and every attempt gets a row in
[ledger.md](ledger.md) and, when green, a commit with its minutes (`run_length: 11 min, no hints`).

### Mon 16 Nov: day 1

- [ ] Before block 1: `uv run pytest -q tests/m01 drills/00-diagnostic drills/01-arrays-hashing` ends
      with `201 failed, 5 passed`. The red is the module; the
      five green tests read your code, and they stay green. `uv sync` and the pre-commit hook are
      already done in this clone (on a new clone, run `uv sync` and `tools/install-hooks.sh` first).
      Open the book with `uv run python tools/serve-book.py`, at http://localhost:8767.
- [ ] Block 1, 2 h 20 this once. The spec ritual, 20 minutes: read
      [the Module 1 spec](modules/01-measure/README.md), settle its six "Decisions for the spec
      ritual", write them on the "Spec ritual" line of [log.md](log.md), and commit
      `Module 1: spec frozen`.
- [ ] Then set 00, [the diagnostic](drills/00-diagnostic/README.md), cold and in order: `run_length`
      (15 min), `top_endpoints` (20), `pair_with_sum` (20), `balanced` (15), `merge_intervals` (25),
      `moving_average` (20). Every lookup goes in log.md's "Diagnostic" list. The redos fall due on
      Wed 18 and Mon 23 Nov. Then ask Claude for the review.
- [ ] Block 3: chapter 0, Start here (5 questions), and chapter 1, Two clocks (11 programs, 4 Try its,
      8 questions).
- [ ] Block 4, 2 h today: M1 `time_calls`, with chapter 8's "Milestone 1".
      `uv run pytest tests/m01 -k time_calls` turns green; commit `M1: time_calls green`.
- [ ] Block 5: the review, five lines under "Mon 16 Nov 2026" in log.md, and five rows of
      [CONCEPTS.md](CONCEPTS.md) out loud. For tomorrow: chapter 7's "How the drills work", "The
      order of this module" and "Grouping by a key into a dict of lists".

### Tue 17 Nov: day 2

- [ ] Block 1: a warm-up on yesterday's lookups. Then `group_anagrams` (25 min) and `tidy_path`
      (25 min, a review drill: name its pattern in the ledger afterwards). Their redos fall due on
      Thu 19 and Tue 24 Nov.
- [ ] Block 3: chapter 2, Tails and percentiles (11 programs, 3 Try its, 8 questions).
- [ ] Block 4: M2 `histogram`. `uv run pytest tests/m01/test_histogram.py`; commit
      `M2: histogram green`.
- [ ] Block 5: the review, the log, five CONCEPTS rows. For tomorrow's redos: chapter 7's section for
      each diagnostic problem that was not green inside its time box, and "The three piles of a
      partition".

### Wed 18 Nov: day 3

- [ ] Block 1, 1 h 30 today (decision 6 of the spec): the six redos of set 00, then `sort_colours`
      (25 min), the partition step that M3 builds on. Its redos fall due on Fri 20 and Wed 25 Nov.
- [ ] Block 3: chapter 3, Partition and select (15 programs, 3 Try its, 6 questions).
- [ ] Block 4, 2 h 30 today: M3 `quickselect`. `uv run pytest tests/m01/test_quickselect.py`; commit
      `M3: quickselect green`. Then start M4 `percentile`.
- [ ] Block 5: the review, the log, five CONCEPTS rows, and chapter 7's "A set for constant-time
      membership" for tomorrow. The Wednesday check: compare the milestones done with chapter 0's
      table. If you are behind by more than one, decide tonight
      ([docs/methodology.md](docs/methodology.md), "When a module runs long").

### Thu 19 Nov: day 4

- [ ] Block 1: the redos of `group_anagrams` and `tidy_path`, then `longest_streak` (30 min). Its
      redos fall due on Sat 21 and Thu 26 Nov.
- [ ] Block 3: chapter 4, Pictures in the terminal (17 programs, 3 Try its, 7 questions).
- [ ] Block 4: finish M4. `uv run pytest tests/m01/test_percentile.py` is the first half of "Done
      when"; commit `M4: percentile green`. Then M5: `summarise`, `render_report` and `main`.
      `uv run pytest tests/m01 -k summarise` and `uv run pytest tests/m01/test_report.py`, then look at
      `uv run python -m llm101.bench --n 300 --bins 15`; commit `M5: the report on screen`.
- [ ] Block 5: the review, the log, five CONCEPTS rows, and chapter 7's "A running total" for
      tomorrow (with "Remembering what you have seen", if you have not read it yet).

### Fri 20 Nov: day 5

- [ ] Block 1: the `sort_colours` redo, then `count_stretches` (35 min), then `free_slots` (30 min, a
      review drill) if the hour allows; otherwise it waits for Monday. Their +2 redos fall on Sunday,
      so they move to Mon 23 Nov; the +7 redos fall due on Fri 27 Nov.
- [ ] Block 3: chapter 5, Where the time goes (11 programs, 3 Try its, 7 questions).
- [ ] Block 4: M6 `slowest_lines`, and `--profile` in `main`.
      `uv run pytest tests/m01/test_slowest_lines.py` is the second half of "Done when"; then
      `uv run python -m llm101.bench --n 100 --profile`; commit `M6: slowest_lines green`.
- [ ] Block 5: the review, the log, five CONCEPTS rows.

### Sat 21 Nov: day 6

- [ ] Block 1: the `longest_streak` redo, then the mock round: say "mock" to Claude Code. This week
      the mock is a drill ([docs/methodology.md](docs/methodology.md), "The day").
- [ ] Block 3: chapter 6, Boxes and arrays (12 programs, 3 Try its, 7 questions).
- [ ] Block 4: M7, the Experiment in [BENCH.md](modules/01-measure/BENCH.md). Write the prediction and
      commit it (`M7: prediction`) before any run; then measure, explain, and commit
      `M7: the Experiment`.
- [ ] Block 5: the review; the Check yourself of chapters 7 and 8; and, with Claude, the first row of
      the readiness table at the foot of [ledger.md](ledger.md).

### When "Done when" passes

- [ ] Add `"m01"` to `done` in `pyproject.toml`, set Module 1 to done in the README, write the
      "Module 1 done" lines in log.md, and ask for the review of the whole module.

### Mon 23 Nov: what the week leaves

- [ ] Block 1 holds eight redos: set 00's six at +7 days, and Friday's two, moved from Sunday. They
      come first; `free_slots`, if it waited, comes after them.

## When Module 1 is done

- [ ] Decide the first row of [docs/parking-lot.md](docs/parking-lot.md): the live tutor in the book.
- [ ] Ask Claude for Module 1's katas.
- [ ] Module 2's spec ritual. The draft is written ahead: the spec
      ([modules/02-tokenizer/README.md](modules/02-tokenizer/README.md)), the stubs, the tests, set 02
      (six problems, a debugging drill and six Write its) and the book. Settle its six decisions, write
      them in log.md, and commit `Module 2: spec frozen`; Claude changes the material to match the same
      morning. One sitting of about an hour: the README, the book's chapter 00 and chapter 7's "How the
      drills work" and "Following links" first, then the twenty-minute ritual. Day 1's read block holds
      chapter 01 alone.

## Before the module that needs it

- [ ] Before Module 5: set up the Raspberry Pi (ssh, uv, Python 3.13, a clone of this repository), and
      record its model and memory in [docs/setup.md](docs/setup.md).
- [ ] After Module 5: goal.md may be reopened, and the second row of the parking lot is decided.
- [ ] After Module 6: write-up 1, in [notes/](notes/README.md).
- [ ] From Module 7 on: every Friday, 30 minutes on one merged pull request in vLLM.
- [ ] Before Module 8: rent a GPU for one hour and start vLLM on it once, so that the module does not
      begin with setting up an account. Record the card and its price in docs/setup.md.
- [ ] After Module 8: write-up 2.
