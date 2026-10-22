import argparse
from pathlib import Path

from PIL import Image
import numpy as np

from tb.lib.bmp import write_bmp


def convert(src: Path, dst: Path):
    img = Image.open(src).convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side)).resize((256, 256), Image.Resampling.LANCZOS)
    arr = np.array(img, dtype=np.uint8)
    write_bmp(dst, arr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    args = ap.parse_args()
    convert(Path(args.src), Path(args.dst))


if __name__ == "__main__":
    main()
