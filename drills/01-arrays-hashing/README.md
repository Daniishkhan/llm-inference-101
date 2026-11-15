# Set 01: arrays and hashing, and the partition

Module 1's drills. goal.md's "Practise" line for the module is *arrays and hashing; quickselect, for
percentiles*. Two of the three arrays-and-hashing problems in goal.md's table are already in set 00:
`pair_with_sum` is Two Sum, and `top_endpoints` is Top K Frequent Elements on an access log. This set
adds Group Anagrams, a streak that needs a set to be linear, and the three-way partition that the
module's quickselect (M3) is built on.

| # | Problem | Stub | Time box | When |
|---|---|---|---|---|
| 1 | Group the anagrams | `group_anagrams.py` | 25 min | Day 2 |
| 2 | Sort three colours in one pass | `sort_colours.py` | 25 min | Day 3, before M3 |
| 3 | The longest streak | `longest_streak.py` | 30 min | Day 4 |

The rest of each day's drill block is the redos that the ledger says are due.

```sh
uv run pytest drills/01-arrays-hashing/test_group_anagrams.py
```

Two of these tests read your code: `longest_streak` and `sort_colours` fail if they call `sorted()` or
`.sort()`. The point of both is to do without.

After each problem: its row in [the ledger](../../ledger.md), and a commit if it is green.
