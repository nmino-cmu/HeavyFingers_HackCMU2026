"""Local crops for enroll. Never imported by the worker."""
from __future__ import annotations

import io
import math
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

FACE_N = 64
PIXELS = FACE_N * FACE_N
VOICE_N = 16
PRINT_N = 16


def _parse_bmp_wh(data: bytes) -> tuple[int, int, list[float]]:
    if data[:2] != b"BM":
        raise ValueError("not bmp")
    off = struct.unpack_from("<I", data, 10)[0]
    header = struct.unpack_from("<IiiHHI", data, 14)
    w, h = header[1], header[2]
    bpp = header[4]
    if bpp != 24 or w <= 0:
        raise ValueError("need 24-bit bmp")
    bottom_up = h > 0
    h = abs(h)
    row_b = ((w * 3 + 3) // 4) * 4
    pixels = []
    for y in range(h):
        src_y = h - 1 - y if bottom_up else y
        row = data[off + src_y * row_b : off + src_y * row_b + w * 3]
        for x in range(w):
            b, g, r = row[x * 3 : x * 3 + 3]
            pixels.append((r + g + b) / (3 * 255.0))
    return w, h, pixels


def _parse_bmp(data: bytes) -> list[float]:
    w, h, pixels = _parse_bmp_wh(data)
    if w == FACE_N and h == FACE_N:
        return pixels
    return _nearest(pixels, w, h, FACE_N, FACE_N)


def decode_gray(data: bytes) -> tuple[int, int, list[float]]:
    """Full-res gray [0,1]. JPEG/PNG via sips."""
    if data[:2] == b"BM":
        return _parse_bmp_wh(data)
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "in.bin"
        dst = Path(td) / "out.bmp"
        src.write_bytes(data)
        r = subprocess.run(["sips", "-s", "format", "bmp", str(src), "--out", str(dst)], capture_output=True)
        if r.returncode != 0 or not dst.is_file():
            raise ValueError("image decode failed")
        return _parse_bmp_wh(dst.read_bytes())


def crop_grid(data: bytes, box: dict, margin: float = 0.28) -> list[float]:
    """Normalized box → 64×64 gray. box keys x,y,w,h in 0..1 (top-left)."""
    w, h, px = decode_gray(data)
    mx = max(0.0, float(box["x"]) - margin * float(box["w"]))
    my = max(0.0, float(box["y"]) - margin * float(box["h"]))
    mw = min(1.0 - mx, float(box["w"]) * (1 + 2 * margin))
    mh = min(1.0 - my, float(box["h"]) * (1 + 2 * margin))
    x0, y0 = int(mx * w), int(my * h)
    x1, y1 = max(x0 + 1, int((mx + mw) * w)), max(y0 + 1, int((my + mh) * h))
    cw, ch = x1 - x0, y1 - y0
    cut = [px[min(h - 1, y0 + y) * w + min(w - 1, x0 + x)] for y in range(ch) for x in range(cw)]
    return _nearest(cut, cw, ch, FACE_N, FACE_N)


def _nearest(px, w, h, nw, nh):
    out = []
    for y in range(nh):
        sy = min(h - 1, y * h // nh)
        for x in range(nw):
            sx = min(w - 1, x * w // nw)
            out.append(px[sy * w + sx])
    return out


def image_to_grid(data: bytes) -> list[float]:
    """Any still → 64×64 gray in [0,1]. JPEG/PNG via sips; BMP parsed here."""
    if data[:2] == b"BM":
        return _parse_bmp(data)
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "in.bin"
        dst = Path(td) / "out.bmp"
        src.write_bytes(data)
        r = subprocess.run(
            ["sips", "-z", str(FACE_N), str(FACE_N), "-s", "format", "bmp", str(src), "--out", str(dst)],
            capture_output=True,
        )
        if r.returncode != 0 or not dst.is_file():
            raise ValueError("image decode failed")
        return _parse_bmp(dst.read_bytes())


def wav_pcm(data: bytes) -> tuple[list[int], int]:
    with wave.open(io.BytesIO(data), "rb") as w:
        ch = w.getnchannels()
        sw = w.getsampwidth()
        n = w.getnframes()
        raw = w.readframes(n)
        rate = w.getframerate()
    if sw != 2:
        raise ValueError("need 16-bit wav")
    samples = struct.unpack("<%dh" % (len(raw) // 2), raw)
    if ch > 1:
        samples = samples[0::ch]
    if not samples:
        raise ValueError("empty wav")
    return list(samples), int(rate)


def wav_to_voice(data: bytes) -> list[float]:
    """16-D log-FFT bands, mean-centered, L2-normalized. Length-invariant speaker crop."""
    import numpy as np

    samples, rate = wav_pcm(data)
    x = np.asarray(samples, dtype=np.float64) / 32768.0
    env = np.abs(x)
    thr = max(0.01, 0.12 * float(env.max() or 0))
    hit = np.where(env > thr)[0]
    if hit.size:
        x = x[int(hit[0]) : int(hit[-1]) + 1]
    if x.size < 512:
        x = np.pad(x, (0, 512 - x.size))
    spec = np.abs(np.fft.rfft(x * np.hanning(x.size)))
    freqs = np.fft.rfftfreq(x.size, 1.0 / rate)
    hi = min(7000.0, rate / 2 - 1)
    edges = np.geomspace(80.0, hi, VOICE_N + 1)
    vec = []
    for i in range(VOICE_N):
        m = (freqs >= edges[i]) & (freqs < edges[i + 1])
        band = spec[m]
        vec.append(float(np.log10(float(np.mean(band * band)) + 1e-12)))
    v = np.asarray(vec, dtype=np.float64)
    v = v - v.mean()
    nrm = float(np.linalg.norm(v)) or 1.0
    return (v / nrm).tolist()


def qa_voice(data: bytes, min_s: float = 6.0) -> dict:
    samples, rate = wav_pcm(data)
    n = len(samples)
    dur = n / float(rate)
    peak = max(abs(s) for s in samples) / 32768.0
    rms = math.sqrt(sum(s * s for s in samples) / n) / 32768.0
    clip = sum(1 for s in samples if abs(s) > 32000) / n
    ok = dur >= min_s and peak >= 0.08 and rms >= 0.018 and clip < 0.03
    reason = ""
    if dur < min_s:
        reason = f"need {min_s:.0f}s of speech, got {dur:.1f}s"
    elif peak < 0.08 or rms < 0.018:
        reason = "too quiet — speak closer"
    elif clip >= 0.03:
        reason = "clipping — back up from the mic"
    return {"ok": ok, "seconds": dur, "peak": peak, "rms": rms, "clip": clip, "reason": reason}


def image_to_print(data: bytes) -> list[float]:
    """Finger still → 16 (x,y,θ). Webcam print; not NBIS."""
    g = image_to_grid(data)
    mag = []
    for y in range(1, FACE_N - 1):
        for x in range(1, FACE_N - 1):
            i = y * FACE_N + x
            gx = g[i + 1] - g[i - 1]
            gy = g[i + FACE_N] - g[i - FACE_N]
            mag.append((gx * gx + gy * gy, x, y, gx, gy))
    mag.sort(reverse=True)
    pts = mag[:PRINT_N]
    while len(pts) < PRINT_N:
        pts.append((0.0, 0, 0, 0.0, 0.0))
    out = []
    for _m, x, y, gx, gy in pts:
        out.extend([x / FACE_N, y / FACE_N, (math.atan2(gy, gx) + math.pi) / (2 * math.pi)])
    return out
