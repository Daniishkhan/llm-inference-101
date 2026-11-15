# Set 02: heaps and linked lists

Module 2's drills. goal.md's "Practise" line for the module is *hash maps (pair counts), heaps (best
merge first), linked lists (merging in place)*. Hash maps were set 01's pattern, so this set gives its
four pattern problems to the other two: two on linked lists, two on heaps.

A set has six problems: four on the module's pattern, and two for review. A review problem does not
say which pattern it needs. Naming it is part of the drill, and the name goes in the ledger's Pattern
column. The set also has one debugging drill.

| Drill | Problem | Stub | Time box | When |
|---|---|---|---|---|
| 02-1 | Turn a linked list around | `reverse_list.py` | 20 min | Day 1, if the redos leave room (read chapter 7's "Following links" before day 1, with the spec) |
| 02-2 | Merge two sorted linked lists | `merge_two_lists.py` | 20 min | Day 2 |
| 02-5 | How many days until it is warmer? (review) | `days_to_wait.py` | 30 min | Day 2 |
| 02-3 | The k largest values | `k_largest.py` | 25 min | Day 3 |
| 02-4 | Merge many sorted runs | `merge_sorted_runs.py` | 35 min | Day 4 |
| 02-7 | The print queue (debugging) | `print_queue.py` | 20 min | Day 5 |
| 02-6 | The longest stretch that ends in a draw (review) | `longest_draw.py` | 35 min | Day 5, if the hour allows |

**Redos come first, every day.** This week starts with eight of them from Module 1 (set 00's six at +7
days, and two of set 01's), and set 01's +7 redos fall due on days 2 to 5. A new problem that does not
fit in the hour waits for the next drill block. A redo is never skipped to make room for a new problem.

**The debugging drill** is a finished program with a fault: some of its tests fail. Find the fault, say
in one sentence why it is one, and fix it with the smallest change you can. It gets one ledger row
(the Pattern column holds what the fault was) and no redos.

```sh
uv run pytest drills/02-heaps-lists/test_reverse_list.py
```

Three of these test files read your code: `k_largest` fails if it calls `sorted()`, `.sort()`,
`heapq.nlargest` or `heapq.nsmallest`, `merge_sorted_runs` if it calls `sorted()`, `.sort()` or
`heapq.merge`, and `merge_two_lists` if it calls `sorted()` or `.sort()`. Each of those tests calls your function first, so it is red until the function works.
Four time your function on a long input and stop it after two seconds (`k_largest`,
`merge_sorted_runs`, `days_to_wait` and `longest_draw`). The linked-list tests check
that you reused the nodes you were given.

## Write it: one short function per chapter

From Module 2 on, each concept chapter of the book ends with a **Write it**: a function of about ten
lines on that chapter's mechanism, written from the empty stub in ten minutes. Each gets one ledger
row (set `02w`) and no redos.

| Chapter | Write it | Stub |
|---|---|---|
| 1 Bytes and UTF-8 | Count the characters in UTF-8 bytes without decoding them | `warmups/count_characters.py` |
| 2 Pairs and merges | The busiest hour of a day of requests | `warmups/busiest_hour.py` |
| 3 Encoding by rank | Turn a lookup table around | `warmups/invert_table.py` |
| 4 GPT-2's tokenizer | Read a palette of colours from a JSON file | `warmups/read_palette.py` |
| 5 Heaps and linked lists | The next job off a heap, skipping the cancelled ones | `warmups/next_alive.py` |
| 6 Tokens as cost | How much of a conversation fits in a context window | `warmups/messages_that_fit.py` |

```sh
uv run pytest drills/02-heaps-lists/warmups/test_count_characters.py
```

After each problem: its row in [the ledger](../../ledger.md), and a commit if it is green.
