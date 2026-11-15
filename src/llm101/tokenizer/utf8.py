"""UTF-8 by hand: how a character becomes one to four bytes.

Milestone M1. The tests compare your bytes with str.encode("utf-8"), and they read this file: it may
not call .encode() or .decode(), import codecs, or hand a string and an encoding to bytes() or
bytearray().
"""


def utf8_encode(text: str) -> bytes:
    """The UTF-8 bytes of text, worked out from each character's code point (ord) with shifts and
    masks.

    A code point c takes as many bytes as it needs, and every byte after the first starts with the
    bits 10:

        c from 0 to 0x7F            1 byte    0xxxxxxx
        c from 0x80 to 0x7FF        2 bytes   110xxxxx 10xxxxxx
        c from 0x800 to 0xFFFF      3 bytes   1110xxxx 10xxxxxx 10xxxxxx
        c from 0x10000 to 0x10FFFF  4 bytes   11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

    Write c in binary with exactly as many bits as the row has x slots (7, 11, 16 or 21), with
    zeros in front, and share those bits out over the slots from left to right. é is 0xE9, eight
    bits; written in 11, it is 00011 101001, so its bytes are 110 00011 and 10 101001: 0xC3 0xA9.

        utf8_encode("A")   ->  b"A"                     0x41: one byte
        utf8_encode("é")   ->  b"\\xc3\\xa9"              0xE9: two bytes
        utf8_encode("€")   ->  b"\\xe2\\x82\\xac"          0x20AC: three bytes
        utf8_encode("")    ->  b""

    Raises ValueError for a code point from 0xD800 to 0xDFFF. Those are surrogates, halves of a pair
    that UTF-16 uses; they are not characters, and UTF-8 has no bytes for them.
    """
    raise NotImplementedError("TODO(you)")
