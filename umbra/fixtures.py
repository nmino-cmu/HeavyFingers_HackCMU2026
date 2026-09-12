"""Shared Umbra fixtures. Pure numpy-free stdlib where possible; reference() uses math only."""
from __future__ import annotations

import math

N = 32
# handedness, openness[32], iou, dx, speech[32], end_finger, digit[3], n_faces, n_hands, av_sync, order_ok
V_OK = [0.9137]
V_OK += [0.5 + 0.45 * math.sin(2 * math.pi * 2 * t / N) for t in range(N)]
V_OK += [0.4271, 0.1873]
V_OK += [1.0 if 2 <= t < 26 else 0.0 for t in range(N)]
V_OK += [0.7319, 1.0, 0.0, 0.0, 1.0, 1.0, 0.6127, 1.0]
assert len(V_OK) == 75

CARD_RRP = {"hand": "right", "side": "right", "end": "pinky"}
IDX = {"S5": 0, "S6": 1, "S7": 2, "S8": 3, "S9": 4, "S10": 5, "S11": 6, "S12": 7, "S13": 8, "S14": 9}
REF_OK = [1] * 10


def _clone():
    return list(V_OK)


def mutant(name):
    v = _clone()
    if name == "V_LEFT":
        v[0] = 0.0863
    elif name == "V_FIST":
        v[1:33] = [0.12] * N
    elif name == "V_ONECYCLE":
        v[1:33] = [0.5 + 0.45 * math.sin(2 * math.pi * t / N) for t in range(N)]
    elif name == "V_RAMP":
        v[1:33] = [0.1 + 0.8 * t / (N - 1) for t in range(N)]
    elif name == "V_FAR":
        v[33] = 0.0213
    elif name == "V_WRONGSIDE":
        v[34] = -0.1873
    elif name == "V_TALKTHENMOVE":
        v[35:67] = [1.0 if 0 <= t < 12 else 0.0 for t in range(N)]
        v[1:33] = [0.5 + (0.4 if 16 <= t < 32 else 0.0) for t in range(N)]
    elif name == "V_NOZOOM":
        v[67] = 0.1187
    elif name == "V_INDEX":
        v[68:71] = [0.0, 1.0, 0.0]
    elif name == "V_REVERSE":
        v[1:33] = list(reversed(v[1:33]))
    elif name == "V_TWOFACES":
        v[71] = 2.0
    elif name == "V_NOHANDS":
        v[72] = 0.0
    elif name == "V_DUB":
        v[73] = 0.0421
    else:
        raise KeyError(name)
    return v


MUTANTS = [
    "V_LEFT",
    "V_FIST",
    "V_ONECYCLE",
    "V_RAMP",
    "V_FAR",
    "V_WRONGSIDE",
    "V_TALKTHENMOVE",
    "V_NOZOOM",
    "V_INDEX",
    "V_REVERSE",
    "V_TWOFACES",
    "V_NOHANDS",
    "V_DUB",
]


def reference(v, card):
    """Cleartext bits. Not imported by the worker."""
    h, openness, iou, dx = v[0], v[1:33], v[33], v[34]
    speech, endf = v[35:67], v[67]
    digit, nf, nh, av, order = v[68:71], v[71], v[72], v[73], v[74]
    want_right = card.get("hand") == "right"
    s5 = int((h >= 0.5) == want_right)
    # two peaks two troughs via sign changes of derivative
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
