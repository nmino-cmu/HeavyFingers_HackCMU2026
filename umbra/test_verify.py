#!/usr/bin/env python3
"""Live sign-in verify: roster 752886 + real Vultr face L2."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

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


def test_load_live():
    from umbra.live_person import live_id
    from umbra.verify import load_person

    pid = live_id()
    if not pid:
        print("LIVE_PROFILE skip (empty roster)")
        return
    ctx, evk, faces, voices = load_person(pid)
    check(len(faces) >= 3, len(faces))
    check(len(voices) >= 1, len(voices))
    check(len(evk) > 1000, len(evk))
    check(ctx.has_secret_key(), "sk stays on mac")


def test_split_take():
    from umbra.verify import split_take

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
    frame, audio, wav, src = split_take(open(mp4, "rb").read())
    check(frame and frame[:2] == b"\xff\xd8", "jpeg frame")
    check(audio and audio[:4] == b"RIFF", "wav")
    check(wav and os.path.isfile(wav), wav)
    check(src and os.path.isfile(src), src)


def test_wave_from_l2s():
    from umbra.verify import wave_from_l2s

    check(not wave_from_l2s([20, 20, 20]), "photo / no wave")
    check(not wave_from_l2s([20, 300, 300]), "filter drop — never you again")
    check(not wave_from_l2s([300, 300, 300]), "never you")
    check(wave_from_l2s([20, 300, 25]), "you — occlude — you")
    check(wave_from_l2s([15, 18, 400, 999, 22]), "multi-frame wave")
    check(not wave_from_l2s([]), "empty")


def test_vultr_face_uses_profile():
    os.environ.setdefault("UMBRA_WORKER_URL", "http://207.246.126.149:8080")
    from umbra.enroll_extract import image_to_grid
    from umbra.face_ckks import decrypt_l2, encrypt_vec, pack_face
    from umbra.live_person import live_id
    from umbra.verify import _post, load_person

    pid = live_id()
    if not pid:
        print("VULTR_FACE skip (empty roster)")
        return
    ctx, evk, faces, _voices = load_person(pid)
    td = tempfile.mkdtemp()
    bmp = os.path.join(td, "g.bmp")
    # 64x64 gray via sips from a tiny ppm
    ppm = os.path.join(td, "g.ppm")
    open(ppm, "wb").write(b"P6\n64 64\n255\n" + b"\x40\x40\x40" * 4096)
    subprocess.check_call(["sips", "-s", "format", "jpeg", ppm, "--out", os.path.join(td, "g.jpg")], stdout=subprocess.DEVNULL)
    probe = encrypt_vec(ctx, image_to_grid(open(os.path.join(td, "g.jpg"), "rb").read()))
    body = pack_face(evk, faces[0], probe)
    out = _post("/face", body, timeout=120)
    l2 = decrypt_l2(ctx, out)
    check(l2 >= 0, l2)
    check(l2 > 200, "gray must not match live face")
    print("VULTR_FACE_L2", l2, "profile", pid)


def main():
    test_load_live()
    test_split_take()
    test_wave_from_l2s()
    test_vultr_face_uses_profile()
    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
