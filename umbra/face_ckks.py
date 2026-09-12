"""Mac-side CKKS face client. Secret key never leaves this process.

Wire: TenSEAL 0.3.16 (farm x86 cp310 max). Do not mix 0.3.17.
"""
from __future__ import annotations

import struct

import tenseal as ts

POLY_DEGREE = 16384
# 9 primes → one CKKS ct serializes ≥ 1MB (4 primes was ~459KB).
COEFF_MOD_BIT_SIZES = [60, 40, 40, 40, 40, 40, 40, 40, 60]
GLOBAL_SCALE = 2**40
FACE_N = 64
PIXELS = FACE_N * FACE_N
MATCH_L2_MAX = 1.0


def face_a() -> list[float]:
    return [(((i * 17 + j * 31) % 251) / 255.0) for i in range(FACE_N) for j in range(FACE_N)]


def face_b() -> list[float]:
    return [(((i * 41 + j * 13) % 197) / 255.0) for i in range(FACE_N) for j in range(FACE_N)]


def reference_match(tmpl: list[float], probe: list[float]) -> int:
    l2 = sum((a - b) ** 2 for a, b in zip(tmpl, probe))
    return int(l2 < MATCH_L2_MAX)


def new_context() -> ts.Context:
    ctx = ts.context(ts.SCHEME_TYPE.CKKS, POLY_DEGREE, coeff_mod_bit_sizes=COEFF_MOD_BIT_SIZES)
    ctx.global_scale = GLOBAL_SCALE
    return ctx


def evk_bytes(ctx: ts.Context) -> bytes:
    return ctx.serialize(save_secret_key=False)


def encrypt_vec(ctx: ts.Context, pixels: list[float]) -> bytes:
    if len(pixels) != PIXELS:
        raise ValueError("need 64x64")
    return ts.ckks_vector(ctx, pixels).serialize()


def decrypt_l2(ctx: ts.Context, blob: bytes) -> float:
    vals = ts.ckks_vector_from(ctx, blob).decrypt()
    return float(sum(vals[:PIXELS]))


def match_bit(l2: float) -> int:
    return int(l2 < MATCH_L2_MAX)


def pack_face(evk: bytes, tmpl: bytes, probe: bytes) -> bytes:
    if len(evk) < 32 or len(tmpl) < 32 or len(probe) < 32:
        raise ValueError("short ckks blob")
    return struct.pack(">I", len(evk)) + evk + struct.pack(">I", len(tmpl)) + tmpl + probe


def unpack_face(body: bytes) -> tuple[bytes, bytes, bytes]:
    if len(body) < 8:
        raise ValueError("body too short")
    evk_len = struct.unpack(">I", body[:4])[0]
    if evk_len < 32 or evk_len > len(body) - 8:
        raise ValueError("invalid evk length")
    evk = body[4 : 4 + evk_len]
    rest = body[4 + evk_len :]
    tmpl_len = struct.unpack(">I", rest[:4])[0]
    if tmpl_len < 32 or tmpl_len > len(rest) - 4:
        raise ValueError("invalid tmpl length")
    tmpl = rest[4 : 4 + tmpl_len]
    probe = rest[4 + tmpl_len :]
    if len(probe) < 32:
        raise ValueError("missing probe")
    return evk, tmpl, probe


def looks_like_plaintext_face(body: bytes, content_type: str = "") -> bool:
    ct = (content_type or "").lower()
    if "json" in ct or "image/" in ct or "text/" in ct:
        return True
    if body[:8] == b"\x89PNG\r\n\x1a\n" or body[:3] == b"\xff\xd8\xff" or body[:4] == b"RIFF":
        return True
    if len(body) in (PIXELS * 4, PIXELS * 8) and len(body) % 4 == 0:
        n = len(body) // 4
        if n == PIXELS:
            vals = struct.unpack(f">{n}f", body[: PIXELS * 4] if len(body) == PIXELS * 8 else body)
            if all(-0.1 <= x <= 1.1 or 0.0 <= x <= 255.0 for x in vals[:64]):
                return True
    if body[:1] in (b"{", b"[") and b"0.2468" in body:
        return True
    return False


def eval_l2_ciphertext(evk: bytes, tmpl: bytes, probe: bytes) -> bytes:
    """Worker path: public context only. Must not require a secret key."""
    ctx = ts.context_from(evk)
    if ctx.has_secret_key():
        raise ValueError("sk on wire")
    a = ts.ckks_vector_from(ctx, tmpl)
    b = ts.ckks_vector_from(ctx, probe)
    diff = a - b
    # ponytail: elementwise sq, no galois (evk was 415MB). Client sums slots.
    return (diff * diff).serialize()
