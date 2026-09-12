#!/usr/bin/env python3
"""Merge integrity: UI chrome + local enroll/verify + Solana files, no leaks."""
from __future__ import annotations

import os
import sys

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def test_sources_present():
    check(os.path.isfile(os.path.join(ROOT, "umbra/solana_wallet.py")), "solana_wallet")
    check(os.path.isfile(os.path.join(ROOT, "umbra/test_solana_escrow.py")), "test_solana_escrow")
    check(os.path.isfile(os.path.join(ROOT, "umbra/web/home.html")), "home.html")
    check(os.path.isfile(os.path.join(ROOT, "umbra/web/windows.js")), "windows.js")
    check(os.path.isfile(os.path.join(ROOT, "umbra/web/assets/logo.png")), "logo")
    check(os.path.isfile(os.path.join(ROOT, "umbra/web/assets/oval.svg")), "oval")


def test_ui_chrome():
    for name in ("index.html", "enroll.html", "signin.html", "home.html"):
        html = open(os.path.join(ROOT, "umbra/web", name)).read()
        check("data-umbra-bg" in html, f"{name} desktop bg")
        check("windows.js" in html, f"{name} windows")


def test_enroll_functionality():
    html = open(os.path.join(ROOT, "umbra/web/enroll.html")).read()
    check("VOICE_MIN_MS = 12000" in html, "enroll 12s")
    check("grabFrame" in html, "enroll grabFrame")
    check("snapFinger" in html, "enroll finger")
    check("readFaces" in html, "enroll read faces")
    js = open(os.path.join(ROOT, "umbra/web/umbra.js")).read()
    check("grabFrame:" in js, "umbra.grabFrame")
    check("escrows:" in js, "umbra.escrows")


def test_signin_functionality():
    html = open(os.path.join(ROOT, "umbra/web/signin.html")).read()
    check("VOICE_MIN_MS = 12000" in html, "signin 12s")
    check("audioTake" in html, "signin side audio")
    check('fd.append("audio"' in html, "signin posts audio")
    check("armed" in html, "signin oval arm")


def test_verify_parts_audio():
    from umbra.web.serve import _verify_parts

    bound = "----umbra-test"
    ctype = "multipart/form-data; boundary=" + bound
    def part(name, payload, filename=None):
        dispo = f'Content-Disposition: form-data; name="{name}"'
        if filename:
            dispo += f'; filename="{filename}"'
        return f"--{bound}\r\n{dispo}\r\n\r\n".encode() + payload + b"\r\n"
    body = part("take", b"videobytes", "take.webm") + part("audio", b"audiobytes", "mic.webm") + part("id", b"abc123") + f"--{bound}--\r\n".encode()
    out = _verify_parts(ctype, body)
    check(len(out) == 4, out)
    take_b, card, pid, audio_side = out
    check(take_b == b"videobytes", take_b)
    check(audio_side == b"audiobytes", audio_side)
    check(pid == "abc123", pid)
    check(card == {}, card)


def test_escrow_listing_no_secrets():
    import json
    from pathlib import Path

    from umbra.web.serve import ROOT as WEB_ROOT

    d = WEB_ROOT / "umbra/fixtures/escrows"
    check(d.is_dir(), d)
    rows = []
    for p in sorted(d.glob("*.json")):
        if p.name.endswith(".keypair.json"):
            continue
        rec = json.loads(p.read_text())
        check("keypair_path" in rec, "fixture has key path on disk")
        rows.append(
            {k: rec.get(k) for k in ("id", "status", "amount_sol", "payer", "payee", "escrow_address", "deposit_explorer", "settle_explorer")}
        )
    blob = json.dumps({"escrows": rows})
    check("keypair" not in blob, blob)
    check(len(rows) >= 1, rows)
    check(all(r.get("id") for r in rows), rows)
    check(WEB_ROOT == Path(ROOT), WEB_ROOT)


def main():
    test_sources_present()
    test_ui_chrome()
    test_enroll_functionality()
    test_signin_functionality()
    test_verify_parts_audio()
    test_escrow_listing_no_secrets()
    print("ok", CHECKS_RUN)


if __name__ == "__main__":
    main()
