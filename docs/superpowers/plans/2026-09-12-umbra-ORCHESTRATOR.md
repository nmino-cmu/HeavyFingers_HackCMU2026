# Umbra orchestrator (thin dispatcher)

You do **not** implement Umbra. You do **not** open Fable as the builder. Compute is metered.

**Builder for every phase:** Grok 4.6 xhigh FAST (`cursor-grok-4.6-xhigh-fast`) (human 2026-09-12 07:18 ET). **Fable 5.1** only if that builder’s lattice compile is stuck — then one empty-history Task + one retry, then next stack or `LOCAL_CLEAR` (RULES). Never Composer 2.5.

Faster Vultr VMs are allowed for compile, test, eval, and the demo (**≥16 GB**, ~60 GB / high-CPU OK, no 96 GB+ unless a 60 OOM'd). Do not compile on live `umbra-choreo` until cutover XOR. Mac FHE = one probe run; if it cannot land on Vultr → Mac `LOCAL_CLEAR`.

## Unbreakable hard stop

Before spawning **anything**, run:

```bash
python3 umbra/hard_stop.py
```

Exit 99 means **stop forever**. Do not spawn another Task. Do not “one more slice.” Do not negotiate.

Hard stop is true if **any** of:

- Wall clock ≥ **2026-09-12 15:30:00 America/New_York**
- File `umbra/HARD_STOP` exists (touch that file to kill the run)
- `umbra/STOPPED.md` already exists

Then write/keep `umbra/STOPPED.md` and halt.

## Loop (no context rot)

1. `python3 umbra/hard_stop.py` or halt.
2. Human 2026-09-12 07:26: **P3–P8 in parallel** (separate worktrees + farm VMs). P9 only after P4-DONE (or hour ≥ 14 after P4).
3. Spawn **one Grok 4.6 xhigh FAST Task per live phase** (`cursor-grok-4.6-xhigh-fast`), empty history, prompt = [RULES](2026-09-12-umbra-RULES.md) + that `P*.md` + farm IP + “stop at `umbra/phases/P<N>-DONE.md`.” Never `resume`. Never Composer 2.5. Never two Tasks on the same VM or the same worktree.
4. When it returns, read **only** `umbra/phases/P<N>-DONE.md` (or `BLOCKED.md`). Do not read `umbra/**` source. Do not keep the Task transcript.
5. BLOCKED → halt. DONE → git add/commit/push (no `.env`) → goto 1.

Do not paste [GOAL-PROMPT](../specs/2026-09-12-umbra-GOAL-PROMPT.md). Do not open a Fable Goal for this loop.
