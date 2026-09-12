"""decode_gray works without sips (Vultr / public host)."""
from __future__ import annotations

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PIL import Image
import umbra.enroll_extract as ee


def test_decode_gray_pil():
    buf = io.BytesIO()
    Image.new("RGB", (32, 24), (40, 80, 120)).save(buf, format="JPEG")
    raw = buf.getvalue()
    which = ee.shutil.which
    ee.shutil.which = lambda n: None if n == "sips" else which(n)
    try:
        w, h, px = ee.decode_gray(raw)
        g = ee.image_to_grid(raw)
    finally:
        ee.shutil.which = which
    assert w == 32 and h == 24 and len(px) == 32 * 24, (w, h, len(px))
    assert len(g) == 64 * 64, len(g)
    print("DECODE_GRAY_PIL ok")


if __name__ == "__main__":
    test_decode_gray_pil()
