"""Drill 01-6: the free slots of a day.

A day runs from minute day_start to minute day_end. You are given the busy periods of that day as
(start, end) pairs of minutes, in any order. A period covers the minutes from start up to, and not
including, end. Periods may overlap each other, touch each other, repeat, sit inside one another, or
stick out past either end of the day.

Return the free slots: the stretches of the day that no busy period covers, as (start, end) pairs
in order of time. No two slots touch or overlap: free minutes with nothing busy between them are one
slot.

    free_slots([(60, 120), (300, 360)], 0, 480)                ->  [(0, 60), (120, 300), (360, 480)]
    free_slots([(100, 200), (150, 250), (250, 300)], 0, 400)   ->  [(0, 100), (300, 400)]
    free_slots([(40, 60), (10, 20)], 0, 100)                   ->  [(0, 10), (20, 40), (60, 100)]
    free_slots([(-50, 30), (90, 500)], 0, 100)                 ->  [(30, 90)]
    free_slots([(0, 100)], 0, 100)                             ->  []
    free_slots([], 0, 100)                                     ->  [(0, 100)]

You may assume that start < end in every period, and that day_start < day_end. The list you are
given must come back unchanged.

Time box: 30 minutes.
"""


def free_slots(busy: list[tuple[int, int]], day_start: int, day_end: int) -> list[tuple[int, int]]:
    raise NotImplementedError("TODO(you)")
