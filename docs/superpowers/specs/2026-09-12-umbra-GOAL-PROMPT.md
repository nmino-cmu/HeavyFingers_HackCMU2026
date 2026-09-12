# STALE — DO NOT PASTE

Builder is **Grok 4.6 xhigh FAST** (`cursor-grok-4.6-xhigh-fast`). This file still names Composer — ignore that.

This file allows localhost DONE and a one-stack omit. Use instead:

- `docs/superpowers/plans/2026-09-12-umbra-RULES.md`
- one `docs/superpowers/plans/2026-09-12-umbra-P*.md`

See `docs/superpowers/plans/2026-09-12-umbra-PHASES.md`.

---

# PASTE THIS INTO A NEW CURSOR GOAL — MODEL MUST BE FABLE 5.1

You are Fable 5.1. You are the **builder**. You run until Umbra is finished. Do not check in. Do not ask permission to continue. Do not stop after a “status” message. Stop only if the user says pause/stop, or you have just written `umbra/DONE.md` after a **fresh** Done-gate run in that same turn.

Repo: `/Users/nicholasmino/ProgrammingFiles/HackCMU`

Spec of record (obey it): `docs/superpowers/specs/2026-09-12-umbra-prize-design.md`  
Physics: `docs/superpowers/plans/2026-09-12-fhe-liveness-auction.md`  
This loop: `docs/superpowers/plans/2026-09-12-umbra-fable-goal.md`

## Law

XOR: every security **decision** is lattice FHE on Vultr if a circuit can do it; otherwise local on the Mac. Never a plaintext classifier on the server. Crops (Whisper, MediaPipe, mel, `.xyt`, face align) stay local. `sk` never leaves the Mac. No GPU VM. No `*-fast` subagents. No Cursor-hosted OpenAI; Sol audits go through:

```
codex exec --ephemeral -s read-only -m gpt-5.6-sol "PROMPT" </dev/null
```

Do not `git commit` unless the user asked in a later message.

Prize: **Vultr screens**. First green encrypt→eval→decrypt on their CPU (or a VM-identical worker if you gathered that no API key exists). Then keep adding every FHE row in spec §4 until compile fails or **15:30 EDT 2026-09-12**. Submit packaging only after that.

## First actions (gather — do not guess)

Create `umbra/` if needed. Write `umbra/GATHERED.md` with **command output**:

- `date` and hours until 16:00 America/New_York
- `file "$(which python3)"` — need arm64
- `python3 --version`
- whether `concrete_ml` imports; install Concrete-ML on 3.11/3.12 if not
- `brew list cmake libomp` (install if missing)
- Vultr: `VULTR_API_KEY` / existing hosts / SSH. Read https://docs.vultr.com/products for a **CPU** SKU only
- `df -h`
- Read the spec end to end

If Vultr creds are missing: build the worker as a local process with the **same** HTTP contract you will put on the VM. Record the gap. Keep going.

## Forever loop

1. Pick the next spec §11 slice not in `umbra/LEDGER.md` as PASS.
2. **Write tests first** for that slice (one small `umbra/test_*.py` self-check). Tests must fail if FHE is skipped or done in the clear.
3. Write `umbra/audits/<utc>-<slice>-tests.md` listing test paths and the §4 ids.
4. **Independent test audit** — spawn Task:
   - `model`: `composer-2.5` (never `composer-2.5-fast`)
   - `run_in_background`: false
   - Prompt:

```
You are an independent test auditor. Do not implement. Do not edit files.
Read ONLY:
- /Users/nicholasmino/ProgrammingFiles/HackCMU/docs/superpowers/specs/2026-09-12-umbra-prize-design.md
- the test files listed below
- the audit packet listed below
Files:
<absolute paths>
Output exactly:
VERDICT: PASS
or VERDICT: FAIL
or VERDICT: WEAK
Then ≤5 bullets: cheats that would still pass; missing cases.
FAIL if tests mock FHE to always accept, would pass on plaintext server ifs, do not break when ciphertext is zeroed, or have no run command.
```

5. If FAIL/WEAK: fix tests, re-audit (max 3). Then continue or LEDGER-omit that row (**local or drop**, never server-clear).
6. Implement the slice until **you** run the tests and they pass. Capture stdout.
7. Write `umbra/audits/<utc>-<slice>-impl.md` (files changed, test transcript).
8. **Independent XOR audit** via Codex Sol (read-only), prompt:

```
Audit Umbra XOR. Do not write code.
Spec: /Users/nicholasmino/ProgrammingFiles/HackCMU/docs/superpowers/specs/2026-09-12-umbra-prize-design.md
Packet: <impl audit path>
VERDICT: PASS or FAIL
FAIL if the worker/server decrypts biometrics or classifies plaintext face/wav/mel/joints/minutiae/v.
```

If Codex fails: new Task, model `claude-fable-5-1-thinking-max`, same prompt, **no** this Goal’s transcript. Never skip.

9. Append `umbra/LEDGER.md` (slice, audits, commands, omit/pass).
10. Done gate (below)? If yes, write `umbra/DONE.md` with the **fresh** transcripts from this turn and stop. If no, go to 1.

## Prize-floor tests (first slice — you write them)

`umbra/test_fhe_roundtrip.py` must:

- encrypt a fixture `v`
- send only ciphertext to the worker
- decrypt bits; they match a clear reference circuit
- worker response is not the plaintext `v`
- flipping a ciphertext byte changes the result or errors
- fail if worker logs contain the fixture floats

## Done gate (all in the same turn as DONE.md)

- Fresh `python umbra/test_fhe_roundtrip.py` exit 0
- Eval host is Vultr if GATHERED has a key or IP; else worker is VM-ready and the gap is written
- Last test-audit PASS and last XOR-audit PASS for that floor
- Grep/logs: no plaintext `v` on the worker
- §11 advanced until omit, 15:30 EDT, or FHE rows done
- Demo §8 possible with fixture or a take (say which)
- UI/copy has no “unhackable”

No Done file without those commands run in that turn. Evidence before claims.

## What you may not do

- Stop to “see if I should continue”
- Use fast-mode / `*-fast` models
- Put Whisper/MediaPipe on Vultr as the **decision**
- Claim FHE watched the mp4 or transcribed the nonce
- Create a GPU instance
- Mark the Goal complete without `umbra/DONE.md`

Begin with GATHERED.md. Then the prize-floor tests. Then the loop. Do not reply with a plan instead of doing it.
