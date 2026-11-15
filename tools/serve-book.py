"""serve-book.py: serve the books at http://localhost:8767 (or a port you pass).

Serves docs/book/, which holds the course front page (docs/book/index.html, served at /) and one
book per module (Module 1 at http://localhost:8767/01-measure/), like `python -m http.server`, with
one header added: Cache-Control: no-cache. That makes the browser re-check every page on each visit,
so an edit to a book shows up on a normal reload instead of an old cached copy.

It listens on this Mac only (127.0.0.1 and ::1, the two spellings of localhost), so other machines
on your network cannot reach it. If another program already holds the port (an old
`python -m http.server`, say), it refuses to start rather than share the port with it. It serves
files and nothing else: there is no tutor route (the tutor panel copies prompts for Claude Code),
and a POST or OPTIONS request gets 405.

Usage:  uv run python tools/serve-book.py          # port 8767
        uv run python tools/serve-book.py 9000     # another port
Stop with Ctrl-C.
"""

from __future__ import annotations

import functools
import http.server
import socket
import sys
import threading
from pathlib import Path

BOOKS = Path(__file__).resolve().parent.parent / "docs" / "book"
DEFAULT_PORT = 8767


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def refuse(self) -> None:
        self.send_error(405, "This server only serves files")

    do_POST = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = refuse


class Server6(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6


def port_taken(port: int) -> str | None:
    """Return the address something is already listening on, or None."""
    for family, addr in ((socket.AF_INET6, "::1"), (socket.AF_INET, "127.0.0.1")):
        try:
            with socket.socket(family, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((addr, port)) == 0:
                    return addr
        except OSError:
            pass
    return None


def main(argv: list[str]) -> int:
    port = int(argv[0]) if argv else DEFAULT_PORT
    taken = port_taken(port)
    if taken:
        print(
            f"Port {port} is already in use on {taken} by another program, perhaps an older book "
            f"server or `python -m http.server`.\nStop that one first (Ctrl-C in its terminal), or "
            f"use another port: uv run python tools/serve-book.py {port + 1}"
        )
        return 1
    handler = functools.partial(NoCache, directory=str(BOOKS))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        try:  # browsers try ::1 first for "localhost"
            httpd6 = Server6(("::1", port), handler)
            threading.Thread(target=httpd6.serve_forever, daemon=True).start()
        except OSError:
            pass
        print(f"Serving the books at http://localhost:{port}/  (Ctrl-C to stop)", flush=True)
        for book in sorted(p.name for p in BOOKS.iterdir() if (p / "index.html").is_file()):
            print(f"  {book}: http://localhost:{port}/{book}/", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
