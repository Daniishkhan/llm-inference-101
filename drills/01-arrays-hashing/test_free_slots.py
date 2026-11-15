import random

from hypothesis import given
from hypothesis import strategies as st

from free_slots import free_slots


def slots(busy, day_start, day_end):
    """Call free_slots and return its answer as a list of tuples."""
    return [tuple(slot) for slot in free_slots(busy, day_start, day_end)]


def test_two_busy_periods():
    assert slots([(60, 120), (300, 360)], 0, 480) == [(0, 60), (120, 300), (360, 480)]


def test_periods_that_overlap_or_touch_leave_no_slot_between_them():
    assert slots([(100, 200), (150, 250), (250, 300)], 0, 400) == [(0, 100), (300, 400)]


def test_periods_in_any_order():
    assert slots([(40, 60), (10, 20)], 0, 100) == [(0, 10), (20, 40), (60, 100)]


def test_periods_that_stick_out_past_the_day():
    assert slots([(-50, 30), (90, 500)], 0, 100) == [(30, 90)]


def test_a_day_that_is_full():
    assert slots([(0, 100)], 0, 100) == []


def test_a_day_with_nothing_in_it():
    assert slots([], 0, 100) == [(0, 100)]


def test_a_period_inside_another():
    assert slots([(10, 90), (30, 40)], 0, 100) == [(0, 10), (90, 100)]


def test_periods_outside_the_day_do_not_count():
    assert slots([(500, 600), (-90, -10)], 0, 480) == [(0, 480)]


def test_periods_that_only_touch_the_ends_of_the_day():
    assert slots([(-10, 0), (100, 110)], 0, 100) == [(0, 100)]


def test_the_same_period_twice():
    assert slots([(20, 30), (20, 30)], 0, 50) == [(0, 20), (30, 50)]


def test_a_day_that_does_not_start_at_zero():
    assert slots([(540, 600)], 480, 720) == [(480, 540), (600, 720)]


def test_the_list_you_were_given_is_not_changed():
    busy = [(40, 60), (10, 20)]
    free_slots(busy, 0, 100)
    assert busy == [(40, 60), (10, 20)]


@given(
    lengths=st.lists(st.integers(1, 50), min_size=1, max_size=9),
    day_start=st.integers(-500, 500),
    starts_busy=st.booleans(),
    seed=st.integers(),
)
def test_a_day_built_from_known_stretches(lengths, day_start, starts_busy, seed):
    # Lay busy and free stretches end to end. Cut each busy stretch into two periods that overlap
    # or touch, and sometimes put a third inside it. Let the first and the last stick out past the
    # day, add periods that lie wholly outside it, repeat one, shuffle, and expect the free
    # stretches back.
    rng = random.Random(seed)
    busy, free = [], []
    at, is_busy = day_start, starts_busy
    for i, length in enumerate(lengths):
        end = at + length
        if is_busy:
            first_end = rng.randint(at + 1, end)
            second_start = rng.randint(at, min(first_end, end - 1))
            before = rng.randint(0, 30) if i == 0 else 0
            after = rng.randint(0, 30) if i == len(lengths) - 1 else 0
            busy += [(at - before, first_end), (second_start, end + after)]
            if length >= 3 and rng.random() < 0.5:
                busy.append((at + 1, end - 1))
        else:
            free.append((at, end))
        at, is_busy = end, not is_busy
    if rng.random() < 0.5:
        busy.append((day_start - 90, day_start - rng.randint(0, 40)))
    if rng.random() < 0.5:
        busy.append((at + rng.randint(0, 40), at + 90))
    if busy:
        busy.append(rng.choice(busy))
    rng.shuffle(busy)
    assert slots(busy, day_start, at) == free
