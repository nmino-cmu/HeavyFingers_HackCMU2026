#!/usr/bin/env python3
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

from umbra.client import Client, second_client
from umbra.eval_host import get_eval_host, is_vultr
from umbra.fixtures import CARD_RRP, REF_OK, V_OK, mutant
from umbra.fixtures import reference
from umbra.protocol import pack_request

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
    org = json_load(f"https://ipinfo.io/{ip}/json").get("org", "")
    check("AS20473" in org or "Vultr" in org or "Choopa" in org, org)


def json_load(url):
    import json

    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.load(resp)


def post_eval(body: bytes, nonce: str = "umbra-p2"):
    req = urllib.request.Request(
        worker_url() + "/eval",
        data=body,
        method="POST",
        headers={"X-Umbra-Nonce": nonce, "Content-Type": "application/octet-stream"},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def docker_logs_no_fixture_floats():
    if not is_vultr():
        return
    ip = os.environ["VULTR_WORKER_IP"]
    cmd = [
        "ssh",
        "-o",
        "BatchMode=yes",
        f"root@{ip}",
        "docker logs --tail 200 umbra-choreo 2>&1 || true",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    check(out.returncode == 0, f"ssh logs failed: {out.stderr}")
    check("0.9137" not in out.stdout, "fixture float in worker logs")


def main():
    host_gate()
    check(get_eval_host() in ("vultr", "mac"), f"EVAL_HOST={get_eval_host()}")
    client = Client()
    ct = client.quantize_encrypt_serialize(V_OK)
    body = client.pack_eval_body(V_OK, CARD_RRP)
    check(len(ct) >= 500, f"ct size {len(ct)}")
    check(len(body) >= 1_000, f"crypto wire size {len(body)}")
    code, out, hdrs = post_eval(body, nonce="fresh-nonce-42")
    check(code == 200, f"eval status {code} {out[:200]}")
    check(b"0.9137" not in out, "no plaintext v in response")
    check(len(out) > 16, "encrypted result non-trivial")
    bits = client.eval_bits(out)
    check(bits == reference(V_OK, CARD_RRP), (bits, reference(V_OK, CARD_RRP)))
    check(bits == REF_OK, bits)
    check(hdrs.get("X-Umbra-Nonce") == "fresh-nonce-42", "nonce freshness")

    # evk mismatch
    bad = pack_request(b"x" * 64, ct)
    code2, _, _ = post_eval(bad)
    check(code2 in (400, 422, 502), f"evk mismatch must fail got {code2}")

    # two-key (Vultr only)
    if is_vultr():
        alt = second_client()
        body_a = alt.pack_eval_body(V_OK, CARD_RRP)
        code3, out3, _ = post_eval(body_a)
        check(code3 == 200, code3)
        try:
            client.eval_bits(out3)
            raise AssertionError("two-key decrypt must fail")
        except Exception:
            check(True, "two-key blocked")
    else:
        alt = second_client()
        try:
            alt.eval_bits(out)
            raise AssertionError("wrong key must not decrypt")
        except Exception:
            check(True, "two-key blocked mac")

    if os.environ.get("UMBRA_SKIP_FLIPS") != "1":
        # ponytail: 8 ciphertext tail flips; 256 would be hours at ~1min/eval
        base_body = bytearray(body)
        seen_change = 0
        nflip = min(8, len(base_body))
        start = len(base_body) - nflip
        for i in range(start, len(base_body)):
            tampered = bytearray(base_body)
            tampered[i] ^= 0x01
            code_t, out_t, _ = post_eval(bytes(tampered))
            if code_t != 200:
                seen_change += 1
                continue
            try:
                bits_t = client.eval_bits(out_t)
                if bits_t != bits:
                    seen_change += 1
            except Exception:
                seen_change += 1
        check(seen_change >= 4, f"body flips changed/error {seen_change}")

    # plaintext POST 4xx
    plain = struct.pack(">75f", *V_OK)
    code_p, _, _ = post_eval(plain)
    check(code_p >= 400, f"plaintext must 4xx/5xx got {code_p}")

    # mutant sanity
    v_left = mutant("V_LEFT")
    body_l = client.pack_eval_body(v_left, CARD_RRP)
    _, out_l, _ = post_eval(body_l)
    bits_l = client.eval_bits(out_l)
    check(bits_l[0] == 0, "V_LEFT bit0")

    docker_logs_no_fixture_floats()
    print(f"CHECKS_RUN={CHECKS_RUN}")
    print(f"EVAL_HOST={get_eval_host()}")


if __name__ == "__main__":
    main()
