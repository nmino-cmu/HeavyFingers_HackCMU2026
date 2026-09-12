"""Public video card (clear, Mac). Whisper stays on this machine."""
from __future__ import annotations

import os
import random
import sys

WORDS = (
    "the lazy dog fox am is hack win project asterisk "
    "quick brown jumps over cmu lattice cipher nonce"
).split()
HANDS = ("left", "right")
SIDES = ("left", "right")
ENDS = ("pinky", "index", "thumb")

_model = None


def generate(rng: random.Random | None = None) -> dict:
    r = rng or random.Random()
    n = r.randint(8, 12)
    nonce = " ".join(r.sample(WORDS, n))
    return {
        "say": nonce,
        "nonce": nonce,
        "hand": r.choice(HANDS),
        "motion": "clench_unclench",
        "where": "in_front_of_face",
        "side": r.choice(SIDES),
        "end": r.choice(ENDS),
    }


generate_card = generate


def render(card: dict) -> str:
    return (
        f"say:    {card['say']}\n"
        f"hand:   {card['hand']}\n"
        f"motion: {card['motion']}\n"
        f"where:  {card['where']}\n"
        f"side:   {card['side']}\n"
        f"end:\n"
    )


def transcribe(audio_path: str) -> str:
    """Whisper on the Mac. Never called from the worker."""
    global _model
    import whisper

    if _model is None:
        name = os.environ.get("UMBRA_WHISPER_MODEL", "tiny.en")
        _model = whisper.load_model(name)
    return _model.transcribe(
        str(audio_path),
        language="en",
        temperature=0,
        condition_on_previous_text=False,
    )["text"]


def main(argv=None) -> int:
    print(render(generate()), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
