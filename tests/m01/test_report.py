"""M5: render_report and the program. Run: uv run pytest tests/m01/test_report.py"""

import io
import re
import subprocess
import sys

import numpy as np
from rich.console import Console

from llm101.bench.report import render_report
from llm101.bench.timing import Report, Timings

# A fixed benchmark: 500 calls between 1.0 and 1.5 ms, and a tail of three slow ones.
WALL = [1_000_000 + 10_000 * (i % 50) for i in range(500)] + [9_000_000, 12_000_000, 20_000_000]
TIMINGS = Timings(wall_ns=WALL, cpu_ns=[w // 2 for w in WALL])
REPORT = Report(
    n=len(WALL),
    mean_ns=float(np.mean(WALL)),
    min_ns=min(WALL),
    p50_ns=float(np.percentile(WALL, 50)),
    p95_ns=float(np.percentile(WALL, 95)),
    p99_ns=float(np.percentile(WALL, 99)),
    max_ns=max(WALL),
    throughput_per_s=len(WALL) / (sum(WALL) / 1e9),
    cpu_share=0.5,
)


def printed(renderable, width=200):
    """What rich prints for renderable, as plain text, without writing to the screen."""
    console = Console(file=io.StringIO(), record=True, width=width, color_system=None)
    console.print(renderable)
    return console.export_text()


def expected_bars(bins, bar_width):
    counts = [int(c) for c in np.histogram(WALL, bins=bins)[0]]
    largest = max(counts)
    return [max(1, round(c / largest * bar_width)) for c in counts if c > 0]


def test_render_report_returns_it_and_prints_nothing(capsys):
    renderable = render_report(REPORT, TIMINGS)
    assert capsys.readouterr().out == "", "render_report returns the report; the caller prints it"
    printed(renderable)


def test_render_report_shows_the_numbers_that_matter():
    text = printed(render_report(REPORT, TIMINGS)).lower()
    for label in ("p50", "p95", "p99", "throughput"):
        assert label in text
    assert str(REPORT.n) in text


def test_render_report_draws_one_bar_per_bin_that_is_not_empty():
    text = printed(render_report(REPORT, TIMINGS, bins=10, bar_width=40))
    bars = [len(run) for run in re.findall("█+", text)]
    assert bars == expected_bars(10, 40)


def test_render_report_the_fullest_bin_gets_the_full_width():
    text = printed(render_report(REPORT, TIMINGS, bins=5, bar_width=25))
    bars = [len(run) for run in re.findall("█+", text)]
    assert max(bars) == 25
    assert bars == expected_bars(5, 25)


def report_of(wall):
    """A Report for a list of wall times, worked out with numpy."""
    return Report(
        n=len(wall),
        mean_ns=float(np.mean(wall)),
        min_ns=min(wall),
        p50_ns=float(np.percentile(wall, 50)),
        p95_ns=float(np.percentile(wall, 95)),
        p99_ns=float(np.percentile(wall, 99)),
        max_ns=max(wall),
        throughput_per_s=len(wall) / (sum(wall) / 1e9),
        cpu_share=1.0,
    )


def test_render_report_rounds_half_a_character_the_way_round_does():
    # Three bins of 16, 5 and 1 calls, 40 characters wide: 40, then 5/16 of 40 = 12.5, then
    # 1/16 of 40 = 2.5. round() takes a half to the even neighbour, so the bars are 40, 12 and 2.
    wall = [1_000] * 16 + [2_000] * 5 + [3_000]
    timings = Timings(wall_ns=wall, cpu_ns=wall)
    text = printed(render_report(report_of(wall), timings, bins=3, bar_width=40))
    bars = [len(run) for run in re.findall("█+", text)]
    assert bars == [40, 12, 2], (
        "a bar of 12.5 characters is round(12.5), which is 12, and 2.5 is 2 (see the docstring)"
    )


def test_the_program_prints_a_report():
    command = [sys.executable, "-m", "llm101.bench", "--n", "30", "--warmup", "2", "--bins", "5"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    assert "p99" in result.stdout.lower()
    assert "█" in result.stdout
