# Umbra P0 — Infra Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Two Vultr CPU VMs on one VPC, UFW correct, worker ≥16 GB, env + GATHERED match live IPs, smoke HTTP still works.

**Architecture:** Keep umbra-orch at 1 GB (ingress only). Upgrade umbra-worker in place to `vc2-6c-16gb` (or destroy/recreate on the same VPC/firewall if upgrade is refused). Do not merge onto one box.

**Tech Stack:** `vultr-cli`, Ubuntu 22.04, ufw, Docker, SSH.

## Global Constraints

Obey [`2026-09-12-umbra-RULES.md`](2026-09-12-umbra-RULES.md). Two VMs. No wallets in this phase. A 1 GB worker is **not** a ticket to local FHE — upgrade it. No GPU. No commit unless asked.

---

### Task 1: Confirm smoke (already done once)

**Files:**
- Modify: `umbra/GATHERED.md` if IPs or plans changed
- Test: shell only

**Interfaces:**
- Consumes: `~/.umbra-vultr.env` / `umbra/.env`
- Produces: live `ORCH_PUBLIC`, `WORKER_PUBLIC`, `UMBRA_ORCH_VPC_IP`, `UMBRA_FHE_VPC_IP`

- [ ] **Step 1: Account + list**

```bash
source ~/.umbra-vultr.env
vultr-cli account info
vultr-cli instance list
vultr-cli vpc list
```

Expected: credit present; labels `umbra-orch` / `umbra-worker`; VPC `10.20.0.0/24`.

- [ ] **Step 2: SSH + VPC ping**

```bash
ssh root@$VULTR_ORCH_IP 'hostname; ping -c 1 -W 2 '"$UMBRA_FHE_VPC_IP"
ssh root@$VULTR_WORKER_IP 'hostname; ping -c 1 -W 2 '"$UMBRA_ORCH_VPC_IP"
```

Expected: `umbra-orch` / `umbra-worker`, 0% loss.

- [ ] **Step 3: At execution start**

If those two steps already match GATHERED, mark this task done immediately (smoke already ran).

---

### Task 2: UFW on both boxes

**Files:** none in repo. Remote `/etc/ufw`.

- [ ] **Step 1: Orch rules**

```bash
ssh root@$VULTR_ORCH_IP 'ufw allow 22/tcp; ufw allow 8080/tcp; ufw allow from 10.20.0.0/24; ufw --force enable; ufw status verbose'
```

Expected: 22, 8080, and `10.20.0.0/24` ALLOW.

- [ ] **Step 2: Worker rules (no public FHE)**

```bash
ssh root@$VULTR_WORKER_IP 'ufw allow 22/tcp; ufw allow from 10.20.0.0/24; ufw --force enable; ufw status verbose'
```

Expected: 22 and VPC subnet only. No 8080/8081 from Anywhere.

- [ ] **Step 3: Re-hit smoke HTTP**

```bash
curl -sS --max-time 8 "$UMBRA_WORKER_URL/"
ssh root@$VULTR_ORCH_IP "curl -sS --max-time 5 http://$UMBRA_FHE_VPC_IP:8081/" || true
```

Expected: orch public still answers (or connection refused if the python smoke unit was stopped — that is OK). Worker public `:8081` from the Mac must time out.

---

### Task 3: Upgrade worker to 16 GB

**Files:**
- Modify: `umbra/.env`, `~/.umbra-vultr.env`, `umbra/GATHERED.md`

**Interfaces:**
- Produces: worker plan `vc2-6c-16gb`, RAM ≥ 16384. Public/VPC IPs may change — rewrite env.

- [ ] **Step 1: Upgrade (preferred)**

```bash
vultr-cli instance upgrade --help
vultr-cli instance update $UMBRA_WORKER_ID --plan vc2-6c-16gb
# if update/upgrade is not supported:
# snapshot optional; destroy worker; recreate with --vpc-ids $UMBRA_VPC_ID --firewall-group <worker-fw> --plan vc2-6c-16gb --os 1743 --label umbra-worker
```

Expected: plan `vc2-6c-16gb`. Pending charges rise (~$0.11/hr). Stop if `account info` pending + hourly would burn the remaining credit before 16:00 — then BLOCKED with the numbers, do not invent a Mac FHE host and call it Vultr.

- [ ] **Step 2: Wait SSH, Docker, VPC NIC**

```bash
ssh root@$VULTR_WORKER_IP 'free -m | head -2; docker info | head -3; ip -4 addr | grep 10.20'
```

Expected: Mem total ≥ 16000; docker; a `10.20.0.x` address. If the VPC IP changed, write it to env + GATHERED. Re-apply Task 2 UFW.

- [ ] **Step 3: Rewrite GATHERED**

Replace the “1 GB smoke” paragraph with the new plan, IPs, and `free -m` paste. Do not put the API key in GATHERED.

---

### Task 4: Phase gate

- [ ] **Step 1: Write `umbra/phases/P0-DONE.md`**

Must include: instance list, `free -m` on worker, ufw status both, VPC ping, `UMBRA_WORKER_URL`.

- [ ] **Step 2: Fresh cursor-grok-4.6-xhigh-fast** reads only RULES + this plan + P0-DONE + GATHERED. Last line `VERDICT: PASS` only if worker RAM ≥ 16 GB and orch ≠ worker.

Do not start P1 in this Goal.
