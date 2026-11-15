"""M1 (time_calls) and M5 (summarise).

One milestone at a time: uv run pytest tests/m01 -k time_calls
"""

import ast
import inspect
import math
import time

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from llm101.bench.timing import Timings, summarise, time_calls

# ---------------------------------------------------------------------------- M1: time_calls


def test_time_calls_records_n_calls():
    timings = time_calls(lambda: None, n=7)
    assert len(timings.wall_ns) == 7
    assert len(timings.cpu_ns) == 7


def test_time_calls_calls_fn_warmup_plus_n_times():
    calls = []
    time_calls(lambda: calls.append(1), n=5, warmup=3)
    assert len(calls) == 8


def test_time_calls_records_whole_nanoseconds():
    timings = time_calls(lambda: sum(range(100)), n=10)
    for value in timings.wall_ns + timings.cpu_ns:
        assert isinstance(value, int)
        assert value >= 0


def test_time_calls_does_not_record_the_warmup_calls():
    calls = []

    def slow_at_first():
        calls.append(1)
        if len(calls) <= 3:
            time.sleep(0.05)

    timings = time_calls(slow_at_first, n=5, warmup=3)
    assert max(timings.wall_ns) < 25_000_000, "a 50 ms warm-up call was recorded"


def test_time_calls_records_the_calls_in_order():
    calls = []

    def slower_each_time():
        calls.append(1)
        time.sleep(0.01 * len(calls))  # 10, 20, 30, 40 ms: far enough apart to stay in order

    timings = time_calls(slower_each_time, n=4)
    assert timings.wall_ns == sorted(timings.wall_ns)


def test_time_calls_wall_time_includes_waiting():
    timings = time_calls(lambda: time.sleep(0.005), n=5)
    assert min(timings.wall_ns) >= 4_000_000, "each call slept for about 5 ms"


def test_time_calls_a_sleeping_function_uses_little_cpu():
    timings = time_calls(lambda: time.sleep(0.005), n=10)
    assert sum(timings.cpu_ns) < 0.2 * sum(timings.wall_ns)


def test_time_calls_a_busy_function_uses_cpu_most_of_the_time():
    timings = time_calls(lambda: sum(range(300_000)), n=10)
    assert sum(timings.cpu_ns) > 0.5 * sum(timings.wall_ns)


def test_time_calls_reads_the_two_clocks_its_docstring_names():
    # Names used in the code itself; the docstring is a string, so it does not count.
    tree = ast.parse(inspect.getsource(time_calls))
    used = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
    used |= {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert "perf_counter_ns" in used
    assert "process_time_ns" in used


@pytest.mark.parametrize(("n", "warmup"), [(0, 0), (-1, 0), (5, -1)])
def test_time_calls_rejects_bad_counts(n, warmup):
    with pytest.raises(ValueError):
        time_calls(lambda: None, n=n, warmup=warmup)


# ----------------------------------------------------------------------------- M5: summarise


def test_summarise_the_docstring_example():
    report = summarise(Timings(wall_ns=[1_000_000, 3_000_000], cpu_ns=[1_000_000, 1_000_000]))
    assert report.n == 2
    assert report.min_ns == 1_000_000
    assert report.max_ns == 3_000_000
    assert report.mean_ns == pytest.approx(2_000_000.0)
    assert report.p50_ns == pytest.approx(2_000_000.0)
    assert report.p95_ns == pytest.approx(2_900_000.0)
    assert report.p99_ns == pytest.approx(2_980_000.0)
    assert report.throughput_per_s == pytest.approx(500.0)
    assert report.cpu_share == pytest.approx(0.5)


@given(st.lists(st.integers(1, 10**9), min_size=1, max_size=300))
def test_summarise_matches_numpy_on_random_timings(wall):
    cpu = [w // 2 for w in wall]
    report = summarise(Timings(wall_ns=wall, cpu_ns=cpu))
    assert report.n == len(wall)
    assert report.min_ns == min(wall)
    assert report.max_ns == max(wall)
    assert report.mean_ns == pytest.approx(float(np.mean(wall)))
    for q, got in [(50, report.p50_ns), (95, report.p95_ns), (99, report.p99_ns)]:
        assert got == pytest.approx(float(np.percentile(wall, q)), rel=1e-9)
    assert report.throughput_per_s == pytest.approx(len(wall) / (sum(wall) / 1e9))
    assert report.cpu_share == pytest.approx(sum(cpu) / sum(wall))


def test_summarise_with_no_time_at_all():
    report = summarise(Timings(wall_ns=[0, 0], cpu_ns=[0, 0]))
    assert report.throughput_per_s == math.inf
    assert report.cpu_share == 0.0


def test_summarise_rejects_empty_timings():
    with pytest.raises(ValueError):
        summarise(Timings(wall_ns=[], cpu_ns=[]))


def test_summarise_uses_your_percentile():
    tree = ast.parse(inspect.getsource(summarise))
    called = {
        getattr(node.func, "id", None) or getattr(node.func, "attr", None)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    }
    assert "percentile" in called, "summarise computes p50, p95 and p99 with your percentile()"
