"""Numpy/torch choreography floor — cleartext reference for training; card baked at compile."""
from __future__ import annotations

import math

N = 32


def bits_from_v(v, card):
    """Pure cleartext bits (0/1). Used to train the FHE surrogate."""
    h, openness, iou, dx = v[0], v[1:33], v[33], v[34]
    speech, endf = v[35:67], v[67]
    digit, nf, nh, av, order = v[68:71], v[71], v[72], v[73], v[74]
    want_right = card.get("hand") == "right"
    s5 = int((h >= 0.5) == want_right)
    d = [openness[i + 1] - openness[i] for i in range(31)]
    peaks = sum(1 for i in range(30) if d[i] > 0.02 and d[i + 1] < -0.02)
    troughs = sum(1 for i in range(30) if d[i] < -0.02 and d[i + 1] > 0.02)
    s6 = int(peaks >= 2 and troughs >= 2)
    s7 = int(iou > 0.1)
    want_pos = 1 if card.get("side") == "right" else -1
    s8 = int((1 if dx >= 0 else -1) == want_pos)
    motion = [1.0 if i and abs(openness[i] - openness[i - 1]) > 0.05 else 0.0 for i in range(32)]
    inter = sum(1 for a, b in zip(speech, motion) if a > 0.5 and b > 0.5)
    union = sum(1 for a, b in zip(speech, motion) if a > 0.5 or b > 0.5)
    s9 = int(union > 0 and inter / union > 0.2)
    s10 = int(endf > 0.4)
    end_name = card.get("end", "pinky")
    oh = {"pinky": 0, "index": 1, "thumb": 2}[end_name]
    s11 = int(digit[oh] >= 0.5)
    s12 = int(order >= 0.5)
    s13 = int(nf == 1 and nh == 1)
    s14 = int(av > 0.3)
    return [s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]


def training_rows(card, fixtures_module):
    """Build (X, y) for compile from fixtures + mutants (exact fit)."""
    rows_x, rows_y = [], []
    base = [fixtures_module.V_OK] + [fixtures_module.mutant(m) for m in fixtures_module.MUTANTS]
    for v in base:
        rows_x.append(v)
        rows_y.append(bits_from_v(v, card))
    return rows_x, rows_y
