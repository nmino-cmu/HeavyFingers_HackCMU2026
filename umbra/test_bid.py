#!/usr/bin/env python3
"""P8 S24 sealed bid.

Single-key Concrete caveat: both amounts are encrypted under one
FHEModelClient key, so that key holder can decrypt both bids. The worker
never holds sk and must not see plaintext amounts.

Tie policy: equal amounts decrypt to index 0 (first bid wins).
"""
from __future__ import annotations

import ipaddress
import os
import pathlib
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import urllib.parse

import numpy as np

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.eval_host import get_eval_host
from umbra.protocol import pack_request

ARTIFACT_DIR = pathlib.Path(os.environ.get("UMBRA_BID_ARTIFACTS", "umbra/artifacts-bid"))
LOW, HIGH = 7391, 12457
CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def host_gate():
    url = os.environ["UMBRA_WORKER_URL"].rstrip("/")
    host = urllib.parse.urlparse(url).hostname
    ip = ipaddress.ip_address(socket.gethostbyname(host))
    check(ip.version == 4 and ip.is_global, "orch must be public IPv4")
    check(str(ip) == os.environ["VULTR_ORCH_IP"], "URL must be orch public IP")
    vpc = ipaddress.ip_address(os.environ["UMBRA_FHE_VPC_IP"])
    check(vpc in ipaddress.ip_network("10.20.0.0/24"), "bind target must be VPC")
    check(str(vpc) != "10.20.0.5", "never live P2 worker")


class BidClient:
    def __init__(self, artifact_dir=None, key_dir=None):
        from concrete.ml.deployment import FHEModelClient

        self.artifact_dir = pathlib.Path(artifact_dir or ARTIFACT_DIR)
        self._key_dir = key_dir or tempfile.mkdtemp(prefix="umbra-bid-")
        self._client = FHEModelClient(path_dir=str(self.artifact_dir), key_dir=self._key_dir)
        self._client.generate_private_and_evaluation_keys()
        self.evk = self._client.get_serialized_evaluation_keys()

    def encrypt_pair(self, a, b) -> bytes:
        x = np.asarray([[float(a), float(b)]], dtype=np.float64)
        return self._client.quantize_encrypt_serialize(x)

    def pack(self, a, b) -> bytes:
        return pack_request(self.evk, self.encrypt_pair(a, b))

    def winner_idx(self, encrypted_result: bytes) -> int:
        out = self._client.deserialize_decrypt_dequantize(encrypted_result)
        vals = np.asarray(out).reshape(-1)
        if vals.size == 1:
            return 1 if float(vals[0]) > 0 else 0
        return 1 if float(vals[1]) > float(vals[0]) else 0


HOP_PY = (
    "import sys,urllib.request,urllib.error\n"
    "vpc,port,path,nonce,ctype=sys.argv[1:6]\n"
    "body=sys.stdin.buffer.read()\n"
    "req=urllib.request.Request('http://%s:%s%s'%(vpc,port,path),data=body,method='POST',"
    "headers={'Content-Type':ctype,'X-Umbra-Nonce':nonce})\n"
    "try:\n"
    " r=urllib.request.urlopen(req,timeout=180)\n"
    " st,nh,out=r.status,r.headers.get('X-Umbra-Nonce') or '',r.read()\n"
    "except urllib.error.HTTPError as e:\n"
    " st,nh,out=e.code,e.headers.get('X-Umbra-Nonce') or '',e.read()\n"
    "sys.stdout.buffer.write(('%s\\n%s\\n'%(st,nh)).encode()+out)\n"
)


def ensure_hop():
    orch = os.environ["VULTR_ORCH_IP"]
    proc = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", f"root@{orch}", "cat > /tmp/umbra_bid_hop.py"],
        input=HOP_PY.encode(),
        capture_output=True,
        timeout=20,
    )
    check(proc.returncode == 0, proc.stderr.decode()[:200] or "hop install failed")


def post_bid(body: bytes, nonce: str = "umbra-p8", ctype: str = "application/octet-stream"):
    orch = os.environ["VULTR_ORCH_IP"]
    vpc = os.environ["UMBRA_FHE_VPC_IP"]
    proc = subprocess.run(
        [
            "ssh",
            "-o",
            "BatchMode=yes",
            f"root@{orch}",
            "python3",
            "/tmp/umbra_bid_hop.py",
            vpc,
            "8085",
            "/bid",
            nonce,
            ctype,
        ],
        input=body,
        capture_output=True,
        timeout=240,
    )
    check(proc.returncode == 0, proc.stderr.decode()[:400] or "ssh post failed")
    line1, rest = proc.stdout.split(b"\n", 1)
    nonce_line, out = rest.split(b"\n", 1)
    return int(line1), out, nonce_line.decode()


def logs_have_no_amounts():
    farm = os.environ["UMBRA_FARM_IP"]
    out = subprocess.run(
        [
            "ssh",
            "-o",
            "BatchMode=yes",
            f"root@{farm}",
            "docker logs --tail 200 umbra-bid 2>&1 || true; echo '---'; tail -n 200 /var/log/umbra-bid.log 2>/dev/null || true",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    check(out.returncode == 0, out.stderr)
    blob = out.stdout + out.stderr
    check(str(LOW) not in blob, "low amount in worker logs")
    check(str(HIGH) not in blob, "high amount in worker logs")


def farm_has_no_sk():
    farm = os.environ["UMBRA_FARM_IP"]
    out = subprocess.run(
        [
            "ssh",
            "-o",
            "BatchMode=yes",
            f"root@{farm}",
            "find /opt/umbra/artifacts-bid /opt/umbra/build /tmp "
            "\\( -name client.zip -o -name '*.sk' \\) 2>/dev/null || true",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    check(out.returncode == 0, out.stderr)
    hits = [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]
    check(not hits, f"secret material on farm: {hits}")


def compile_bid_circuit(out_dir: pathlib.Path) -> None:
    """TinyS5-style Linear(2,2) compare. Closed-form weights, no training."""
    import torch
    from torch import nn
    from concrete.ml.deployment import FHEModelDev
    from concrete.ml.torch.compile import compile_torch_model

    class TinyBid(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc = nn.Linear(2, 2, bias=False)
            with torch.no_grad():
                # out0=a-b, out1=b-a; argmax → winner index
                self.fc.weight.copy_(torch.tensor([[1.0, -1.0], [-1.0, 1.0]]))

        def forward(self, x):
            return self.fc(x)

    rng = np.random.RandomState(0)
    xs = rng.uniform(1.0, 20000.0, size=(48, 2)).astype(np.float32)
    extras = np.asarray([[1.0, 2.0], [2.0, 1.0], [100.0, 100.0], [5000.0, 15000.0], [15000.0, 5000.0]], dtype=np.float32)
    xs = np.vstack([xs, extras])
    model = TinyBid().eval()
    quantized = compile_torch_model(model, xs, n_bits=8)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    FHEModelDev(path_dir=str(out_dir), model=quantized).save()
    print(f"saved artifacts to {out_dir}")


def main():
    host_gate()
    ensure_hop()
    check(get_eval_host() in ("vultr", "mac"), f"EVAL_HOST={get_eval_host()}")
    client = BidClient()
    body = client.pack(LOW, HIGH)
    check(len(body) >= 200, f"crypto wire size {len(body)}")
    code, out, _ = post_bid(body)
    check(code == 200, f"bid {code} {out[:200]}")
    check(client.winner_idx(out) == 1, "high second amount must win")

    code_s, out_s, _ = post_bid(client.pack(HIGH, LOW))
    check(code_s == 200, f"swapped {code_s} {out_s[:200]}")
    check(client.winner_idx(out_s) == 0, "high first amount must win")

    alt = BidClient(key_dir=tempfile.mkdtemp(prefix="umbra-bid-b-"))
    code_a, out_a, _ = post_bid(alt.pack(LOW, HIGH))
    check(code_a == 200, f"alt {code_a}")
    try:
        client.winner_idx(out_a)
        raise AssertionError("two-key decrypt must fail")
    except Exception:
        check(True, "two-key blocked")

    code_p, _, _ = post_bid(struct.pack(">2q", LOW, HIGH))
    check(400 <= code_p < 500, f"int64 POST must 4xx got {code_p}")

    if get_eval_host() == "vultr":
        logs_have_no_amounts()
        farm_has_no_sk()

    print(f"CHECKS_RUN={CHECKS_RUN}")
    print(f"EVAL_HOST={get_eval_host()}")


if __name__ == "__main__":
    if "--compile" in sys.argv:
        compile_bid_circuit(ARTIFACT_DIR)
    else:
        main()
