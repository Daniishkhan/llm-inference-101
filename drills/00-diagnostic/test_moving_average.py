import pytest

from moving_average import MovingAverage


def test_the_first_number_is_its_own_mean():
    window = MovingAverage(3)
    assert window.add(10) == 10.0


def test_the_mean_before_the_window_is_full():
    window = MovingAverage(3)
    window.add(10)
    assert window.add(20) == 15.0


def test_the_oldest_number_drops_out_once_the_window_is_full():
    window = MovingAverage(3)
    for value in (10, 20, 30):
        window.add(value)
    assert window.add(40) == 30.0
    assert window.add(50) == 40.0


def test_a_window_of_one_returns_the_last_number():
    window = MovingAverage(1)
    assert window.add(7) == 7.0
    assert window.add(-3) == -3.0


def test_fractions():
    window = MovingAverage(2)
    window.add(0.1)
    assert window.add(0.2) == pytest.approx(0.15)


def test_add_returns_a_float():
    window = MovingAverage(2)
    assert isinstance(window.add(4), float)


def test_two_windows_do_not_share_their_numbers():
    first = MovingAverage(2)
    second = MovingAverage(2)
    first.add(100)
    assert second.add(2) == 2.0


def test_a_size_below_one_is_refused():
    with pytest.raises(ValueError):
        MovingAverage(0)
    with pytest.raises(ValueError):
        MovingAverage(-2)
