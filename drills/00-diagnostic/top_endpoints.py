"""Diagnostic 2: the busiest endpoints in an access log.

Each line of the log is one request: five fields separated by single spaces.

    2026-11-14T09:15:02Z GET /api/users 200 12ms

    timestamp, method, path, status, duration

Count the requests per path (the method does not matter) and return the k busiest paths as
(path, count) pairs, busiest first. Paths with the same count come in alphabetical order.

    top_endpoints(lines, 2)  ->  [("/api/users", 3), ("/health", 2)]

Blank lines (empty, or only spaces) are skipped. If there are fewer than k paths, return them all.

Time box: 20 minutes.
"""


def top_endpoints(lines: list[str], k: int) -> list[tuple[str, int]]:
    raise NotImplementedError("TODO(you)")
