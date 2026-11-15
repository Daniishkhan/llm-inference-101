"""Drill 01-1: group the words that are anagrams of each other.

Two words are anagrams when one is the other with its letters in a different order: "stop",
"pots" and "tops" are anagrams; so are "cat" and "act". Every word uses the lowercase letters a to z
only, and the empty string counts as a word.

Given a list of words, put the anagrams together and return the list of groups:

- the groups come in the order in which their first word appears in the input;
- inside a group, the words keep their input order;
- a word that appears twice appears twice in its group.

    group_anagrams(["stop", "cat", "pots", "act", "tops", "dog"])
        ->  [["stop", "pots", "tops"], ["cat", "act"], ["dog"]]
    group_anagrams(["", ""])  ->  [["", ""]]
    group_anagrams([])        ->  []

Comparing every word with every other word works, but it is quadratic in the number of words. Aim
for one pass over the words.

Time box: 25 minutes.
"""


def group_anagrams(words: list[str]) -> list[list[str]]:
    raise NotImplementedError("TODO(you)")
