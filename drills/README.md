# Drills

Classic problems by pattern, from the table at the end of [goal.md](../goal.md), each set in Claude's
own words. One problem is a stub (`name.py`, whose function raises `NotImplementedError`) and its tests
(`test_name.py`, beside it). The rules (hands only, time boxes, out loud, the ledger and its redos) are
in [docs/methodology.md](../docs/methodology.md), "Drills and the ledger".

| Set | Pattern | Module | Problems |
|---|---|---|---|
| [00-diagnostic](00-diagnostic/README.md) | Mixed: a cold measurement of where you are | Day 1 | run_length, top_endpoints, pair_with_sum, balanced, merge_intervals, moving_average |
| [01-arrays-hashing](01-arrays-hashing/README.md) | Arrays and hashing; the partition behind quickselect | 1 | group_anagrams, longest_streak, sort_colours |

```sh
uv run pytest drills/01-arrays-hashing/test_sort_colours.py    # one problem
uv run pytest drills/01-arrays-hashing                         # a whole set
```

Drills never run in CI: a redo empties a function, and that is meant to be red.

## Katas

An engine kata is a function of a finished module, typed again cold in 30 to 45 minutes
([docs/methodology.md](../docs/methodology.md), "Engine katas"). Its stub and tests go in
`drills/katas/`, and Claude prepares them when the module is done. There are none yet.
