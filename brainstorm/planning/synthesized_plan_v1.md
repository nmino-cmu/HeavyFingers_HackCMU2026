# Synthesized ideation plan v1

Fri Sep 11, 2026. Inputs: [Fable plan](fable_plan.md), [Astra plan](astra_plan.md), [ground truth](../research/competition_ground_truth.md).

This is **not** an average. Disagreements are resolved below. Do not launch the 100 until the 8-auditor pass and `final_ideation_plan.md` exist.

Objective: maximize **P(≥1 prize)** with a real **overall-win** path. 19h build. One track. 3 min demo. Ignore campus-only cohorts.

---

## Disagreements (explicit)

| Topic | Fable | Astra | Resolution | Why |
|---|---|---|---|---|
| Launch the 100 now? | Yes at 9pm; UNKNOWNs reweight at jury | **No** until preflight, model check, staffing | **No until audit + 10-min preflight.** Then launch. Do not wait on K2/Vultr/Sandia | User forbade launch before audit. Astra is right that a bad runtime wastes the night. Fable is right that UNKNOWNs change weights, not cells |
| Score scale | Integers 1–5 | Richer, closer to user 0–10 | **0–10 as specified in the user rubric.** Integers only. ≤20-word justification each | User letter definitions are the contract. Fable’s 1–5 loses resolution the later ranks need |
| Letter `R` | Fable = track **Relevance** | User = **Reliability** | **User letters win.** Track relevance = `Rel` (0–10). Reliability stays `R` | Silent collision would corrupt rankings |
| Raw idea count | 20 = 5 obvious-dump + 15 real | 15 raw, no dump | **5 obvious-dump + 15 real + top 3 developed** | Dump is cheap and estimates the field (Fable). Depth stays on 15+3 (both) |
| Gemini specialists | 5 (eligibility rides free) | 8 | **6** | Fable’s “rides free” is correct; 5 is thin for multimodal-only search |
| Solana / Auth0 / Mongo | 9 / 8 / 6 | 8 / 8 / 8 | **8 / 8 / 6** | Solana thin-field is real; Mongo persist-only will flood the room — hunt Atlas *features*, not more slot count |
| IFM / Sandia | 6 / 6 | 4 / 3 | **5 / 5** | Dedicated prizes, thin field, unstated bars. 3 is too few; 6 overweights UNKNOWN access |
| Open-world | 16 TRACK | 20 open | **18 open-world** (must still name a home track) | Need grand-path mass; every submit needs a track |
| Physical I/O cohort | 5 (Medicly pattern) | none | **4 Physical I/O** | 2025 grand was visible sensor→spatial transform. Not campus-specific |
| Pipeline duration | Hard 1h50m ideation, build by 10:50pm | Full tournament; abort to build if clock dies | **Run the user’s full pipeline.** Escape hatch: if 100-loop overruns, skip build-sim on ranks 16–30 and shrink jury to 8 — Fable’s skip table. Never call a partial run “the 100” | User forbade premature convergence. Fable’s 90-min tournament is too shallow for 300 ideas |
| Loop-1 web search | Forbidden | More verification later | **No web on loop 1.** Red team + later stages may search | 100 agents googling “food hackathon” is mode collapse |
| P(any prize) | `p_max + 0.5*(1-p_max)*p_rest` | Scenario overlay, no naive sum | **Keep Fable’s formula** + Astra’s 3 field-size scenarios as a sensitivity column | Formula is honest about correlation. Scenarios stop fake precision |
| Prize EV weights | Grand 10, Solana/Auth0 5, Gemini 2 | Utility ranges, conservative | **Use Fable’s weight table as tie-break only.** Primary sort is P(any) then overall gate | EV would over-pick hardware stacks that slip |
| Final pick rule | top-8 overall ∩ top-8 P(any); G≥3; human veto | overall-win gate then min regret | **Both:** must pass overall-win gate (not a sniper-only winner) **and** be top-tier P(any). Human veto on top 3. One backup with a switch trigger | Prevents Ledger-only builds and also prevents a beautiful unwinnable art piece |
| Pilot | none | 10-min quality/throughput pilot | **2-agent pilot after audit, before the 100** | Cheap. If reports are shallow, rewrite the prompt once |

---

## Final allocation (100)

| IDs | n | Cohort | Hard constraint |
|---|---:|---|---|
| 001–018 | 18 | Open-world / overall | Grand path first. Must name a home track. Visible before/after. No sponsor required |
| 019–024 | 6 | Gemini | A Gemini-only capability is load-bearing (multimodal / long context / structured+tools). Text chat = fail |
| 025–032 | 8 | ElevenLabs | Voice is the loop, not TTS on the last sentence |
| 033–040 | 8 | Solana | Devnet state change the judge can see. Ornamental wallet = fail |
| 041–047 | 7 | Vultr | Visible compute/GPU/job. Hosting URL = fail |
| 048–055 | 8 | Auth0 | Identity changes behavior. Login gate = fail |
| 056–061 | 6 | MongoDB Atlas | Atlas *feature* on screen (vector/geo/change streams/…). Persist-only = fail |
| 062–071 | 10 | Stack | Assigned pair; both pass bolt test; max 3 sponsors |
| 072–076 | 5 | Anti-AI | No LLM in the essential loop |
| 077–081 | 5 | Demo-first | Design the 30s wow, then the product. Substance required |
| 082–086 | 5 | Research-lab | One hard core a systems/ML person respects; still demoable |
| 087–090 | 4 | Physical I/O | Phone/cam/mic in; spatial or realtime out. No bought hardware |
| 091–095 | 5 | IFM / K2 | K2 load-bearing; **mandatory Gemini fallback** that keeps the demo |
| 096–100 | 5 | Sandia cyber | Real security mechanism on stage. No live third-party targets |

STACK pairs: 062 Auth0+Mongo, 063 Solana+Mongo, 064 ElevenLabs+Gemini, 065 Vultr+Gemini, 066 Vultr+Mongo, 067 Auth0+Solana, 068 ElevenLabs+Auth0, 069 Solana+Vultr, 070 Gemini+Mongo, 071 ElevenLabs+Solana.

Home tracks rotate Opt / Multi / Travel / Food by `id mod 4`. Soft lens; Relevance must still be honest.

If K2 is dead at preflight: 091–092 → open-world, 093–095 → demo-first.  
If no Vultr code: 041–043 → open-world, 044–047 → demo-first.  
If Sandia gate fails us: 096–100 → open-world.  
If Cursor bar requires Grok Imagine/Bot in-product: steal 070–071 from stack → Cursor specialists.

---

## Firewall (loop 1)

**Shared:** `planning/shared_packet.md` only (facts, banned list, tests, estimator, schema). No allocation totals, no other agents, no tournament favorites.

**Private:** cohort brief, home track, seed triple (domain / technique / twist), 3 forbids, stack pair.

**Forbidden:** reading `agents/**` or `results/**`; web search; wave-to-wave prompt edits; human steering mid-waves.

First cross-agent view: clustering on one-liners, then red team.

---

## Scoring (user rubric, no early collapse)

Store **raw 0–10 integers** + short why.

**Official:** U usefulness, T tech complexity, O originality, D demo, **Rel** track relevance.

**Execution:** F feasibility, R reliability, P polishability, S scope efficiency.

**Competitive:** N novelty vs expected field, M memorability, J judge comprehension, W wow.

**Per sponsor p:** E eligibility, C centrality, X capability exploitation, B bolted-on penalty (0 organic … 10 shameless), Q competitiveness in that category. `SponsorWinScore_p` separate — **never average sponsors**.

**Strategic:** A multi-award surface, G grand potential, H team advantage, K killer-demo density, Y story coherence.

**Risks (higher = worse):** I integration, API external, DR demo, SR scope, CR commodity/wrapper, ER explanation, AR already-exists, BR boring.

**Five rankings (parent):**

1. Overall-winner: U T O D M P R J W G Rel  
2. P(any prize): Fable formula on calibrated buckets `{0,.02,.05,.10,.20,.35,.50}`  
3. Sponsor-sniper: max `SponsorWinScore_p` with C high and B low  
4. Risk-adjusted: overall minus risk ranks  
5. Upside: T O G W N  

Kill flags apply before rank. Self-scores replaced by red team from round 2.

**P(any):** `p_any = p_max + 0.5 * (1-p_max) * (1 - Π_{k≠argmax}(1-p_k))`.  
If `p_any` claimed > 0.8 → flag overconfident.

---

## Agent loop (each of 100)

1. Read packet + private card.  
2. Write **5 obvious-dump** (what the room builds tonight).  
3. Write **15 real raw** in 3 batches of 5; force mechanism change across batches.  
4. Banned-list + wrapper/bolt/hardware/data kills.  
5. Develop **top 3** (user’s full identity / product / architecture / sponsor / feasibility / competition / kill-test sections).  
6. Self-rank 1–3. Nominate primary.  
7. Write `agents/initial/NNN.md` + one JSON block (schema in Fable §14, letters remapped to this file).

Specialists: ≥5 raw ideas must still be a product if the sponsor is deleted (Astra). Exposes prize-only shells.

---

## Tournament (after 100)

User’s pipeline, Fable filenames, Astra’s “no filler if short”:

300 developed → parse/dedupe/cluster → top 50 (floors: each track ≥5, each cohort ≥2)  
→ 20 recombination agents (user; Fable had 6 — **use 20**)  
→ red team on ~30 (advocate + judge + skeptics + sponsor + red team per idea)  
→ build-sim ~15  
→ demo-sim 90s scripts  
→ 8 battle cards  
→ 12-persona jury, pairwise, no casual ties  
→ `FINAL_BRAINSTORM_DECISION.md`

Escape hatch if wall-clock is dying: skip build-sim on 16–30; jury 8 not 12. **Do not** skip the 100.

---

## Kill / bolt / demo tests (keep both plans)

- Delete sponsor → cheapest substitute. Demo unchanged? Bolted. `B=10`, that `p=0`.  
- Delete LLM. Nothing left? Kill.  
- Critical path > 11h to a working core loop → kill.  
- Data not obtainable in 1h → kill.  
- Hardware not in bags → kill.  
- Paid API outside free/MLH → kill.  
- Demo must survive 20s model stall and reset in ≤60s.  
- Banned list: Fable table §11 ∪ Astra §11 ∪ user §19 heuristics.

---

## Scope estimator

Fable’s person-hour tax (×1.8, +integration, +unknown) vs **31.7 effective hours**.  
Astra’s **last 4 hours reserved** for polish/submit/demo — adopt.  
Capacity = 4 × (H − 4 polish − 3 sleep) × 0.65. If team is 3, parent edits seeds before launch.

---

## Preflight (10 minutes, after audit, before the 100)

1. Confirm `cursor-grok-4.6-xhigh-fast` actually launches.  
2. Record headcount + hardware/skills one-liner.  
3. Compile `shared_packet.md` + `seeds.csv` + prompt template.  
4. Run **2 pilot agents** (one open-world, one specialist). If JSON invalid or ideas are wrappers, fix prompt **once**.  
5. Then launch 100 in waves (20 at a time or whatever the runtime allows). Failed agent: retry once, then drop the cell.

---

## Would we launch the 100 after this file?

**Not yet.** Next: 8 auditors → `audit_summary.md` → `final_ideation_plan.md` → preflight → 100.

Astra prompt for a human Codex/ChatGPT session (if CLI dies): `planning/ASTRA_PROMPT.md`.
