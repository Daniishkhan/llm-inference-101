import json

import pytest

from read_palette import read_palette


def write(path, palette):
    path.write_text(json.dumps(palette, ensure_ascii=False), encoding="utf-8")
    return path


def test_the_example(tmp_path):
    path = write(tmp_path / "palette.json", {"sky": [135, 206, 235], "grün": [0, 128, 0]})
    assert read_palette(path) == {"sky": "#87ceeb", "grün": "#008000"}


def test_an_empty_palette(tmp_path):
    assert read_palette(write(tmp_path / "empty.json", {})) == {}


def test_the_order_of_the_file_is_kept(tmp_path):
    path = write(tmp_path / "two.json", {"white": [255, 255, 255], "black": [0, 0, 0]})
    assert list(read_palette(path).items()) == [("white", "#ffffff"), ("black", "#000000")]


@pytest.mark.parametrize("channel", [256, -1])
def test_a_number_outside_0_to_255(tmp_path, channel):
    path = write(tmp_path / "bad.json", {"bad": [channel, 0, 0]})
    with pytest.raises(ValueError):
        read_palette(path)
