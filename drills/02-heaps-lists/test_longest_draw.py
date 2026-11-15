import random
import signal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from longest_draw import longest_draw


def test_the_examples():
    assert longest_draw("WLWWL") == 4
    assert longest_draw("WWLLW") == 4
    assert longest_draw("WWW") == 0
    assert longest_draw("") == 0


def test_one_game():
    assert longest_draw("W") == 0
    assert longest_draw("L") == 0


def test_the_whole_season_is_a_draw():
    assert longest_draw("WLLW") == 4


def test_the_draw_is_at_the_end():
    assert longest_draw("WWWWLWLL") == 6


def test_alternating_results():
    assert longest_draw("WLWLWLW") == 6


def mountain(heights):
    """For each height h, h wins and then h losses."""
    return "".join("W" * h + "L" * h for h in heights)


@given(
    heights=st.lists(st.integers(1, 6), min_size=1, max_size=8),
    before=st.integers(0, 10),
    after=st.integers(0, 10),
    swap=st.booleans(),
)
def test_a_draw_between_two_winning_streaks(heights, before, after, swap):
    # Wins before and after a mountain cannot join a draw with it, so the mountain is the longest
    # draw. With swap, wins and losses change places, and the answer stays the same.
    season = "W" * before + mountain(heights) + "W" * after
    if swap:
        season = season.translate(str.maketrans("WL", "LW"))
    assert longest_draw(season) == 2 * sum(heights)


class StillRunning(Exception):
    pass


def stop_the_run(signum, frame):
    raise StillRunning


def test_a_season_of_two_hundred_thousand_games_in_two_seconds():
    rng = random.Random(5)
    heights = [rng.randrange(1, 40) for _ in range(5_000)]
    season = "W" * 1_000 + mountain(heights)
    before = signal.signal(signal.SIGALRM, stop_the_run)
    signal.setitimer(signal.ITIMER_REAL, 2.0)
    try:
        result = longest_draw(season)
    except StillRunning:
        pytest.fail("still running after 2 s: trying every start with every end costs n * n steps")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, before)
    assert result == 2 * sum(heights)
