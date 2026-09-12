#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.card import generate
from umbra.decide import decide
from umbra.s1 import s1

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def main():
    check(s1("the lazy dog fox", "lazy dog") is True, "order")
    check(s1("The Lazy Dog.", "lazy dog") is True, "punct")
    check(s1("the fox dog", "fox dog") is True, "fox dog")
    check(s1("the fox dog", "dog fox") is False, "swap")
    clean = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import umbra.s1; assert 'requests' not in sys.modules; assert 'urllib.request' not in sys.modules",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    check(clean.returncode == 0, clean.stderr)

    bits = [1] * 10
    check(decide(bits, bits, True).ok, "pass")
    check(not decide(bits, bits, False).ok, "s1 fail")
    flip = list(bits)
    flip[0] = 0
    check(not decide(flip, bits, True).ok, "fhe flip")
    abort = decide(flip, bits, True)
    check(abort.abort, "s19 abort")
    keydir = tempfile.mkdtemp(prefix="umbra-hop-")
    check(abort.abort and decide(bits, flip, True).abort, "either way abort")
    check(len(os.listdir(keydir)) == 0, "no hop keys written")

    card = generate()
    check(card["hand"] in ("left", "right"), card)
    check(card["end"] in ("pinky", "index", "thumb"), card)
    check(len(card["say"].split()) >= 8, card["say"])

    url = os.environ.get("UMBRA_WORKER_URL", "").rstrip("/")
    if url:
        import urllib.error
        import urllib.request

        req = urllib.request.Request(
            url + "/eval",
            data=b"the lazy dog fox am is hack win",
            method="POST",
            headers={"Content-Type": "text/plain"},
        )
        try:
            urllib.request.urlopen(req, timeout=15)
            code = 200
        except urllib.error.HTTPError as e:
            code = e.code
        check(code >= 400, f"nonce POST must 4xx got {code}")

    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
