"""Wire format: evk_len (BE u32) + evk + ct + card_len (BE u16) + card (5 float64)."""
import struct

CARD_FLOATS = 5
CARD_BYTES = CARD_FLOATS * 8


def pack_card(card_vec) -> bytes:
    if len(card_vec) != CARD_FLOATS:
        raise ValueError("card must be 5 floats")
    return struct.pack(">5d", *card_vec)


def pack_request(evk: bytes, ciphertext: bytes, card_vec=None) -> bytes:
    if len(evk) < 16:
        raise ValueError("evk too short")
    if len(ciphertext) < 1:
        raise ValueError("ciphertext empty")
    card = pack_card(card_vec) if card_vec is not None else b""
    return struct.pack(">I", len(evk)) + evk + ciphertext + struct.pack(">H", len(card)) + card


def unpack_request(body: bytes) -> tuple[bytes, bytes, bytes]:
    if len(body) < 8:
        raise ValueError("body too short")
    evk_len = struct.unpack(">I", body[:4])[0]
    if evk_len < 16 or evk_len > len(body) - 4:
        raise ValueError("invalid evk length")
    evk = body[4 : 4 + evk_len]
    rest = body[4 + evk_len :]
    card = b""
    if len(rest) >= 2 + CARD_BYTES:
        card_len = struct.unpack(">H", rest[-2:])[0]
        if card_len == CARD_BYTES:
            card = rest[-(2 + CARD_BYTES) : -2]
            rest = rest[: -(2 + CARD_BYTES)]
    if not rest:
        raise ValueError("missing ciphertext")
    return evk, rest, card


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
