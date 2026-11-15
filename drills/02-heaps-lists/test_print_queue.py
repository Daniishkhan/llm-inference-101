from print_queue import Job, run_order


def test_the_example():
    jobs = [Job("report", 2), Job("photo", 1), Job("letter", 2)]
    assert run_order(jobs) == ["photo", "report", "letter"]


def test_different_priorities():
    jobs = [Job("c", 3), Job("a", 1), Job("b", 2)]
    assert run_order(jobs) == ["a", "b", "c"]


def test_no_jobs():
    assert run_order([]) == []


def test_jobs_with_the_same_priority_print_in_the_order_they_were_sent():
    jobs = [Job("zebra", 1), Job("apple", 1), Job("mango", 1)]
    assert run_order(jobs) == ["zebra", "apple", "mango"]


def test_a_busy_morning():
    jobs = [Job(f"job-{i:03}", i % 3) for i in range(30)]
    expected = [f"job-{i:03}" for p in range(3) for i in range(30) if i % 3 == p]
    assert run_order(jobs) == expected
