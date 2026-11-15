# Methodology: how a day and a module run

The plan is [goal.md](../goal.md); the tutor's rules are [CLAUDE.md](../CLAUDE.md). This page is the
routine that carries both. It changes only between modules, with a dated line at the bottom.

**The plan holds still until Module 5 is done.** Until then goal.md is not reopened: an idea gets one
row in [docs/parking-lot.md](parking-lot.md) with the date on which it is decided, and the day's
block goes on.

## The day (8 hours, Monday to Saturday)

goal.md's session has four steps: drill, build, measure, log. The day keeps them in that order and
puts two more blocks between them: one private hour that lives outside this repository, and the
reading that feeds the build.

| Block | Length | What |
|---|---|---|
| **1. Drill** | 1 h | Redos due in the [ledger](../ledger.md) first, then one or two new problems on the module's pattern. Typed by hand, timed, said out loud |
| **2. Private** | 1 h | Kept in `../interview-prep`, outside this repository. It comes second so that it is never the block that gets skipped |
| **3. Read** | 1 h 30 | Today's book chapter, by cover and retype: read a program, cover it, type it into `scratch/` from memory, then compare and run it. Check-yourself questions are answered before the answers are opened |
| **4. Build** | 3 h | The day's milestone, red to green. No Claude in this block except to decode an error message |
| **5. Measure, review, log** | 1 h 30 | Run the measurement (from Module 2 on, with your Module 1 harness), commit, ask for the review, five lines in [log.md](../log.md), five rows of [CONCEPTS.md](../CONCEPTS.md) out loud |

- **Sunday is off, every week.** Eight hours a day only holds with one day that is not part of it.
- **An appointment that cannot move replaces whichever block it lands on.**
- **Saturday's drill block is a mock round**, and it rotates (CLAUDE.md, "Mock rounds"):
  1. *A drill.* Say "mock" and Claude interviews you on a fresh problem from a pattern you have done.
  2. *An engine kata* ("Engine katas", below).
  3. *From Phase 2 on, an inference system-design round.* Say "mock design". Claude gives a serving
     problem with numbers in it; you talk for 35 minutes: requirements, the arithmetic of capacity, the
     path of one request, what you would measure first.
- **From Module 7 on, Friday's read block gives 30 minutes to one merged pull request** in vLLM
  ("Reading reference code", below).
- **Cover and retype.** Copying a program from the page trains your fingers. Rebuilding it from memory
  trains what an interview asks for. If the read block is running out, type the remaining programs
  with the page open: every program is still typed, and the ones you rebuilt are the ones that count.
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

The drills are the classic problems from the patterns table in goal.md and others like them, set in
Claude's own words, each a stub and a test file in `drills/<set>/`. Each module's README names its set.

**A set has six problems.** Four are on the module's pattern, in rising difficulty. Two are for review:
they use a pattern from an earlier set and do not say which, because an interview does not say either.
Naming the pattern afterwards, in the ledger, is part of those two drills. Six a week, each redone
twice, is about what the drill hour holds: roughly 80 problems by week 13 and 120 by the end.

**From set 02 on, a set also has one debugging drill**: a short program with a failing test or a slow
path. You have 20 minutes to find the fault, say why it is one, and fix it. It gets one ledger row and
no redos.

1. **Hands only.** Nothing writes code but you: no agent, no completion, no paste. Looking up syntax in
   the Python docs is allowed and gets written down; the list of lookups is the next morning's warm-up.
2. **Time boxes.** Easy 20 minutes, medium 35, unless the stub says otherwise. At the bell, ask for one
   rung or log a timeout.
3. **Out loud.** Say what you are doing while you solve. An interview is graded on what the interviewer
   hears.
4. **The ledger.** Every attempt gets a row in [ledger.md](../ledger.md): minutes, rungs, lookups,
   runs, result (`green`, `green+hint` or `timeout`).
5. **Dry-run before you run.** When you think you are done, walk two inputs through your code by hand,
   one of them an edge case. Only then run the tests, and count the runs until green. An interview
   often has no tests to lean on, so the aim is green on the first run.
6. **Redos.** Two days and seven days after the first attempt, empty the function (git keeps your first
   version) and type it again, cold. A problem you cannot redo is not solved yet. A redo that falls on a
   Sunday moves to the Monday.
7. **A timeout has no reveal.** The problem stays open and comes back at the +2 day redo, with the rungs
   you have not used yet.
8. **One commit per solved drill**, with the minutes in the message: `pair_with_sum: 11 min, no hints`.
9. **Redos come first.** A new problem that does not fit in the hour waits for the next drill block,
   and the last ones of a set may spill into the next module's first days. A redo is never skipped to
   make room for a new problem.

Drills never run in CI: a redo empties a function, and that is meant to be red.

## Engine katas

An interview asks in 45 minutes for what a module took you a week to build. A kata closes that gap: a
function you have already finished, typed again from an empty stub, cold.

1. **When.** A module's katas open when the module is done. Claude prepares them then: a stub in
   `drills/katas/` and that function's tests, pointed at the stub. Your finished code in `src/` is not
   touched, so CI stays green.
2. **Time box.** 30 to 45 minutes, said out loud, like a drill.
3. **No hints.** If you are stuck at the bell, log a timeout. Afterwards, and only afterwards, compare
   with your first version in git.
4. **The ledger.** A kata gets a row like any drill, with the set written as `kata m01`, and comes back
   after 2 days and after 7.

## The review ritual

After each milestone, or at least once a day, and for the whole module at its end: commit first, then
ask Claude for the review (CLAUDE.md, "What a review contains": correctness, complexity, clarity, idioms,
performance, the real engine, three questions). Write the three questions and your answers into log.md.
Do not act on review notes before the next build block; let them settle.

## Readiness

Each Saturday, in the review, Claude works out three numbers from the ledger with you and writes them
at its foot:

1. Of your last ten new problems, how many were green inside the time box with no rungs.
2. The median minutes of those ten.
3. Of the redos that fell due this week, how many were green on the first run.

**You are ready for a coding screen** when the first number is 8 or more and at least five of the ten
had a time box of 30 minutes or longer. Until then the numbers say what to work on: rungs point at a
pattern, long minutes at fluency, many runs at checking your own code.

A few weeks before you expect coding screens, add two timed sessions a week on a real interview
platform, in the private block. By then the unfamiliar part is the editor, not the problems.

## Write-ups

goal.md asks for four short pieces, in your own words, in [notes/](../notes/README.md): after Phase 1,
after the GPU baseline in Module 8, after Phase 2 and after Phase 3.

- **Numbers first.** The headline measurement is in the first two sentences, with its machine and date.
  Every number comes from a `BENCH.md`.
- **Under 800 words**, with one table or chart, what surprised you, and what you would measure next.
- **Two hours**, taken from that day's block 5.
- **Claude does not write or rewrite them.** Ask for a check once a draft exists: Claude says where a
  number does not match its `BENCH.md`, where a claim is wrong and where a passage is unclear. You rewrite.

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

**Running** a reference engine is not reading it. Module 8 measures real vLLM from the outside, as a
server you send requests to, before you have built your own batching.

**One merged pull request a week, from Module 7 on.** In Friday's read block, take 30 minutes for one
merged pull request in vLLM, in the area whose tests you have just turned green. Write three lines in
log.md: what it changed, why, and one question you would have asked in review. This is how the pull
request that ends Phase 3 gets found: by the time you choose it in Module 14 you have read a dozen.
That pull request is typed by you. Claude may explain the project's code and its conventions and may
review your diff, and never writes it.

---

*Changelog:* 2026-11-15, after a day-by-day check of week 1: a redo that falls on a Sunday moves to the
Monday. 2026-11-15, after an audit of the lesson structure the same day: a set has six problems,
two of them for review with the pattern not named; a debugging drill from set 02 on; cover and retype
in the read block; a dry run and a count of test runs; three readiness numbers each Saturday; from
Module 2 on, one "write it" exercise and at most eight programs a chapter (docs/book/assets/SPEC.md).
2026-11-15, after the audit of goal.md the same day: the plan holds still until Module 5 is
done; Saturday's mock rotates between a drill, an engine kata and a system-design round; engine katas;
the four write-ups; one merged pull request a week from Module 7 on. 2026-11-15 first version, from cpp-101's methodology (spec ritual, red-green-commit,
review, retrieval, slips) and interview-prep's rules (hands only, time boxes, the ledger and its redos,
mock rounds, the private block).
