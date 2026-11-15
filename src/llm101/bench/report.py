"""The report on the screen, drawn with rich.

Milestone M5, with summarise (timing.py) and main (__main__.py).
"""

from rich.console import RenderableType

from llm101.bench.timing import Report, Timings


def render_report(
    report: Report, timings: Timings, bins: int = 20, bar_width: int = 40
) -> RenderableType:
    """The report as something rich can print: a table of the numbers, then a histogram.

    Return it; do not print it. The caller prints: Console().print(render_report(report, timings)).

    The table shows n, min, mean, p50, p95, p99, max, the throughput and the CPU share, with times
    in a readable unit (ns, µs, ms or s; how you choose is up to you). Its labels include the words
    p50, p95, p99 and throughput.

    The histogram is of the wall times, from your histogram(timings.wall_ns, bins): one line per
    bin, in order. A line shows where its bin starts, a bar of full-block characters "█", and the
    bin's count. The fullest bin's bar is bar_width characters long. Every other bin's bar is
    round(count / largest_count * bar_width) characters, but never fewer than 1 when the count is
    not zero. An empty bin has no bar.
    """
    raise NotImplementedError("TODO(you)")
