"""Desk view filter. Chain truth stays on disk / explorer; HTTP never re-emits keys."""
from __future__ import annotations

import hashlib

# Known fixture cluster — public JSON must not contain these.
CLUSTER = (
    "VWvZgaSaWtZZnpiS5An9zSuuzTkRhELFfTbCHbvt9C4",
    "DfgYv1sw56hVBtz753Hn6pKMg5kWiJjWUCJ91ek7af2K",
    "6rUpr7yNr7TmTcqrnFzUCKpBvSoiU6WUikcMsMiDXEok",
    "2dRiRZe6kJ1HbntGfgmrQywGfpH2aDH6QVHyEZxbcN6J",
    "FtCrarAViQip5oCuugUvkj3dvP2ctniGwA8At56kBmV3",
    "5wuWojRBn8qW6rf6jzwSBDfG2C2ak2WoQFWD8L9c9SUD",
    "6rUpr7yNr7TmTcqr",
    "2dRiRZe6kJ1HbntG",
)

FACTS = {
    "view": "cutout",
    "memo": False,
    "roster_on_chain": False,
    "spend_keys": "mac-only",
    "prices": "fhe",
    "receipts": "aes-gcm-1of1",
    "inbox": "local-webcrypto",
}


def nym(s: str) -> str:
    return hashlib.sha256(("umbra-view-v1" + (s or "")).encode()).hexdigest()[:12]


def public_escrow(rec: dict) -> dict:
    return {
        "nym": nym(str(rec.get("id") or rec.get("escrow_address") or "")),
        "status": rec.get("status"),
        "deposit_explorer": rec.get("deposit_explorer"),
        "settle_explorer": rec.get("settle_explorer"),
    }


def public_receipt(rec: dict) -> dict:
    return {
        "lot": nym(str(rec.get("auction_id") or "")),
        "tag": nym(str(rec.get("mint") or "")),
        "explorer": rec.get("explorer"),
    }


def public_hop(hop: dict | None) -> dict:
    if not hop:
        return {}
    addrs = hop.get("addrs") or {}
    explorers = hop.get("explorers") or []
    out = {"explorers": explorers, "hops": len(hop.get("sigs") or explorers or [])}
    if addrs:
        out["cutout"] = {k: nym(str(v)) for k, v in addrs.items()}
    return out


def view_leaks(blob: str) -> list[str]:
    hits = [s[:8] for s in CLUSTER if s in blob]
    for k in ("payer", "payee", "recipient", "keypair", "ciphertext", "auction_id", "escrow_address"):
        if k in blob:
            hits.append(k)
    return hits
