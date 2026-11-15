"""The harness as a program: benchmark a small workload and print the report.

    uv run python -m llm101.bench                  # 1000 calls of demo(), after 50 warm-up calls
    uv run python -m llm101.bench --n 200 --bins 10
    uv run python -m llm101.bench --profile        # also the five slowest lines of demo() (M6)

Arguments, all optional:

    --n N        recorded calls (default 1000)
    --warmup N   calls before recording starts (default 50)
    --bins N     histogram bins (default 20)
    --profile    after the report, print the five slowest lines of demo(): for each, its line
                 number, its seconds and its source text

main is milestone M5 (and --profile is part of M6). demo is given: it is the workload, not the work.
"""


def demo() -> int:
    """The workload that the program measures: a little Python, and one slow line."""
    words = ["token"] * 1_000
    joined = " ".join(words)
    squares = [i * i for i in range(20_000)]
    return len(joined) + sum(squares)


def main(argv: list[str] | None = None) -> None:
    """Read the arguments (argv, or the command line when argv is None), benchmark demo(), and print
    the report; with --profile, print the five slowest lines of demo() after it."""
    raise NotImplementedError("TODO(you)")


if __name__ == "__main__":
    main()
