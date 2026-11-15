"""Write it, chapter 6: how much of a conversation fits in a model's context window?

A chat's history is a list of messages, oldest first, and counts[i] is the number of tokens in
message i, at least 1. The model can see at most `window` tokens. Keep the newest messages: count
back from the last one, and stop at the first message that would not fit, even if an older and
shorter one would. Return how many messages you kept.

    messages_that_fit([120, 30, 50, 10], 100)  ->  3     10 + 50 + 30 = 90; the 120 would not fit
    messages_that_fit([40, 60], 100)           ->  2     exactly 100 fits
    messages_that_fit([10, 500], 100)          ->  0     the newest alone is too long
    messages_that_fit([], 100)                 ->  0

Raises ValueError if window is negative. Ten minutes.
"""


def messages_that_fit(counts: list[int], window: int) -> int:
    raise NotImplementedError("TODO(you)")
