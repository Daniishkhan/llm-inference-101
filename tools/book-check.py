"""book-check.py: verify the books in docs/book/.

Checks docs/book/index.html and every docs/book/<book>/*.html (assets/ left out), or the files and
folders given on the command line. For each page:

  * every <pre class="code" data-lang="python"> block, by its data-check:
      run (the default)  written to a fresh temporary folder under its data-file name and run with
                         the project's Python (.venv/bin/python, else this interpreter) with -I, no
                         input, a 10-second limit and that folder as the working directory. It must
                         exit with 0. If a <pre class="output" data-for="FILE"> follows, stdout must
                         equal it (trailing whitespace on each line and at the end is ignored).
      error              must exit with an error. If a pre.output with data-for follows, its last
                         non-empty line must equal the last non-empty line of stderr.
      fragment           not run.
  * a "<" left unescaped inside a pre.code, pre.output or pre.shell (only the <code> wrapper is
    allowed there) is a problem: the browser would read it as a tag and drop the text;
  * every relative href and src (a ?v=N is ignored) must exist, and every #anchor must exist in its
    target page, by the same slug rule as book.js uses for h2 and h3 ids;
  * THE GUARD: no python block, whatever its data-check, may define a guarded name (def NAME(,
    async def NAME(, class NAME, NAME = lambda). The guarded names are the `guarded` list under
    [tool.llm101] in pyproject.toml, together with every module-level function or class in
    src/llm101/**/*.py and drills/**/*.py (test files left out) whose body still raises
    NotImplementedError, so a new module's stubs are guarded before the list is updated. The one
    exception is `main`: every example program may have one, and SPEC.md forbids in words a main
    that does a module's job.

Prints one line per problem and a summary. Exit code 0 = no problems, 1 = problems.

Usage:  uv run python tools/book-check.py
        uv run python tools/book-check.py docs/book/01-measure
        uv run python tools/book-check.py docs/book/01-measure/01-two-clocks.html
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import urllib.parse
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = 10
CHECKS = ("run", "error", "fragment")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
PRE_OPEN = re.compile(r"<pre\b([^>]*)>", re.IGNORECASE)
CLASS_ATTR = re.compile(r"""\bclass\s*=\s*["']([^"']*)["']""", re.IGNORECASE)


def slug(text: str) -> str:
    """The anchor book.js gives an h2 or h3 without an id: the text, trimmed and lower-cased, every
    run of characters other than a-z and 0-9 turned into one hyphen, a hyphen at either end
    dropped. "Milestone 1: time_calls" -> "milestone-1-time-calls". Keep it identical to
    slug() in docs/book/assets/book.js."""
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", text.strip().lower()))


# ---------------------------------------------------------------------------------------------
# Reading a page
# ---------------------------------------------------------------------------------------------
@dataclass
class Block:
    kind: str  # code, output or shell
    lang: str
    file: str | None
    for_: str | None
    check: str | None
    line: int
    text: str = ""


@dataclass
class Page:
    blocks: list[Block] = field(default_factory=list)
    links: list[tuple[str, int]] = field(default_factory=list)
    ids: set[str] = field(default_factory=set)


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.page = Page()
        self._block: Block | None = None
        self._heading: tuple[str, bool] | None = None  # (tag, has its own id)
        self._heading_text = ""
        self._main = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]
        if "id" in a:
            self.page.ids.add(a["id"])
        if tag == "main":
            self._main += 1
        if tag == "pre":
            cls = a.get("class", "").split()
            kind = next((k for k in ("code", "output", "shell") if k in cls), None)
            if kind:
                self._block = Block(
                    kind=kind,
                    lang=a.get("data-lang") or ("python" if kind == "code" else kind),
                    file=a.get("data-file"),
                    for_=a.get("data-for"),
                    check=a.get("data-check"),
                    line=line,
                )
        if tag in ("a", "link") and a.get("href"):
            self.page.links.append((a["href"], line))
        if tag in ("script", "img", "source", "iframe") and a.get("src"):
            self.page.links.append((a["src"], line))
        if tag in ("h2", "h3") and self._main and self._heading is None:
            self._heading = (tag, "id" in a)
            self._heading_text = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre" and self._block is not None:
            self.page.blocks.append(self._block)
            self._block = None
        if tag == "main":
            self._main -= 1
        if self._heading and tag == self._heading[0]:
            if not self._heading[1]:
                self.page.ids.add(slug(self._heading_text))
            self._heading = None

    def handle_data(self, data: str) -> None:
        if self._block is not None:
            self._block.text += data
        if self._heading is not None:
            self._heading_text += data


def parse(source: str) -> Page:
    c = Collector()
    c.feed(source)
    c.close()
    for b in c.page.blocks:  # HTML drops one newline right after <pre>; so does the browser
        if b.text.startswith("\n"):
            b.text = b.text[1:]
    return c.page


def unescaped_lt(source: str) -> list[int]:
    """Line numbers of a "<" inside a pre.code, pre.output or pre.shell other than its <code>
    wrapper and the closing tags."""
    lines = []
    for m in PRE_OPEN.finditer(source):
        cls = CLASS_ATTR.search(m.group(1))
        if not cls or not {"code", "output", "shell"} & set(cls.group(1).split()):
            continue
        end = source.find("</pre>", m.end())
        end = len(source) if end < 0 else end
        start = m.end()
        inner = source[start:end]
        opening = re.match(r"\s*<code\b[^>]*>", inner)
        skip = opening.end() if opening else 0
        closing = re.search(r"</code>\s*$", inner)
        stop = closing.start() if closing else len(inner)
        for k in range(skip, stop):
            if inner[k] == "<":
                lines.append(source.count("\n", 0, start + k) + 1)
                break
    return lines


# ---------------------------------------------------------------------------------------------
# The guard
# ---------------------------------------------------------------------------------------------
def raises_not_implemented(node: ast.AST) -> bool:
    for n in ast.walk(node):
        if isinstance(n, ast.Raise) and n.exc is not None:
            exc = n.exc.func if isinstance(n.exc, ast.Call) else n.exc
            if isinstance(exc, ast.Name) and exc.id == "NotImplementedError":
                return True
    return False


# Too generic to guard: every example program may define one. SPEC.md rules out, in words, a main
# that does a module's job (for Module 1: one that times a function many times and prints a report).
UNGUARDED = {"main"}


def stub_names(root: Path) -> set[str]:
    """Module-level functions and classes of src/llm101 and drills/ whose body raises
    NotImplementedError (a class counts when any of its methods does), apart from UNGUARDED."""
    names: set[str] = set()
    for base in (root / "src" / "llm101", root / "drills"):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.py")):
            if path.name.startswith("test_"):
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (SyntaxError, UnicodeDecodeError):
                continue
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if raises_not_implemented(node) and node.name not in UNGUARDED:
                        names.add(node.name)
    return names


def listed_names(root: Path) -> set[str]:
    """The `guarded` list under [tool.llm101] in pyproject.toml."""
    path = root / "pyproject.toml"
    if not path.is_file():
        return set()
    with path.open("rb") as f:
        data = tomllib.load(f)
    return set(data.get("tool", {}).get("llm101", {}).get("guarded", []))


def guarded_names(root: Path) -> set[str]:
    return listed_names(root) | stub_names(root)


def defines(text: str, name: str) -> bool:
    n = re.escape(name)
    return bool(
        re.search(rf"\bdef\s+{n}\b", text)
        or re.search(rf"\bclass\s+{n}\b", text)
        or re.search(rf"\b{n}\s*(?::[^=\n]*)?=\s*lambda\b", text)
    )


# ---------------------------------------------------------------------------------------------
# Running blocks
# ---------------------------------------------------------------------------------------------
def find_python(root: Path) -> str:
    venv = root / ".venv" / "bin" / "python"
    return str(venv) if venv.exists() else sys.executable


def norm(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.replace("\r", "").split("\n")).rstrip() + "\n"


def last_line(s: str) -> str:
    lines = [line.rstrip() for line in s.replace("\r", "").split("\n") if line.strip()]
    return lines[-1] if lines else ""


def first_difference(want: str, got: str) -> str:
    w, g = want.split("\n"), got.split("\n")
    for i in range(max(len(w), len(g))):
        a = w[i] if i < len(w) else "(nothing)"
        b = g[i] if i < len(g) else "(nothing)"
        if a != b:
            return f"line {i + 1}: book says {a!r}, program printed {b!r}"
    return "they differ"


DROPPED_ENV = {
    "FORCE_COLOR",
    "CLICOLOR_FORCE",
    "HYPOTHESIS_PROFILE",
    # The variables by which hypothesis (and others) recognise a CI service.
    "CI",
    "GITHUB_ACTIONS",
    "TF_BUILD",
    "BUILDKITE",
    "CIRCLECI",
    "CIRRUS_CI",
    "CODEBUILD_BUILD_ID",
    "GITLAB_CI",
    "HEROKU_TEST_RUN_ID",
    "TEAMCITY_VERSION",
    "BUILD_ID",
    "JENKINS_URL",
}


def run_block(python: str, text: str, fname: str, tmp: Path) -> subprocess.CompletedProcess | None:
    folder = Path(tempfile.mkdtemp(dir=tmp))
    (folder / fname).write_text(text, encoding="utf-8")
    # Run each example as it runs on the reader's machine: no forced colour, and none of the
    # variables a CI service sets, because hypothesis notices them and changes what it prints.
    env = {k: v for k, v in os.environ.items() if k not in DROPPED_ENV}
    env.update({"COLUMNS": "80", "LINES": "25", "NO_COLOR": "1"})
    try:
        return subprocess.run(
            [python, "-I", fname],
            cwd=folder,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return None


# ---------------------------------------------------------------------------------------------
# Checking a page
# ---------------------------------------------------------------------------------------------
class Checker:
    def __init__(self, root: Path, guarded: set[str], python: str) -> None:
        self.root = root
        self.guarded = sorted(guarded)
        self.python = python
        self._ids: dict[Path, set[str]] = {}
        self.blocks_run = 0

    def label(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    def ids_of(self, path: Path) -> set[str]:
        path = path.resolve()
        if path not in self._ids:
            self._ids[path] = parse(path.read_text(encoding="utf-8")).ids
        return self._ids[path]

    def check(self, path: Path, tmp: Path) -> list[str]:
        name = self.label(path)
        source = path.read_text(encoding="utf-8")
        page = parse(source)
        self._ids[path.resolve()] = page.ids
        problems = [
            f"{name}:{line}: an unescaped '<' inside a code block; write &lt;"
            for line in unescaped_lt(source)
        ]
        problems += self.check_blocks(name, page, tmp)
        problems += self.check_links(name, path, page)
        return problems

    def check_blocks(self, name: str, page: Page, tmp: Path) -> list[str]:
        problems: list[str] = []
        files = [b.file for b in page.blocks if b.kind == "code" and b.file]
        for f in sorted({f for f in files if files.count(f) > 1}):
            problems.append(f"{name}: data-file {f!r} is used by more than one block")
        for b in page.blocks:
            if b.kind == "output" and b.for_ and b.for_ not in files:
                problems.append(
                    f"{name}:{b.line}: pre.output data-for={b.for_!r} has no code block"
                )
        for i, b in enumerate(page.blocks):
            if b.kind != "code" or b.lang != "python":
                continue
            fname = b.file or f"block_{b.line}.py"
            where = f"{name}:{b.line} [{fname}]"
            for g in self.guarded:
                if defines(b.text, g):
                    problems.append(f"{where}: defines the guarded name {g!r}")
            check = b.check or "run"
            if check not in CHECKS:
                problems.append(f"{where}: data-check={check!r} is not one of {', '.join(CHECKS)}")
                continue
            if check == "fragment":
                continue
            if "/" in fname or "\\" in fname or fname in ("", ".", ".."):
                problems.append(f"{where}: data-file must be a plain file name")
                continue
            expected = next(
                (o for o in page.blocks[i + 1 :] if o.kind == "output" and o.for_ == b.file),
                None,
            )
            self.blocks_run += 1
            r = run_block(self.python, b.text, fname, tmp)
            if r is None:
                problems.append(f"{where}: still running after {TIMEOUT} s")
                continue
            if check == "error":
                if r.returncode == 0:
                    problems.append(f"{where}: data-check=error, but it exited with 0")
                elif expected is not None:
                    want, got = last_line(expected.text), last_line(r.stderr)
                    if want != got:
                        problems.append(
                            f"{where}: last line of stderr is {got!r}, the book says {want!r}"
                        )
                continue
            if r.returncode != 0:
                tail = last_line(r.stderr) or last_line(r.stdout)
                problems.append(f"{where}: exit code {r.returncode}: {tail}")
                continue
            if expected is not None:
                want, got = norm(expected.text), norm(r.stdout)
                if want != got:
                    problems.append(f"{where}: output differs, {first_difference(want, got)}")
        return problems

    def check_links(self, name: str, path: Path, page: Page) -> list[str]:
        problems: list[str] = []
        for href, line in page.links:
            if SCHEME.match(href) or href.startswith("/"):
                continue  # another site, or an absolute path: not checked
            target, _, frag = href.partition("#")
            target = urllib.parse.unquote(target.partition("?")[0])
            if target:
                tpath = (path.parent / target).resolve()
                if not tpath.exists():
                    problems.append(f"{name}:{line}: broken link {href!r} (no such file)")
                    continue
                if tpath.is_dir():
                    tpath = tpath / "index.html"
                if frag and tpath.suffix == ".html" and tpath.is_file():
                    if frag not in self.ids_of(tpath):
                        problems.append(f"{name}:{line}: broken anchor {href!r}")
            elif frag and frag not in page.ids:
                problems.append(f"{name}:{line}: broken anchor {href!r}")
        return problems


def default_files(root: Path) -> list[Path]:
    book = root / "docs" / "book"
    files = [book / "index.html"] if (book / "index.html").is_file() else []
    for d in sorted(p for p in book.iterdir() if p.is_dir() and p.name != "assets"):
        files += sorted(d.glob("*.html"))
    return files


def collect(args: list[str], root: Path) -> list[Path]:
    if not args:
        return default_files(root)
    files: list[Path] = []
    for a in args:
        p = Path(a)
        files += sorted(p.glob("*.html")) if p.is_dir() else [p]
    return files


def main(argv: list[str] | None = None, root: Path = ROOT, python: str | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    files = collect(args, root)
    checker = Checker(root, guarded_names(root), python or find_python(root))
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="book-check-") as tmp:
        for f in files:
            if not f.is_file():
                problems.append(f"{f}: no such file")
                continue
            problems += checker.check(f, Path(tmp))
    for p in problems:
        print(p)
    print(
        f"book-check: {len(files)} files, {checker.blocks_run} blocks run, "
        f"{len(problems)} problem{'' if len(problems) == 1 else 's'}"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
