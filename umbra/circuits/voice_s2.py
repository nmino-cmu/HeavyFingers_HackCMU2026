"""TinyS2: 16-D log-mel band means. No fat CNN. S11/S14 stay in P3 choreo."""
from __future__ import annotations

import math

MEL_N = 64
VEC_N = 16
# ponytail: enrolled template is compiled Linear weights; encrypt-enroll if S16 two-input lands
THRESH = 0.30


def make_mel(kind: str):
    """Deterministic 64×64 log-mel crop (Mac-side). Never upload this grid."""
    n = MEL_N
    floor = 0.04
    mel = [[floor for _ in range(n)] for _ in range(n)]
    if kind == "A":
        bands = range(0, 16)
    elif kind == "B":
        bands = range(48, 64)
    else:
        raise KeyError(kind)
    for t in range(n):
        for b in bands:
            mel[b][t] = 0.92 + 0.04 * ((t + b) % 5) / 4.0
    return mel


def band_vec(mel):
    """Mean each 4-band group over time → 16 floats."""
    n = len(mel)
    width = n // VEC_N
    out = []
    for i in range(VEC_N):
        acc = 0.0
        cnt = 0
        for b in range(i * width, (i + 1) * width):
            row = mel[b]
            acc += sum(row)
            cnt += n
        out.append(acc / cnt)
    return out


def l2norm(v):
    s = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / s for x in v]


def enrolled_weight():
    return l2norm(band_vec(make_mel("A")))


def query_vec(kind: str):
    return l2norm(band_vec(make_mel(kind)))


def reference_s2(vec):
    """Cleartext S2 bit. Not imported by the worker."""
    w = enrolled_weight()
    score = sum(a * b for a, b in zip(vec, w))
    return [int(score >= THRESH)]


MEL_A = make_mel("A")
MEL_B = make_mel("B")
VEC_A = query_vec("A")
VEC_B = query_vec("B")


def _selfcheck():
    assert len(MEL_A) == MEL_N and len(MEL_A[0]) == MEL_N
    assert len(VEC_A) == VEC_N
    assert reference_s2(VEC_A) == [1], reference_s2(VEC_A)
    assert reference_s2(VEC_B) == [0], reference_s2(VEC_B)
    assert sum(a * b for a, b in zip(VEC_A, VEC_B)) < THRESH


if __name__ == "__main__":
    _selfcheck()
    print("voice_s2 ok", reference_s2(VEC_A), reference_s2(VEC_B))
