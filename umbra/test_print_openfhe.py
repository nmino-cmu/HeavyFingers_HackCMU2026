#!/usr/bin/env python3
"""S4 OpenFHE: client encrypts, farm-a EvalSub, client decrypts match bit."""
from __future__ import annotations

import os
import subprocess
import sys
import urllib.error
import urllib.request

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


def vpc_url():
    ip = os.environ["UMBRA_FHE_VPC_IP"]
    port = os.environ.get("UMBRA_OPENFHE_PRINT_PORT", "8092")
    return f"http://{ip}:{port}"


def _post(path, body, extra=None):
    headers = {"Content-Type": "application/octet-stream"}
    if extra:
        headers.update(extra)
    req = urllib.request.Request(vpc_url() + path, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def _run_checks():
    from umbra.fixtures import CARD_RRP
    from umbra.print_openfhe_client import OpenFHEPrintClient, second_openfhe_print_client
    from umbra.print_xyt import match_bit, parse_xyt

    fixt = os.path.join(ROOT, "umbra", "fixtures", "print")
    pinky = parse_xyt(open(os.path.join(fixt, "pinky.xyt"), encoding="utf-8").read())
    index = parse_xyt(open(os.path.join(fixt, "index.xyt"), encoding="utf-8").read())
    check(match_bit(pinky, pinky) == 1, "ref same")
    check(match_bit(pinky, index) == 0, "ref cross")

    client = OpenFHEPrintClient()
    code_e, out_e = _post("/enroll", client.pack_enroll(pinky), {"X-Umbra-Digit": "pinky"})
    check(code_e == 200, f"enroll {code_e} {out_e[:200]}")

    code, out = _post("/print", client.pack_print(pinky, CARD_RRP))
    check(code == 200, f"same {code} {out[:200]}")
    check(client.decrypt_bit(out) == 1, "same finger bit")

    code_b, out_b = _post("/print", client.pack_print(index, CARD_RRP))
    check(code_b == 200, f"cross {code_b} {out_b[:200]}")
    check(client.decrypt_bit(out_b) == 0, "wrong finger must be 0")

    alt = second_openfhe_print_client()
    code_k, _ = _post("/print", alt.pack_print(pinky, CARD_RRP))
    check(code_k >= 400, f"two-key status {code_k}")

    plain = open(os.path.join(fixt, "pinky.xyt"), "rb").read()
    code_p, _ = _post("/print", plain)
    check(code_p >= 400, f"plaintext xyt must 4xx got {code_p}")

    print(f"CHECKS_RUN={CHECKS_RUN}")
    print("EVAL_HOST=vultr")


def _can_import_openfhe():
    try:
        import openfhe  # noqa: F401

        return True
    except Exception:
        return False


def _run_on_farm():
    jump = os.environ.get("UMBRA_OPENFHE_JUMP") or os.environ.get("UMBRA_FARMA_IP")
    if not jump:
        raise SystemExit("set UMBRA_OPENFHE_JUMP (farm-a public IP)")
    key = os.path.expanduser("~/.ssh/id_ed25519")
    remote = f"/tmp/umbra-ofhe-test-{os.getpid()}"
    need = [
        "umbra/__init__.py",
        "umbra/protocol.py",
        "umbra/fixtures.py",
        "umbra/print_xyt.py",
        "umbra/print_openfhe_client.py",
        "umbra/test_print_openfhe.py",
        "umbra/fixtures/print/pinky.xyt",
        "umbra/fixtures/print/index.xyt",
    ]
    subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-i", key, f"root@{jump}", f"rm -rf {remote} && mkdir -p {remote}/umbra/fixtures/print"],
        check=True,
        timeout=30,
    )
    for rel in need:
        subprocess.run(
            ["scp", "-o", "BatchMode=yes", "-i", key, os.path.join(ROOT, rel), f"root@{jump}:{remote}/{rel}"],
            check=True,
            timeout=60,
        )
    vpc = os.environ["UMBRA_FHE_VPC_IP"]
    port = os.environ.get("UMBRA_OPENFHE_PRINT_PORT", "8092")
    env = f"UMBRA_FHE_VPC_IP={vpc} UMBRA_OPENFHE_PRINT_PORT={port} PYTHONPATH={remote}"
    proc = subprocess.run(
        [
            "ssh",
            "-o",
            "BatchMode=yes",
            "-i",
            key,
            f"root@{jump}",
            f"{env} python3 {remote}/umbra/test_print_openfhe.py; ec=$?; rm -rf {remote}; "
            "find /opt/umbra/print-openfhe /tmp -name client.zip -o -name '*.sk' 2>/dev/null | head; exit $ec",
        ],
        timeout=180,
    )
    raise SystemExit(proc.returncode)


def main():
    if _can_import_openfhe():
        _run_checks()
        return
    _run_on_farm()


if __name__ == "__main__":
    main()
