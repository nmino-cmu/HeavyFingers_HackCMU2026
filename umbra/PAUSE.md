# Umbra UNPAUSED 2026-09-12 07:26 America/New_York

Human said **continue** and **parallel everything**. Orchestrator is live. P3–P8 spawn together. Do not resume `70b7d2bf`.

Hard stop still **continue** (deadline 15:30 ET). `umbra/HARD_STOP` was **not** created.

## Resume

Say **continue**. Next phase is **P3** (no `P3-DONE.md`). Spawn a **new** empty-history **Grok 4.6 xhigh FAST** (`cursor-grok-4.6-xhigh-fast`) Task (never resume `70b7d2bf`). Never Composer 2.5. Fast mode is standing law (`.cursor/rules/umbra-fast-mode.mdc`). Do not docker build without `</dev/null`. Do not `docker rm` `umbra-choreo`. Faster Vultr VMs OK for compile, test, eval, and the demo (not on live `:8086` until cutover XOR; ≥16 GB, ~60 GB / high-CPU fine, don’t go way overboard). Mac FHE = one probe; if Vultr cannot serve it → `LOCAL_CLEAR`.

P2 floor is live and must stay up:
- Orch `207.246.126.149:8080` → `http://10.20.0.5:8086`
- TinyS5 in `umbra-choreo` pid 191235 (in-memory). Disk: Mac `umbra/artifacts/{client,server}.zip` and worker `/opt/umbra/artifacts-p2/` plus restored `/opt/umbra/artifacts/server.zip`
- `test_sk_absent` forbids `client.zip` on the worker (P2 copy is `client.zip.bak`)

## Done (on origin/main)

| Phase | Commit | Fact |
|---|---|---|
| P0 | `fc01c93` | 16 GB worker `64.176.200.124` VPC `10.20.0.5` |
| P1 | `20b0531` | orch `:8080` |
| P2 | `2747e67` | Concrete S5 `EVAL_HOST=vultr` CHECKS_RUN=20. TinyS5 only (bit0 = v[0]≥0.5). OpenFHE missing. |

## P3 WIP (uncommitted, keep these files)

Modified: `umbra/client.py`, `deploy/choreo.sh`, `fixtures.py`, `protocol.py`, `test_fhe_roundtrip.py`, `test_harness_negative.py`, `tools/compile_choreo.py`, `worker/choreo_server.py`

Untracked: `umbra/test_choreo.py`, `umbra/test_ledger_consistency.py` (`brainstorm/` unrelated)

Last P3 compile (`umbra-compile` Exited 1): **`cleartext mismatch after 25000 steps`** — 128-wide `ChoreoP3` MLP did not fit fixtures. Do not retry that net. Next try: TinyS5-style Linear / per-bit thresholds (P2 lesson), or LOCAL_FHE with LEDGER. Reuse `umbra-choreo` (already has concrete-ml + ld); do not pip in a new container.

Agent [P3 choreography bits](70b7d2bf-6d4d-4e63-b721-1f3d093fbb5e) was interrupted; **do not resume it**.

## Do not

- Commit `umbra/.env`
- `docker build` with SSH heredoc stdin (hangs)
- `docker commit` on this worker (pauses/hangs)
- Label Mac eval as Vultr
- Start P8/P9 before P4-DONE (P9 before P5–P8 only if hour ≥ 14 ET after P4)
