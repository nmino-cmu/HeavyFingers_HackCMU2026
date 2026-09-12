# Final ideation plan (post-audit)

Survives the 8-auditor pass by applying `audit_summary.md`. This is the plan the 100 run under.

**T_commit:** 90 minutes after the last `agents/initial/*.md` lands, or **11:00pm EDT**, whichever first. At T_commit the team picks from whatever has been ranked. Do not call a partial inbox “the 100.”

**Model:** `cursor-grok-4.6-xhigh-fast`. Waves of 8, raise to 12 if reports are valid. Retry once per ID.

---

## Allocation (100)

| IDs | n | Cohort | Subcells (must differ) |
|---|---:|---|---|
| 001–022 | 22 | Open-world | Rotate home track. Grand-path. Visible before/after |
| 023–024 | 2 | Gemini | Image/video in → structured decision out |
| 025–026 | 2 | Gemini | Long-context document/set |
| 027–028 | 2 | Gemini | Tool-calling / live loop |
| 029–030 | 2 | ElevenLabs | Conversational agent (barge-in) |
| 031–032 | 2 | ElevenLabs | Multi-voice scene / characters |
| 033–034 | 2 | ElevenLabs | Accessibility / eyes-busy |
| 035–036 | 2 | ElevenLabs | Game or sim where voice *is* state |
| 037–038 | 2 | Solana | Shared pot / escrow / split |
| 039–040 | 2 | Solana | Provable fairness / commit-reveal |
| 041–042 | 2 | Solana | High-frequency game ticks |
| 043–044 | 2 | Solana | Portable identity or receipt |
| 045–047 | 3 | Vultr | GPU job on screen |
| 048–049 | 2 | Vultr | Always-on / multi-agent sim |
| 050–051 | 2 | Vultr | Fan-out workers the UI shows |
| 052–053 | 2 | Auth0 | Delegated agent (Token Vault / CIBA) |
| 054–055 | 2 | Auth0 | Roles that change the product |
| 056–057 | 2 | Auth0 | Passwordless / physical presence |
| 058–059 | 2 | Auth0 | Cross-user permission boundary |
| 060–061 | 2 | Atlas | Vector search the user can see |
| 062–063 | 2 | Atlas | Geospatial |
| 064–065 | 2 | Atlas | Change streams / live sync |
| 066–073 | 8 | Stack | Pairs below; product-need first |
| 074–078 | 5 | Anti-AI | No LLM in the essential loop |
| 079–083 | 5 | Demo-first | 10-second visible hook, then product |
| 084–088 | 5 | Research-lab | One hard core; must still wow in 30s |
| 089–092 | 4 | Physical I/O | Phone/cam/mic → spatial/realtime out |
| 093–096 | 4 | IFM K2 | K2 load-bearing + Gemini fallback that keeps demo |
| 097–100 | 4 | Sandia | Real defensive mechanism on stage; no live third parties |

STACK: 066 Auth0+Atlas, 067 Solana+Atlas, 068 11L+Gemini, 069 Vultr+Gemini, 070 Auth0+Solana, 071 11L+Auth0, 072 Solana+Vultr, 073 Gemini+Atlas.

Home track = `[Optimization, Multiplayer, Traveling, Food][id % 4]`.

---

## Loop 1 contract

Each agent reads **only** `planning/shared_packet.md` + its private card in the prompt.

1. 5 obvious-dump one-liners (field estimate).  
2. 15 real raw, 3 batches of 5, mechanism must change across batches.  
3. Develop top 3. **Each developed idea must use ≥1 of {domain, technique, twist}.**  
4. Full user sections (identity, experience, architecture, sponsor, feasibility, competition, kill test).  
5. Scores 0–10 integers + ≤20-word why. User letters. `Rel` = track relevance. `R` = reliability.  
6. Write `agents/initial/NNN.md` with one JSON fence.

**No web. No other agent files.**

Specialists: ≥5 raw ideas remain a product if the sponsor is deleted.

---

## Official vs internal sponsor

For each claimed sponsor:

- `E` = official eligibility (thin bars count).  
- `C, X, B` = our depth bar.  
- `SponsorWinScore_p = 0.25*E + 0.30*C + 0.25*X + 0.20*(10-B)`  
- Bolted (`B≥8` or bolt test fail): `p_p = 0` for **competitiveness**, `E` may still be high.  
- Do not delete IFM cells if K2 unverified; require fallback. Cursor: no specialist cells.

---

## Kills (parent re-checks from JSON)

U<4; wrapper (delete LLM → nothing); banned pattern (product, not keyword); hardware not in bags; paid API; data >1h; critical path (parent-computed) >11h; >3 load-bearing sponsors; live third-party attack.

---

## Rankings (no early single score)

0. **Official-five:** U T O D Rel  
1. **Overall:** official-five + M P R J W G K, with floors D≥6 W≥5  
2. **P(any_adj):** Fable `p_any` × parent `p_ship_core` × `p_demo_ok`  
3. **Sniper:** max SponsorWinScore  
4. **Risk-adjusted:** overall − risk ranks  
5. **Stage:** D W K M J  
6. **Upside:** T O G W N — cannot be the pick unless Stage rank ≤8

**Pick:** among ideas passing judge gate (U≥6 D≥6 Rel≥6 F≥5 W≥5, not killed), maximize `p_any_adj`. Tie → higher official-five. Human veto. One backup + switch trigger.

`p_any = p_max + 0.5*(1-p_max)*(1-Π_{k≠max}(1-p_k))`. Buckets {0,.02,.05,.10,.20,.35,.50}.

---

## After the 100 (slim)

1. Parse + parent mechanical kills + cluster one-liners.  
2. Novelty web pass on top 50 (2 agents).  
3. 8 recombiners.  
4. Top ~30: one critic + one judge each.  
5. Build-sim + 180s demo-sim on ~12.  
6. 8 battle cards if time.  
7. 8-persona jury if time (not 12).  
8. `FINAL_BRAINSTORM_DECISION.md`.

If T_commit hits earlier: pick from the latest ranking that exists.

---

## Wave order (interleaved)

Not 001–100 sequential. Each wave of 8 mixes open + 2–3 specialists + 1 anti/demo/research.

Pilot: IDs 001 (open) and 037 (Solana escrow) first. If JSON broken, fix template once, then continue.
