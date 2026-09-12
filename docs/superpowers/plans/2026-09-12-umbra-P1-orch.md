# Umbra P1 — Orch + VPC contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Real `orch` container on umbra-orch that accepts blobs on public `:8080` and forwards them to a process on `$UMBRA_FHE_VPC_IP`. No FHE yet. `test_vpc.py` green.

**Architecture:** FastAPI (or stdlib `http.server` if that is enough) in Docker on orch. Worker runs a stub that echoes ciphertext and never sees floats. Bind stub to VPC IP only.

**Tech Stack:** Docker, Python 3.11+, `requests`, ufw, two VMs.

## Global Constraints

Obey [`2026-09-12-umbra-RULES.md`](2026-09-12-umbra-RULES.md). Requires `umbra/phases/P0-DONE.md`. No FHE compile in this phase.

---

### Task 1: Failing tests

**Files:**
- Create: `umbra/test_vpc.py`
- Create: `umbra/fixtures.py` (host-gate helpers only)

**Interfaces:**
- Consumes: `UMBRA_WORKER_URL`, `VULTR_ORCH_IP`, `VULTR_WORKER_IP`, `UMBRA_FHE_VPC_IP`, `UMBRA_VPC_ID`
- Produces: tests that fail until orch + stub are deployed

- [ ] **Step 1: Write `umbra/test_vpc.py`**

```python
import os, socket, sys, ipaddress, json, urllib.request, urllib.parse, subprocess, requests
if not __debug__:
    sys.exit("refusing -O")
CHECKS_RUN = 0
def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1

url = os.environ["UMBRA_WORKER_URL"]  # KeyError if unset — do not default
host = urllib.parse.urlparse(url).hostname
ip = ipaddress.ip_address(socket.gethostbyname(host))
check(ip.version == 4 and ip.is_global, "orch URL must be public IPv4")
check(str(ip) == os.environ["VULTR_ORCH_IP"], "URL host must be orch public")
org = json.load(urllib.request.urlopen(f"https://ipinfo.io/{ip}/json", timeout=8)).get("org", "")
check("AS20473" in org or "Vultr" in org or "Choopa" in org, org)
fhe_ip = os.environ["UMBRA_FHE_VPC_IP"]
ping = subprocess.run(["ssh", f"root@{os.environ['VULTR_ORCH_IP']}", f"ping -c 1 -W 2 {fhe_ip}"], capture_output=True)
check(ping.returncode == 0, ping.stderr.decode())
nc = subprocess.run(["nc", "-z", "-w", "2", os.environ["VULTR_WORKER_IP"], "8081"], capture_output=True)
check(nc.returncode != 0, "worker public 8081 must be closed")
h = requests.get(url.rstrip("/") + "/health", timeout=8).json()
mid = subprocess.check_output(["ssh", f"root@{os.environ['VULTR_ORCH_IP']}", "cat /etc/machine-id"], text=True).strip()
check(h["machine_id"] == mid, (h, mid))
blob = b"x" * 200_000
r = requests.post(url.rstrip("/") + "/eval", data=blob, headers={"X-Umbra-Nonce": "deadbeef"}, timeout=15)
check(r.status_code == 200 and len(r.content) > 0, r.status_code)
check(b"0.9137" not in r.content, "no fixture floats")
check("deadbeef" in r.headers.get("X-Umbra-Nonce", "") + r.text, "nonce echoed")
print(f"CHECKS_RUN={CHECKS_RUN}")
```

Use `urllib.parse` (import it). Do not skip if env missing.

- [ ] **Step 2: Run — must fail**

```bash
source ~/.umbra-vultr.env
python3 umbra/test_vpc.py
```

Expected: FAIL (no `/health` or `/eval` on real orch yet, or python smoke unit is not the contract).

- [ ] **Step 3: composer-2.5 test audit** (RULES prompt). FAIL if localhost default exists.

---

### Task 2: Stub on worker + orch proxy

**Files:**
- Create: `umbra/worker/stub_echo.py` — bind `UMBRA_FHE_VPC_IP:8081`, echo body, no decrypt
- Create: `umbra/orch/app.py` — `POST /eval` forwards to `http://$UMBRA_FHE_VPC_IP:8081/eval`
- Create: `umbra/deploy/Dockerfile.orch`, `umbra/deploy/Dockerfile.stub`
- Create: `umbra/deploy/orch.sh`, `umbra/deploy/stub.sh` — scp + docker run + ufw

**Interfaces:**
- `POST /eval` bytes in, bytes out. Header `X-Umbra-Nonce` echoed.
- `GET /health` → `{"role":"orch","machine_id":"...","hostname":"umbra-orch"}`
- Worker stub `GET /health` → worker machine-id. Listen `$UMBRA_FHE_VPC_IP:8081` only. Other paths (`/print` etc.) can 404 until later phases.

- [ ] **Step 1: Implement the two processes** (stdlib or FastAPI; one file each).
- [ ] **Step 2: Deploy**

```bash
# worker
scp umbra/worker/stub_echo.py root@$VULTR_WORKER_IP:/opt/umbra/
ssh root@$VULTR_WORKER_IP 'ufw allow from 10.20.0.0/24; docker run -d --name stub --network host ...'
# orch
scp umbra/orch/app.py root@$VULTR_ORCH_IP:/opt/umbra/
ssh root@$VULTR_ORCH_IP 'ufw allow 8080/tcp; docker run -d --name orch --network host ...'
```

- [ ] **Step 3: Re-run `python3 umbra/test_vpc.py`** Expected: PASS, `CHECKS_RUN>=8`.
- [ ] **Step 4: Fresh composer-2.5 re-runs the command.** Then `umbra/phases/P1-DONE.md`.

Do not start P2 in this Goal.
