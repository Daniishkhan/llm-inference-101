import ast
import inspect
import random

from hypothesis import given
from hypothesis import strategies as st

import tidy_path as module
from tidy_path import tidy_path

names = st.text(alphabet="abcxyz019._-", min_size=1, max_size=6).filter(
    lambda name: name not in {".", ".."}
)
NOISE = ["", ".", "tmp/.."]
LIBRARIES = {"os", "posixpath", "ntpath", "pathlib", "importlib"}


def untidy(folders, rng):
    """Write the path to `folders` with noise that does not change what it means."""
    parts = []
    if rng.random() < 0.3:
        parts.append("..")  # one up from the root is still the root
    for folder in folders:
        parts.extend(rng.choice(NOISE) for _ in range(rng.randrange(3)))
        parts.append(folder)
    parts.extend(rng.choice(NOISE) for _ in range(rng.randrange(3)))
    return "/" + "/".join(parts) + rng.choice(["", "/"])


def test_slashes_in_a_row_and_at_the_end():
    assert tidy_path("/home//user/") == "/home/user"


def test_one_dot_changes_nothing_and_two_dots_go_up():
    assert tidy_path("/a/./b/../../c/") == "/c"


def test_there_is_nothing_above_the_root():
    assert tidy_path("/../") == "/"


def test_up_past_the_root_and_down_again():
    assert tidy_path("/a/../../b") == "/b"


def test_two_dots_at_the_end():
    assert tidy_path("/a/b/c/..") == "/a/b"


def test_three_dots_is_a_name():
    assert tidy_path("/...") == "/..."


def test_names_may_hold_dots():
    assert tidy_path("/.config/app.d/../x.y") == "/.config/x.y"


def test_the_root():
    assert tidy_path("/") == "/"


def test_only_slashes():
    assert tidy_path("////") == "/"


def test_a_tidy_path_comes_back_unchanged():
    assert tidy_path("/usr/local/bin") == "/usr/local/bin"


def test_it_does_not_hand_the_work_to_a_library():
    source = inspect.getsource(module)
    assert "__import__" not in source, "do it by hand (see the docstring)"
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported = [(node.module or "").split(".")[0]]
        else:
            continue
        for name in imported:
            assert name not in LIBRARIES, "do it by hand (see the docstring)"


@given(folders=st.lists(names, max_size=6), seed=st.integers())
def test_noise_that_changes_nothing(folders, seed):
    # Start from known folder names. Add extra slashes, single dots and a folder that is entered and
    # left again, and expect the tidy path back.
    tidy = "/" + "/".join(folders)
    assert tidy_path(untidy(folders, random.Random(seed))) == tidy


@given(folders=st.lists(names, max_size=6), seed=st.integers())
def test_tidying_twice_changes_nothing_more(folders, seed):
    once = tidy_path(untidy(folders, random.Random(seed)))
    assert tidy_path(once) == once
