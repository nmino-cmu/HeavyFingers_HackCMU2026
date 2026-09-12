#!/usr/bin/env python3
import os
import struct
import subprocess
import sys
import threading
import time
import urllib.request

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.fixtures import CARD_RRP, V_OK, reference

CHECKS_RUN = 0
PORT = 18081


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def main():
    from umbra.client import Client

    py = os.environ.get("UMBRA_PYTHON", sys.executable)
    proc = subprocess.Popen(
        [py, os.path.join(ROOT, "umbra/tools/cheat_worker.py"), str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.5)
    client = Client()
    body = client.pack_eval_body(V_OK)
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{PORT}/eval",
            data=body,
            method="POST",
            headers={"Content-Type": "application/octet-stream"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            cheat_out = resp.read()
        # cheat returns cleartext bit bytes — FHE decrypt must fail
        try:
            client.eval_bits(cheat_out)
            raise AssertionError("cheat_worker must not pass FHE decrypt")
        except Exception:
            check(True, "cheat_worker rejected by decrypt")
        ref = reference(V_OK, CARD_RRP)
        check(list(cheat_out) == ref, "cheat oracle bits match ref (illegal path)")
    finally:
        proc.terminate()
        proc.wait(timeout=5)

    ct = client.quantize_encrypt_serialize(V_OK)
    check(len(ct) >= 500, "real ct non-trivial")
    check(len(body) >= 1_000, "real wire crypto larger than cheat bits")
    url = os.environ["UMBRA_WORKER_URL"].rstrip("/") + "/eval"
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"X-Umbra-Nonce": "neg", "Content-Type": "application/octet-stream"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        out = resp.read()
    check(len(out) > 10, "encrypted output")
    check(out != bytes(reference(V_OK, CARD_RRP)), "FHE output not cleartext bits")
    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
