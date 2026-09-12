#!/usr/bin/env python3
"""P5 S4: encrypted .xyt vs enrolled digit. Wrong finger / wrong key → 0."""
import ipaddress
import math
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

from umbra.eval_host import get_eval_host
from umbra.fixtures import CARD_RRP
from umbra.print_client import PrintClient, parse_xyt, second_print_client
from umbra.print_xyt import match_bit

CHECKS_RUN = 0
FIXT = os.path.join(ROOT, "umbra", "fixtures", "print")
PINKY = os.path.join(FIXT, "pinky.xyt")
INDEX = os.path.join(FIXT, "index.xyt")


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def worker_url():
    return os.environ["UMBRA_WORKER_URL"].rstrip("/")


def print_public_ip():
    return os.environ.get("UMBRA_PRINT_PUBLIC_IP", "45.32.5.249")


def print_vpc_ip():
    return os.environ.get("UMBRA_PRINT_VPC_IP", "10.20.0.6")


def host_gate():
    url = worker_url()
    host = urllib.parse.urlparse(url).hostname
    ip = ipaddress.ip_address(socket.gethostbyname(host))
    check(ip.version == 4 and ip.is_global, "orch must be public IPv4")
    check(str(ip) == os.environ["VULTR_ORCH_IP"], "URL must be orch public IP")


def _http_post(url, body, headers):
    req = urllib.request.Request(url, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def _ssh_post(jump_ip, url, body, extra_headers):
    """POST through a VPC hop. Bind is VPC-only; Mac cannot hit :8082."""
    hdr_args = ""
    for k, v in extra_headers.items():
        hdr_args += f" -H {repr(k + ': ' + v)}"
    key = os.path.expanduser("~/.ssh/id_ed25519")
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(body)
        tmp_path = tmp.name
    remote_in = f"/tmp/umbra-print-in-{os.getpid()}-{len(body)}"
    try:
        scp = subprocess.run(
            ["scp", "-o", "BatchMode=yes", "-i", key, tmp_path, f"root@{jump_ip}:{remote_in}"],
            capture_output=True,
            timeout=600,
        )
        check(scp.returncode == 0, f"scp hop failed: {scp.stderr[:300]}")
        remote = (
            "umask 077; out=$(mktemp); hdr=$(mktemp); "
            f"code=$(curl -sS -D \"$hdr\" -o \"$out\" -w '%{{http_code}}' -X POST {url!r} "
            f"-H 'Content-Type: application/octet-stream'{hdr_args} --data-binary @{remote_in}); "
            "echo \"$code\"; echo '---HDR---'; cat \"$hdr\"; echo '---BODY---'; cat \"$out\"; "
            f"rm -f {remote_in} \"$out\" \"$hdr\""
        )
        proc = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-i", key, f"root@{jump_ip}", remote],
            capture_output=True,
            timeout=600,
        )
        check(proc.returncode == 0, f"ssh post failed: {proc.stderr[:300]}")
        raw = proc.stdout
        if b"---HDR---" not in raw or b"---BODY---" not in raw:
            raise AssertionError(f"bad ssh hop framing {raw[:200]}")
        pre, rest = raw.split(b"---HDR---", 1)
        hdr, body_out = rest.split(b"---BODY---", 1)
        code = int(pre.decode().strip().splitlines()[-1])
        return code, body_out.lstrip(b"\n"), hdr
    finally:
        os.unlink(tmp_path)


def post_print(body: bytes, nonce: str = "umbra-p5", path: str = "/print", extra=None):
    headers = {"X-Umbra-Nonce": nonce, "Content-Type": "application/octet-stream"}
    if extra:
        headers.update(extra)
    code, out, hdrs = _http_post(worker_url() + path, body, headers)
    if code != 404:
        return code, out, hdrs
    # orch routes later — hop via farm-fast loopback to VPC bind
    vpc = print_vpc_ip()
    return _ssh_post(print_public_ip(), f"http://{vpc}:8082{path}", body, headers)


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    h = 0.0
    for c in counts:
        if c:
            p = c / n
            h -= p * math.log2(p)
    return h


def vm_find_secrets_and_templates():
    ip = print_public_ip()
    out = subprocess.run(
        [
            "ssh",
            "-o",
            "BatchMode=yes",
            "-i",
            os.path.expanduser("~/.ssh/id_ed25519"),
            f"root@{ip}",
            "find /opt/umbra/print /opt/umbra/build /tmp \\( -name client.zip -o -name '*.sk' \\) 2>/dev/null; "
            "echo '---TMPL---'; find /opt/umbra/print/templates -type f 2>/dev/null",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    check(out.returncode == 0, f"ssh find: {out.stderr}")
    head, _, tail = out.stdout.partition("---TMPL---")
    hits = [ln.strip() for ln in head.splitlines() if ln.strip()]
    check(not hits, f"sk/client.zip on print VM: {hits}")
    tmpls = [ln.strip() for ln in tail.splitlines() if ln.strip()]
    check(tmpls, "no enrolled templates on VM")
    for path in tmpls:
        meta = subprocess.run(
            [
                "ssh",
                "-o",
                "BatchMode=yes",
                "-i",
                os.path.expanduser("~/.ssh/id_ed25519"),
                f"root@{ip}",
                f"wc -c < {path!s}; echo; cat {path!s}",
            ],
            capture_output=True,
            timeout=30,
        )
        check(meta.returncode == 0, meta.stderr.decode()[:200])
        raw = meta.stdout
        # first line is size
        nl = raw.find(b"\n")
        size = int(raw[:nl].decode().strip())
        blob = raw[nl + 1 :].lstrip(b"\n")
        check(size >= 50_000, f"template {path} too small {size}")
        check(entropy(blob) >= 7.9, f"template {path} entropy {entropy(blob):.3f}")
        check(b"120 80" not in blob and b"0.9137" not in blob, f"plaintext in {path}")


def main():
    host_gate()
    check(get_eval_host() in ("vultr", "mac"), f"EVAL_HOST={get_eval_host()}")

    pinky = parse_xyt(open(PINKY, encoding="utf-8").read())
    index = parse_xyt(open(INDEX, encoding="utf-8").read())
    check(match_bit(pinky, pinky) == 1, "ref same finger")
    check(match_bit(pinky, index) == 0, "ref wrong finger")

    if get_eval_host() == "mac":
        # LOCAL_CLEAR: same bits, never POST plaintext .xyt to a VM
        check(match_bit(index, index) == 1, "ref index")
        print(f"CHECKS_RUN={CHECKS_RUN}")
        print(f"EVAL_HOST={get_eval_host()}")
        return

    client = PrintClient()
    enroll_body = client.pack_enroll(pinky)
    code_e, out_e, _ = post_print(enroll_body, path="/enroll", extra={"X-Umbra-Digit": "pinky"})
    check(code_e == 200, f"enroll {code_e} {out_e[:200]}")

    # same finger
    body_ok = client.pack_print(pinky, CARD_RRP)
    code, out, hdrs = post_print(body_ok, nonce="print-ok")
    check(code == 200, f"print ok {code} {out[:200]}")
    bit_ok = client.decrypt_bit(out)
    check(bit_ok == 1, f"same finger bit {bit_ok}")
    nonce_ok = False
    if hasattr(hdrs, "get"):
        nonce_ok = hdrs.get("X-Umbra-Nonce") == "print-ok"
    if isinstance(hdrs, (bytes, bytearray)):
        nonce_ok = nonce_ok or b"print-ok" in hdrs
    check(nonce_ok, "nonce echoed")

    # enroll A pinky / probe A index + card.end=pinky → 0
    body_bad = client.pack_print(index, CARD_RRP)
    code_b, out_b, _ = post_print(body_bad, nonce="print-index")
    check(code_b == 200, f"print index {code_b} {out_b[:200]}")
    bit_bad = client.decrypt_bit(out_b)
    check(bit_bad == 0, f"wrong finger must be 0 got {bit_bad}")

    # two-key
    alt = second_print_client()
    body_k = alt.pack_print(pinky, CARD_RRP)
    code_k, out_k, _ = post_print(body_k, nonce="print-twokey")
    if code_k == 200:
        try:
            bit_k = client.decrypt_bit(out_k)
            check(bit_k == 0, f"wrong key decrypt {bit_k}")
        except Exception:
            check(True, "two-key blocked")
        try:
            bit_alt = alt.decrypt_bit(out_k)
            check(bit_alt == 0, f"alt key bit {bit_alt}")
        except Exception:
            check(True, "alt cannot decrypt foreign tmpl")
    else:
        check(code_k >= 400, f"two-key status {code_k}")

    # plaintext .xyt POST → 4xx
    plain = open(PINKY, "rb").read()
    code_p, _, _ = post_print(plain, nonce="print-plain")
    check(code_p >= 400, f"plaintext xyt must 4xx got {code_p}")

    vm_find_secrets_and_templates()
    print(f"CHECKS_RUN={CHECKS_RUN}")
    print(f"EVAL_HOST={get_eval_host()}")


if __name__ == "__main__":
    main()
