#!/usr/bin/env python3
"""Same-vs-other separation + one Vultr /face timing. Not a biometric cert."""
from __future__ import annotations

import io
import math
import os
import struct
import sys
import time
import wave

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def _tone(freq, seconds, rate=16000) -> bytes:
    n = int(rate * seconds)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        frames = bytearray()
        for i in range(n):
            frames += struct.pack("<h", int(12000 * math.sin(2 * math.pi * freq * i / rate)))
        w.writeframes(bytes(frames))
    return buf.getvalue()


def _l2(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def test_voice_fft():
    from umbra.enroll_extract import qa_voice, wav_to_voice

    a = wav_to_voice(_tone(220, 0.8))
    b = wav_to_voice(_tone(220, 1.6))
    c = wav_to_voice(_tone(440, 0.8))
    same = _l2(a, b)
    other = _l2(a, c)
    check(len(a) == 16, len(a))
    check(abs(sum(x * x for x in a) - 1) < 1e-3, a)
    check(same < 0.15, f"same-tone L2 {same}")
    check(other > same * 4, f"sep voice same={same:.4f} other={other:.4f}")
    q = qa_voice(_tone(220, 0.4), min_s=6)
    check(not q["ok"], q)
    q2 = qa_voice(_tone(220, 7.0), min_s=6)
    check(q2["ok"], q2)
    print(f"VOICE_L2 same_tone={same:.4f} other_octave={other:.4f} thresh=1.2")
    return same, other


def test_face_pixel_l2():
    from umbra.enroll_extract import FACE_N

    n = FACE_N * FACE_N
    a = [(((i * 17 + 9) % 251) / 255.0) for i in range(n)]
    b = [min(1.0, x + 0.03) for x in a]
    c = [((i * 41 + 3) % 197) / 255.0 for i in range(n)]
    same = _l2(a, b)
    other = _l2(a, c)
    check(same < 90, same)
    check(other > same * 3, (same, other))
    print(f"FACE_L2 same_+3pct={same:.1f} other_pattern={other:.1f} thresh=90")
    return same, other


def test_pose_v_len():
    import subprocess
    import tempfile
    from umbra.pose_v import v_from_take

    td = tempfile.mkdtemp()
    mp4 = os.path.join(td, "t.mp4")
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=gray:s=320x240:d=1",
            "-f", "lavfi", "-i", "sine=f=440:d=1", "-shortest", "-pix_fmt", "yuv420p", mp4,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    v = v_from_take(mp4, open(mp4, "rb").read(), {"hand": "right", "side": "right", "end": "pinky"})
    check(len(v) == 75, len(v))


def test_vultr_face_ms():
    os.environ.setdefault("UMBRA_WORKER_URL", "http://207.246.126.149:8080")
    from umbra.enroll_extract import FACE_N
    from umbra.face_ckks import decrypt_l2, encrypt_vec, new_context, pack_face, evk_bytes
    from umbra.verify import _post

    n = FACE_N * FACE_N
    a = [(((i * 17 + 9) % 251) / 255.0) for i in range(n)]
    b = [min(1.0, x + 0.03) for x in a]
    c = [((i * 41 + 3) % 197) / 255.0 for i in range(n)]
    ctx = new_context()
    evk = evk_bytes(ctx)
    ta = encrypt_vec(ctx, a)
    tb = encrypt_vec(ctx, b)
    tc = encrypt_vec(ctx, c)
    t0 = time.perf_counter()
    same = decrypt_l2(ctx, _post("/face", pack_face(evk, ta, tb), timeout=120))
    other = decrypt_l2(ctx, _post("/face", pack_face(evk, ta, tc), timeout=120))
    ms = int((time.perf_counter() - t0) * 1000 / 2)
    check(same < 90, f"vultr same {same}")
    check(other > same * 2, f"vultr sep {same} {other}")
    print(f"VULTR_FACE same={same:.2f} other={other:.2f} ms_per={ms}")
    return same, other, ms


def main():
    vs, vo = test_voice_fft()
    fs, fo = test_face_pixel_l2()
    test_pose_v_len()
    try:
        test_vultr_face_ms()
    except Exception as e:
        print("VULTR_FACE skip", type(e).__name__, e)
    print(f"CHECKS_RUN={CHECKS_RUN}")
    print("MARGIN voice", f"{vo/max(vs,1e-9):.1f}x", "face", f"{fo/max(fs,1e-9):.1f}x")


if __name__ == "__main__":
    main()
