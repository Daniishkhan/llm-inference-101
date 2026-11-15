# Methodology: how a day and a module run

The plan is [goal.md](../goal.md); the tutor's rules are [CLAUDE.md](../CLAUDE.md). This page is the
routine that carries both. It changes only between modules, with a dated line at the bottom.

## The day (8 hours, Monday to Saturday)

goal.md's session has four steps: drill, build, measure, log. The day keeps them in that order and
puts two more blocks between them: one private hour that lives outside this repository, and the
reading that feeds the build.

| Block | Length | What |
|---|---|---|
| **1. Drill** | 1 h | Redos due in the [ledger](../ledger.md) first, then one or two new problems on the module's pattern. Typed by hand, timed, said out loud |
| **2. Private** | 1 h | Kept in `../interview-prep`, outside this repository. It comes second so that it is never the block that gets skipped |
| **3. Read** | 1 h 30 | Today's book chapter. Every example is typed into `scratch/` and run, not copied. Check-yourself questions are answered before the answers are opened |
| **4. Build** | 3 h | The day's milestone, red to green. No Claude in this block except to decode an error message |
| **5. Measure, review, log** | 1 h 30 | Run the measurement (from Module 2 on, with your Module 1 harness), commit, ask for the review, five lines in [log.md](../log.md), five rows of [CONCEPTS.md](../CONCEPTS.md) out loud |

- **Sunday is off, every week.** Eight hours a day only holds with one day that is not part of it.
- **An appointment that cannot move replaces whichever block it lands on.**
- **Saturday's drill block is a mock round**: say "mock" and Claude interviews you on a fresh problem
  from a pattern you have already done (CLAUDE.md, "Mock rounds").
- **Stop the build block on time**, even mid-bug. Write the bug down in log.md and come back tomorrow.
  Bugs you sleep on are faster.

## A module, start to finish

1. **The spec ritual (20 minutes, before the module starts).** Claude drafts the module's README: the
   concept, the pattern, where a real engine does it, the spec, the contract, the milestones, "Done
   when", stretch goals and a short list of *decisions for the spec ritual*. You read it, settle each
   decision, and freeze it with a commit (`Module 2: spec frozen`). Claude then writes the stubs, the tests
   and the book to the frozen spec. (Module 1 is the exception: its material exists before its ritual,
   so that you could start on day one. Anything the ritual changes, Claude changes the same morning.)
2. **Read and build**, milestone by milestone, in the order the README gives.
3. **Measure.** Each module's `BENCH.md` has an Experiment: a prediction written *before* the run, the
   measurement, and two sentences on why. A surprised prediction is worth more than a confirmed one.
4. **Done when.** When the README's "Done when" passes: add the module to `done` under `[tool.llm101]`
   in `pyproject.toml`, so that CI keeps its tests green from then on; set its row in the README to done;
   write the module's five lines in log.md; ask for the review of the whole module.
5. **Then the next module's spec ritual.** Not before: material is written one module ahead, never more.

After the ritual the spec is frozen. You may *reduce* scope later by moving a requirement to "stretch",
in writing, with the date. You may not quietly redefine what "done" means, and Claude may only propose
such a move.

## Red, green, commit

Work one test at a time, in the milestone order the README gives you:

```sh
uv run pytest tests/m01 -x                  # stop at the first failure
uv run pytest tests/m01 -k quickselect      # only the tests whose name contains "quickselect"
```

Read the first failing message. Make only that one pass. Run again. Commit at every green milestone with
a message that names it (`M1: quickselect green`). The pre-commit hook refuses a commit whose files are
not formatted (`uv run ruff format <file>` fixes that) or fail the lint check. A module with seven
commits that each turn a milestone green is the record a reviewer wants to see.

## When you are stuck in the build

1. Re-read the test that fails and the docstring of the function in the stub.
2. Reproduce the smallest version of the problem in `scratch/`.
3. Ask Claude for **one rung** of the hint ladder, and say which rung you are on. The build chapter of
   each book also has the rungs for every milestone, folded away.
4. Only after the tests are green, ask for a review.

## Drills and the ledger

The drills are the classic problems from the patterns table in goal.md, set in Claude's own words, each
a stub and a test file in `drills/<set>/`. Each module's README names its set.

1. **Hands only.** Nothing writes code but you: no agent, no completion, no paste. Looking up syntax in
   the Python docs is allowed and gets written down; the list of lookups is the next morning's warm-up.
2. **Time boxes.** Easy 20 minutes, medium 35, unless the stub says otherwise. At the bell, ask for one
   rung or log a timeout.
3. **Out loud.** Say what you are doing while you solve. An interview is graded on what the interviewer
   hears.
4. **The ledger.** Every attempt gets a row in [ledger.md](../ledger.md): minutes, rungs, lookups,
   result (`green`, `green+hint` or `timeout`).
5. **Redos.** Two days and seven days after the first attempt, empty the function (git keeps your first
   version) and type it again, cold. A problem you cannot redo is not solved yet.
6. **A timeout has no reveal.** The problem stays open and comes back at the +2 day redo, with the rungs
   you have not used yet.
7. **One commit per solved drill**, with the minutes in the message: `pair_with_sum: 11 min, no hints`.

Drills never run in CI: a redo empties a function, and that is meant to be red.

## The review ritual

After each milestone, or at least once a day, and for the whole module at its end: commit first, then
ask Claude for the review (CLAUDE.md, "What a review contains": correctness, complexity, clarity, idioms,
performance, the real engine, three questions). Write the three questions and your answers into log.md.
Do not act on review notes before the next build block; let them settle.

## The log

[log.md](../log.md) holds, per session, five lines in your own words on what surprised you, and per
module, the measurement in one line and five lines on the module. Blockers and dated scope changes go in
the module's section. Two honest lines written at the end of the day beat a paragraph written on Sunday.

## Spaced retrieval

Memory needs retrieval, not re-reading. In block 5, pick five rows of [CONCEPTS.md](../CONCEPTS.md)
whose status is `in progress` or `owned`, cover the table, and explain each out loud in two sentences
with one concrete example. A row you cannot explain is marked `rusty` and goes to the front of tomorrow's
read block. Rows move to `owned` only after they have been used in a module *and* explained in a review.

## When a module runs long

A module is done when "Done when" passes, not when the week ends. The week is still the yardstick:

1. **Wednesday evening**, check the milestone list. Behind by more than one milestone? Decide now, not
   on Saturday.
2. First lever: move the stretch goals out of the module entirely.
3. Second lever: move one requirement that is not part of "Done when" to "stretch", in writing, dated,
   in the README and in log.md.
4. Never: paste a solution, weaken a test, skip the measurement or the log, or drop a "Done when".

A slow module with green tests and an honest log is a success. A fast one with pasted code is a failure
that looks like success until someone asks you to explain it.

## Reading reference code

nano-vLLM, vLLM, SGLang, tiktoken and Hugging Face transformers exist to be *checked against*: tests use
them to know **what** the answer must be, never to show **how** to write it. Read their source for a
piece only after your own version of that piece passes its tests, and then write in log.md what they did
better. Phase 3 is reading vLLM on purpose, and it comes after you have built your own engine.

---

*Changelog:* 2026-11-15 first version, from cpp-101's methodology (spec ritual, red-green-commit,
review, retrieval, slips) and interview-prep's rules (hands only, time boxes, the ledger and its redos,
mock rounds, the private block).
