import random
import signal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from count_stretches import count_stretches

small = st.lists(st.integers(-9, 9), max_size=40)
targets = st.integers(-20, 20)


def test_the_first_example():
    assert count_stretches([1, 1, 1], 2) == 2


def test_a_stretch_can_be_one_number():
    assert count_stretches([1, 2, 3], 3) == 2


def test_negative_numbers_bring_the_sum_back():
    assert count_stretches([3, 4, -7, 1, 3, 3], 7) == 3


def test_a_target_of_zero():
    assert count_stretches([1, -1, 1, -1], 0) == 4


def test_every_stretch_of_zeros_adds_up_to_zero():
    assert count_stretches([0, 0, 0], 0) == 6


def test_one_number_that_is_the_target():
    assert count_stretches([5], 5) == 1


def test_one_number_that_is_not_the_target():
    assert count_stretches([5], 4) == 0


def test_an_empty_list_has_no_stretch():
    assert count_stretches([], 0) == 0


def test_the_whole_list_is_a_stretch():
    assert count_stretches([2, -5, 9], 6) == 1


def test_the_list_you_were_given_is_not_changed():
    numbers = [3, 4, -7, 1]
    count_stretches(numbers, 7)
    assert numbers == [3, 4, -7, 1]


class StillRunning(Exception):
    pass


def stop_the_run(signum, frame):
    raise StillRunning


def test_two_hundred_thousand_numbers_in_two_seconds():
    # An alarm stops the call after two seconds, so that a slow answer fails at once and does not
    # keep you waiting for minutes.
    rng = random.Random(1)
    numbers = [rng.randint(-5, 5) for _ in range(200_000)]
    before = signal.signal(signal.SIGALRM, stop_the_run)
    signal.setitimer(signal.ITIMER_REAL, 2.0)
    try:
        count_stretches(numbers, 3)
    except StillRunning:
        pytest.fail("still running after 2 s: trying every start with every end is too slow")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, before)


@given(n=st.integers(0, 60))
def test_zeros_and_a_target_of_zero(n):
    # Every stretch of zeros adds up to zero, and a list of n numbers has n * (n + 1) / 2 stretches.
    assert count_stretches([0] * n, 0) == n * (n + 1) // 2


@given(n=st.integers(0, 60), k=st.integers(1, 70))
def test_ones(n, k):
    # In a list of n ones, a stretch adds up to k exactly when it is k numbers long.
    assert count_stretches([1] * n, k) == max(0, n - k + 1)


@given(numbers=small, target=targets)
def test_reading_the_list_backwards_changes_nothing(numbers, target):
    assert count_stretches(numbers[::-1], target) == count_stretches(numbers, target)


@given(numbers=small, target=targets)
def test_flipping_every_sign_changes_nothing(numbers, target):
    assert count_stretches([-x for x in numbers], -target) == count_stretches(numbers, target)


@given(left=small, right=small, target=targets)
def test_a_wall_splits_the_list_in_two(left, right, target):
    # A stretch that holds the wall is far too big to add up to the target, so the two sides are
    # counted separately.
    wall = 1000
    whole = count_stretches([*left, wall, *right], target)
    assert whole == count_stretches(left, target) + count_stretches(right, target)
