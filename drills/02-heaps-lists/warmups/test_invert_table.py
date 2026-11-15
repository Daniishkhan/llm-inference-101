import pytest

from invert_table import invert_table


def test_the_examples():
    assert invert_table({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert invert_table({}) == {}


def test_a_shared_value_is_refused_and_named():
    with pytest.raises(ValueError, match="1"):
        invert_table({"a": 1, "b": 1})


def test_inverting_twice_gives_the_table_back():
    table = {chr(65 + i): i for i in range(26)}
    assert invert_table(invert_table(table)) == table


def test_the_table_you_were_given_is_not_changed():
    table = {"x": 9}
    invert_table(table)
    assert table == {"x": 9}
