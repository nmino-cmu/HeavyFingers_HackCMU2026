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
    silent = os.path.join(td, "v.mp4")
    wav_in = os.path.join(td, "a.wav")
    subprocess.check_call(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=gray:s=320x240:d=1", "-an", "-pix_fmt", "yuv420p", silent],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.check_call(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=f=440:d=1", "-ac", "1", "-ar", "16000", wav_in],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    frame2, audio2, wav2, _src2 = split_take(open(silent, "rb").read())
    check(audio2 is None, "video-only take has no audio")
    frame3, audio3, wav3, _src3 = split_take(open(silent, "rb").read(), open(wav_in, "rb").read())
    check(frame3 and audio3 and audio3[:4] == b"RIFF", "sidecar mic becomes wav")
    check(wav3 and os.path.isfile(wav3), wav3)
    quiet = os.path.join(td, "quiet.mp4")
    loud = os.path.join(td, "loud.wav")
    subprocess.check_call(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=gray:s=320x240:d=2",
            "-f", "lavfi", "-i", "aevalsrc=0:d=2",
            "-shortest", "-pix_fmt", "yuv420p", quiet,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.check_call(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=f=440:d=2", "-ac", "1", "-ar", "16000", loud],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _f4, audio4, _w4, _s4 = split_take(open(quiet, "rb").read(), open(loud, "rb").read())
    from umbra.enroll_extract import wav_pcm

    samples, rate = wav_pcm(audio4)
    peak = max(abs(s) for s in samples) / 32768.0
    check(peak > 0.1, f"quiet mux must not beat loud sidecar peak={peak}")


def test_wave_from_l2s():
    from umbra.verify import wave_from_l2s

    check(not wave_from_l2s([20, 20, 20]), "photo / no wave")
    check(wave_from_l2s([20, 300, 300]), "you then cover")
    check(not wave_from_l2s([300, 300, 300]), "never you")
    check(wave_from_l2s([20, 300, 25]), "you — occlude — you")
    check(wave_from_l2s([15, 18, 400, 999, 22]), "multi-frame wave")
    check(not wave_from_l2s([]), "empty")
    check(wave_from_l2s([343, 343, 120, 118, 110, 122]), "cover first then you")
    from umbra.verify import _hand_on_face

    face = {"x": 0.3, "y": 0.2, "w": 0.3, "h": 0.4}
    check(_hand_on_face(face, [{"cx": 0.18, "cy": 0.4}]), "hand just outside the face box is a wave")
    check(not _hand_on_face(face, [{"cx": 0.0, "cy": 0.99}]), "hand in the corner is not a wave")
    src = open(os.path.join(ROOT, "umbra/verify.py"), encoding="utf-8").read()
    check("grid_for_enroll" in src, "verify uses the enroll crop")
    check("len(good) >= 1" in src, "one matching frame is enough")
    check("FACE_CALLS" in src and "FACE_FRAME_N" in src, "same /face budget, more samples")
    check("qa_voice(audio)" in src, "verify refuses short voice")
    check("_clip_dur" in src and "_hand_on_face" in src, "wave spans the take; hand cover is local")


def test_take_frames_dense():
    from umbra.verify import take_frames

    td = tempfile.mkdtemp()
    mp4 = os.path.join(td, "t.mp4")
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=gray:s=320x240:d=3",
            "-pix_fmt", "yuv420p", mp4,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    frames = take_frames(mp4)
    check(len(frames) >= 16, f"dense samples {len(frames)}")
    check(all(f[:2] == b"\xff\xd8" for f in frames), "jpegs")
    long = os.path.join(td, "long.mp4")
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=gray:s=320x240:d=12",
            "-pix_fmt", "yuv420p", long,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    wide = take_frames(long)
    check(len(wide) >= 20, f"12s take must be sampled end-to-end {len(wide)}")
    # last 2s white, first 10s black — wave lives at the end; at least 6 samples must be from there
    endy = os.path.join(td, "end.mp4")
    subprocess.check_call(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=black:s=160x120:d=10",
            "-f", "lavfi", "-i", "color=c=white:s=160x120:d=2",
            "-filter_complex", "[0][1]concat=n=2:v=1:a=0",
            "-pix_fmt", "yuv420p", endy,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    end_frames = take_frames(endy)
    whites = 0
    jp = os.path.join(td, "one.jpg")
    raw = os.path.join(td, "one.gray")
    for jpeg in end_frames:
        open(jp, "wb").write(jpeg)
        subprocess.check_call(
            ["ffmpeg", "-y", "-i", jp, "-vf", "scale=8:8,format=gray", "-f", "rawvideo", raw],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        px = open(raw, "rb").read()
        if px and (sum(px) / len(px)) > 80:
            whites += 1
    check(whites >= 6, f"end-of-take wave samples {whites}/{len(end_frames)}")


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
    check(l2 > 220, "gray must not match live face")
    print("VULTR_FACE_L2", l2, "profile", pid)


def test_voice_thresh_rejects_other_talker():
    # 490603 face-pass take L2 0.053; last take (other talker, face 377) L2 0.093.
    from umbra.verify import VOICE_L2_MAX

    check(0.053 < VOICE_L2_MAX, VOICE_L2_MAX)
    check(VOICE_L2_MAX < 0.093, VOICE_L2_MAX)


def test_voice_stricter_when_face_fails():
    from umbra.verify import VOICE_L2_MAX, apply_voice_after_face, voice_max

    check(voice_max(True) == VOICE_L2_MAX, "face ok keeps voice bar")
    check(voice_max(False) < VOICE_L2_MAX, "face fail tightens voice")
    mid = (voice_max(False) + VOICE_L2_MAX) / 2
    jobs = {"face": {"ok": False}, "voice": {"ok": True, "l2": mid, "max": VOICE_L2_MAX}}
    apply_voice_after_face(jobs)
    check(not jobs["voice"]["ok"], mid)
    jobs2 = {"face": {"ok": True}, "voice": {"ok": True, "l2": mid, "max": VOICE_L2_MAX}}
    apply_voice_after_face(jobs2)
    check(jobs2["voice"]["ok"], mid)


def main():
    test_load_live()
    test_split_take()
    test_wave_from_l2s()
    test_take_frames_dense()
    test_voice_thresh_rejects_other_talker()
    test_voice_stricter_when_face_fails()
    test_vultr_face_uses_profile()
    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
