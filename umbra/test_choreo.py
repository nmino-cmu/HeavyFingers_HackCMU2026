#!/usr/bin/env python3
"""P3 choreography bits S5–S14 + card binding (S15 public inputs)."""
import ipaddress
import os
import socket
import struct
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.client import Client
from umbra.eval_host import get_eval_host
from umbra.fixtures import (
    CARD_LRP,
    CARD_RLP,
    CARD_RRI,
    CARD_RRP,
    IDX,
    MUTANTS,
    REF_OK,
    V_OK,
    encode_card,
    mutant,
    reference,
)

CHECKS_RUN = 0


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


def post_eval(body: bytes, nonce: str = "umbra-p3"):
    req = urllib.request.Request(
        worker_url() + "/eval",
        data=body,
        method="POST",
        headers={"X-Umbra-Nonce": nonce, "Content-Type": "application/octet-stream"},
    )
    try:
        with urllib.request.urlopen(req, timeout=900) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def eval_bits(client, v, card):
    body = client.pack_eval_body(v, card)
    code, out, _ = post_eval(body)
    check(code == 200, f"eval {code} {out[:200]}")
    return client.eval_bits(out)


def audit_no_client_card_xor():
    src = open(os.path.join(ROOT, "umbra/client.py"), encoding="utf-8").read()
    idx = src.find("def eval_bits")
    tail = src[idx:] if idx >= 0 else src
    check("reference(" not in tail, "client eval_bits must not call reference()")
    if "deserialize_decrypt" in tail:
        after = tail.split("deserialize_decrypt", 1)[1]
        check("encode_card" not in after and "CARD_" not in after, "client must not apply card after decrypt")


def main():
    host_gate()
    audit_no_client_card_xor()
    check(get_eval_host() in ("vultr", "mac"), f"EVAL_HOST={get_eval_host()}")

    client = Client()
    bits_ok = eval_bits(client, V_OK, CARD_RRP)
    ref_ok = reference(V_OK, CARD_RRP)
    check(bits_ok == ref_ok, (bits_ok, ref_ok))
    check(bits_ok == REF_OK, bits_ok)

    # same ciphertext, different public card constants (S15 binding)
    ct = client.quantize_encrypt_serialize(V_OK)
    body_rrp = client.pack_eval_body_from_ct(ct, CARD_RRP)
    body_lrp = client.pack_eval_body_from_ct(ct, CARD_LRP)
    check(body_rrp != body_lrp, "card must change wire body")
    _, out_rrp, _ = post_eval(body_rrp)
    _, out_lrp, _ = post_eval(body_lrp)
    bits_rrp = client.eval_bits(out_rrp)
    bits_lrp = client.eval_bits(out_lrp)
    check(bits_rrp == REF_OK, bits_rrp)
    check(bits_lrp[IDX["S5"]] == 0, f"CARD_LRP S5 {bits_lrp}")
    check(sum(bits_lrp) < sum(bits_rrp), "card flip must change decrypted bits")

    bits_rlp = eval_bits(client, V_OK, CARD_RLP)
    check(bits_rlp[IDX["S8"]] == 0, f"CARD_RLP S8 {bits_rlp}")
    bits_rri = eval_bits(client, V_OK, CARD_RRI)
    check(bits_rri[IDX["S11"]] == 0, f"CARD_RRI S11 {bits_rri}")

    # S8 pinned: +0.1873 / side=right -> 1; minus -> 0; plus + side=left -> 0
    v_plus = list(V_OK)
    v_plus[34] = 0.1873
    check(reference(v_plus, CARD_RRP)[IDX["S8"]] == 1, "ref S8 plus right")
    v_minus = list(V_OK)
    v_minus[34] = -0.1873
    check(reference(v_minus, CARD_RRP)[IDX["S8"]] == 0, "ref S8 minus right")
    check(reference(v_plus, CARD_RLP)[IDX["S8"]] == 0, "ref S8 plus left card")

    # S6 / S9 mutants
    for name in ("V_FIST", "V_ONECYCLE", "V_RAMP"):
        b = eval_bits(client, mutant(name), CARD_RRP)
        check(b[IDX["S6"]] == 0, f"{name} S6 {b}")
    check(eval_bits(client, mutant("V_TALKTHENMOVE"), CARD_RRP)[IDX["S9"]] == 0, "V_TALKTHENMOVE S9")

    # one mutant -> exactly one bit flips vs REF_OK
    for m in MUTANTS:
        v = mutant(m)
        got = eval_bits(client, v, CARD_RRP)
        want = reference(v, CARD_RRP)
        check(got == want, f"{m} got={got} want={want}")
        diff = [i for i, (a, b) in enumerate(zip(got, want)) if a != b]
        check(not diff, f"{m} mismatch at {diff}")
        if m != "V_REVERSE":
            flips = [i for i, (a, b) in enumerate(zip(got, REF_OK)) if a != b]
            check(len(flips) >= 1, f"{m} must flip at least one bit {got}")

    # plaintext rejected
    plain = struct.pack(">75f", *V_OK)
    code_p, _, _ = post_eval(plain)
    check(code_p >= 400, f"plaintext must 4xx got {code_p}")

    if get_eval_host() == "vultr":
        ip = os.environ["VULTR_WORKER_IP"]
        out = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", f"root@{ip}", "docker logs --tail 200 umbra-choreo 2>&1 || true"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        check(out.returncode == 0, out.stderr)
        check("0.9137" not in out.stdout, "fixture float in worker logs")

    print(f"CHECKS_RUN={CHECKS_RUN}")
    print(f"EVAL_HOST={get_eval_host()}")


if __name__ == "__main__":
    main()
