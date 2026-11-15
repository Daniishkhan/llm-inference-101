"""build-pages.py: build the static copy of the books that GitHub Pages serves.

Copies docs/book/ into OUT (default: build-pages/ at the repository root), so docs/book/index.html,
the course front page, becomes the site root OUT/index.html and docs/book/01-measure/ becomes
OUT/01-measure/. On the way it:

  * rewrites every relative link that leaves docs/book/ (goal.md, docs/setup.md, a module README,
    ...) into a link to that file on GitHub, because the online copy holds only the books;
  * marks every page <html data-hosted="static">, so the tutor panel knows it is the online copy
    and tells you to paste its prompts into Claude Code in your own clone of the repository;
  * leaves out the author files (assets/*.md, assets/TEMPLATE.html), which are not pages.

The source files are never modified. Exit code 0 = built, 1 = a link pointed at something that is
not in the repository (the copy is still written, so you can look at it).

Usage:  uv run python tools/build-pages.py [OUT]
        uv run python -m http.server 8768 --directory build-pages     # look at the result

GitHub Actions sets GITHUB_SERVER_URL, GITHUB_REPOSITORY and GITHUB_REF_NAME; outside Actions the
links point at https://github.com/Daniishkhan/llm-inference-101 on main.
"""

from __future__ import annotations

import os
import posixpath
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = "docs/book"  # repo-relative, with forward slashes
MARKER = ".build-pages"  # proves an existing OUT folder is ours to replace
LEAVE_ALONE = ("#", "/", "http:", "https:", "mailto:", "data:", "javascript:")
ATTR = re.compile(r'\b(href|src)="([^"]*)"')


def is_author_file(rel: str) -> bool:
    """Files under docs/book that are notes for whoever writes a book, not pages for readers."""
    parts = rel.split("/")
    return (
        len(parts) >= 2
        and parts[-2] == "assets"
        and (rel.endswith(".md") or parts[-1] == "TEMPLATE.html")
    )


def prepare_out(out: Path, root: Path = ROOT) -> None:
    """Refuse anything that is not a fresh folder or a previous build, then empty it."""
    book_dir = root / BOOK
    if out == root or out in root.parents or out == book_dir or book_dir in out.parents:
        sys.exit(f"build-pages: refusing to write into {out}")
    if out.exists():
        if any(out.iterdir()) and not (out / MARKER).exists():
            sys.exit(f"build-pages: {out} exists and was not made by this script; choose another")
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / MARKER).touch()


def rewrite_page(
    rel: str, text: str, base_url: str, ref: str, problems: list[str], root: Path = ROOT
) -> tuple[str, int]:
    """Point links that leave docs/book at GitHub; mark the page as statically hosted."""
    count = 0

    def fix(m: re.Match[str]) -> str:
        nonlocal count
        attr, value = m.group(1), m.group(2)
        if not value or value.startswith(LEAVE_ALONE):
            return m.group(0)
        path, hash_sign, fragment = value.partition("#")
        path = path.partition("?")[0]
        if not path:
            return m.group(0)
        target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), path))
        if target == BOOK or target.startswith(BOOK + "/"):
            return m.group(0)  # stays inside the published copy
        on_disk = root.joinpath(*target.split("/"))
        if target.startswith("..") or not on_disk.exists():
            problems.append(f"{rel}: {attr}={value!r} points at {target}, not in the repository")
            return m.group(0)
        kind = "tree" if on_disk.is_dir() else "blob"
        count += 1
        return f'{attr}="{base_url}/{kind}/{ref}/{target}{hash_sign}{fragment}"'

    text = ATTR.sub(fix, text)
    text, marked = re.subn(r"<html\b", '<html data-hosted="static"', text, count=1)
    if not marked:
        problems.append(f"{rel}: no <html> tag, so the page cannot be marked as statically hosted")
    return text, count


def build(out: Path, base_url: str, ref: str, root: Path = ROOT) -> tuple[int, int, int, list[str]]:
    """Copy and rewrite; return (pages, other files, links rewritten, problems)."""
    book_dir = root / BOOK
    if not (book_dir / "index.html").is_file():
        sys.exit(f"build-pages: {BOOK}/index.html, the site root, is missing")
    prepare_out(out, root)
    problems: list[str] = []
    pages = files = links = 0
    for dirpath, dirnames, filenames in os.walk(book_dir):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            src = Path(dirpath) / name
            inner = src.relative_to(book_dir).as_posix()
            rel = f"{BOOK}/{inner}"
            if is_author_file(rel):
                continue
            dst = out / inner
            dst.parent.mkdir(parents=True, exist_ok=True)
            if name.endswith(".html"):
                text, n = rewrite_page(
                    rel, src.read_text(encoding="utf-8"), base_url, ref, problems, root
                )
                dst.write_text(text, encoding="utf-8")
                pages += 1
                links += n
            else:
                shutil.copy2(src, dst)
                files += 1
    return pages, files, links, problems


def main(argv: list[str]) -> int:
    out = Path(argv[0] if argv else ROOT / "build-pages").resolve()
    server = os.environ.get("GITHUB_SERVER_URL") or "https://github.com"
    repo = os.environ.get("GITHUB_REPOSITORY") or "Daniishkhan/llm-inference-101"
    ref = os.environ.get("GITHUB_REF_NAME") or "main"
    base_url = f"{server}/{repo}"
    pages, files, links, problems = build(out, base_url, ref)
    print(
        f"build-pages: {pages} pages and {files} other files into {out}; "
        f"{links} links now point at {base_url} ({ref}); the site root is index.html"
    )
    for p in problems:
        print(f"  problem: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
