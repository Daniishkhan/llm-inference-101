"""Drill 01-5: tidy a path.

You are given an absolute path as a string. It starts with "/" and may be untidy:

- several slashes in a row mean the same as one;
- "." means "this folder" and changes nothing;
- ".." means "one folder up". Above the root there is nothing, so at the root it changes nothing;
- a slash at the end means nothing.

Return the shortest path that means the same. It starts with one "/", its folder names are
separated by one "/", and it has no "." or "..", and no slash at the end. The root itself is "/".

    tidy_path("/home//user/")       ->  "/home/user"
    tidy_path("/a/./b/../../c/")    ->  "/c"
    tidy_path("/../")               ->  "/"
    tidy_path("/a/../../b")         ->  "/b"
    tidy_path("/a/b/c/..")          ->  "/a/b"
    tidy_path("/...")               ->  "/..."     three dots is a name like any other
    tidy_path("/")                  ->  "/"

Any other run of characters between two slashes is a name: ".config", "x.y" and "..." are names.

Do it by hand: the tests read your file and fail if it imports os, posixpath or pathlib.

Time box: 25 minutes.
"""


def tidy_path(path: str) -> str:
    raise NotImplementedError("TODO(you)")
