"""Local .xyt crop → fixed vector + cleartext match bit. Worker must not import this."""
from __future__ import annotations

N_MIN = 16
DIM = N_MIN * 3
# match if sum((p-t)^2) < T on unit-scaled coords
THRESH = 4.0
# TFHE ints 0..20 so sum of squares stays < 16-bit for the compare TLU
SCALE = 20
THRESH_INT = int(THRESH * SCALE * SCALE)  # 1600


def parse_xyt(text: str) -> list[float]:
    pts = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.replace(",", " ").split()
        if len(parts) < 3:
            continue
        x, y, th = float(parts[0]), float(parts[1]), float(parts[2])
        pts.append((x / 500.0, y / 500.0, th / 360.0))
        if len(pts) == N_MIN:
            break
    while len(pts) < N_MIN:
        pts.append((0.0, 0.0, 0.0))
    out = []
    for x, y, th in pts:
        out.extend([x, y, th])
    return out


def dist2(a, b) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def match_bit(probe, tmpl) -> int:
    return int(dist2(probe, tmpl) < THRESH)


def to_int(vec) -> list[int]:
    """0..SCALE ints for TFHE. dist_int < THRESH_INT ↔ dist_float < THRESH."""
    return [max(0, min(SCALE, int(round(x * SCALE)))) for x in vec]
