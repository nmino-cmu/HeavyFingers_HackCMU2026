# Umbra P2 — Prize-floor FHE Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Verification floor: encrypt `v` on the Mac, eval bits, decrypt on the Mac. Try **Concrete and OpenFHE** on the worker. Local Mac only if both absolutely cannot compile (RULES). A cheat numpy worker must fail the suite.

**Architecture:** Client holds `sk`. Worker has server artifact + `evk` only. Orch `POST /eval` → `$UMBRA_FHE_VPC_IP:8081`. Circuit: card + `v` → bits (S5 minimum; more if it compiles). Fixtures are in RULES, not the old launch plan.

**Tech Stack:** Concrete-ML **and** OpenFHE tried on the **16 GB worker**. Eval on Vultr if either works.

## Global Constraints

Obey RULES. Requires P0 + P1 DONE. Worker RAM ≥ 16 GB. No Solana. `RESULT` + `STACKS_TRIED` in LEDGER. Local fallback must not be labeled Vultr.

---

### Task 1: Fixtures + failing floor tests

**Files:**
- Create: `umbra/fixtures.py` — values **copied from RULES** (do not open the Cursor launch plan)
- Create: `umbra/test_fhe_roundtrip.py`, `umbra/test_harness_negative.py`, `umbra/test_sk_absent.py`
- Create: `umbra/tools/cheat_worker.py`

**Interfaces:**
- `reference(v, card) -> ndarray[10] uint8` — pure numpy, no `concrete` import
- Client: `FHEModelClient` / `fhe.Client` — `quantize_encrypt_serialize` / `deserialize_decrypt_dequantize`

- [ ] **Step 1: Write tests** — two-key, evk-mismatch, freshness, `len(ct)>=100_000`, 256 body flips (no “or errors”), plaintext POST 4xx, nonce, `ssh docker logs`, host-gate. First line `if not __debug__: sys.exit("refusing -O")`. `test_sk_absent.py`: no `client.zip` / `*.sk` on the worker (`ssh find`, fail if SSH fails). If `EVAL_HOST=mac`, skip two-key-against-Vultr but still fail a worker that holds `sk`.
- [ ] **Step 2: `cheat_worker.py`** = `np.frombuffer` + `reference()` + bit bytes. `test_harness_negative.py` must `raise` against it.
- [ ] **Step 3: Run tests** — FAIL (no circuit).
- [ ] **Step 4: cursor-grok-4.6-xhigh-fast test audit.**

---

### Task 2: Compile + deploy (new Grok 4.6 xhigh FAST Task, empty history)

**Files:**
- Create: `umbra/circuits/choreo_floor.py` — the numpy function the compiler sees
- Create: `umbra/client.py`
- Create: `umbra/worker/choreo_server.py` — load `server.zip` only; no `decrypt`, no `client.zip`
- Create: `umbra/deploy/Dockerfile.choreo`

**Interfaces:**
- `POST /eval` body = ciphertext bytes + evk (multipart or two blobs). No JSON floats.
- Worker bind `$UMBRA_FHE_VPC_IP:8081`.

- [ ] **Step 1: Concrete on the worker** — new `cursor-grok-4.6-xhigh-fast` Task, this plan + RULES only. Fable 5.1 only if compile is stuck. If it fails, LEDGER `cmd`/`stderr`, then **OpenFHE** (second Task). If both fail on ≥16 GB, `LOCAL_FHE` then `LOCAL_CLEAR` on the Mac (RULES). Never plaintext on the worker.
- [ ] **Step 2: Deploy** replace stub. `ss` listen address is `$UMBRA_FHE_VPC_IP:8081`, not `0.0.0.0:8081`. Re-apply UFW.
- [ ] **Step 3:**

```bash
source ~/.umbra-vultr.env
python3 umbra/test_fhe_roundtrip.py
python3 umbra/test_harness_negative.py
python3 umbra/test_sk_absent.py
python3 umbra/test_vpc.py
```

Expected: exit 0. Floor `CHECKS_RUN>=20` if `EVAL_HOST=vultr`. Two-key/evk/freshness required for `VULTR_*` only.

- [ ] **Step 4: Codex Sol XOR** on `umbra/worker/**` and `umbra/deploy/**`.
- [ ] **Step 5: Fresh cursor-grok-4.6-xhigh-fast re-runs the commands.** `P2-DONE.md` lists `STACKS_TRIED` and `EVAL_HOST` per bit. No wallets.

This is the Vultr prize floor. Do not start P3 in this Goal.
