from __future__ import annotations

from tb.lib.golden import encode_row


def _base():
    return {
        "COLOR": 0,
        "COMBINE": 0,
        "K1_SHIFT": 0,
        "K1_ROW0": encode_row(0, 0, 0),
        "K1_ROW1": encode_row(0, 1, 0),
        "K1_ROW2": encode_row(0, 0, 0),
        "K2_SHIFT": 0,
        "K2_ROW0": encode_row(0, 0, 0),
        "K2_ROW1": encode_row(0, 0, 0),
        "K2_ROW2": encode_row(0, 0, 0),
    }


def gray():
    p = _base()
    p["COLOR"] = 1
    return p


def blur():
    p = _base()
    p["K1_SHIFT"] = 4
    p["K1_ROW0"] = encode_row(1, 2, 1)
    p["K1_ROW1"] = encode_row(2, 4, 2)
    p["K1_ROW2"] = encode_row(1, 2, 1)
    return p


def edge():
    p = _base()
    p["COLOR"] = 1
    p["COMBINE"] = 2
    p["K1_ROW0"] = encode_row(-1, 0, 1)
    p["K1_ROW1"] = encode_row(-2, 0, 2)
    p["K1_ROW2"] = encode_row(-1, 0, 1)
    p["K2_ROW0"] = encode_row(-1, -2, -1)
    p["K2_ROW1"] = encode_row(0, 0, 0)
    p["K2_ROW2"] = encode_row(1, 2, 1)
    return p


def invert():
    p = _base()
    p["COMBINE"] = 0x10
    return p


def edge_sqrt():
    p = edge()
    p["COMBINE"] = 3
    return p


PRESETS = {
    "gray": gray,
    "blur": blur,
    "edge": edge,
    "invert": invert,
    "edge_sqrt": edge_sqrt,
}
