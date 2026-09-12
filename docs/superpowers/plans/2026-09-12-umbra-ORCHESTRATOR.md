# Umbra orchestrator (thin dispatcher)

You do **not** implement Umbra. You do **not** open Fable as the builder. Compute is metered.

**Builder for every phase:** `composer-2.5` (never `*-fast`). **Fable 5.1** only if that builder’s lattice compile is stuck — then one empty-history Task + one retry, then next stack or `LOCAL_*` (RULES).

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
2. Next phase = first `P<N>` in [PHASES](2026-09-12-umbra-PHASES.md) verification order that has no `umbra/phases/P<N>-DONE.md`. After P4, if hour ≥ 14 America/New_York, next is P9; else P5…P8 then P9.
3. Spawn **one** Task: `composer-2.5`, empty history, prompt = [RULES](2026-09-12-umbra-RULES.md) + that `P*.md` + “stop at `umbra/phases/P<N>-DONE.md`.” Never `resume`.
4. When it returns, read **only** `umbra/phases/P<N>-DONE.md` (or `BLOCKED.md`). Do not read `umbra/**` source. Do not keep the Task transcript.
5. BLOCKED → halt. DONE → git add/commit/push (no `.env`) → goto 1.

Do not paste [GOAL-PROMPT](../specs/2026-09-12-umbra-GOAL-PROMPT.md). Do not open a Fable Goal for this loop.
