# Umbra — one Grok 4.6 xhigh FAST Task per phase

Dispatcher: [`ORCHESTRATOR`](2026-09-12-umbra-ORCHESTRATOR.md). **Not** a Fable Goal. Paste RULES + **one** `P*.md` into a **Grok 4.6 xhigh FAST** (`cursor-grok-4.6-xhigh-fast`) Task (empty history). Fable only if compile is stuck. Never Composer 2.5.

Do **not** paste [`../specs/2026-09-12-umbra-GOAL-PROMPT.md`](../specs/2026-09-12-umbra-GOAL-PROMPT.md) (STALE).

## Now — verification (do this first)

| Phase | File | Stop | Needs |
|---|---|---|---|
| P0 Infra | [P0-infra](2026-09-12-umbra-P0-infra.md) | `umbra/phases/P0-DONE.md` | API key |
| P1 Orch | [P1-orch](2026-09-12-umbra-P1-orch.md) | `P1-DONE.md` | P0 |
| P2 Floor FHE | [P2-floor-fhe](2026-09-12-umbra-P2-floor-fhe.md) | `P2-DONE.md` | P0 16 GB + P1 |
| P3 Choreo | [P3-choreo](2026-09-12-umbra-P3-choreo.md) | `P3-DONE.md` | P2 |
| P4 S1 + S19 | [P4-s1-s19](2026-09-12-umbra-P4-s1-s19.md) | `P4-DONE.md` | P2 |

Each FHE row: Mac FHE probe (one run) → Vultr (live worker or extra compile VMs, Concrete **and** OpenFHE; SEAL too for face) → else Mac `LOCAL_CLEAR` (RULES). Never plaintext on a VM.

## Then — more verification

| Phase | File | Needs |
|---|---|---|
| P5 Print | [P5-print](2026-09-12-umbra-P5-print.md) | P4 |
| P6 Voice / digit | [P6-voice-digit](2026-09-12-umbra-P6-voice-digit.md) | P4 |
| P7 Face | [P7-face](2026-09-12-umbra-P7-face.md) | P4 |

## Last — money (do not start early)

| Phase | File | Notes |
|---|---|---|
| P8 Sealed bid | [P8-bid](2026-09-12-umbra-P8-bid.md) | Amounts under FHE, not the wallet |
| **P9 Hops / wallet** | [P9-hops-ui](2026-09-12-umbra-P9-hops-ui.md) | After P4. If the clock is short, **P9 before P5–P8**. |

P9 is required for the unlinkable-bid pitch. It is last, not dropped forever.
