from __future__ import annotations

import struct
from pathlib import Path

import numpy as np

WIDTH = 256
HEIGHT = 256
BPP = 24
HEADER_SIZE = 54
PIXELS_SIZE = WIDTH * HEIGHT * 3
FILE_SIZE = HEADER_SIZE + PIXELS_SIZE


class BmpError(ValueError):
    pass


def read_bmp(path: str | Path) -> np.ndarray:
    data = Path(path).read_bytes()
    if len(data) != FILE_SIZE:
        raise BmpError(f"Unexpected BMP size: {len(data)}")
    if data[:2] != b"BM":
        raise BmpError("Invalid BMP signature")

    file_size = struct.unpack_from("<I", data, 2)[0]
    pixel_offset = struct.unpack_from("<I", data, 10)[0]
    dib_size = struct.unpack_from("<I", data, 14)[0]
    width = struct.unpack_from("<i", data, 18)[0]
    height = struct.unpack_from("<i", data, 22)[0]
    planes = struct.unpack_from("<H", data, 26)[0]
    bpp = struct.unpack_from("<H", data, 28)[0]
    compression = struct.unpack_from("<I", data, 30)[0]
    image_size = struct.unpack_from("<I", data, 34)[0]

    if file_size != FILE_SIZE:
        raise BmpError("Invalid file size field")
    if dib_size != 40:
        raise BmpError("Unsupported DIB header")
    if width != WIDTH or abs(height) != HEIGHT:
        raise BmpError("Unsupported image dimensions")
    if planes != 1 or bpp != BPP:
        raise BmpError("Unsupported pixel format")
    if compression != 0:
        raise BmpError("Compressed BMP not supported")
    if image_size not in (0, PIXELS_SIZE):
        raise BmpError("Invalid pixel payload size")
    if pixel_offset != HEADER_SIZE:
        raise BmpError("Unsupported pixel offset")

    payload = data[HEADER_SIZE:HEADER_SIZE + PIXELS_SIZE]
    arr = np.frombuffer(payload, dtype=np.uint8).reshape(HEIGHT, WIDTH, 3)
    arr = arr[:, :, ::-1]
    if height > 0:
        arr = arr[::-1]
    return arr.copy()


def write_bmp(path: str | Path, img: np.ndarray) -> None:
    arr = np.asarray(img, dtype=np.uint8)
    if arr.shape != (HEIGHT, WIDTH, 3):
        raise BmpError(f"Expected shape {(HEIGHT, WIDTH, 3)}, got {arr.shape}")

    bgr_bottom_up = arr[::-1, :, ::-1]
    header = bytearray(HEADER_SIZE)
    header[0:2] = b"BM"
    struct.pack_into("<I", header, 2, FILE_SIZE)
    struct.pack_into("<I", header, 10, HEADER_SIZE)
    struct.pack_into("<I", header, 14, 40)
    struct.pack_into("<i", header, 18, WIDTH)
    struct.pack_into("<i", header, 22, HEIGHT)
    struct.pack_into("<H", header, 26, 1)
    struct.pack_into("<H", header, 28, BPP)
    struct.pack_into("<I", header, 30, 0)
    struct.pack_into("<I", header, 34, PIXELS_SIZE)

    Path(path).write_bytes(bytes(header) + bgr_bottom_up.tobytes())


def to_stream(img: np.ndarray):
    arr = np.asarray(img, dtype=np.uint8)
    if arr.shape != (HEIGHT, WIDTH, 3):
        raise ValueError("Expected 256x256x3 image")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = (int(v) for v in arr[y, x])
            tdata = (r << 16) | (g << 8) | b
            idx = y * WIDTH + x
            yield tdata, int(idx == 0), int(x == WIDTH - 1)


def from_stream(words):
    out = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for idx, (tdata, _tuser, _tlast) in enumerate(words):
        if idx >= WIDTH * HEIGHT:
            raise ValueError("Too many stream words")
        y, x = divmod(idx, WIDTH)
        out[y, x, 0] = (int(tdata) >> 16) & 0xFF
        out[y, x, 1] = (int(tdata) >> 8) & 0xFF
        out[y, x, 2] = int(tdata) & 0xFF
    if len(words) != WIDTH * HEIGHT:
        raise ValueError("Not enough stream words")
    return out
