"""Diagnostic 6: a moving average (a small class).

A MovingAverage remembers the most recent `size` numbers it has been given. Each call to add()
takes one more number and returns the mean of the numbers it remembers.

    window = MovingAverage(3)
    window.add(10)  ->  10.0     mean of 10
    window.add(20)  ->  15.0     mean of 10, 20
    window.add(30)  ->  20.0     mean of 10, 20, 30
    window.add(40)  ->  30.0     mean of 20, 30, 40: the 10 has dropped out

A size below 1 makes no sense: the constructor raises ValueError.

Time box: 20 minutes.
"""


class MovingAverage:
    def __init__(self, size: int) -> None:
        raise NotImplementedError("TODO(you)")

    def add(self, value: float) -> float:
        raise NotImplementedError("TODO(you)")
