"""Write it, chapter 4: read a palette of colours from a JSON file.

The file holds one JSON object. Each key is a colour's name, and each value is a list of three whole
numbers from 0 to 255: its red, green and blue. Return a dict from each name to the colour's hex
code: "#", then two lower-case hex digits for each of red, green and blue, in the file's order.

    a file holding   {"sky": [135, 206, 235], "grün": [0, 128, 0]}
    read_palette(path)  ->  {"sky": "#87ceeb", "grün": "#008000"}

Read the file as UTF-8, whatever this machine's default encoding is. Raises ValueError if a number
is outside 0 to 255. Ten minutes.
"""

from pathlib import Path


def read_palette(path: Path) -> dict[str, str]:
    raise NotImplementedError("TODO(you)")
