import pytest

from busiest_hour import busiest_hour


def test_the_examples():
    assert busiest_hour(["09:15", "14:02", "09:59", "14:30"]) == 9
    assert busiest_hour(["23:01"]) == 23


def test_a_tie_goes_to_the_earlier_hour_whatever_the_order():
    assert busiest_hour(["14:02", "09:15", "14:30", "09:59"]) == 9


def test_the_most_requests_win():
    assert busiest_hour(["08:00", "17:10", "17:20", "17:59", "08:30"]) == 17


def test_midnight_is_hour_zero():
    assert busiest_hour(["00:00", "00:59", "12:00"]) == 0


def test_no_times():
    with pytest.raises(ValueError):
        busiest_hour([])
