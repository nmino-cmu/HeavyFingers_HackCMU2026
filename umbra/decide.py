"""Local AND of existing FHE bits + S1. S19 abort. No hop keys on fail."""
from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Result:
    ok: bool
    abort: bool
    reason: str
    keydir: str
    rpc: int

    @property
    def passed(self) -> bool:
        return self.ok

    @property
    def aborted(self) -> bool:
        return self.abort


def _pairs(fhe_bits, local_bits):
    """AND over bits that exist. None / missing P3 slots are omitted."""
    out = []
    for f, loc in zip(fhe_bits, local_bits):
        if f is None or loc is None:
            continue
        out.append((int(f), int(loc)))
    return out


def _wipe(keydir: str) -> str:
    p = Path(keydir)
    p.mkdir(parents=True, exist_ok=True)
    for child in p.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    return str(p)


def decide(fhe_bits, local_bits, s1_ok, *, keydir=None) -> Result:
    """Pass only all-1 AND S1. Any 0 fails. FHE≠local → abort. Abort/fail: empty keydir, rpc=0."""
    d = keydir or tempfile.mkdtemp(prefix="umbra-hop-")
    pairs = _pairs(fhe_bits, local_bits)
    if any(f != loc for f, loc in pairs):
        return Result(False, True, "s19", _wipe(d), 0)
    if not s1_ok:
        return Result(False, False, "s1", _wipe(d), 0)
    if any(f != 1 for f, _ in pairs):
        return Result(False, False, "bit", _wipe(d), 0)
    Path(d).mkdir(parents=True, exist_ok=True)
    Path(d, ".pass").write_text("1\n")
    return Result(True, False, "pass", d, 0)
