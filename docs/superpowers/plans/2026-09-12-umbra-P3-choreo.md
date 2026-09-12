# Umbra P3 — Choreography bits Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Isolated FHE bits S5–S14 (as many as compile) plus card binding S15 on the worker. One mutant → exactly one bit flips.

**Architecture:** Same Concrete/OpenFHE worker as P2. Widen the circuit. Card constants are **public inputs to the circuit**, not client-side XOR after decrypt.

**Tech Stack:** Same as P2.

## Global Constraints

Obey RULES. Requires P2-DONE. No wallets. Per bit: try Concrete **and** OpenFHE on the worker. If both fail (stderr in LEDGER), `LOCAL_FHE` then `LOCAL_CLEAR` on the Mac — still ship the bit so verification works. Never a worker-side plaintext predicate.

---

### Task 1: `umbra/test_choreo.py` + `umbra/test_ledger_consistency.py`

**Files:** create those two. Fixtures already in `umbra/fixtures.py`.

**Interfaces:**
- Mutants: `V_LEFT`, `V_FIST`, `V_ONECYCLE`, `V_RAMP`, `V_FAR`, `V_WRONGSIDE`, `V_TALKTHENMOVE`, `V_NOZOOM`, `V_INDEX`, `V_REVERSE`, `V_TWOFACES`, `V_NOHANDS`, `V_DUB`
- `IDX = {S5:0,…,S14:9}`
- Same `ct`, `CARD_RRP` → all-1; `CARD_LRP` → S5=0; `CARD_RLP` → S8=0; `CARD_RRI` → S11=0
- S8 pinned: `+0.1873`/side=right → 1; minus → 0; plus + side=left → 0
- S6: fist / one-cycle / ramp → 0 (not `max-min`)
- S9: talk-then-move → 0

- [ ] **Step 1: Write failing tests.** Auditor greps `umbra/client.py` for card logic after `decrypt` — FAIL if present.
- [ ] **Step 2: composer-2.5 test audit.**
- [ ] **Step 3: Implement circuit widen** via a **new** Fable 5.1 Task. Redeploy worker.
- [ ] **Step 4: Run choreo + floor + vpc + harness.** Codex XOR. Fresh composer-2.5 re-run. `umbra/phases/P3-DONE.md`.

Do not start P4 in this Goal.
