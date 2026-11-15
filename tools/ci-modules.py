#!/usr/bin/env python3
"""Run each module's tests and report; fail only for the modules that are done.

This is what the CI `modules` job runs, and you can run it yourself:

    uv run python tools/ci-modules.py

For every tests/mNN folder it runs pytest, counts what passed and failed, and prints a table (also
to $GITHUB_STEP_SUMMARY when CI sets it). It exits with 1 only if a module listed in [tool.llm101]
done in pyproject.toml has a test that fails: an open module's red tests are the expected state
while you work on it, and a done module must stay green.
"""

import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNT = re.compile(r"(\d+) (passed|failed|errors?|skipped|xfailed|xpassed)")


def done_modules() -> set[str]:
    with open(ROOT / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)
    return set(config.get("tool", {}).get("llm101", {}).get("done", []))


def run_module(folder: Path) -> tuple[dict[str, int], int]:
    """Run one module's tests; return the counts from pytest's summary line and its exit code."""
    command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no"]
    result = subprocess.run([*command, str(folder)], cwd=ROOT, capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    counts: dict[str, int] = {}
    for number, word in COUNT.findall(lines[-1] if lines else ""):
        counts["errors" if word.startswith("error") else word] = int(number)
    return counts, result.returncode


def main() -> int:
    done = done_modules()
    folders = sorted(p for p in (ROOT / "tests").glob("m[0-9][0-9]") if p.is_dir())
    rows = ["| Module | State | Passed | Failed | Errors |", "|---|---|---|---|---|"]
    broken = []
    for folder in folders:
        counts, code = run_module(folder)
        state = "done" if folder.name in done else "open"
        passed = counts.get("passed", 0)
        failed = counts.get("failed", 0)
        errors = counts.get("errors", 0)
        rows.append(f"| {folder.name} | {state} | {passed} | {failed} | {errors} |")
        if state == "done" and (failed or errors or code not in (0, 5)):
            broken.append(folder.name)

    table = "\n".join(rows)
    print(table)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## Modules\n\nRed tests are expected in an open module.\n\n" + table + "\n")

    if broken:
        print(f"\nA module marked done has failing tests: {', '.join(broken)}", file=sys.stderr)
        return 1
    print("\nEvery module marked done is green." if done else "\nNo module is marked done yet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
