"""Drill 02-5: how many days until it is warmer?

You are given the noon temperature of each day, in order. For each day, work out how many days you
would wait for a strictly warmer noon. If no later day is warmer, the answer for that day is 0.

    days_to_wait([20, 22, 19, 18, 25, 21])  ->  [1, 3, 2, 1, 0, 0]
        day 0 (20): day 1 is warmer, 1 day later
        day 1 (22): day 4 (25) is the first warmer day, 3 days later
        day 4 (25): nothing later is warmer, so 0
    days_to_wait([30, 30, 30])  ->  [0, 0, 0]      equal is not warmer
    days_to_wait([])            ->  []

Looking ahead from every day costs n * n steps when the days get colder and colder. Do it in time
proportional to n: the tests give you 200,000 days and two seconds. The list you are given must
come back unchanged.

Time box: 30 minutes.
"""


def days_to_wait(temperatures: list[float]) -> list[int]:
    raise NotImplementedError("TODO(you)")
