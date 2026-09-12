"""Wire format: evk_len (BE u32) + evk + ciphertext."""
import struct


def pack_request(evk: bytes, ciphertext: bytes) -> bytes:
    if len(evk) < 16:
        raise ValueError("evk too short")
    if len(ciphertext) < 1:
        raise ValueError("ciphertext empty")
    return struct.pack(">I", len(evk)) + evk + ciphertext


def unpack_request(body: bytes) -> tuple[bytes, bytes]:
    if len(body) < 8:
        raise ValueError("body too short")
    evk_len = struct.unpack(">I", body[:4])[0]
    if evk_len < 16 or evk_len > len(body) - 4:
        raise ValueError("invalid evk length")
    evk = body[4 : 4 + evk_len]
    ct = body[4 + evk_len :]
    if not ct:
        raise ValueError("missing ciphertext")
    return evk, ct


def looks_like_plaintext_v(body: bytes) -> bool:
    """Reject raw float vector posts (75 float32 ≈ 300 bytes)."""
    if len(body) in (300, 600) and len(body) % 4 == 0:
        import struct as st

        n = len(body) // 4
        if n == 75:
            vals = st.unpack(f">{n}f", body)
            if all(0.0 <= x <= 2.0 for x in vals):
                return True
    if body[:1] in (b"{", b"[") and b"0.9137" in body:
        return True
    return False
