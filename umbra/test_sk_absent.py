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

from umbra.eval_host import is_vultr

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def worker_find():
    ip = os.environ["VULTR_WORKER_IP"]
    cmd = [
        "ssh",
        "-o",
        "BatchMode=yes",
        f"root@{ip}",
        "find /opt/umbra /tmp \\( -name client.zip -o -name '*.sk' \\) 2>/dev/null",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    check(out.returncode == 0, f"ssh find failed: {out.stderr}")
    hits = [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]
    check(not hits, f"secret material on worker: {hits}")


def local_worker_with_sk_fails():
    """Mac holds client.zip; that filename on a worker tree is the leak the SSH find flags."""
    src = os.path.join(ROOT, "umbra", "artifacts", "client.zip")
    check(os.path.isfile(src), "mac client.zip present")
    with tempfile.TemporaryDirectory() as td:
        leaked = os.path.join(td, "client.zip")
        with open(src, "rb") as inf, open(leaked, "wb") as outf:
            outf.write(inf.read())
        check(os.path.basename(leaked) == "client.zip", "named client.zip")


def main():
    if is_vultr():
        worker_find()
    else:
        worker_find()  # still require SSH to worker when reachable
    local_worker_with_sk_fails()
    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
