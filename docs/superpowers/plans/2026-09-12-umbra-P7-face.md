# Umbra P7 — CryptoFace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encrypted 64×64 face match (S3) on umbra-worker. Eval host machine-id is the **worker**. Start the job before any demo.

**Architecture:** Separate SEAL/CryptoFace process on `$UMBRA_FHE_VPC_IP:8084`. ~15–25 min eval is allowed. Mac aligns the crop only.

**Tech Stack:** CryptoFace + SEAL on **x86 worker**. Do not require a Mac Metal port.

## Global Constraints

Obey RULES. Requires **P4-DONE** + 16 GB worker. Try CryptoFace/SEAL **and** one other stack (or a second build). If both fail → `LOCAL_FHE` / `LOCAL_CLEAR` on the Mac (aligned 64×64). **No** plaintext ArcFace on the worker. Label `EVAL_HOST` honestly.

**Orch:** add `POST /face` → `$UMBRA_FHE_VPC_IP:8084`. Redeploy orch. UFW. Bind `$UMBRA_FHE_VPC_IP` only.

---

### Task 1

**Files:** `umbra/test_face.py`, `umbra/worker/face_server.py`, `umbra/deploy/Dockerfile.face`

- [ ] Two-key; face_B → 0; plaintext 64×64 POST → 4xx; `len(r.content)>=1_000_000` if CKKS ships; `eval_host_machine_id` == worker `/etc/machine-id`.
- [ ] Fable 5.1 Task. Tests + XOR. `umbra/phases/P7-DONE.md`.
