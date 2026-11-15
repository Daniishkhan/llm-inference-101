"""Timing calls, and summarising the times.

Milestone M1 is time_calls. Milestone M5 is summarise (with render_report in report.py).
"""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Timings:
    """What time_calls measured: one entry per recorded call, in call order, in nanoseconds."""

    wall_ns: list[int]  # wall-clock time of each call, from time.perf_counter_ns()
    cpu_ns: list[int]  # CPU time of each call, from time.process_time_ns()


@dataclass(frozen=True)
class Report:
    """The summary of one benchmark. Times are in nanoseconds; throughput is in calls per second."""

    n: int
    mean_ns: float
    min_ns: int
    p50_ns: float
    p95_ns: float
    p99_ns: float
    max_ns: int
    throughput_per_s: float
    cpu_share: float


def time_calls(fn: Callable[[], object], n: int, warmup: int = 0) -> Timings:
    """Call fn() `warmup` times without recording anything, then `n` times, recording each call.

    Each recorded call is timed twice, around the call and nothing else:

    - wall time with time.perf_counter_ns(): a stopwatch, which keeps running while fn waits;
    - CPU time with time.process_time_ns(): the time this process spent computing.

    fn takes no arguments. To time a call that needs some, wrap it: time_calls(lambda: f(x), 100).
    Whatever fn returns is ignored.

        timings = time_calls(lambda: sum(range(1_000)), n=5)
        len(timings.wall_ns), len(timings.cpu_ns)  ->  (5, 5)

    Raises ValueError if n < 1 or warmup < 0.
    """
    raise NotImplementedError("TODO(you)")


def summarise(timings: Timings) -> Report:
    """Summarise one benchmark: the spread of its wall times, its throughput and its CPU share.

    - n: the number of recorded calls.
    - mean_ns, min_ns, max_ns: of the wall times.
    - p50_ns, p95_ns, p99_ns: percentiles of the wall times, computed with your percentile().
    - throughput_per_s: recorded calls per second of wall time, n / (total wall time in seconds).
    - cpu_share: total CPU time / total wall time. Busy work gives about 1, waiting about 0.

    If the total wall time is 0, throughput_per_s is math.inf and cpu_share is 0.0.

        summarise(Timings(wall_ns=[1_000_000, 3_000_000], cpu_ns=[1_000_000, 1_000_000]))
            ->  Report(n=2, mean_ns=2000000.0, min_ns=1000000, p50_ns=2000000.0, p95_ns=2900000.0,
                       p99_ns=2980000.0, max_ns=3000000, throughput_per_s=500.0, cpu_share=0.5)

    Raises ValueError if there are no timings.
    """
    raise NotImplementedError("TODO(you)")
