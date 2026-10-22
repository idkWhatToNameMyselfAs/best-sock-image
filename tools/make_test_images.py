from pathlib import Path

import numpy as np

from tb.lib.bmp import write_bmp


OUT = Path(__file__).resolve().parents[1] / "images"
OUT.mkdir(parents=True, exist_ok=True)


def _save(name: str, img: np.ndarray):
    write_bmp(OUT / f"{name}.bmp", img)


def main():
    _save("black", np.zeros((256, 256, 3), dtype=np.uint8))
    _save("white", np.full((256, 256, 3), 255, dtype=np.uint8))

    ramp_h = np.tile(np.arange(256, dtype=np.uint8), (256, 1))
    _save("ramp_h", np.stack([ramp_h, ramp_h, ramp_h], axis=2))

    ramp_v = np.tile(np.arange(256, dtype=np.uint8).reshape(256, 1), (1, 256))
    _save("ramp_v", np.stack([ramp_v, ramp_v, ramp_v], axis=2))

    yy, xx = np.indices((256, 256))
    checker = (((xx + yy) & 1) * 255).astype(np.uint8)
    _save("checker_1px", np.stack([checker, checker, checker], axis=2))

    corners = np.zeros((256, 256, 3), dtype=np.uint8)
    corners[0, 0] = corners[0, -1] = corners[-1, 0] = corners[-1, -1] = 255
    _save("corners", corners)

    rgb_bars = np.zeros((256, 256, 3), dtype=np.uint8)
    bars = [
        [255, 0, 0],
        [0, 255, 0],
        [0, 0, 255],
        [255, 255, 0],
        [0, 255, 255],
        [255, 0, 255],
        [255, 255, 255],
        [0, 0, 0],
    ]
    for i, color in enumerate(bars):
        rgb_bars[:, i * 32:(i + 1) * 32] = color
    _save("rgb_bars", rgb_bars)

    rng = np.random.default_rng(2026)
    noise = rng.integers(0, 256, size=(256, 256, 3), dtype=np.uint8)
    _save("noise", noise)


if __name__ == "__main__":
    main()
