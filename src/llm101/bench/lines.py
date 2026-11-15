"""A line timer: where did the time go, line by line?

Milestone M6. It answers the second half of the module's "Done when".
"""

from collections.abc import Callable


def slowest_lines(
    fn: Callable[..., object], *args: object, **kwargs: object
) -> list[tuple[int, float]]:
    """Run fn(*args, **kwargs) once under a line tracer, and say where its time went, line by line.

    Returns (line number, seconds) for every line of fn's own body that ran, slowest first. Line
    numbers are those of fn's source file. A line that runs many times, in a loop, adds up all its
    runs. Time spent inside a function that fn calls counts toward the line of fn that made the
    call; the callee's own lines are not listed.

    Build it on sys.settrace (book chapter 5). The tracer must be gone when slowest_lines returns,
    and also when fn raises, in which case the exception goes on to the caller.

    What fn returns is not needed.
    """
    raise NotImplementedError("TODO(you)")
