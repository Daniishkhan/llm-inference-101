# BENCH: Module 1, Measure first

Fill this in at M7. Book chapter 6 explains the measurement. The harness you measure with is your own
(M1 to M5).

## The machine

| Date | Machine | Power | Python | numpy |
|---|---|---|---|---|
| | MacBook, Apple M5, 24 GB, macOS 26.7.2 | mains | 3.13.18 | 2.5.4 |

## Experiment

**Question.** Summing the squares of the numbers 0 to 999,999: how much faster is numpy than a Python
loop, and how many bytes does each keep per number?

**Prediction.** Write it before you run anything: a number and a reason.

- numpy is about ___ times faster, because
- a list of a million floats keeps about ___ bytes per number, and a numpy array about ___, because

**Measurement.** With your harness: `time_calls`, then `summarise`, at least 100 recorded calls each.

| What | n | p50 | p95 | p99 | Throughput (calls/s) | CPU share |
|---|---|---|---|---|---|---|
| A Python loop over a list | | | | | | |
| numpy, one vectorised expression | | | | | | |

| What | Bytes in total | Bytes per number | How you measured it |
|---|---|---|---|
| A list of 1,000,000 floats | | | `sys.getsizeof` of the list, plus each float |
| A numpy float64 array of 1,000,000 | | | `.nbytes`, plus `sys.getsizeof` of the array object |

**Explanation.** Two sentences: why the ratio is what it is, and what surprised you.

## The harness on itself (optional)

What does `time_calls` add to every call? Time `lambda: None` and write down its p50: that is the floor
under every number above.
