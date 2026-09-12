#!/usr/bin/env python3
"""P4: public card, Whisper S1, decide() AND + S19 abort."""
import ipaddress
import os
import socket
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.card import generate
from umbra.decide import decide
from umbra.fixtures import CARD_RRP, V_OK, reference
from umbra.s1 import s1

CHECKS_RUN = 0
NONCE = "the lazy dog fox"


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def worker_url():
    return os.environ["UMBRA_WORKER_URL"].rstrip("/")


def host_gate():
    url = worker_url()
    host = urllib.parse.urlparse(url).hostname
    ip = ipaddress.ip_address(socket.gethostbyname(host))
    check(ip.version == 4 and ip.is_global, "orch must be public IPv4")
    check(str(ip) == os.environ["VULTR_ORCH_IP"], "URL must be orch public IP")


def post_bytes(path, body: bytes, ctype="text/plain"):
    req = urllib.request.Request(
        worker_url() + path,
        data=body,
        method="POST",
        headers={"Content-Type": ctype},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_s1_import_has_no_http():
    script = (
        "import sys; sys.path.insert(0, %r); import umbra.s1; "
        "bad=[m for m in ('requests','urllib.request') if m in sys.modules]; "
        "raise SystemExit('http in sys.modules: '+str(bad) if bad else 0)"
    ) % ROOT
    r = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    check(r.returncode == 0, r.stderr + r.stdout)


def test_s1_words():
    check(s1("The lazy dog fox.", NONCE) is True, "capitalize+period")
    check(s1("the lazy fox dog", NONCE) is False, "swap fox dog")
    check(s1(NONCE, NONCE) is True, "exact")
    check(s1("the lazy dog fox", "lazy dog") is True, "order")
    check(s1("The Lazy Dog.", "lazy dog") is True, "punct")
    check(s1("the fox dog", "fox dog") is True, "fox dog prefix")
    check(s1("the fox dog", "dog fox") is False, "swap")
    check(s1("the lazy dog", NONCE) is False, "missing word")


def test_decide_and_s19():
    bits = [1] * 10
    r = decide(bits, bits, True)
    check(r.ok and r.passed and not r.abort, "all-1 AND S1")
    check(r.rpc == 0, "pass rpc")

    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "hop.json"), "w").write("{}")
        r = decide(bits, bits, False, keydir=td)
        check((not r.ok) and (not r.abort), "S1 fail")
        check(os.listdir(td) == [], f"no hop keys on fail: {os.listdir(td)}")
        check(r.rpc == 0, "fail rpc")

    flip = list(bits)
    flip[0] = 0
    r = decide(flip, flip, True)
    check((not r.ok) and (not r.abort), "matched zero fails")

    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "hop.json"), "w").write("{}")
        r = decide(flip, bits, True, keydir=td)
        check(r.abort and not r.ok, "FHE flip abort")
        check(os.listdir(td) == [], f"abort empty keydir {os.listdir(td)}")
        check(r.rpc == 0, "abort zero RPC")

    r = decide(bits, flip, True)
    check(r.abort and r.rpc == 0, "local flip abort")

    r = decide([1, None], [1, None], True)
    check(r.ok, "omit missing P3")
    r = decide([1], [1, 0], True)
    check(r.ok, "extra local omitted")


def test_card_cli():
    card = generate()
    check(card["hand"] in ("left", "right"), card)
    check(card["end"] in ("pinky", "index", "thumb"), card)
    check(len(card["say"].split()) >= 8, card["say"])
    env = os.environ.copy()
    env["PYTHONPATH"] = ROOT + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    out = subprocess.check_output(
        [sys.executable, "-m", "umbra.card"], cwd=ROOT, env=env, text=True
    )
    for key in ("say:", "hand:", "motion:", "where:", "side:", "end:"):
        check(key in out, f"card missing {key}")
    say = [ln.split(":", 1)[1].strip() for ln in out.splitlines() if ln.startswith("say:")][0]
    n = len(say.split())
    check(8 <= n <= 12, f"nonce word count {n}")


def test_whisper_mac():
    from umbra.card import transcribe

    with tempfile.TemporaryDirectory() as td:
        aiff = os.path.join(td, "n.aiff")
        wav = os.path.join(td, "n.wav")
        subprocess.check_call(["say", "-o", aiff, NONCE])
        subprocess.check_call(["afconvert", aiff, wav, "-f", "WAVE", "-d", "LEI16@16000"])
        text = transcribe(wav)
        check(s1(text, NONCE), f"whisper {text!r}")


def test_nonce_post_4xx():
    host_gate()
    code, body = post_bytes("/eval", NONCE.encode(), "text/plain")
    check(400 <= code < 500, f"nonce POST must 4xx got {code} {body[:80]!r}")
    check(NONCE.encode() not in body, "nonce must not come back as a result")


def test_live_fhe_decide():
    from umbra.client import Client

    host_gate()
    client = Client()
    body = client.pack_eval_body(V_OK, CARD_RRP)
    req = urllib.request.Request(
        worker_url() + "/eval",
        data=body,
        method="POST",
        headers={"X-Umbra-Nonce": "p4-card", "Content-Type": "application/octet-stream"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        out = resp.read()
    fhe = client.eval_bits(out)
    local = reference(V_OK, CARD_RRP)
    n = min(len(fhe), len(local))
    fhe, local = fhe[:n], local[:n]
    check(n >= 1, "P2 bit0 must exist")
    r = decide(fhe, local, s1("The lazy dog fox.", NONCE))
    check(r.ok, f"live AND fail fhe={fhe} local={local}")
    flipped = list(local)
    flipped[0] = 1 - flipped[0]
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "hop.json"), "w").write("{}")
        bad = decide(fhe, flipped, True, keydir=td)
        check(bad.abort, "S19 live abort")
        check(os.listdir(td) == [], "live abort wiped keys")
        check(bad.rpc == 0, "live abort zero RPC")


def main():
    test_s1_import_has_no_http()
    test_s1_words()
    test_decide_and_s19()
    test_card_cli()
    test_whisper_mac()
    test_nonce_post_4xx()
    test_live_fhe_decide()
    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
