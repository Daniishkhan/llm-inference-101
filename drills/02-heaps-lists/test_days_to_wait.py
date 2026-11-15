import random
import signal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from days_to_wait import days_to_wait


def test_the_examples():
    assert days_to_wait([20, 22, 19, 18, 25, 21]) == [1, 3, 2, 1, 0, 0]
    assert days_to_wait([30, 30, 30]) == [0, 0, 0]
    assert days_to_wait([]) == []


def test_one_day():
    assert days_to_wait([12.5]) == [0]


def test_warmer_every_day():
    assert days_to_wait([1, 2, 3, 4]) == [1, 1, 1, 0]


def test_colder_every_day():
    assert days_to_wait([4, 3, 2, 1]) == [0, 0, 0, 0]


def test_a_dip_and_a_peak():
    assert days_to_wait([5, 3, 4, 3, 6]) == [4, 1, 2, 1, 0]


def test_fractions_of_a_degree():
    assert days_to_wait([20.5, 20.25, 20.75]) == [2, 1, 0]


def test_the_list_you_were_given_is_not_changed():
    temperatures = [3, 1, 2]
    days_to_wait(temperatures)
    assert temperatures == [3, 1, 2]


@given(st.lists(st.integers(-5, 5), max_size=60))
def test_each_answer_points_at_the_first_warmer_day(temperatures):
    # Check each answer instead of working it out: the day it points at is warmer, and no day in
    # between is; an answer of 0 means no later day is warmer.
    answer = days_to_wait(temperatures)
    assert len(answer) == len(temperatures)
    for day, wait in enumerate(answer):
        today = temperatures[day]
        if wait == 0:
            assert all(later <= today for later in temperatures[day + 1 :]), f"day {day}"
        else:
            assert temperatures[day + wait] > today, f"day {day}"
            assert all(t <= today for t in temperatures[day + 1 : day + wait]), f"day {day}"


class StillRunning(Exception):
    pass


def stop_the_run(signum, frame):
    raise StillRunning


@pytest.mark.parametrize("order", ["colder every day", "random"])
def test_two_hundred_thousand_days_in_two_seconds(order):
    if order == "colder every day":
        temperatures = list(range(200_000, 0, -1))
    else:
        rng = random.Random(4)
        temperatures = [rng.randrange(-30, 45) for _ in range(200_000)]
    before = signal.signal(signal.SIGALRM, stop_the_run)
    signal.setitimer(signal.ITIMER_REAL, 2.0)
    try:
        result = days_to_wait(temperatures)
    except StillRunning:
        pytest.fail("still running after 2 s: looking ahead from every day costs n * n steps")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, before)
    assert len(result) == 200_000
    if order == "colder every day":
        assert result == [0] * 200_000
