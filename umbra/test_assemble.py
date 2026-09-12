#!/usr/bin/env python3
"""Assemble AND: omit missing farm lanes; do not require every box."""
import os
import sys

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.assemble import LABELS, merge_bits, run
from umbra.decide import decide

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def main():
    f, loc = merge_bits([([1] * 10, [1] * 10), (None, None), ([1], [1]), ([1], [1])])
    check(f == [1] * 12, f)
    check(loc == [1] * 12, loc)
    check(decide(f, loc, True).ok, "all-1 plus omitted print")
    check(not decide([1, 0], [1, 0], True).ok, "zero farm bit fails")
    check(decide([1, None], [1, None], True).ok, "None omitted")
    check(len(LABELS) == 16, LABELS)
    from umbra.assemble import SAMPLES, run_lane

    check([s["id"] for s in SAMPLES] == ["choreo", "print", "voice", "face", "bid", "words"], SAMPLES)
    w = run_lane("words")
    check(w["ok"] and w["bits"] == [1], w)
    if os.environ.get("UMBRA_ASSEMBLE_LIVE") == "1":
        d, payload = run()
        check(payload["lanes"]["choreo"] is not None, f"choreo lane {payload['lanes']}")
        check(len(payload["bits"]) == 16, payload["bits"])
        check(d.ok or payload["lanes"]["choreo"] == [1] * 10, f"choreo {payload}")
        if all(payload["lanes"][k] == [1] for k in ("voice", "face", "bid") if payload["lanes"][k] is not None):
            check(payload["lanes"]["choreo"] == [1] * 10, "choreo all-1")
            check(d.ok, f"live AND {payload}")
        print("lanes", payload["lanes"])
    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
