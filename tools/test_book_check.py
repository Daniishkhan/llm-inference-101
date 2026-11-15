"""Tests for tools/book-check.py, on small books built in tmp_path."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "book_check", Path(__file__).resolve().parent / "book-check.py"
)
assert _spec and _spec.loader
book_check = importlib.util.module_from_spec(_spec)
sys.modules["book_check"] = book_check
_spec.loader.exec_module(book_check)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>t</title></head>
<body>
<main>
<h1>A page</h1>
{body}
</main>
</body>
</html>
"""


def make_root(tmp_path: Path, guarded: list[str] | None = None) -> Path:
    """A repository in miniature: one stub that raises, one written function, one test file."""
    root = tmp_path / "repo"
    (root / "src" / "llm101" / "toy").mkdir(parents=True)
    (root / "src" / "llm101" / "toy" / "core.py").write_text(
        "def stubbed(x):\n"
        '    raise NotImplementedError("TODO(you)")\n\n\n'
        "def written(x):\n"
        "    return x\n\n\n"
        "class Counter:\n"
        "    def add(self, value):\n"
        '        raise NotImplementedError("TODO(you)")\n'
    )
    (root / "drills" / "set").mkdir(parents=True)
    (root / "drills" / "set" / "puzzle.py").write_text(
        "def solve(items):\n    raise NotImplementedError\n"
    )
    (root / "drills" / "set" / "test_puzzle.py").write_text(
        "def helper():\n    raise NotImplementedError\n"
    )
    names = ", ".join(f'"{n}"' for n in (guarded or []))
    (root / "pyproject.toml").write_text(f"[tool.llm101]\ndone = []\nguarded = [{names}]\n")
    (root / "docs" / "book" / "b").mkdir(parents=True)
    return root


def write_page(root: Path, name: str, body: str) -> Path:
    path = root / "docs" / "book" / "b" / name
    path.write_text(PAGE.format(body=body), encoding="utf-8")
    return path


def check(root: Path, path: Path, tmp_path: Path) -> list[str]:
    checker = book_check.Checker(root, book_check.guarded_names(root), sys.executable)
    run_dir = tmp_path / "runs"
    run_dir.mkdir(exist_ok=True)
    return checker.check(path, run_dir)


def code(text: str, file: str = "demo.py", check: str = "run") -> str:
    return (
        f'<pre class="code" data-lang="python" data-file="{file}" data-check="{check}">'
        f"<code>{text}</code></pre>"
    )


def output(text: str, file: str = "demo.py") -> str:
    return f'<pre class="output" data-for="{file}"><code>{text}</code></pre>'


# ---- the guard -----------------------------------------------------------------------------


def test_guard_collects_stubs_that_raise_and_ignores_the_rest(tmp_path):
    root = make_root(tmp_path)
    names = book_check.guarded_names(root)
    assert {"stubbed", "Counter", "solve"} <= names
    assert "written" not in names  # its body no longer raises
    assert "helper" not in names  # test files are not stubs
    assert "add" not in names  # methods are guarded through their class


@pytest.mark.parametrize(
    "snippet",
    [
        "def stubbed(x):\n    return x\n",
        "async def stubbed(x):\n    return x\n",
        "class Counter:\n    pass\n",
        "solve = lambda items: items\n",
    ],
)
def test_guard_catches_a_planted_definition_in_any_block(tmp_path, snippet):
    root = make_root(tmp_path)
    page = write_page(root, "p.html", code(snippet, check="fragment"))
    problems = check(root, page, tmp_path)
    assert len(problems) == 1
    assert "guarded name" in problems[0] and "p.html" in problems[0]


def test_guard_ignores_other_names_and_calls(tmp_path):
    root = make_root(tmp_path)
    body = code("def stubbed_twice(x):\n    return x\n\n\nprint(len([1, 2]))\n")
    body += output("2\n")
    page = write_page(root, "p.html", body)
    assert check(root, page, tmp_path) == []


def test_main_is_never_guarded_even_as_a_stub(tmp_path):
    root = make_root(tmp_path)
    (root / "src" / "llm101" / "toy" / "__main__.py").write_text(
        'def main():\n    raise NotImplementedError("TODO(you)")\n'
    )
    assert "main" not in book_check.guarded_names(root)
    body = code('def main():\n    print("hi")\n\n\nmain()\n') + output("hi\n")
    page = write_page(root, "p.html", body)
    assert check(root, page, tmp_path) == []


def test_a_name_in_the_pyproject_list_is_guarded_without_a_stub(tmp_path):
    root = make_root(tmp_path, guarded=["percentile", "Report"])
    assert {"percentile", "Report"} <= book_check.guarded_names(root)
    page = write_page(
        root, "p.html", code("def percentile(v, q):\n    return 0\n", check="fragment")
    )
    problems = check(root, page, tmp_path)
    assert len(problems) == 1 and "'percentile'" in problems[0]


# ---- running blocks ------------------------------------------------------------------------


def test_a_run_block_with_matching_output_passes(tmp_path):
    root = make_root(tmp_path)
    body = code('for word in ["measure", "first"]:\n    print(word, len(word))\n')
    body += output("measure 7   \nfirst 5\n\n")  # trailing spaces and blank lines are ignored
    page = write_page(root, "p.html", body)
    assert check(root, page, tmp_path) == []


def test_mismatched_output_is_a_problem(tmp_path):
    root = make_root(tmp_path)
    page = write_page(root, "p.html", code('print("measure")\n') + output("first\n"))
    problems = check(root, page, tmp_path)
    assert len(problems) == 1 and "output differs" in problems[0]


def test_a_failing_run_block_is_a_problem(tmp_path):
    root = make_root(tmp_path)
    page = write_page(root, "p.html", code("1 / 0\n"))
    problems = check(root, page, tmp_path)
    assert len(problems) == 1 and "ZeroDivisionError" in problems[0]


def test_an_error_block_that_does_not_fail_is_a_problem(tmp_path):
    root = make_root(tmp_path)
    page = write_page(root, "p.html", code('print("fine")\n', check="error"))
    problems = check(root, page, tmp_path)
    assert len(problems) == 1 and "exited with 0" in problems[0]


def test_an_error_block_compares_the_last_line_of_stderr(tmp_path):
    root = make_root(tmp_path)
    good = code('raise ValueError("k is out of range")\n', "a.py", "error")
    good += output(
        "Traceback (most recent call last):\n  ...\nValueError: k is out of range\n", "a.py"
    )
    bad = code('raise KeyError("k")\n', "b.py", "error") + output("ValueError: nope\n", "b.py")
    page = write_page(root, "p.html", good + bad)
    problems = check(root, page, tmp_path)
    assert len(problems) == 1 and "b.py" in problems[0]


# ---- HTML, links and anchors ---------------------------------------------------------------


def test_an_unescaped_less_than_is_a_problem(tmp_path):
    root = make_root(tmp_path)
    page = write_page(root, "p.html", code("if 1 <2:\n    pass\n", check="fragment"))
    problems = check(root, page, tmp_path)
    assert any("unescaped '<'" in p for p in problems)
    page = write_page(root, "q.html", code("if 1 &lt;2:\n    pass\n", check="fragment"))
    assert check(root, page, tmp_path) == []


def test_a_missing_link_target_is_a_problem(tmp_path):
    root = make_root(tmp_path)
    page = write_page(root, "p.html", '<p><a href="nowhere.html">x</a></p>')
    problems = check(root, page, tmp_path)
    assert len(problems) == 1 and "broken link" in problems[0]


def test_anchors_follow_the_book_js_slug_rule(tmp_path):
    root = make_root(tmp_path)
    write_page(root, "other.html", "<h2>Milestone 1: time_calls</h2><h3 id='own'>Kept</h3>")
    good = '<a href="other.html#milestone-1-time-calls">a</a> <a href="other.html#own">b</a>'
    good += ' <a href="#here-it-is">c</a> <a href="../../../pyproject.toml?v=1">d</a>'
    page = write_page(root, "p.html", f"<h2>Here: it is!</h2><p>{good}</p>")
    assert check(root, page, tmp_path) == []


def test_a_missing_anchor_is_a_problem(tmp_path):
    root = make_root(tmp_path)
    write_page(root, "other.html", "<h2>Two clocks</h2><h3 id='own'>Kept</h3>")
    links = '<a href="other.html#three-clocks">a</a> <a href="other.html#kept">b</a>'
    page = write_page(root, "p.html", f"<p>{links} <a href='#nothing'>c</a></p>")
    problems = check(root, page, tmp_path)
    assert len(problems) == 3 and all("broken anchor" in p for p in problems)


def test_slug_matches_examples():
    assert book_check.slug("  The problem: one timing lies ") == "the-problem-one-timing-lies"
    assert book_check.slug("Python's clocks (and why)") == "python-s-clocks-and-why"
