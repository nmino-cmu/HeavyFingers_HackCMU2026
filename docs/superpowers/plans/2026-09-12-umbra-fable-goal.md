# STALE — DO NOT USE AS LAW

Use `2026-09-12-umbra-RULES.md` + one `2026-09-12-umbra-P*.md`. This file still says localhost-first and one Goal for everything.

---

# Umbra Fable 5.1 goal — run-until-finished plan

> **For agentic workers:** This plan is the **operating system** for a Cursor Goal. It does not implement Umbra in this session. The Goal (model **Fable 5.1** / `claude-fable-5-1-thinking-max`) pastes `docs/superpowers/specs/2026-09-12-umbra-GOAL-PROMPT.md` and does not stop until the Done gate is evidenced.

**Goal:** A single Fable 5.1 Goal builds Umbra to the max-FHE spec, gathering its own facts, writing its own tests, and passing those tests through an **independent** auditor before implementation; it loops until the Done gate is true.

**Architecture:** Builder Goal never marks a slice done. A fresh auditor (no builder chat, no builder memory) sees only spec + tests (then later spec + tests + diff). Codex Sol is the second-vendor XOR auditor. A ledger on disk is the only shared state.

**Tech Stack:** Cursor Goal · Fable 5.1 · Task `composer-2.5` (not `*-fast`) · `codex exec --ephemeral -s read-only -m gpt-5.6-sol` · Concrete-ML / OpenFHE / CryptoFace as the spec says

## Global Constraints

- Spec of record: `docs/superpowers/specs/2026-09-12-umbra-prize-design.md` (XOR law, §4 controls, Vultr CPU, no GPU).
- Physics note: `docs/superpowers/plans/2026-09-12-fhe-liveness-auction.md`.
- **Do not stop** for check-ins. Stop only if the user says pause/stop, or the Done gate is evidenced.
- **No `*-fast` agents.** Independent audit model is `composer-2.5` or a **new** Fable 5.1 context. Never `composer-2.5-fast`.
- OpenAI audit: Codex CLI only (`codex exec --ephemeral -s read-only -m gpt-5.6-sol "…" </dev/null`). No Cursor Sol.
- Never plaintext biometrics on Vultr. Never a cleartext server model.
- Do not commit secrets. Do not `git commit` unless the user later asks.
- Prize floor by **noon** local: Mac encrypt → Vultr FHE eval → Mac decrypt, with captured stdout.
- Hard stop for new scope: **Saturday 4:00pm EDT 2026-09-12**. After that, only evidence packaging.
- Client `sk` never uploaded. No GPU VM.

---

## Files the Goal owns

| Path | Role |
|---|---|
| `umbra/GATHERED.md` | Facts the Goal collected (Python arch, Vultr, packages, time left) |
| `umbra/LEDGER.md` | Append-only: slice, tests, audit ids, verdicts, evidence commands |
| `umbra/DONE.md` | Written **last**, only after Done gate commands were run in that turn |
| `umbra/audits/<utc>-<slice>-tests.md` | Packet sent to the test auditor |
| `umbra/audits/<utc>-<slice>-impl.md` | Packet sent to the XOR/impl auditor |
| `umbra/` | Application code the Goal creates as it goes |

---

## Loop (do not exit)

```
GATHER  →  pick next §11 slice  →  write tests  →  INDEPENDENT TEST AUDIT
        →  implement until tests pass  →  INDEPENDENT IMPL/XOR AUDIT
        →  append LEDGER  →  if Done gate: write DONE.md and stop
        →  else next slice
```

If an audit is FAIL or WEAK: fix the **tests or code**, re-audit (max 3). Then note in LEDGER and either drop that §4 row to **local/omit** (never server-cleartext) or change approach.

---

### Task 1: Goal prompt exists and is paste-ready

**Files:**
- Create: `docs/superpowers/specs/2026-09-12-umbra-GOAL-PROMPT.md`
- Create: `docs/superpowers/plans/2026-09-12-umbra-fable-goal.md` (this file)

**Interfaces:**
- Consumes: Umbra spec
- Produces: the string the human pastes into a **new Cursor Goal, model Fable 5.1**

- [x] **Step 1:** Write both files in the repo (this session).
- [ ] **Step 2:** Human opens Cursor Goal, selects **Fable 5.1**, pastes the GOAL-PROMPT, starts it. Do not start a Goal on Grok.

---

### Task 2: Independent test-audit contract (builder must copy this)

**Auditor sees:** spec § law + §4 row ids for this slice, and the test files. **Not** `LEDGER.md` rationalizations, not a “please pass” note.

**Auditor verdict (exactly one):** `PASS` | `FAIL` | `WEAK`

Must FAIL if any:

- Tests would pass if Vultr ran a plaintext `if` on the tensor
- Tests mock FHE to always return accept
- Tests do not fail when ciphertext is replaced by zeros
- Tests assert implementation internals instead of encrypt→eval→decrypt
- No command is specified to run the tests

**How the Goal invokes it:**

```
Task:
  description: Umbra test audit
  model: composer-2.5
  subagent_type: generalPurpose
  run_in_background: false
  prompt: |
    You are an independent test auditor. Do not implement. Do not edit.
    Read ONLY:
    - docs/superpowers/specs/2026-09-12-umbra-prize-design.md (law + §4)
    - <list test files>
    - umbra/audits/<this>-tests.md
    Output:
    VERDICT: PASS|FAIL|WEAK
    5 bullets max: what a cheat would still pass; what is missing.
```

---

### Task 3: Independent impl/XOR audit (second vendor)

After tests are green **on the machine**:

```
codex exec --ephemeral -s read-only -m gpt-5.6-sol "$(cat <<'EOF'
You audit Umbra XOR law. Do not write code.
Read docs/superpowers/specs/2026-09-12-umbra-prize-design.md and the diff/files listed in umbra/audits/<this>-impl.md
VERDICT: PASS|FAIL
Fail if any plaintext face/wav/mel/joints/minutiae/v is sent to a server handler that decrypts or classifies in the clear.
EOF
)" </dev/null
```

If Codex is unavailable, spawn a **new** Fable 5.1 Task with the same firewall (no builder history). Record the error in LEDGER; do not skip the audit.

---

### Task 4: Data the Goal must gather itself (no asking the human unless a secret is missing)

Write `umbra/GATHERED.md` with command output, not guesses:

| Fact | Command / source |
|---|---|
| Time now + hours to 16:00 EDT | `date` |
| Python arch | `file "$(which python3)"` must contain `arm64` |
| Python version | `python3 --version` (3.11 or 3.12 for Concrete) |
| Concrete | `python3 -c "import concrete_ml"` or install |
| OpenFHE / cmake / libomp | `brew list libomp cmake` |
| Vultr | env `VULTR_API_KEY` or existing instance; docs.vultr.com CPU SKUs |
| SSH target | `~/.ssh/config` or inventory |
| Solana | `solana --version` / install if hops slice |
| Disk | `df -h` on Mac and VM |
| Spec §4 / §11 | read the markdown |

If Vultr credentials are absent: implement and prove the FHE loop **localhost first**, keep the same encrypt/eval/decrypt API, then deploy when a key or IP appears. Do not invent keys. Do not block forever — note the gap and continue local-shaped worker that is VM-ready.

---

### Task 5: Tests the Goal must author (per slice)

Each slice gets **one** small runner (assert / `python -m` self-check), not a framework.

Minimum for the prize-floor slice (`umbra/test_fhe_roundtrip.py`):

- Encrypt a known `v`
- Worker (local or Vultr) returns ciphertext
- Decrypt ≠ plaintext `v`
- Decrypted bits match a cleartext reference circuit on that `v`
- Tamper: flip a ciphertext byte → decrypt fails or bits change
- Fail if worker logs contain raw `v` floats

Later slices add tests that **fail** if that §4 control is skipped or done in the clear on the worker.

---

### Task 6: Done gate (all must be true in the **same** turn as DONE.md)

1. `umbra/test_fhe_roundtrip.py` run **fresh**; exit 0; transcript in LEDGER.
2. Worker was Vultr **or** GATHERED proves no creds and the worker is the same binary path a VM would run; if creds exist, Vultr **must** be the eval host.
3. Latest test-audit `PASS` and latest XOR-audit `PASS` for the prize-floor slice.
4. Client does not send plaintext `v` (grep worker logs + XOR audit).
5. §11 walk continued until: a row cannot compile, or 15:30 EDT, or all FHE rows in §4 that are not “Impossible” have a circuit or an explicit LEDGER omit.
6. Demo script §8 can be executed with a recorded take **or** a fixture `v` (state which).
7. No `unhackable` in UI copy.

Only then write `umbra/DONE.md` and the Goal may stop.

---

## Human start (only human step)

1. New **Cursor Goal**.
2. Model: **Fable 5.1**.
3. Paste `docs/superpowers/specs/2026-09-12-umbra-GOAL-PROMPT.md` in full.
4. Leave it alone until `umbra/DONE.md` exists or you say pause.
