# Umbra P5 — OpenFHE print Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encrypted `.xyt` match vs enrolled digit template on umbra-worker (S4). Wrong finger / wrong key → 0. No Touch ID.

**Architecture:** OpenFHE process **separate** from Concrete. Bind `$UMBRA_FHE_VPC_IP:8082`. Orch routes `/print`. Templates at rest are ciphertext, ≥50 KB, entropy ≥ 7.9.

**Tech Stack:** OpenFHE on the worker. Mac: `.xyt` extract local; encrypt; decrypt bit.

## Global Constraints

Obey RULES. Requires **P4-DONE** (verification first). Try OpenFHE **and** Concrete for S4 on the worker. If both fail → `LOCAL_FHE` / `LOCAL_CLEAR` on the Mac (same `.xyt` → bit). Never a plaintext matcher on the worker.

**Orch:** add `POST /print` → `$UMBRA_FHE_VPC_IP:8082`. Redeploy orch. UFW as RULES. Bind print to `$UMBRA_FHE_VPC_IP` only.

---

### Task 1

**Files:** `umbra/test_print.py`, `umbra/worker/print_server.py`, `umbra/deploy/Dockerfile.print`

- [ ] Two-key; enroll A pinky / probe A index + card.end=pinky → 0; plaintext `.xyt` POST → 4xx; `find` on VM has no tiny float templates.
- [ ] New Fable 5.1 Task compiles OpenFHE match.
- [ ] Tests on `$UMBRA_WORKER_URL`. Codex XOR. `umbra/phases/P5-DONE.md`.
