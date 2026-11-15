"""M6: slowest_lines, and the second half of "Done when".

Run: uv run pytest tests/m01/test_slowest_lines.py

The functions below are the patients. Each marks its slow line with a comment, and the tests find
that line's number by reading the source.
"""

import inspect
import random
import subprocess
import sys

import pytest

from llm101.bench.lines import slowest_lines

DATA = list(range(200_000))
random.Random(0).shuffle(DATA)
SMALL = DATA[:20_000]


def line_of(fn, marker):
    lines, start = inspect.getsourcelines(fn)
    for offset, text in enumerate(lines):
        if marker in text:
            return start + offset
    raise AssertionError(f"no line containing {marker!r} in {fn.__name__}")


def source_lines_of(fn):
    lines, start = inspect.getsourcelines(fn)
    return set(range(start, start + len(lines)))


def one_slow_line():
    small = 1
    big = sorted(DATA)  # the slow line
    total = small + 1
    return total, len(big)


def helper():
    return sorted(DATA)


def calls_a_slow_helper():
    small = 1
    big = helper()  # the slow line
    return small, len(big)


def many_small_beat_one_big():
    once = sorted(DATA[:50_000])  # once
    for _ in range(10):
        part = sorted(SMALL)  # ten times
    return len(once) + len(part)


def test_done_when_it_names_the_slow_line_of_a_test_function():
    result = slowest_lines(one_slow_line)
    assert result[0][0] == line_of(one_slow_line, "# the slow line")


def test_slowest_lines_lists_the_lines_that_ran_and_no_others():
    body = {
        line_of(one_slow_line, "small = 1"),
        line_of(one_slow_line, "# the slow line"),
        line_of(one_slow_line, "total = small + 1"),
        line_of(one_slow_line, "return total"),
    }
    reported = {line for line, _ in slowest_lines(one_slow_line)}
    assert body <= reported, "every line of the body that ran is listed"
    assert reported <= source_lines_of(one_slow_line), "only lines of one_slow_line itself"


def test_slowest_lines_come_slowest_first():
    seconds = [s for _, s in slowest_lines(many_small_beat_one_big)]
    assert seconds == sorted(seconds, reverse=True)
    assert all(s >= 0 for s in seconds)


def test_slowest_lines_a_callee_counts_toward_the_line_that_called_it():
    result = slowest_lines(calls_a_slow_helper)
    assert result[0][0] == line_of(calls_a_slow_helper, "# the slow line")
    assert not source_lines_of(helper) & {line for line, _ in result}, "helper's own lines appear"


def test_slowest_lines_a_line_in_a_loop_adds_up_its_runs():
    # Ten sorts of 20,000 numbers take longer than one sort of 50,000, but only if all ten count.
    result = slowest_lines(many_small_beat_one_big)
    assert result[0][0] == line_of(many_small_beat_one_big, "# ten times")


def test_slowest_lines_passes_the_arguments_through():
    def add(a, b=0):
        return a + b  # the only line

    result = slowest_lines(add, 2, b=3)
    assert line_of(add, "# the only line") in [line for line, _ in result]


def test_slowest_lines_removes_its_tracer():
    before = sys.gettrace()
    slowest_lines(one_slow_line)
    assert sys.gettrace() is before


class Boom(Exception):
    """An exception of the test's own, so that nothing else can be mistaken for it."""


def test_slowest_lines_removes_its_tracer_when_fn_raises():
    before = sys.gettrace()

    def fails():
        raise Boom()

    with pytest.raises(Boom):
        slowest_lines(fails)
    assert sys.gettrace() is before


def test_the_program_prints_the_slowest_lines_with_profile():
    command = [sys.executable, "-m", "llm101.bench", "--n", "20", "--warmup", "1", "--profile"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    assert result.returncode == 0, result.stderr
    assert "squares = [i * i for i in range(20_000)]" in result.stdout, (
        "the slowest line of demo() and its source text should be in the output. If the line "
        "number is there but the text is not, rich read the square brackets as markup "
        "(book chapter 4)"
    )
