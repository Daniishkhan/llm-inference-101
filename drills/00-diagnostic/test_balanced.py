from balanced import is_balanced


def test_empty_text_is_balanced():
    assert is_balanced("") is True


def test_text_without_brackets_is_balanced():
    assert is_balanced("no brackets here") is True


def test_one_pair_of_each_kind():
    assert is_balanced("()") is True
    assert is_balanced("[]") is True
    assert is_balanced("{}") is True


def test_nested_brackets():
    assert is_balanced("{[()]}") is True


def test_brackets_side_by_side():
    assert is_balanced("()[]{}") is True


def test_other_characters_are_ignored():
    assert is_balanced("a(b[c]{d})e") is True


def test_the_wrong_kind_of_closing_bracket():
    assert is_balanced("(]") is False


def test_closed_in_the_wrong_order():
    assert is_balanced("([)]") is False


def test_never_closed():
    assert is_balanced("((") is False
    assert is_balanced("{[]") is False


def test_closed_before_it_was_opened():
    assert is_balanced(")(") is False
    assert is_balanced("]") is False


def test_one_closing_bracket_too_many():
    assert is_balanced("())") is False
