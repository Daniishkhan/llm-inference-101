import pytest

from messages_that_fit import messages_that_fit


def test_the_examples():
    assert messages_that_fit([120, 30, 50, 10], 100) == 3
    assert messages_that_fit([40, 60], 100) == 2
    assert messages_that_fit([10, 500], 100) == 0
    assert messages_that_fit([], 100) == 0


def test_it_stops_at_the_first_message_that_does_not_fit():
    # The 5-token message would fit, but the 200 after it does not: the history stops at the 200.
    assert messages_that_fit([5, 200, 10], 100) == 1


def test_a_window_of_nothing():
    assert messages_that_fit([1, 1], 0) == 0


def test_everything_fits():
    assert messages_that_fit([1, 2, 3], 1_000) == 3


def test_a_negative_window():
    with pytest.raises(ValueError):
        messages_that_fit([1], -1)
