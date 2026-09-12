"""Sign-in verify: crop on the Mac, FHE on Vultr, decrypt here.

Sends stored roster cts plus a fresh aligned probe. No plaintext media to Vultr.
"""
from __future__ import annotations

import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import tempfile

import tenseal as ts

from umbra.enroll_extract import wav_to_voice
from umbra.face_ckks import decrypt_l2, encrypt_vec, pack_face
from umbra.live_person import live_id
from umbra.roster import Roster, unpack_record
from umbra.s1 import s1

HERE = Path(__file__).resolve().parent
os.environ.setdefault("UMBRA_WORKER_URL", "http://207.246.126.149:8080")
os.environ.setdefault("UMBRA_KEY_DIR", str(HERE / "enroll_keys" / "_circuit"))

# After Vision-align + FFT voice. Old 752886 enroll (unaligned / time-RMS) will miss — re-enroll.
FACE_L2_MAX = float(os.environ.get("UMBRA_FACE_L2_MAX", "90"))
VOICE_L2_MAX = float(os.environ.get("UMBRA_VOICE_L2_MAX", "1.2"))
# ponytail: occlusion = FHE L2 vs enroll, not a hand net. Recover-as-you is the filter-drop check.
OCCLUDE_L2 = float(os.environ.get("UMBRA_OCCLUDE_L2", "140"))
NO_FACE_L2 = 999.0

LANES = ("face", "voice", "words", "wave")


def wave_from_l2s(scores, match=None, occlude=None) -> bool:
    """You, then a miss (hand / cover), then you again. Still photo and filter-drop fail."""
    match = FACE_L2_MAX if match is None else match
    occlude = OCCLUDE_L2 if occlude is None else occlude
    saw_me = False
    saw_miss = False
    for s in scores:
        if s is None:
            st = "miss"
        elif s < match:
            st = "me"
        elif s >= occlude:
            st = "miss"
        else:
            continue
        if st == "me":
            if saw_miss:
                return True
            saw_me = True
        elif st == "miss" and saw_me:
            saw_miss = True
    return False


def _post(path: str, body: bytes, timeout: int = 600) -> bytes:
    from umbra.assemble import post

    return post(path, body, timeout=timeout)


def load_person(pid: str = ""):
    pid = pid or live_id()
    if not pid:
        raise ValueError("enroll first")
    rec = unpack_record(Roster(HERE / "roster_data").get(pid))
    ctx = ts.context_from((HERE / "enroll_keys" / pid / "ctx.bin").read_bytes())
    evk = (HERE / "enroll_keys" / pid / "evk.bin").read_bytes()
    faces = [b for k, _n, b in rec["items"] if k == "face"]
    voices = [b for k, _n, b in rec["items"] if k == "voice"]
    if not faces or not voices:
        raise ValueError("roster missing face or voice ct")
    return ctx, evk, faces, voices


def _suffix(data: bytes) -> str:
    if len(data) > 8 and data[4:8] == b"ftyp":
        return ".mp4"
    if data[:4] == b"\x1aE\xdf\xa3":
        return ".webm"
    if data[:4] == b"RIFF":
        return ".wav"
    return ".bin"


def split_take(data: bytes) -> tuple[bytes | None, bytes | None, str | None, str | None]:
    td = tempfile.mkdtemp(prefix="umbra-take-")
    src = Path(td) / f"take{_suffix(data)}"
    src.write_bytes(data)
    jpg, wav = Path(td) / "f.jpg", Path(td) / "a.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-frames:v", "1", "-q:v", "2", str(jpg)],
        capture_output=True,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)],
        capture_output=True,
    )
    frame = jpg.read_bytes() if jpg.is_file() and jpg.stat().st_size > 32 else None
    audio = wav.read_bytes() if wav.is_file() and wav.stat().st_size > 64 else None
    return frame, audio, str(wav) if audio else None, str(src)


def take_frames(src: str, n: int = 8) -> list[bytes]:
    td = Path(src).parent
    dst = td / "p%02d.jpg"
    subprocess.run(
        ["ffmpeg", "-y", "-i", src, "-vf", "fps=3", "-frames:v", str(n), "-q:v", "2", str(dst)],
        capture_output=True,
    )
    out = []
    for p in sorted(td.glob("p*.jpg")):
        b = p.read_bytes()
        if len(b) > 32:
            out.append(b)
    return out


def _voice_grid(vec: list[float]) -> list[float]:
    return (list(vec) + [0.0] * 4096)[:4096]


def _lane(name, ok=False, **extra):
    return {"id": name, "ok": bool(ok), **extra}


def _timed(name, fn):
    t0 = time.perf_counter()
    out = fn()
    out["ms"] = int((time.perf_counter() - t0) * 1000)
    return out


def _one_face(ctx, evk, tmpl, probe_ct):
    return decrypt_l2(ctx, _post("/face", pack_face(evk, tmpl, probe_ct)))


def _min_face(ctx, evk, tmpls, probe_ct):
    scores = []
    with ThreadPoolExecutor(max_workers=min(4, len(tmpls))) as pool:
        futs = [pool.submit(_one_face, ctx, evk, tmpl, probe_ct) for tmpl in tmpls]
        for fut in as_completed(futs):
            scores.append(fut.result())
    return min(scores)


def _frame_l2(ctx, evk, tmpls, jpeg: bytes) -> float:
    from umbra.face_qa import inspect_bytes, _largest
    from umbra.enroll_extract import crop_grid

    face = _largest((inspect_bytes(jpeg).get("faces") or []))
    if not face or float(face["w"]) < 0.12:
        return NO_FACE_L2
    probe = encrypt_vec(ctx, crop_grid(jpeg, face))
    return _min_face(ctx, evk, tmpls, probe)


def _face_wave_job(ctx, evk, tmpls, frames: list[bytes], fallback: bytes | None):
    jpgs = list(frames) or ([fallback] if fallback else [])
    series = [NO_FACE_L2] * len(jpgs)
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(jpgs)))) as pool:
        futs = {pool.submit(_frame_l2, ctx, evk, tmpls, jpeg): i for i, jpeg in enumerate(jpgs)}
        for fut in as_completed(futs):
            series[futs[fut]] = fut.result()
    good = [s for s in series if s < FACE_L2_MAX]
    best = min(good) if good else min(series)
    face_ok = len(good) >= 2
    return (
        _lane("face", face_ok, l2=best, series=series, max=FACE_L2_MAX),
        _lane("wave", wave_from_l2s(series), series=series, occlude=OCCLUDE_L2),
    )


def _voice_job(ctx, evk, tmpls, probe_ct):
    l2 = decrypt_l2(ctx, _post("/face", pack_face(evk, tmpls[0], probe_ct)))
    return _lane("voice", l2 < VOICE_L2_MAX, l2=l2, max=VOICE_L2_MAX)


def _words_job(wav_path, nonce):
    if not wav_path or not nonce:
        return _lane("words", False, err="no audio")
    from umbra.card import transcribe

    text = transcribe(wav_path)
    return _lane("words", s1(text, nonce), text=text)


def warm() -> None:
    """Load Whisper only. Concrete keygen in-process SIGSEGV'd the server (LLVM)."""
    from umbra.card import transcribe

    Path(os.environ["UMBRA_KEY_DIR"]).mkdir(parents=True, exist_ok=True)
    td = tempfile.mkdtemp(prefix="umbra-warm-")
    wav = Path(td) / "s.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=f=440:d=1", "-ac", "1", "-ar", "16000", str(wav)],
        capture_output=True,
    )
    try:
        transcribe(str(wav))
    except Exception:
        pass


def run(take: bytes, card: dict | None = None, person_id: str = "") -> dict:
    person_id = person_id or live_id()
    if not person_id:
        raise ValueError("enroll first")
    card = card or {}
    t0 = time.perf_counter()
    ctx, evk, faces, voices = load_person(person_id)
    frame, audio, wav_path, src_path = split_take(take)
    if frame is None and audio is None:
        raise ValueError("take has no frame or audio")
    jobs = {}
    frames = take_frames(src_path) if src_path else []

    def face_wave():
        t0 = time.perf_counter()
        face, wave = _face_wave_job(ctx, evk, faces, frames, frame)
        ms = int((time.perf_counter() - t0) * 1000)
        face["ms"] = ms
        wave["ms"] = ms
        return face, wave

    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = {}
        fw = pool.submit(face_wave)
        if audio is not None:
            vec16 = wav_to_voice(audio)
            probe_v = encrypt_vec(ctx, _voice_grid(vec16))
            futs[pool.submit(_timed, "voice", lambda: _voice_job(ctx, evk, voices, probe_v))] = "voice"
            futs[pool.submit(_timed, "words", lambda: _words_job(wav_path, card.get("say") or card.get("nonce") or ""))] = "words"
        try:
            jobs["face"], jobs["wave"] = fw.result()
        except Exception as e:
            jobs["face"] = _lane("face", False, err=str(e)[:240], ms=0)
            jobs["wave"] = _lane("wave", False, err=str(e)[:240], ms=0)
        for fut in as_completed(futs):
            name = futs[fut]
            try:
                jobs[name] = fut.result()
            except Exception as e:
                jobs[name] = _lane(name, False, err=str(e)[:240], ms=0)
    for name in LANES:
        jobs.setdefault(name, _lane(name, False, err="skipped", ms=0))
    lights = [1 if jobs[n]["ok"] else 0 for n in LANES]
    total_ms = int((time.perf_counter() - t0) * 1000)
    return {
        "id": person_id,
        "ok": all(jobs[n]["ok"] for n in ("face", "voice", "words", "wave")),
        "lanes": jobs,
        "labels": list(LANES),
        "bits": lights,
        "ms": {n: jobs[n].get("ms", 0) for n in LANES} | {"total": total_ms},
        "thresh": {"face": FACE_L2_MAX, "voice": VOICE_L2_MAX},
        "profile": {"faces": len(faces), "voices": len(voices)},
    }


if __name__ == "__main__":
    ctx, evk, faces, voices = load_person()
    print("live", live_id(), "faces", len(faces), "voices", len(voices), "evk", len(evk))
