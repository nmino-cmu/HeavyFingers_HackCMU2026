"""Public video card. Cleartext, Mac-only."""
from __future__ import annotations

import json
import random

HANDS = ("left", "right")
SIDES = ("left", "right")
ENDS = ("pinky", "index", "thumb")
NONCE = (
    "the lazy dog fox am is hack win project asterisk"
).split()


def generate(rng: random.Random | None = None) -> dict:
    r = rng or random.Random()
    n = 8 + r.randrange(5)
    words = [r.choice(NONCE) for _ in range(n)]
    return {
        "say": " ".join(words),
        "hand": r.choice(HANDS),
        "motion": "clench_unclench",
        "where": "in_front_of_face",
        "side": r.choice(SIDES),
        "end": r.choice(ENDS),
    }


def main():
    print(json.dumps(generate(), indent=2))


if __name__ == "__main__":
    main()
