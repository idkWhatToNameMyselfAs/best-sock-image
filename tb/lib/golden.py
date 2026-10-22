from __future__ import annotations

import math
from typing import Iterable

import numpy as np

from tb.lib import regmap


def decode_row(word: int):
    def sx5(v: int) -> int:
        return v - 32 if v & 0x10 else v

    c0 = sx5(word & 0x1F)
    c1 = sx5((word >> 8) & 0x1F)
    c2 = sx5((word >> 16) & 0x1F)
    return [c0, c1, c2]


def encode_row(c0: int, c1: int, c2: int):
    def ux5(v: int) -> int:
        return v & 0x1F

    return ux5(c0) | (ux5(c1) << 8) | (ux5(c2) << 16)


def cfg_from_regs(values: dict[str, int]):
    regs = {k: regmap.RESET.get(k, 0) for k in regmap.ADDR.keys()}
    regs.update({k.upper(): v for k, v in values.items()})
    cfg = {
        "gray": bool(regs.get("COLOR", 0) & 0x1),
        "k1": np.array([
            decode_row(regs.get("K1_ROW0", 0)),
            decode_row(regs.get("K1_ROW1", 0)),
            decode_row(regs.get("K1_ROW2", 0)),
        ], dtype=np.int64),
        "k1_shift": int(regs.get("K1_SHIFT", 0) & 0x7),
        "k2": np.array([
            decode_row(regs.get("K2_ROW0", 0)),
            decode_row(regs.get("K2_ROW1", 0)),
            decode_row(regs.get("K2_ROW2", 0)),
        ], dtype=np.int64),
        "k2_shift": int(regs.get("K2_SHIFT", 0) & 0x7),
        "mode": int(regs.get("COMBINE", 0) & 0x3),
        "invert": bool((regs.get("COMBINE", 0) >> 4) & 0x1),
    }
    return cfg


def _to_gray(img: np.ndarray):
    r = img[:, :, 0].astype(np.int64)
    g = img[:, :, 1].astype(np.int64)
    b = img[:, :, 2].astype(np.int64)
    y = (77 * r + 150 * g + 29 * b + 128) >> 8
    out = np.stack((y, y, y), axis=2)
    return out.astype(np.int64)


def _kernel(img: np.ndarray, k: np.ndarray, shift: int):
    h, w, _ = img.shape
    pad = np.pad(img.astype(np.int64), ((1, 1), (1, 1), (0, 0)), mode="edge")
    out = np.zeros((h, w, 3), dtype=np.int64)
    for yy in range(h):
        for xx in range(w):
            for rr in range(3):
                for cc in range(3):
                    out[yy, xx] += k[rr, cc] * pad[yy + rr, xx + cc]
    if shift > 0:
        out = (out + (1 << (shift - 1))) >> shift
    return out


def _clamp_rgb(v: np.ndarray):
    return np.clip(v, 0, 255).astype(np.uint8)


def run(img: np.ndarray, cfg: dict[str, object]):
    work = img.astype(np.int64)
    if cfg["gray"]:
        work = _to_gray(img)
    a = _kernel(work, cfg["k1"], int(cfg["k1_shift"]))
    b = _kernel(work, cfg["k2"], int(cfg["k2_shift"]))
    mode = int(cfg["mode"])
    if mode == 0:
        v = a
    elif mode == 1:
        v = np.abs(a)
    elif mode == 2:
        v = np.abs(a) + np.abs(b)
    elif mode == 3:
        v = np.zeros_like(a)
        for idx in np.ndindex(a.shape):
            av = int(a[idx])
            bv = int(b[idx])
            v[idx] = math.isqrt(av * av + bv * bv)
    else:
        v = a
    out = _clamp_rgb(v)
    if cfg["invert"]:
        out = (255 - out).astype(np.uint8)
    return out
