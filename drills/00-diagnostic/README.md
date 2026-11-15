# Set 00: the diagnostic

Six small problems, cold. The point is a measurement, not a score: how long each one takes today, and
what you had to look up. Week 1 is built from the result.

Rules for the next two hours:

- Zed only, with this project's settings (no predictions, no completion). No agent, no search engine.
- The Python docs are allowed (`python3 -c "help(str.split)"`, or docs.python.org). Write down every
  lookup.
- One problem at a time, in order. Start a timer when you open the stub. Stop it at green or at the time
  box, whichever comes first, and move on. Unfinished is a result too.
- Say what you are doing out loud as you go.

| # | Problem | Stub | Time box |
|---|---|---|---|
| 1 | Run-length encoding | `run_length.py` | 15 min |
| 2 | The busiest endpoints in a log | `top_endpoints.py` | 20 min |
| 3 | Two numbers that add up to a target | `pair_with_sum.py` | 20 min |
| 4 | Balanced brackets | `balanced.py` | 15 min |
| 5 | Merge intervals | `merge_intervals.py` | 25 min |
| 6 | A moving average (a small class) | `moving_average.py` | 20 min |

Run one problem's tests from the repository root:

```sh
uv run pytest drills/00-diagnostic/test_run_length.py
```

After each problem: its row in [the ledger](../../ledger.md), and a commit if it is green. When all six
are done, or two hours have passed, ask Claude for the review.
