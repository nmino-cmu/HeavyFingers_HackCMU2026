#!/usr/bin/env python3
"""P7 S3: encrypted 64x64 face match. Two-key; face_B -> 0; plaintext 4xx."""
from __future__ import annotations

import ipaddress
import json
import os
import socket
import struct
import subprocess
import sys
import urllib.error
import urllib.request

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.eval_host import get_eval_host, is_vultr
from umbra.face_ckks import (
    PIXELS,
    decrypt_l2,
    encrypt_vec,
    evk_bytes,
    face_a,
    face_b,
    match_bit,
    new_context,
    pack_face,
    reference_match,
)

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def face_url():
    return os.environ["UMBRA_FACE_URL"].rstrip("/")


def face_ssh():
    return os.environ.get("UMBRA_FACE_SSH") or ("root@" + os.environ["UMBRA_FACE_PUBLIC_IP"])


def post_face(body: bytes, nonce: str = "umbra-p7"):
    req = urllib.request.Request(
        face_url() + "/face",
        data=body,
        method="POST",
        headers={"X-Umbra-Nonce": nonce, "Content-Type": "application/octet-stream"},
    )
    try:
        with urllib.request.urlopen(req, timeout=900) as resp:
            return resp.status, resp.read(), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def health():
    with urllib.request.urlopen(face_url() + "/health", timeout=15) as resp:
        return json.load(resp), resp.headers


def ssh(cmd: str, timeout: int = 30) -> str:
    out = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", face_ssh(), cmd],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    check(out.returncode == 0, f"ssh fail: {out.stderr}")
    return out.stdout


def main():
    host = get_eval_host()
    check(host in ("vultr", "mac"), f"EVAL_HOST={host}")

    src = open(os.path.join(ROOT, "umbra/worker/face_server.py"), encoding="utf-8").read()
    check("import insightface" not in src and "import torch" not in src, "no plaintext net import")
    check("onnxruntime" not in src, "no onnx")
    check(".decrypt(" not in src, "worker file must not decrypt")

    a, b = face_a(), face_b()
    check(reference_match(a, a) == 1, "ref A/A")
    check(reference_match(a, b) == 0, "ref A/B")

    h, hdrs = health()
    mid = h.get("machine_id") or hdrs.get("X-Umbra-Machine-Id")
    check(bool(mid) and mid != "unknown", f"machine_id {mid}")

    if is_vultr():
        want = ssh("cat /etc/machine-id").strip()
        check(mid == want, f"eval_host_machine_id {mid} != worker {want}")
        check(h.get("hostname", "").startswith("umbra-"), h.get("hostname"))
        pub = os.environ["UMBRA_FACE_PUBLIC_IP"]
        ip = ipaddress.ip_address(socket.gethostbyname(pub))
        check(ip.version == 4 and ip.is_global, "face ssh host must be public")
        # VPC bind: public :8084 must be closed
        sock = socket.socket()
        sock.settimeout(3)
        try:
            sock.connect((pub, 8084))
            open_pub = True
        except OSError:
            open_pub = False
        finally:
            sock.close()
        check(not open_pub, "8084 must not be public")
        hits = ssh(
            "find /opt/umbra/build/umbra /opt/umbra/face-venv /tmp/umbra-face.log "
            "\\( -name client.zip -o -name '*.sk' \\) 2>/dev/null || true"
        )
        check(not hits.strip(), f"sk on face host: {hits}")
        logs = ssh("tr '\\0' ' ' < /tmp/umbra-face.log 2>/dev/null | tail -c 20000 || true")
        check("0.2468" not in logs, "fixture token in logs")

    ctx = new_context()
    evk = evk_bytes(ctx)
    check(not __import__("tenseal").context_from(evk).has_secret_key(), "evk has no sk")

    body_ok = pack_face(evk, encrypt_vec(ctx, a), encrypt_vec(ctx, a))
    code, out, rh = post_face(body_ok, nonce="face-nonce-7")
    check(code == 200, f"A/A {code} {out[:200]}")
    check(rh.get("X-Umbra-Nonce") == "face-nonce-7", "nonce")
    check(rh.get("X-Umbra-Machine-Id") == mid, "machine header")
    if host == "vultr":
        check(len(out) >= 1_000_000, f"CKKS result too small {len(out)}")
    l2_ok = decrypt_l2(ctx, out)
    bit_ok = match_bit(l2_ok)
    check(bit_ok == 1, f"A/A l2={l2_ok} bit={bit_ok}")

    body_b = pack_face(evk, encrypt_vec(ctx, a), encrypt_vec(ctx, b))
    code_b, out_b, _ = post_face(body_b)
    check(code_b == 200, f"A/B {code_b}")
    bit_b = match_bit(decrypt_l2(ctx, out_b))
    check(bit_b == 0, f"face_B must be 0 l2={decrypt_l2(ctx, out_b)}")

    ctx2 = new_context()
    try:
        l2_wrong = decrypt_l2(ctx2, out)
        # TenSEAL may not throw; wrong sk must not recover A/A (~0).
        two_key_blocked = abs(l2_wrong - l2_ok) > 1.0
    except Exception:
        two_key_blocked = True
    check(two_key_blocked, "two-key must not recover A/A")

    plain = struct.pack(f">{PIXELS}f", *a)
    code_p, _, _ = post_face(plain)
    check(code_p >= 400, f"plaintext 64x64 must 4xx got {code_p}")

    print(f"CHECKS_RUN={CHECKS_RUN}")
    print(f"EVAL_HOST={host}")
    print(f"eval_host_machine_id={mid}")


if __name__ == "__main__":
    main()
