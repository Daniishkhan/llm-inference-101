import time

from pair_with_sum import pair_with_sum


def test_the_pair_at_the_front():
    assert pair_with_sum([2, 7, 11, 15], 9) == (0, 1)


def test_the_pair_at_the_back():
    assert pair_with_sum([1, 4, 9, 20, 30], 50) == (3, 4)


def test_the_pair_far_apart():
    assert pair_with_sum([8, 1, 5, 3, 12], 20) == (0, 4)


def test_two_equal_numbers_at_different_positions():
    assert pair_with_sum([3, 3], 6) == (0, 1)


def test_a_position_cannot_be_used_twice():
    assert pair_with_sum([3, 5], 6) is None


def test_negative_numbers_and_zero():
    assert pair_with_sum([-4, 0, 9, 4], 0) == (0, 3)


def test_no_pair():
    assert pair_with_sum([1, 2, 3], 7) is None


def test_an_empty_list_and_a_single_number():
    assert pair_with_sum([], 5) is None
    assert pair_with_sum([5], 5) is None


def test_a_long_list_is_still_fast():
    numbers = list(range(1, 15_001))  # 1, 2, ..., 15000
    target = 14_999 + 15_000  # only the last two numbers add up to it
    start = time.perf_counter()
    result = pair_with_sum(numbers, target)
    seconds = time.perf_counter() - start
    assert result == (14_998, 14_999)
    assert seconds < 0.5, f"took {seconds:.2f} s: a loop inside a loop is too slow here"
