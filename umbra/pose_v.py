"""Build the 75-D choreo crop from Vision frames + wav. Local only."""
from __future__ import annotations

import math
from pathlib import Path
import tempfile

from umbra.enroll_extract import wav_pcm
from umbra.face_qa import inspect_paths

N = 32


def extract_frames(video: Path, n: int = N) -> list[Path]:
    td = Path(tempfile.mkdtemp(prefix="umbra-pose-"))
    dst = td / "f%02d.jpg"
    import subprocess

    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video), "-vf", "fps=8", "-frames:v", str(n), str(dst)],
        capture_output=True,
    )
    return sorted(td.glob("f*.jpg"))


def _speech_mask(wav: bytes) -> list[float]:
    try:
        samples, rate = wav_pcm(wav)
    except Exception:
        return [0.0] * N
    step = max(1, len(samples) // N)
    out = []
    peak = max((abs(s) for s in samples), default=1) or 1
    thr = 0.08 * peak
    for i in range(N):
        chunk = samples[i * step : (i + 1) * step] or [0]
        rms = math.sqrt(sum(s * s for s in chunk) / len(chunk))
        out.append(1.0 if rms > thr else 0.0)
    return out


def _pad(rows: list[dict], n: int = N) -> list[dict]:
    if not rows:
        return [{"faces": [], "hands": []} for _ in range(n)]
    if len(rows) >= n:
        return rows[:n]
    out = list(rows)
    while len(out) < n:
        out.append(rows[-1])
    return out


def v_from_take(video: Path, wav: bytes, card: dict | None = None) -> list[float]:
    frames = extract_frames(video)
    rows = _pad(inspect_paths([str(p) for p in frames]))
    speech = _speech_mask(wav)
    openness, iou, dxs, mouths = [], [], [], []
    right_hits = 0
    hands_n = 0
    faces_n = 0
    thumb = index = pinky = 0.0
    end_span = 0.0
    for i, row in enumerate(rows):
        faces = row.get("faces") or []
        hands = row.get("hands") or []
        faces_n = max(faces_n, len(faces))
        hands_n = max(hands_n, len(hands))
        face = max(faces, key=lambda f: f["w"] * f["h"]) if faces else None
        hand = max(hands, key=lambda h: h.get("span", 0)) if hands else None
        openness.append(float(hand["open"]) if hand else 0.12)
        if hand and hand.get("chirality") == "right":
            right_hits += 1
        if hand and face:
            fx = face["x"] + face["w"] / 2
            # selfie: user's IRL right is the left of the raw frame
            dxs.append(-(hand["cx"] - fx))
            # crude box IoU of face vs a square around the hand
            hx, hy, hs = hand["cx"] - 0.12, hand["cy"] - 0.12, 0.24
            x0 = max(face["x"], hx)
            y0 = max(face["y"], hy)
            x1 = min(face["x"] + face["w"], hx + hs)
            y1 = min(face["y"] + face["h"], hy + hs)
            inter = max(0, x1 - x0) * max(0, y1 - y0)
            union = face["w"] * face["h"] + hs * hs - inter
            iou.append(inter / union if union else 0.0)
        else:
            dxs.append(0.0)
            iou.append(0.0)
        mouths.append(float(face["mouth"]) if face else 0.0)
        if i >= N - 6 and hand:
            end_span = max(end_span, float(hand.get("span") or 0))
            thumb = max(thumb, float(hand.get("thumb") or 0))
            index = max(index, float(hand.get("index") or 0))
            pinky = max(pinky, float(hand.get("pinky") or 0))
    handed = right_hits / max(1, sum(1 for r in rows if r.get("hands")))
    dx = sum(dxs) / max(1, len(dxs))
    iou_m = sum(iou) / max(1, len(iou))
    digit_sum = thumb + index + pinky or 1.0
    digit = [pinky / digit_sum, index / digit_sum, thumb / digit_sum]
    # av: mouth vs speech correlation
    if any(speech) and any(mouths):
        ms = sum(speech) / N
        mm = sum(mouths) / N
        num = sum((speech[i] - ms) * (mouths[i] - mm) for i in range(N))
        den = math.sqrt(
            sum((speech[i] - ms) ** 2 for i in range(N)) * sum((mouths[i] - mm) ** 2 for i in range(N))
        ) or 1.0
        av = max(0.0, min(1.0, 0.5 + 0.5 * num / den))
    else:
        av = 0.4
    early = sum(speech[:16])
    late_close = end_span
    order = 1.0 if early >= 2 and late_close > 0.25 else 0.0
    v = [handed]
    v += openness
    v += [iou_m, dx]
    v += speech
    v += [end_span]
    v += digit
    v += [float(faces_n), float(hands_n), av, order]
    assert len(v) == 75
    return v
