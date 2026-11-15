from top_endpoints import top_endpoints

LOG = [
    "2026-11-14T09:15:02Z GET /api/users 200 12ms",
    "2026-11-14T09:15:03Z GET /health 200 1ms",
    "2026-11-14T09:15:04Z POST /api/users 201 30ms",
    "2026-11-14T09:15:05Z GET /api/orders 500 250ms",
    "2026-11-14T09:15:06Z GET /health 200 1ms",
    "2026-11-14T09:15:07Z GET /api/users 200 11ms",
]


def test_the_busiest_paths_come_first():
    assert top_endpoints(LOG, 2) == [("/api/users", 3), ("/health", 2)]


def test_the_method_does_not_matter():
    lines = [
        "2026-11-14T10:00:00Z GET /a 200 1ms",
        "2026-11-14T10:00:01Z POST /a 201 1ms",
        "2026-11-14T10:00:02Z DELETE /a 204 1ms",
    ]
    assert top_endpoints(lines, 1) == [("/a", 3)]


def test_equal_counts_come_in_alphabetical_order():
    lines = [
        "2026-11-14T10:00:00Z GET /b 200 1ms",
        "2026-11-14T10:00:01Z GET /c 200 1ms",
        "2026-11-14T10:00:02Z GET /a 200 1ms",
    ]
    assert top_endpoints(lines, 3) == [("/a", 1), ("/b", 1), ("/c", 1)]


def test_a_higher_count_beats_the_alphabet():
    lines = [
        "2026-11-14T10:00:00Z GET /z 200 1ms",
        "2026-11-14T10:00:01Z GET /z 200 1ms",
        "2026-11-14T10:00:02Z GET /a 200 1ms",
    ]
    assert top_endpoints(lines, 2) == [("/z", 2), ("/a", 1)]


def test_blank_lines_are_skipped():
    lines = ["", "2026-11-14T10:00:00Z GET /a 200 1ms", "   ", ""]
    assert top_endpoints(lines, 5) == [("/a", 1)]


def test_k_larger_than_the_number_of_paths_returns_them_all():
    assert top_endpoints(LOG, 10) == [("/api/users", 3), ("/health", 2), ("/api/orders", 1)]


def test_k_of_zero_returns_nothing():
    assert top_endpoints(LOG, 0) == []


def test_an_empty_log_returns_nothing():
    assert top_endpoints([], 3) == []
