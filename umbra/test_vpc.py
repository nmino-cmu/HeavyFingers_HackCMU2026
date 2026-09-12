import ipaddress
import json
import os
import socket
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

if not __debug__:
    sys.exit("refusing -O")

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


url = os.environ["UMBRA_WORKER_URL"]
host = urllib.parse.urlparse(url).hostname
ip = ipaddress.ip_address(socket.gethostbyname(host))
check(ip.version == 4 and ip.is_global, "orch URL must be public IPv4")
check(str(ip) == os.environ["VULTR_ORCH_IP"], "URL host must be orch public")
org = json.load(urllib.request.urlopen(f"https://ipinfo.io/{ip}/json", timeout=8)).get("org", "")
check("AS20473" in org or "Vultr" in org or "Choopa" in org, org)
fhe_ip = os.environ["UMBRA_FHE_VPC_IP"]
ping = subprocess.run(
    ["ssh", f"root@{os.environ['VULTR_ORCH_IP']}", f"ping -c 1 -W 2 {fhe_ip}"],
    capture_output=True,
)
check(ping.returncode == 0, ping.stderr.decode())
nc = subprocess.run(
    ["nc", "-z", "-w", "2", os.environ["VULTR_WORKER_IP"], "8081"],
    capture_output=True,
)
check(nc.returncode != 0, "worker public 8081 must be closed")
with urllib.request.urlopen(url.rstrip("/") + "/health", timeout=8) as resp:
    h = json.load(resp)
mid = subprocess.check_output(
    ["ssh", f"root@{os.environ['VULTR_ORCH_IP']}", "cat /etc/machine-id"],
    text=True,
).strip()
check(h["machine_id"] == mid, (h, mid))
blob = b"x" * 200_000
req = urllib.request.Request(
    url.rstrip("/") + "/eval",
    data=blob,
    method="POST",
    headers={"X-Umbra-Nonce": "deadbeef", "Content-Type": "application/octet-stream"},
)
with urllib.request.urlopen(req, timeout=15) as resp:
    body = resp.read()
    nonce_h = resp.headers.get("X-Umbra-Nonce") or ""
check(len(body) > 0, "empty eval")
check(b"0.9137" not in body, "no fixture floats")
check("deadbeef" in nonce_h + body.decode("latin1", "replace"), "nonce echoed")
check(body == blob, "stub echoes ciphertext")
print(f"CHECKS_RUN={CHECKS_RUN}")
