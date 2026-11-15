# Set 01: arrays and hashing, and the partition

Module 1's drills. goal.md's "Practise" line for the module is *arrays and hashing; quickselect, for
percentiles*. Two of the three arrays-and-hashing problems in goal.md's table are already in set 00:
`pair_with_sum` is Two Sum, and `top_endpoints` is Top K Frequent Elements on an access log.

A set has six problems: four on the module's pattern, and two for review. A review problem does not
say which pattern it needs. Naming it is part of the drill, and the name goes in the ledger's Pattern
column.

| Drill | Problem | Stub | Time box | When |
|---|---|---|---|---|
| 01-1 | Group the anagrams | `group_anagrams.py` | 25 min | Day 2 |
| 01-5 | Tidy a path (review) | `tidy_path.py` | 25 min | Day 2 |
| 01-3 | Sort three colours in one pass | `sort_colours.py` | 25 min | Day 3, before M3 |
| 01-2 | The longest streak | `longest_streak.py` | 30 min | Day 4 |
| 01-4 | Count the stretches that add up to a target | `count_stretches.py` | 35 min | Day 5 |
| 01-6 | The free slots of a day (review) | `free_slots.py` | 30 min | Day 5 |

**Redos come first, every day.** A new problem that does not fit in the hour waits for the next drill
block, and the last ones of a set may spill into the first days of the next module. A redo is never
skipped to make room for a new problem.

```sh
uv run pytest drills/01-arrays-hashing/test_group_anagrams.py
```

Three of these test files read your code. `longest_streak` and `sort_colours` fail if they call
`sorted()` or `.sort()`, and `tidy_path` fails if its file imports `os`, `posixpath` or `pathlib`. The
point of all three is to do without.

After each problem: its row in [the ledger](../../ledger.md), and a commit if it is green.
