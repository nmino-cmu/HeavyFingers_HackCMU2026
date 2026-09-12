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
    check(os.path.isfile(os.path.join(ROOT, "umbra/test_solana_receipt_nft.py")), "test_solana_receipt_nft")
    check("mint_encrypted_receipt" in open(os.path.join(ROOT, "umbra/solana_wallet.py")).read(), "nft mint")
    check('FACE_L2_MAX = float(os.environ.get("UMBRA_FACE_L2_MAX", "220"))' in open(os.path.join(ROOT, "umbra/verify.py")).read(), "face 220")
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
    check("snapFinger" not in html and "skipFinger" not in html, "enroll finger")
    check("readFaces" in html, "enroll read faces")
    js = open(os.path.join(ROOT, "umbra/web/umbra.js")).read()
    check("grabFrame:" in js, "umbra.grabFrame")
    check("sealViz:" in js, "umbra.sealViz")
    check("paintLanes:" in js, "umbra.paintLanes")
    check("saveEta:" in js, "umbra.saveEta")
    check("escrows:" in js, "umbra.escrows")
    check("receipts:" in js, "umbra.receipts")
    check("cutout:" in js, "umbra.cutout")
    check("veil()" in js, "umbra.veil")
    check("inbox:" in js, "umbra.inbox")


def test_signin_functionality():
    html = open(os.path.join(ROOT, "umbra/web/signin.html")).read()
    check("VOICE_MIN_MS = 12000" in html, "signin 12s")
    check("audioTake" in html, "signin side audio")
    check('fd.append("audio"' in html, "signin posts audio")
    check("armed" in html, "signin oval arm")
    check("a.play()" not in html, "do not play sidecar and video together")
    check("sealViz" in html and 'classList.toggle("rest"' in html, "signin rest + seal")
    check('id="enter"' in html and "setTimeout(() => location.assign(\"/home\")" not in html, "enter is a click")


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

    from umbra.privacy import public_escrow, view_leaks
    from umbra.web.serve import ROOT as WEB_ROOT

    d = WEB_ROOT / "umbra/fixtures/escrows"
    check(d.is_dir(), d)
    rows = []
    for p in sorted(d.glob("*.json")):
        if p.name.endswith(".keypair.json"):
            continue
        rec = json.loads(p.read_text())
        check("keypair_path" in rec, "fixture has key path on disk")
        rows.append(public_escrow(rec))
    blob = json.dumps({"escrows": rows})
    check(not view_leaks(blob), view_leaks(blob) or blob)
    check(len(rows) >= 1, rows)
    check(all(r.get("nym") and r.get("status") for r in rows), rows)
    check(WEB_ROOT == Path(ROOT), WEB_ROOT)


def test_receipt_listing_no_plaintext():
    import json

    from umbra.privacy import public_receipt, view_leaks

    d = os.path.join(ROOT, "umbra/fixtures/receipts")
    check(os.path.isdir(d), d)
    rows = []
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        rec = json.loads(open(os.path.join(d, name)).read())
        rows.append(public_receipt(rec))
        check("ciphertext_b64" in rec, name)
    blob = json.dumps({"receipts": rows})
    check(not view_leaks(blob), view_leaks(blob) or blob)
    check(len(rows) >= 1, rows)
    check(all(r.get("lot") and r.get("tag") for r in rows), rows)


def test_hop_view_strips_addrs():
    from umbra.privacy import public_hop, view_leaks

    hop = {
        "sigs": ["sigA", "sigB", "sigC"],
        "addrs": {
            "faucet": "VWvZgaSaWtZZnpiS5An9zSuuzTkRhELFfTbCHbvt9C4",
            "ingress": "DfgYv1sw56hVBtz753Hn6pKMg5kWiJjWUCJ91ek7af2K",
            "cutout": "6rUpr7yNr7TmTcqrnFzUCKpBvSoiU6WUikcMsMiDXEok",
            "bid": "2dRiRZe6kJ1HbntGfgmrQywGfpH2aDH6QVHyEZxbcN6J",
        },
        "explorers": ["https://explorer.solana.com/tx/sigA?cluster=devnet"],
    }
    out = public_hop(hop)
    blob = str(out)
    check(out["hops"] == 3, out)
    check("explorers" in out, out)
    check("addrs" not in out and "sigs" not in out, out)
    check(not view_leaks(blob), view_leaks(blob) or blob)
    check(set(out["cutout"]) == {"faucet", "ingress", "cutout", "bid"}, out)


def test_desk_hides_roster():
    html = open(os.path.join(ROOT, "umbra/web/home.html")).read()
    check("Umbra.veil()" in html, "desk uses veil")
    check("people[people.length" not in html, "desk does not pick roster id")
    check("cutoutHud" in html, "privacy hud")
    check("sealForm" in html, "local seal compose")
    from umbra.privacy import view_leaks
    check(not view_leaks(html), view_leaks(html))


def main():
    test_sources_present()
    test_ui_chrome()
    test_enroll_functionality()
    test_signin_functionality()
    test_verify_parts_audio()
    test_escrow_listing_no_secrets()
    test_receipt_listing_no_plaintext()
    test_hop_view_strips_addrs()
    test_desk_hides_roster()
    print("ok", CHECKS_RUN)


if __name__ == "__main__":
    main()
