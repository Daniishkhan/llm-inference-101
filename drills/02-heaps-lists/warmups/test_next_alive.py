import heapq

from next_alive import next_alive


def test_the_example():
    heap = [(1, "a"), (2, "b"), (3, "c")]
    assert next_alive(heap, {"b", "c"}) == "b"
    assert heap == [(3, "c")]


def test_the_top_is_alive():
    heap = [(1, "a"), (2, "b")]
    assert next_alive(heap, {"a", "b"}) == "a"
    assert heap == [(2, "b")]


def test_everything_was_cancelled():
    heap = [(1, "a"), (2, "b")]
    assert next_alive(heap, set()) is None
    assert heap == []


def test_it_keeps_the_heap_a_heap():
    heap = []
    for priority, name in [(5, "e"), (1, "a"), (4, "d"), (2, "b"), (3, "c")]:
        heapq.heappush(heap, (priority, name))
    assert next_alive(heap, {"c", "d", "e"}) == "c"
    assert [heapq.heappop(heap) for _ in range(len(heap))] == [(4, "d"), (5, "e")]
