"""CKKS Conv+square face match. Deeper than L2. Secret key stays on the Mac.

Wire: TenSEAL 0.3.16. 16x16 crop, one 3x3 conv, square, encrypted L2 of features.
"""
from __future__ import annotations

import struct

import tenseal as ts

FACE_N = 16
KERNEL = 3
STRIDE = 1
WINDOWS = (FACE_N - KERNEL) // STRIDE + 1
WINDOWS_NB = WINDOWS * WINDOWS
PIXELS = FACE_N * FACE_N
POLY_DEGREE = 8192
COEFF_MOD_BIT_SIZES = [40, 21, 21, 21, 40]
GLOBAL_SCALE = 2**21
# ponytail: threshold from A/A vs A/B on this kernel; raise if a new crop scale is used.
MATCH_L2_MAX = 8.0
KERNEL_W = (
    (0.11, 0.12, 0.11),
    (0.12, 0.16, 0.12),
    (0.11, 0.12, 0.11),
)


def face_a() -> list[float]:
    return [(((i * 17 + j * 31) % 251) / 255.0) for i in range(FACE_N) for j in range(FACE_N)]


def face_b() -> list[float]:
    return [(((i * 41 + j * 13) % 197) / 255.0) for i in range(FACE_N) for j in range(FACE_N)]


def _img(pixels: list[float]) -> list[list[float]]:
    if len(pixels) != PIXELS:
        raise ValueError("need 16x16")
    return [pixels[i * FACE_N : (i + 1) * FACE_N] for i in range(FACE_N)]


def new_context() -> ts.Context:
    ctx = ts.context(ts.SCHEME_TYPE.CKKS, POLY_DEGREE, coeff_mod_bit_sizes=COEFF_MOD_BIT_SIZES)
    ctx.global_scale = GLOBAL_SCALE
    ctx.generate_galois_keys()
    return ctx


def evk_bytes(ctx: ts.Context) -> bytes:
    return ctx.serialize(save_secret_key=False)


def encrypt_im2col(ctx: ts.Context, pixels: list[float]) -> bytes:
    enc, windows = ts.im2col_encoding(ctx, _img(pixels), KERNEL, KERNEL, STRIDE)
    if windows != WINDOWS_NB:
        raise ValueError(f"windows {windows} != {WINDOWS_NB}")
    return enc.serialize()


def decrypt_l2(ctx: ts.Context, blob: bytes) -> float:
    vals = ts.ckks_vector_from(ctx, blob).decrypt()
    return float(sum(vals[:WINDOWS_NB]))


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
    if len(body) == PIXELS * 4:
        vals = struct.unpack(f">{PIXELS}f", body)
        if all(-0.1 <= x <= 1.1 or 0.0 <= x <= 255.0 for x in vals[:16]):
            return True
    if body[:1] in (b"{", b"[") and b"0.2468" in body:
        return True
    return False


def eval_conv_sq_l2(evk: bytes, tmpl: bytes, probe: bytes) -> bytes:
    """Worker path: public context only. Conv + square + encrypted L2. No decrypt."""
    ctx = ts.context_from(evk)
    if ctx.has_secret_key():
        raise ValueError("sk on wire")
    a = ts.ckks_vector_from(ctx, tmpl)
    b = ts.ckks_vector_from(ctx, probe)
    fa = a.conv2d_im2col(KERNEL_W, WINDOWS_NB)
    fb = b.conv2d_im2col(KERNEL_W, WINDOWS_NB)
    fa.square_()
    fb.square_()
    diff = fa - fb
    return (diff * diff).serialize()


def demo() -> None:
    ctx = new_context()
    evk = evk_bytes(ctx)
    assert not ts.context_from(evk).has_secret_key()
    a, b = face_a(), face_b()
    aa = eval_conv_sq_l2(evk, encrypt_im2col(ctx, a), encrypt_im2col(ctx, a))
    ab = eval_conv_sq_l2(evk, encrypt_im2col(ctx, a), encrypt_im2col(ctx, b))
    d_aa, d_ab = decrypt_l2(ctx, aa), decrypt_l2(ctx, ab)
    assert match_bit(d_aa) == 1, d_aa
    assert match_bit(d_ab) == 0, d_ab
    print(f"ok A/A={d_aa:.4f} A/B={d_ab:.4f} evk={len(evk)}")


if __name__ == "__main__":
    demo()
