"""Write it, chapter 2: the hour of the day with the most requests.

You are given the times of a day's requests as "HH:MM" strings, from "00:00" to "23:59", in any
order. Return the hour, a whole number from 0 to 23, in which the most requests arrived. When two
hours have the same count, the earlier hour wins.

    busiest_hour(["09:15", "14:02", "09:59", "14:30"])  ->  9      9 and 14 both have two
    busiest_hour(["23:01"])                             ->  23

Raises ValueError if there are no times. Ten minutes.
"""


def busiest_hour(times: list[str]) -> int:
    raise NotImplementedError("TODO(you)")
