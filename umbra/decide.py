"""Local AND of FHE bits, local predicates, and S1. No hop keys on abort."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    ok: bool
    abort: bool
    reason: str


def decide(fhe_bits, local_bits, s1_ok) -> Result:
    if list(fhe_bits) != list(local_bits):
        return Result(False, True, "s19")
    if not s1_ok:
        return Result(False, False, "s1")
    if not all(int(b) == 1 for b in fhe_bits):
        return Result(False, False, "bit")
    return Result(True, False, "pass")
