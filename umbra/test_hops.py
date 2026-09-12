#!/usr/bin/env python3
"""P9 hops: real Solana devnet txs. RPC down → exit 1. No fake txs."""
import json
import os
import sys
import tempfile

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.decide import decide
from umbra.hops import (
    MEMO_PROGRAMS,
    fetch_tx,
    inspect_ix_data,
    run,
    template_hashes,
)
from umbra.s1 import s1

CHECKS_RUN = 0
BANNED = (
    "unhackable",
    "fhe watched the video",
    "fhe transcribed",
    "touch id",
    "any website already works",
)


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def main():
    abort = decide([0] + [1] * 9, [1] * 10, True)
    check(abort.abort, "s19 abort")
    keydir = tempfile.mkdtemp(prefix="umbra-hop-")
    out = run(abort, keydir=keydir)
    check(out is None, "abort does not hop")
    check(os.path.isdir(keydir) and len(os.listdir(keydir)) == 0, "abort writes no hop keys")

    html = open(os.path.join(ROOT, "umbra/web/index.html"), encoding="utf-8").read()
    low = html.lower()
    for w in BANNED:
        check(w not in low, f"banned: {w}")
    check("record" in low and "upload" in low, "record/upload crop")
    check("card" in low or "say" in low, "card text")
    check("explorer" in low, "explorer links")
    check("bit" in low or "s5" in low, "lights for bits")

    ok = decide([1] * 10, [1] * 10, s1("the lazy dog fox", "lazy dog"))
    check(ok.ok, "pass")
    keydir = tempfile.mkdtemp(prefix="umbra-hop-")
    hop = run(ok, keydir=keydir)
    check(hop is not None, "pass hops")
    check(len(hop["sigs"]) == 3, hop)
    check(not os.path.exists(keydir), "hop keydir gone after bid")

    addrs = {hop["addrs"][k] for k in ("bid", "cutout", "ingress", "faucet")}
    check(len(addrs) == 4, hop["addrs"])

    prev = json.load(open(os.path.join(ROOT, "umbra/fixtures/prev_pubkeys.json")))
    prev_set = set(prev) if isinstance(prev, list) else set(prev["pubkeys"])
    new = {hop["addrs"][k] for k in ("bid", "cutout", "ingress")}
    check(new.isdisjoint(prev_set), (new, prev_set))

    hashes = template_hashes()
    check(len(hashes) >= 2, hashes)
    for sig in hop["sigs"]:
        tx = fetch_tx(sig)
        check(tx is not None, sig)
        keys = inspect_ix_data(tx)
        check(not (keys["programs"] & MEMO_PROGRAMS), keys["programs"])
        blob = keys["ix_data"]
        for h in hashes:
            check(h not in blob, "template sha256 in ix data")

    print(f"CHECKS_RUN={CHECKS_RUN}")
    print("SIGS", " ".join(hop["sigs"]))
    print("EXPLORER", " ".join(hop["explorers"]))


if __name__ == "__main__":
    main()
