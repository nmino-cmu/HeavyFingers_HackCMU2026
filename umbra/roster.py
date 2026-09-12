"""Encrypted identity roster. Stores ciphertext only. No decrypt."""
from __future__ import annotations

from pathlib import Path

from umbra.protocol import looks_like_plaintext_mel, looks_like_plaintext_v, looks_like_plaintext_xyt

MAGIC = b"UMBR"
KINDS = {"face": 0, "voice": 1, "print": 2}
KIND_NAME = {v: k for k, v in KINDS.items()}


def looks_like_plaintext_enroll(body: bytes) -> bool:
    if not body:
        return True
    if body[:2] == b"BM" or body[:3] == b"\xff\xd8\xff" or body[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    if looks_like_plaintext_mel(body) or looks_like_plaintext_v(body) or looks_like_plaintext_xyt(body):
        return True
    if body[:4] == b"RIFF":
        return True
    if body[:4] != MAGIC:
        return True
    try:
        rec = unpack_record(body)
    except ValueError:
        return True
    for _k, _n, blob in rec["items"]:
        if looks_like_plaintext_mel(blob) or len(blob) < 50_000:
            return True
    return False


def pack_record(person_id: str, items) -> bytes:
    pid = person_id.encode("ascii")
    if not pid or len(pid) > 64:
        raise ValueError("bad id")
    out = bytearray(MAGIC)
    out += bytes([len(pid)]) + pid
    out += len(items).to_bytes(2, "big")
    for kind, name, blob in items:
        if kind not in KINDS:
            raise ValueError(kind)
        if len(blob) < 50_000:
            raise ValueError("ct too small")
        nb = str(name).encode("ascii")
        if len(nb) > 64:
            raise ValueError("name")
        out += bytes([KINDS[kind], len(nb)]) + nb
        out += len(blob).to_bytes(4, "big") + blob
    return bytes(out)


def unpack_record(body: bytes) -> dict:
    if body[:4] != MAGIC:
        raise ValueError("magic")
    n = body[4]
    i = 5
    pid = body[i : i + n].decode("ascii")
    i += n
    count = int.from_bytes(body[i : i + 2], "big")
    i += 2
    items = []
    for _ in range(count):
        kind = KIND_NAME.get(body[i])
        ln = body[i + 1]
        i += 2
        name = body[i : i + ln].decode("ascii")
        i += ln
        bl = int.from_bytes(body[i : i + 4], "big")
        i += 4
        blob = body[i : i + bl]
        i += bl
        if kind is None or len(blob) != bl:
            raise ValueError("item")
        items.append((kind, name, blob))
    return {"id": pid, "items": items}


class Roster:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, body: bytes) -> str:
        if looks_like_plaintext_enroll(body):
            raise ValueError("plaintext rejected")
        rec = unpack_record(body)
        (self.root / f"{rec['id']}.umr").write_bytes(body)
        return rec["id"]

    def get(self, person_id: str) -> bytes:
        p = self.root / f"{person_id}.umr"
        if not p.is_file():
            raise KeyError(person_id)
        return p.read_bytes()

    def ids(self) -> list[str]:
        return sorted(p.stem for p in self.root.glob("*.umr"))

    def summary(self) -> list[dict]:
        out = []
        for i in self.ids():
            rec = unpack_record(self.get(i))
            row = {"id": i, "face": 0, "voice": 0, "print": 0}
            for k, _n, _b in rec["items"]:
                row[k] += 1
            out.append(row)
        return out
