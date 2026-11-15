# Drills

Classic problems by pattern, from the table at the end of [goal.md](../goal.md), each set in Claude's
own words. One problem is a stub (`name.py`, whose function raises `NotImplementedError`) and its tests
(`test_name.py`, beside it). The rules (hands only, time boxes, out loud, the ledger and its redos) are
in [docs/methodology.md](../docs/methodology.md), "Drills and the ledger".

| Set | Pattern | Module | Problems |
|---|---|---|---|
| [00-diagnostic](00-diagnostic/README.md) | Mixed: a cold measurement of where you are | Day 1 | run_length, top_endpoints, pair_with_sum, balanced, merge_intervals, moving_average |
| [01-arrays-hashing](01-arrays-hashing/README.md) | Arrays and hashing; the partition behind quickselect | 1 | group_anagrams, sort_colours, longest_streak, count_stretches; for review: tidy_path, free_slots |

```sh
uv run pytest drills/01-arrays-hashing/test_sort_colours.py    # one problem
uv run pytest drills/01-arrays-hashing                         # a whole set
```

Drills never run in CI: a redo empties a function, and that is meant to be red.

## What a set holds

From set 01 on, a set has six problems: four on its module's pattern, and two for review that do
not say which earlier pattern they need. From set 02 on it also has one debugging drill: a short
program with a failing test or a slow path, to find, explain and fix in 20 minutes.

## Katas

An engine kata is a function of a finished module, typed again cold in 30 to 45 minutes
([docs/methodology.md](../docs/methodology.md), "Engine katas"). Its stub and tests go in
`drills/katas/`, and Claude prepares them when the module is done. There are none yet.
