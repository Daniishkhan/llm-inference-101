from merge_intervals import merge


def test_an_empty_list():
    assert merge([]) == []


def test_a_single_interval():
    assert merge([(4, 7)]) == [(4, 7)]


def test_overlapping_intervals_are_merged():
    assert merge([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]


def test_touching_intervals_are_merged():
    assert merge([(1, 2), (2, 3)]) == [(1, 3)]


def test_neighbours_that_share_no_number_stay_apart():
    assert merge([(1, 2), (3, 4)]) == [(1, 2), (3, 4)]


def test_the_result_is_sorted_by_start():
    assert merge([(5, 6), (1, 2)]) == [(1, 2), (5, 6)]


def test_an_interval_inside_another():
    assert merge([(1, 10), (2, 3), (4, 5)]) == [(1, 10)]


def test_a_chain_merges_into_one():
    assert merge([(6, 8), (1, 3), (3, 5), (5, 6)]) == [(1, 8)]


def test_identical_intervals():
    assert merge([(2, 4), (2, 4)]) == [(2, 4)]


def test_overlaps_in_an_unsorted_list():
    assert merge([(8, 10), (2, 6), (15, 18), (1, 3)]) == [(1, 6), (8, 10), (15, 18)]


def test_the_list_you_were_given_is_not_changed():
    intervals = [(5, 6), (1, 3), (2, 4)]
    merge(intervals)
    assert intervals == [(5, 6), (1, 3), (2, 4)]
