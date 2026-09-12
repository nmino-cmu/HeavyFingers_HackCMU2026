# Umbra P6 — Speaker + digit / AV Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encrypted log-mel CNN (S2) and/or end-digit / `av_sync` (S11, S14) on the worker. Raw wav never uploaded.

**Architecture:** Concrete-ML audio container on `$UMBRA_FHE_VPC_IP:8083`. Mel 64×64 computed on the Mac.

**Tech Stack:** Concrete-ML. No `*.pt` / `*.onnx` plaintext weights on the VM.

## Global Constraints

Obey RULES. Requires **P4-DONE**. Try Concrete **and** OpenFHE. If both fail → local Mac (encrypted mel still preferred). No torch/whisper **on the worker**. No wallets.

**Orch:** add `POST /audio` → `$UMBRA_FHE_VPC_IP:8083`. Redeploy orch. UFW. Bind `$UMBRA_FHE_VPC_IP` only.

---

### Task 1

**Files:** `umbra/test_voice.py`, `umbra/worker/audio_server.py`, `umbra/deploy/Dockerfile.audio`

- [ ] Two-key; mel_B vs A → 0; float32 64×64 POST → 4xx; `find` no `*.pt`.
- [ ] Mutants `V_INDEX` → S11=0, `V_DUB` → S14=0 if those bits still live in the choreo circuit instead of a second net — do not duplicate.
- [ ] Fable 5.1 Task compiles. Tests + XOR. `umbra/phases/P6-DONE.md`.
