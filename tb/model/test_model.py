from pathlib import Path
import tempfile
import math

import numpy as np

from tb.lib import bmp, golden, regmap


def test_regmap_shape():
    assert len(regmap.ADDR) == 20
    vals = sorted(regmap.ADDR.values())
    assert len(set(vals)) == 20
    for v in vals:
        assert v % 4 == 0


def test_encode_row_examples():
    assert golden.encode_row(-1, 0, 1) == 0x0001001F
    assert golden.encode_row(-1, -2, -1) == 0x001F1E1F


def test_bmp_round_trip_size_order():
    img = np.zeros((256, 256, 3), dtype=np.uint8)
    img[0, 0] = [11, 22, 33]
    img[-1, -1] = [44, 55, 66]
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "x.bmp"
        bmp.write_bmp(p, img)
        raw = p.read_bytes()
        assert len(raw) == 196662
        got = bmp.read_bmp(p)
    assert np.array_equal(img, got)


def test_stream_round_trip():
    rng = np.random.default_rng(9)
    img = rng.integers(0, 256, size=(256, 256, 3), dtype=np.uint8)
    words = list(bmp.to_stream(img))
    got = bmp.from_stream(words)
    assert np.array_equal(img, got)


def test_reset_pass_through():
    rng = np.random.default_rng(12)
    img = rng.integers(0, 256, size=(256, 256, 3), dtype=np.uint8)
    cfg = golden.cfg_from_regs({})
    out = golden.run(img, cfg)
    assert np.array_equal(img, out)


def test_gray_formula():
    img = np.zeros((256, 256, 3), dtype=np.uint8)
    img[0, 0] = [100, 150, 200]
    cfg = golden.cfg_from_regs({"COLOR": 1})
    out = golden.run(img, cfg)
    y = (77 * 100 + 150 * 150 + 29 * 200 + 128) >> 8
    assert np.all(out[0, 0] == np.array([y, y, y], dtype=np.uint8))


def test_invert_mode():
    img = np.full((256, 256, 3), 17, dtype=np.uint8)
    cfg = golden.cfg_from_regs({"COMBINE": 0x10})
    out = golden.run(img, cfg)
    assert np.array_equal(out, 255 - img)


def test_blur_flat_unchanged():
    img = np.full((256, 256, 3), 77, dtype=np.uint8)
    cfg = golden.cfg_from_regs(
        {
            "K1_SHIFT": 4,
            "K1_ROW0": golden.encode_row(1, 2, 1),
            "K1_ROW1": golden.encode_row(2, 4, 2),
            "K1_ROW2": golden.encode_row(1, 2, 1),
        }
    )
    out = golden.run(img, cfg)
    assert np.array_equal(out, img)


def test_vertical_edge_saturates_edge_and_sqrt():
    img = np.zeros((256, 256, 3), dtype=np.uint8)
    img[:, 128:] = 255
    regs = {
        "COLOR": 1,
        "COMBINE": 2,
        "K1_ROW0": golden.encode_row(-1, 0, 1),
        "K1_ROW1": golden.encode_row(-2, 0, 2),
        "K1_ROW2": golden.encode_row(-1, 0, 1),
        "K2_ROW0": golden.encode_row(-1, -2, -1),
        "K2_ROW2": golden.encode_row(1, 2, 1),
    }
    out_edge = golden.run(img, golden.cfg_from_regs(regs))
    regs["COMBINE"] = 3
    out_sqrt = golden.run(img, golden.cfg_from_regs(regs))
    assert int(out_edge[128, 127, 0]) == 255
    assert int(out_sqrt[128, 127, 0]) == 255


def test_isqrt_exact_random():
    rng = np.random.default_rng(2026)
    vals = rng.integers(0, 2696716801, size=2000, dtype=np.int64)
    for v in vals:
        assert math.isqrt(int(v)) == int(np.floor(np.sqrt(int(v))))
