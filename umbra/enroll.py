"""Mac enroll: crop → lattice encrypt → roster bytes. sk stays here."""
from __future__ import annotations

import os
import random
from pathlib import Path

from umbra.enroll_extract import image_to_grid, wav_to_voice
from umbra.face_qa import grid_for_enroll
from umbra.face_ckks import encrypt_vec, evk_bytes, new_context
from umbra.roster import Roster, pack_record

def _keyroot() -> Path:
    return Path(os.environ.get("UMBRA_ENROLL_KEYDIR", Path(__file__).resolve().parent / "enroll_keys"))


def default_roster() -> Roster:
    return Roster(os.environ.get("UMBRA_ROSTER", Path(__file__).resolve().parent / "roster_data"))


def _save_sk(ctx, person_id: str) -> None:
    d = _keyroot() / person_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "ctx.bin").write_bytes(ctx.serialize(save_secret_key=True))
    (d / "evk.bin").write_bytes(evk_bytes(ctx))


def _voice_grid(vec: list[float]) -> list[float]:
    # pad 16-D speaker vec into the 64×64 slot the CKKS face circuit already uses
    out = list(vec) + [0.0] * (4096 - len(vec))
    return out[:4096]


def _fresh_id() -> str:
    taken = set()
    try:
        taken = set(default_roster().ids())
    except Exception:
        taken = set()
    for _ in range(32):
        n = str(random.randint(100000, 999999))
        if n not in taken:
            return n
    return str(random.randint(100000000, 999999999))


def enroll_bytes(faces, voices, prints=None, person_id=None):
    if not faces or not voices:
        raise ValueError("need face and voice")
    prints = prints or []
    pid = person_id or _fresh_id()
    ctx = new_context()
    items = []
    for i, raw in enumerate(faces):
        items.append(("face", f"a{i}", encrypt_vec(ctx, grid_for_enroll(raw))))
    for i, raw in enumerate(voices):
        items.append(("voice", f"v{i}", encrypt_vec(ctx, _voice_grid(wav_to_voice(raw)))))
    for i, raw in enumerate(prints):
        items.append(("print", f"p{i}", encrypt_vec(ctx, image_to_grid(raw))))
    _save_sk(ctx, pid)
    return pid, pack_record(pid, items)


def enroll(faces, voices, prints, person_id=None, roster=None):
    """Encrypt on this machine and keep the ciphertext here. Vultr is verify-only."""
    pid, raw = enroll_bytes(faces, voices, prints, person_id=person_id)
    (roster or default_roster()).put(raw)
    return pid, raw
