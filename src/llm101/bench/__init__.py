"""Module 1, measure first: the benchmark harness you will reuse for the rest of the course.

The contract (see modules/01-measure/README.md). Names, signatures, docstrings and the two
dataclasses are given; the bodies are yours.

    timing.py   time_calls, summarise, and the Timings and Report dataclasses
    stats.py    quickselect, percentile, histogram
    report.py   render_report
    lines.py    slowest_lines
    __main__.py main: `uv run python -m llm101.bench`
"""

from llm101.bench.lines import slowest_lines
from llm101.bench.report import render_report
from llm101.bench.stats import histogram, percentile, quickselect
from llm101.bench.timing import Report, Timings, summarise, time_calls

__all__ = [
    "Report",
    "Timings",
    "histogram",
    "percentile",
    "quickselect",
    "render_report",
    "slowest_lines",
    "summarise",
    "time_calls",
]
