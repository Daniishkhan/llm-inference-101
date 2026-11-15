from run_length import encode


def test_empty_text_gives_empty_text():
    assert encode("") == ""


def test_a_single_letter_is_a_run_of_one():
    assert encode("x") == "x1"


def test_runs_are_counted_in_order():
    assert encode("aaabcc") == "a3b1c2"


def test_the_last_run_is_not_forgotten():
    assert encode("abbb") == "a1b3"


def test_the_same_letter_can_start_a_new_run_later():
    assert encode("aabaa") == "a2b1a2"


def test_upper_and_lower_case_are_different_letters():
    assert encode("aAa") == "a1A1a1"


def test_a_run_longer_than_nine():
    assert encode("z" * 12) == "z12"
