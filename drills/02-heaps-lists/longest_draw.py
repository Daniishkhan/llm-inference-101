"""Drill 02-6: the longest stretch of games that ends in a draw.

A team's season is a string of results, one letter per game in the order they were played: "W" for
a win and "L" for a loss. A stretch is one or more games next to each other. Return the length of
the longest stretch with exactly as many wins as losses. If there is none, return 0.

    longest_draw("WLWWL")    ->  4     "WLWW" has 3 wins; "LWWL" has 2 and 2
    longest_draw("WWLLW")    ->  4     "WWLL"
    longest_draw("WWW")      ->  0
    longest_draw("")         ->  0

Trying every start with every end costs n * n steps. Do it in one pass, in time proportional to n:
the tests give you a season of 200,000 games and two seconds.

Time box: 35 minutes.
"""


def longest_draw(results: str) -> int:
    raise NotImplementedError("TODO(you)")
