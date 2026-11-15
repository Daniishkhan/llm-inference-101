"""Write it, chapter 5: the next job off a heap, skipping the ones that were cancelled.

A heap (heapq) holds (priority, name) entries. Some jobs have been cancelled since they were
pushed, and rather than dig them out of the middle of the heap, the program left them in. `alive`
is the set of names that still count. Pop entries until you find one whose name is alive, and
return that name; it leaves the heap like the others. If the heap runs out first, return None.

    heap = [(1, "a"), (2, "b"), (3, "c")]
    next_alive(heap, {"b", "c"})   ->  "b"      (1, "a") was cancelled: popped and dropped
    heap                           ->  [(3, "c")]

Ten minutes.
"""


def next_alive(heap: list[tuple[int, str]], alive: set[str]) -> str | None:
    raise NotImplementedError("TODO(you)")
