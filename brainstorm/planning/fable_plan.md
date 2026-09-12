# Fable plan — HackCMU 2026 ideation search architecture

Written Fri Sep 11, 2026 8:35pm EDT. Planning only. No project ideas in this file. No agents launched.

Answers every numbered section of `ASTRA_PROMPT.md`. Inputs: `research/competition_ground_truth.md`, `research/prior_winners/notes.md`, `HACKCMU_PRIZES_TRACKS.md`. Where ground truth says UNKNOWN this plan picks a working assumption and marks it `ASSUME`.

Objective: maximize P(≥1 prize) with a real grand-prize path. Build window Fri 9:00pm → Sat 4:00pm (19h). The ideation pipeline itself must cost ≤ 1h50m wall-clock or it is eating the prize.

Executor model (set by team lead): `cursor-grok-4.6-xhigh-fast`, 100 agents, fully independent on loop 1.

---

## 0. Clock (hard)

| Time | Step | Owner |
|---|---|---|
| 8:35–8:55pm | Parent compiles `planning/shared_packet.md` + `planning/seeds.csv` from this plan | parent |
| 9:00pm | Launch loop 1: 5 waves × 20 agents, next wave as soon as prior wave's files land (no result feedback between waves) | parent |
| 9:00–10:00pm | Humans at IFM workshop (K2 access), one human at MLH table (Vultr code, Sandia rules, form/IFM-track question) | humans |
| 9:30pm | `results/parse_initial.py` → validate, dedupe, five rankings, 300→50 | parent |
| 9:35–9:50pm | Red team (10 agents × 5 ideas) → 50→30 | parent |
| 9:50–10:15pm | Recombination (6) + build-sim (30) + demo-sim (30) → 30→15→8 | parent |
| 10:00–10:30pm | Humans at Cursor/Grok workshop (Cursor prize bar) | humans |
| 10:15–10:30pm | Jury (12 personas) → 8→3 | parent |
| 10:30–10:50pm | Human pick from top 3. Veto allowed. Decision written to `results/final_decision.md` | team |
| 10:50pm | Build starts. ~17h to Baggage Check | team |

If any stage runs >15 min late, skip build-sim for ideas ranked 16–30 and shrink jury to 8 personas. Never slip the 10:50pm build start past 11:15pm.

Rules check: brainstorming and team formation before 9:00pm are explicitly allowed; loop 1 launches at 9:00pm anyway. No code or design docs for the chosen project before then.

---

## 1. Decomposition of the idea search

No mega-prompt. The search space is factored into **cohort × home track × seed triple**, and each of the 100 agents owns exactly one cell. Cohort fixes *what kind of win* the agent hunts; home track fixes the Relevance anchor (every submission must name one track, so "open-world" without a track is not a real candidate); the seed triple (domain, technique, twist) forces spread inside the cell.

### 1.1 Allocation (100 agents)

The 5 "Only at CMU" slots are gone. Sponsor slots were rebalanced toward thin-field / per-teammate-hardware prizes. Two new cohorts (Sandia Cyber, IFM K2) take dedicated prizes that a beginner-friendly field will mostly ignore. One new cohort (Physical I/O) targets the pattern that won 2025 grand.

| IDs | Cohort | n | Home track | Hard constraint (agent must obey) |
|---|---|---|---|---|
| 001–016 | TRACK (open-world overall) | 16 | Opt 001–005, Multi 006–010, Travel 011–013, Food 014–016 | No sponsor required. Grand-prize path first. Visible before/after in the demo. |
| 017–021 | GEMINI | 5 | rotate Opt/Multi/Travel/Food by id mod 4 | A Gemini capability a plain chat model lacks must be load-bearing: image/video/audio input, ≥100k-token context, strict structured output, tool calling. Text-in/text-out = fail. |
| 022–028 | ELEVENLABS | 7 | rotate | Voice is the interface or the product. Live STT→TTS or conversational agent. Narrating LLM text = fail. |
| 029–037 | SOLANA | 9 | rotate | Devnet program or tx changes what the user sees: ownership, escrow, provable fairness, payment between players/travelers/diners. "We log to chain" = fail. |
| 038–044 | VULTR | 7 | rotate | Compute is visible: a GPU job, batch inference, training-during-the-hackathon, many-agent sim, render farm, whose progress is on screen. Hosting-only = fail. |
| 045–052 | AUTH0 | 8 | rotate | Identity is a primitive of the idea: delegated access, Auth0 for AI Agents / Token Vault, roles that change behavior, passwordless in a physical setting. Login gate = fail. |
| 053–058 | MONGO | 6 | rotate | Atlas feature you would not get from SQLite in 19h: vector search, geospatial, change streams, time series, aggregation pipeline, driving the demo. Persist-only = fail. |
| 059–068 | STACK | 10 | rotate | Assigned pair (below) + track. Both sponsors must pass the bolt test (§7.2). Max 3 sponsors total. |
| 069–074 | SANDIA CYBER | 6 | Opt 069–070, Multi 071–072, Travel 073, Food 074 | Security is the theme; defensive/educational; attack→detect→explain visible on stage. No live third-party targets. |
| 075–080 | IFM K2 | 6 | rotate | K2 load-bearing in a way Gemini cannot substitute: local/offline run, logit access, model comparison, fine-tune/LoRA, K2-as-judge. Mandatory Gemini fallback plan in report. |
| 081–085 | ANTI-AI | 5 | Opt 081–082, Multi 083, Travel 084, Food 085 | No LLM anywhere. Algorithms, solvers, classical CV, DSP, networking, simulation. |
| 086–090 | DEMO-FIRST | 5 | rotate | Design the 3-minute stage moment first, then the product. People's Favorite + Best Design. Audience-in-the-loop via phones allowed. |
| 091–095 | RESEARCH-LAB | 5 | rotate | One hard technical core a CS prof would respect (realtime SLAM, CRDT, custom DSL/compiler, differentiable X, novel solver). Grand via Technical Difficulty. |
| 096–100 | PHYSICAL I/O | 5 | rotate | Camera/mic/phone sensors in; spatial, realtime, or 3D out. No purchased hardware. The Medicly pattern. |

STACK pairs, by id: 059 Auth0+Mongo, 060 Solana+Mongo, 061 ElevenLabs+Gemini, 062 Vultr+Gemini, 063 Vultr+Mongo, 064 Auth0+Solana, 065 ElevenLabs+Auth0, 066 Solana+Vultr, 067 Gemini+Mongo, 068 ElevenLabs+Solana.

Why Gemini dropped to 5: any LLM-using idea from any cohort already uses `gemini-3.8-flash` (free tier), so Gemini eligibility rides free across ~60 of 100 agents. Dedicated Gemini agents only add value if they hunt the distinctive-capability corner, and 5 is enough for that corner. Why Solana up to 9: thinnest field at a beginner CMU event, per-teammate Ledger hardware, and real integration cost means few teams attempt it. Why Auth0 8: per-teammate hardware, but many teams will bolt it on, so the cohort must find identity-as-primitive ideas; that is a harder search than Solana's. Why Mongo 6: crowded, per-teammate hardware, but the differentiated-feature space (vector/geo/change streams) is narrow.

### 1.2 Why cells, not one prompt

One prompt with "give me 300 ideas" returns the model's mode 300 times with adjectives swapped. 100 cells each constrained by cohort + track + seed triple make the mode unreachable in most cells. Coverage is checked after the fact by the dedupe pass (§9.1): if >30% of developed ideas fall into clusters of size ≥4, the cells were too loose, but we do not relaunch (clock); we penalize the clusters.

---

## 2. Diversity mechanisms

### 2.1 Seed triple (private per agent)

Three shuffled lists, shuffled once with seed `2026`, assigned row-wise so every list is covered before it repeats. Stored in `planning/seeds.csv` (columns: `agent_id, cohort, home_track, domain, technique, twist, forbid_1, forbid_2, forbid_3, stack_pair`).

**Domains (40):** logistics, live music, amateur sports, accessibility, agriculture, personal finance, physical security, K-12 teaching, tabletop games, home repair, public transit, parking, emergency response, elder care, language learning, fitness, cycling, hiking, restaurants back-of-house, grocery supply, street food, fermentation/brewing, dietary medicine, campus-agnostic dorm cooking, road trips, air travel, border/visa paperwork, hostels, maps/cartography, translation on the move, board-game night, esports, co-op puzzle, party games, crowd coordination, disaster relief, warehouse picking, manufacturing QA, energy/HVAC, scientific lab automation.

**Techniques (30):** classical CV (OpenCV), pose estimation, depth from monocular video, SLAM/AR anchors, audio DSP/beat tracking, speech diarization, embeddings + vector search, graph shortest path / TSP heuristics, ILP/SAT/CP-SAT solvers, simulated annealing, reinforcement learning (tiny), diffusion/image generation, WebRTC realtime, CRDT sync, WebSockets game loop, procedural generation, physics simulation, time-series anomaly detection, Bayesian inference, OCR + layout, geospatial indexing, blockchain program/escrow, zero-knowledge or commit-reveal, fuzzing/static analysis, network packet analysis, cryptographic signatures, browser extension, phone IMU/sensors, on-device model (Apple Silicon/WebGPU), long-context document reasoning.

**Twists (20):** must work offline, phone is the only device, no screen (voice/haptics only), one button total, audience participates from their phones, must finish a round in 60 seconds, works for two strangers who never met, output is a physical printout/QR, adversarial user assumed, runs continuously for the whole showcase, latency budget 100 ms, must be funny on stage, data is generated live from the room, uses judges as players, model is the villain not the helper, no accounts ever, must be explainable to a 10-year-old, input is a single photo, uses history/replay as the core, the demo is a race against a baseline.

Agent `i` gets `domain[i mod 40]`, `technique[(i*7) mod 30]`, `twist[(i*3) mod 20]`. Seeds are **suggestions to start from**, not requirements: the agent must use at least one of the three in at least 10 of its raw ideas, and may abandon them for the developed 3 if it says why.

### 2.2 Forbidden lists

**Global banned list** (in `shared_packet.md`, all agents): the §11 deceptively-attractive list, verbatim. Any raw idea matching it must be tagged `banned` and cannot be developed.

**Per-agent forbid list** (3 items in `seeds.csv`): 2 techniques and 1 domain drawn from the lists *not* assigned to this agent, rotating so each technique is forbidden for ~7 agents. Pushes the population apart even when seeds are ignored.

### 2.3 Obvious-dump

Every agent's first 5 raw ideas must be labeled `obvious_dump`: "the five things most teams in this room build tonight for this track/sponsor." They are discarded from development but kept in the JSON, because the union across 100 agents is our best estimate of the field (§5.3, correlation risk). This gets the mode out of the model before it can contaminate the real list.

### 2.4 Anti-mode-collapse checks (post hoc, parent)

- Dedupe clusters (§9.1). Cluster size ≥4 → `CR` risk forced to 5 for every member.
- Sponsor stacking count: if >40% of developed ideas list ≥3 sponsors, the STACK cohort leaked; cap sponsors at 3 and re-rank.
- Track skew: if any track has <10% of developed ideas, the tournament keeps its top 3 regardless of score (track prizes in a sparse track are cheap).

---

## 3. Prize targeting

### 3.1 Three strategies, one build

- **Specialists** (54 agents: 42 sponsor + 6 Sandia + 6 IFM) find ideas whose *reason to exist* is a sponsor capability. High P(that one prize), lower grand path.
- **Open-world/track** (16 + 5 anti-AI + 5 research + 5 physical = 31) find grand-path ideas. Sponsors can be added later in recombination if they pass the bolt test.
- **Stackers** (10) + **demo-first** (5) find ideas where 2–3 prizes are plausible from one build.

### 3.2 Weighting given 19h and stacking

Stacking is allowed and MLH prizes are not track-locked, so the final build should target **one track + one primary sponsor + ≤2 free-rider sponsors**. Every extra load-bearing integration costs ~2h and one demo failure point (§12). Rule for the final pick: a sponsor is included only if `Q ≤ 2h` and it passes the bolt test, or it is the primary.

Grand path is not sacrificed for sponsors: the tournament's final ranking (§9.5) requires the winner to be top-8 in the **overall** ranking *and* top-8 in **P(any prize)**. An idea that is #1 sponsor-sniper but #40 overall does not win; it gets recombined into a top-overall idea instead.

### 3.3 Track choice policy

- Relevance is judged, track-only. The 50-word "why" must be writable without stretching.
- Sparse tracks may award 1st only; still, fewer competitors. `ASSUME` field ~60 teams; Food and Traveling absorb most beginner wrapper projects (recipe/itinerary), Optimization and Multiplayer attract fewer but stronger teams. TRACK cohort is weighted 5/5/3/3 toward Opt/Multi because those tracks reward Technical Difficulty natively; Food/Traveling entries must be technically unusual to stand out from the wrapper field, which is a harder search but a bigger relative gap if found.
- IFM is treated as **a prize, not a track** (`ASSUME`). If the Google Form offers IFM as a fifth track, no allocation changes; it only changes the 50-word field for K2-cohort finalists.

---

## 4. Avoiding correlated agents (information firewall)

**Shared (identical for all 100):** `planning/shared_packet.md`, which the parent compiles from: `research/competition_ground_truth.md`, `HACKCMU_PRIZES_TRACKS.md`, `research/prior_winners/notes.md`, `HACKCMU_RESOURCES.md`, `research/sponsor_research/mlh_and_opening.md`, the §11 banned list, the §7 tests, the §12 estimator, and the §14 schema. Nothing else.

**Private (unique per agent):** cohort brief, home track, seed triple, forbid list, stack pair, agent id.

**Firewall rules for loop 1:**
1. No agent reads `brainstorm/agents/**` or `brainstorm/results/**`. The prompt says so and the parent does not attach those paths.
2. No web search, no web fetch. Web results are a shared external mode; 100 agents searching "hackathon ideas food" converge. Novelty checks against the real world happen in red team (§9.2) with search enabled, by 10 agents, not 100.
3. No wave-to-wave feedback. Waves are a rate-limit measure only. Parent never edits the prompt between waves, even if wave 1 looks bad.
4. Each agent writes exactly one file, `agents/initial/NNN.md`, and nothing else. No shared scratch.
5. Parent does not summarize partial results to the team until all 100 land, to stop humans from steering wave 5.

**First moment agents see each other:** the dedupe pass (§9.1), run by one clustering agent over one-liners only. Then red team (5 ideas per agent, scores hidden). Then recombination (10 ideas from ≥3 cohorts). Jury sees full dossiers of 8.

---

## 5. Scoring methodology

### 5.1 Letters (definitions the agents get verbatim)

All scores are integers 1–5. Each score needs a ≤15-word justification. No decimals. No averages in agent output.

Official: **U** usefulness, **T** technical difficulty (vs wrapper), **O** originality, **D** demo quality at 3 min.
Execution: **F** feasibility in 17h by 4 people, **R** relevance to home track, **P** polish reachable, **S** scope-cut survivability (does the 50% version still demo?).
Competitive: **N** novelty vs what this field builds tonight, **M** mode-collapse risk inverted (5 = nobody else builds this), **J** judge legibility (one-sentence core), **W** wow moment exists.
Per-sponsor (one block per sponsor claimed): **E** eligibility per stated bar, **C** centrality (load-bearing), **X** distinctiveness (uses what makes this sponsor different), **B** bar vs likely competitors for that prize, **Q** hours to integrate (5 = ≤1h, 1 = ≥6h).
Strategic: **A** P(any prize) bucket, **G** grand-prize path, **H** stack count plausibly won (1–3+), **K** kill-switch quality (fallback if core tech fails), **Y** team yes-ability (would 4 strong CS students want to build and defend this).
Risks (higher = worse): **I** integration, **API** key/quota/credit, **DR** live demo failure, **SR** scope, **CR** correlation (others build it), **ER** eligibility/rules, **AR** track-ambiguity, **BR** build-blocker (tech nobody on team has touched).

### 5.2 No early collapse

Agents never output a total. Parent computes **five rankings** by Borda count over the relevant letters, with hard kill flags applied first:

| Ranking | Letters (equal weight, Borda) | Tie-break |
|---|---|---|
| overall | U T O D R G W J | lower DR+SR |
| P(any prize) | computed `p_any` (§5.3) | higher H |
| sponsor-sniper | max over claimed sponsors of (E+C+X+B) with Q ≥ 3 | lower I |
| risk-adjusted | overall rank minus rank of (I+API+DR+SR+CR+ER+AR+BR) | higher K |
| upside | T O G W N | higher Y |

Self-scores are inflated and inconsistent across agents. Mitigations: (a) each agent must rank its own 3 developed ideas 1–3, and within-agent rank is used as a sanity check (an idea self-ranked 3rd never passes an idea ranked 1st from the same agent in round 1); (b) round-1 cut uses coarse buckets (top/mid/bottom third per ranking), not exact positions; (c) red team re-scores independently and their scores replace self-scores from round 2 on.

### 5.3 P(any prize) without naive sums

Agents give `p_prize` per category from the bucket set `{0, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50}` for: `grand, track_1st, track_2nd_or_3rd, gemini, elevenlabs, solana, vultr, auth0, mongo, ifm, cursor, sandia, peoples, design`. Any sponsor not load-bearing must be 0.

Parent computes, per idea:

```
p_max  = max_k p_k
p_rest = 1 - prod_{k != argmax}(1 - p_k)
p_any  = p_max + 0.5 * (1 - p_max) * p_rest
```

Full credit for the best single shot, half credit for the rest, because prizes are positively correlated through project quality (one strong build wins several; one weak build wins none). `ponytail:` this is a fixed-ρ shortcut; the upgrade is a per-pair correlation table, unnecessary at n=8.

Field prior injected into agents (shared packet): `ASSUME` 60 teams; ~25 prize slots; base rate for a random submitted team ≈ 0.3 for ≥1 prize; a top-quartile build ≈ 0.6–0.7. Agents are told to calibrate to that, and any idea claiming `p_any > 0.8` is auto-flagged `overconfident` and its A score set to 3.

The `obvious_dump` union is turned into a frequency table by the parse script; any developed idea within one edit of a dump item appearing ≥8 times gets `CR = 5`.

---

## 6. Information gathering

### 6.1 What every agent reads (only this)

`planning/shared_packet.md`. Compiled by the parent at 8:40pm; contains verbatim: event facts + deadline, tracks + one-liners, judging axes + glosses, full prize table with objects and per-teammate notes, MLH sponsor bars and "distinctive" column, the K2/Vultr/Cursor/Sandia UNKNOWNs stated as UNKNOWN, prior-winner patterns, banned list (§11), tests (§7), estimator (§12), schema (§14), field prior (§5.3). About 3,000 words. Agents are told: "Do not assume any prize, rule, or sponsor not in this packet exists."

### 6.2 What humans verify live tonight (parallel with loop 1)

| UNKNOWN | Where / when | If yes | If no |
|---|---|---|---|
| K2 access: hosted endpoint, key, or weights? Latency? | IFM workshop 9–10pm TEP 1403 | IFM cohort ideas stay at full weight | IFM ideas keep only if their Gemini fallback preserves the demo; IFM p set to 0 |
| Vultr $100 code from MLH Coach | MLH table 7–9pm, Discord | Vultr cohort at full weight | Vultr p = 0; Vultr ideas re-judged as plain compute ideas |
| Does the Google Form list IFM as a track? Is the form URL out? | Organizers / Discord by 10pm | Only 50-word field changes | Nothing changes |
| Cursor prize bar | Cursor workshop 10–10:30pm | If "built with Cursor": every finalist is eligible for free, log Cursor usage | If Grok Imagine/Bot required: treat as separate 2h integration, evaluate at recombination |
| Sandia extra rules (eligibility, theme scope) | Sandia table | Confirms cohort | If citizenship or other gate we fail: Sandia p = 0 |
| Auth0 tenant signup works, no card | 5 min, any teammate | — | Auth0 p halves |
| ElevenLabs MLH 3-month sub via MLH email | 5 min | — | Free 10k chars/mo; voice ideas must budget characters |
| Team hardware: laptops with GPU/Apple Silicon, phones, webcams, a spare monitor | teammates now | Physical I/O + on-device model ideas feasible | Those ideas fall to Vultr GPU or Gemini |
| Team headcount and skills (assume 4; ≥1 ML, ≥1 frontend, ≥1 backend/systems) | now | — | F scores re-weighted by parent |

Verification results go into `results/live_verification.md` by 10:15pm; the jury reads it. Nothing before the jury waits on it.

---

## 7. Feasibility, sponsor-fit, novelty, demo tests (operational)

Every developed idea must answer these in the JSON. Failing a **kill** rule sets `kill_flags` and the idea cannot pass round 1.

### 7.1 Feasibility
- **Saturday-10am test:** list components (§12). Critical path must have the core loop demoing end to end by Sat 10:00am (13h in). Critical path > 11h → kill.
- **Data test:** what data does the demo need and where does it come from in ≤1h (generated live, synthetic, public dataset, the room itself)? "We'll find a dataset" → kill.
- **Hardware test:** requires anything not in the team's bags → kill.
- **Credit test:** requires a paid API outside free tiers / MLH credits → kill.
- **Sleep test:** plan must fit 4 people × 14 usable hours with a 3h sleep floor each.

### 7.2 Sponsor fit — the bolt test
For each claimed sponsor: "Delete this sponsor from the build and replace it with the cheapest generic substitute (Postgres, a JSON file, `print`, a hardcoded login, a local TTS, a normal DB). Does the 3-minute demo change in a way a judge would notice?" No noticeable change → sponsor is bolted → `C = 1`, that sponsor's `p = 0`. Agents must write the substitute they imagined.

Additionally per sponsor: Solana must name the on-chain state and who reads it; Vultr must name the job and what the audience sees of it; Auth0 must name the identity decision that changes behavior; Mongo must name the Atlas feature and the query; ElevenLabs must name who is talking to whom; Gemini must name the input modality or capability a chat box lacks; K2 must name why Gemini could not do it.

### 7.3 Novelty
- **Three-products test:** name 3 existing products/repos closest to it. If the differentiator is only "AI" or "for X," → kill.
- **Room test:** "How many of ~60 teams here build something within one step of this tonight?" Answer ≥6 → `CR = 5`, `M = 1`; not a kill, but it loses ties.
- **Wrapper test:** "Delete the LLM. What remains?" Nothing → kill. This applies to every cohort, including Gemini specialists.

### 7.4 Demo
- **Six-beat script:** hook (15s), before-state (30s), the transform (60s), the technical core in one sentence (20s), sponsor moment(s) (30s), close + track why (25s). Missing a visible before/after in beat 2–3 → `D ≤ 2`.
- **Slow-LLM test:** demo survives a 20s model stall or offline wifi (cached result, local fallback, pre-warmed state). No → `DR ≥ 4`.
- **Reset test:** demo can be reset to start in ≤60s (3 judge rooms, expo table, repeated runs).
- **Stranger test (Multiplayer only):** demo works with judges as players or with bots, not with teammates pretending.

### 7.5 Kill rules (any one kills)
Requires hardware not present; requires paid API; critical path > 11h; needs data that cannot exist within 1h; wrapper test fails; matches the banned list; needs > 2 live humans with no bot fallback; core depends on UNKNOWN access (K2 tonight) with no fallback that keeps the demo; violates from-scratch rule (extends an existing team repo); attacks or scrapes a live third party.

---

## 8. Expected-value reasoning

Weights are utility units, not dollars: replacement value × per-teammate multiplier × how much the team would actually care. Grand carries the reputational premium the objective demands.

| Prize | Object | Weight | Why |
|---|---|---|---|
| Grand | HRT Poker Set | 10 | The "serious overall path." Reputation dominates object value. |
| Track 1st | Mini projector + AirPods Pro | 6 | Best object among HackCMU prizes; 4 tracks × 1 winner. |
| Solana | Ledger Nano S Plus ×4 | 5 | Per-teammate hardware; thin field. |
| Auth0 | Headphones ×4 | 5 | Per-teammate hardware; crowded but bolted competitors. |
| Vultr | Portable screens (team, maybe per teammate) | 4 | Good object; thin field; needs code. |
| Mongo | M5Stack ×4 | 4 | Per-teammate hardware; crowded. |
| Sandia Cyber | ANC AirPods | 4 | Dedicated prize, thin field. |
| ElevenLabs | Earbuds | 3 | Team object; moderate field. |
| IFM | Kindle Lite | 3 | Thin field; access UNKNOWN. |
| Cursor | Keyboards | 3 | Bar UNKNOWN; possibly free rider. |
| Track 2nd / 3rd | Visa swag / keyboard | 2 | Depth may not exist in sparse tracks. |
| Gemini | Swag kits | 2 | Most crowded MLH category; low object. |
| People's Favorite | Ticket to Ride | 2 | Expo charisma; demo-first cohort covers. |
| Best Design | QuickSnap | 1 | Rubric UNKNOWN; low object. |

EV per idea (parent computes, not agents): `EV = Σ_k w_k · p_k`. Used only as a **tie-breaker inside the P(any) ranking**, never as the primary ranking, because the objective is P(≥1), and EV would over-reward Solana+Auth0+Mongo stacks that win nothing when the build slips.

Objective ordering for the final pick: (1) `p_any` ≥ 0.5 among finalists, (2) grand path `G ≥ 3`, (3) EV, (4) `Y`.

---

## 9. Selection and tournament architecture

300 developed ideas (100 × 3) → 50 → 30 → 15 → 8 → 3 → 1. Agents inspect each other only from §9.1 on. All tournament agents are the same model unless the team lead changes it.

### 9.1 Round 1: 300 → 50 (parent script + 1 clustering agent, 9:30–9:35pm)
1. `results/parse_initial.py` extracts the JSON block from each `agents/initial/NNN.md`, validates the schema, writes `results/initial_ideas.jsonl`. Malformed files are re-run once with the same prompt (max 10 re-runs; otherwise drop the agent).
2. Apply kill flags. Apply `obvious_dump` frequency → `CR`.
3. Clustering agent reads `results/oneliners.txt` (300 lines: id + one-liner + track) and writes `results/clusters.md`: groups of near-duplicates with a representative id. Cluster size ≥4 → `CR = 5` for all members; only the representative advances.
4. Five Borda rankings (§5.2) → `results/rankings_round1.md`.
5. Keep an idea if: top-50 in ≥2 rankings, or top-10 in any one. Then enforce floors: each cohort keeps ≥2 ideas, each track keeps ≥5. Fill to 50 from the risk-adjusted ranking.

### 9.2 Round 2: red team, 50 → 30 (10 agents, 9:35–9:50pm)
Each red-team agent gets 5 ideas (full dossiers, self-scores stripped), web search **enabled**, and writes `agents/red_team/RT-NN.md` with per idea: existing-products check, wrapper test re-run, bolt test re-run per sponsor, three sharpest objections, one fix, and its own full score block (§5.1). Red-team scores replace self-scores. Ideas are assigned so each agent's 5 come from ≥3 cohorts. Parent re-ranks → `results/rankings_round2.md`, keeps 30 with floors: each track ≥3, each of {Solana, Auth0, Mongo, Vultr, ElevenLabs, Sandia, IFM} ≥1 if any survived red team.

### 9.3 Round 3: recombination + build-sim + demo-sim, 30 → 15 → 8 (9:50–10:15pm)
- **Recombination (6 agents):** each gets 10 of the 30 (overlapping, from ≥3 cohorts), writes `agents/recombination/RC-NN.md` with ≤3 hybrids: a grand-path idea plus a sponsor idea's load-bearing mechanism, each hybrid re-passing the bolt test and estimator. Hybrids enter the pool as new ideas with `parent_ids`. Hybrids cap: 15 new, pool ≤45.
- **Build-sim (one agent per idea, 30 + hybrids, parallel):** writes `agents/build_sim/BS-<idea_id>.md`: hour-by-hour plan Fri 10:50pm → Sat 4:00pm for 4 named roles, critical path, the Sat-10am checkpoint state, the three most likely 2am failures and the scope cut for each. Outputs `critical_path_hours`, `p_ship_core`, `p_ship_polish`.
- **Demo-sim (one agent per idea, parallel):** writes `agents/demo_sim/DS-<idea_id>.md`: the literal 3-minute script with timestamps, what is on screen each beat, the failure at each beat and its fallback, the one sentence a judge repeats to another judge, `p_demo_ok`.
- Parent computes `p_any_adj = p_any × p_ship_core × p_demo_ok`, re-runs the five rankings → `results/rankings_round3.md`. Keep 15 by: top-15 in overall ∩ top-15 in P(any) first, then fill from risk-adjusted. Keep 8 by the same rule from the 15.

### 9.4 Round 4: jury, 8 → 3 (12 agents, 10:15–10:30pm)
Each juror gets all 8 dossiers (idea + red team + build-sim + demo-sim + `results/live_verification.md`) and one persona, writes `agents/jury/J-NN.md` with a full ranking 1–8 and a one-paragraph verdict per idea. Personas: CMU CS professor judge; MLH rep judging sponsor use; HRT quant judge who hates wrappers; Jane Street–style systems engineer; product designer; beginner student in the audience (People's Favorite); skeptical senior hacker who has seen 200 demos; Sandia security engineer; Solana ecosystem judge; ElevenLabs/voice product person; Vultr infra engineer; the team's own tired 3am selves. Borda over 12 rankings → `results/rankings_jury.md`. Top 3 go to the humans.

### 9.5 Final: humans, 3 → 1 (10:30–10:50pm)
Team reads three one-page briefs (`results/finalists/<idea_id>.md`, compiled by parent from dossiers). Pick rule: `p_any_adj ≥ 0.5`, `G ≥ 3`, then EV, then `Y`. Any teammate may veto one finalist. Decision + 50-word track why + sponsor list + role assignment → `results/final_decision.md`. Runner-up is the named pivot if the Sat-10am checkpoint fails.

---

## 10. Per-agent idea count

Change to: **20 raw, of which 5 are the obvious-dump, 15 are real; top 3 developed.** Defense:

- The first 5 ideas from any model are the field's ideas. Making them explicit and disposable (obvious-dump) costs ~100 tokens and buys a field estimate.
- 15 real raw one-liners (≤25 words each, plus a 5-word "why not obvious" tag) is the point where a fast model stops recombining its first ideas and reaches for the seeds. Fewer than 15 and seeds rarely appear; more than 20 and quality collapses into list-padding, which is wasted tokens on a fast model.
- 3 developed keeps each report ≤ ~5k tokens so 100 reports parse in minutes and 300 ideas is a big enough pool that a 50-cut is meaningful. 5 developed would be 500 ideas with worse average depth and no more distinct winners: distinct winners come from distinct cells, not from more ideas per cell.
- Developed ideas must come from raw #6–20, must span ≥2 different seeds or techniques, and the agent must self-rank them 1–3.

---

## 11. Deceptively attractive bad ideas (global banned list + detection)

Any raw idea matching a row is tagged `banned` and cannot be developed. Agents may build the *opposite* of a row.

| Pattern | Detection signal | Why it loses tonight |
|---|---|---|
| "AI for X" chat / copilot over docs | Core verb is "ask," "chat," "summarize," "explain" | Wrapper axis is literally on the judging slide |
| Recipe generator, "what's in my fridge" photo → recipe, meal planner, macro tracker | Food track + LLM + no other tech | The Food track's default; ≥8 teams |
| Itinerary / trip planner, "travel buddy," packing list | Traveling track + LLM | The Traveling track's default; ≥8 teams |
| Schedule / calendar / study-plan optimizer | "optimize" applied to a personal calendar | Optimization's default; no visible technical core |
| Multiplayer trivia / Kahoot clone / Jackbox clone | Rooms + questions + scoreboard | No Technical Difficulty; Multiplayer default |
| Uber / Tinder / Airbnb for X | Two-sided marketplace needing users who are not in the room | Cannot demo liquidity in 3 min |
| Split-the-bill, tip calculator, receipt scanner | OCR + arithmetic | Solved products exist; Originality 1 |
| Food-waste / carbon-footprint / sustainability tracker | Tracker with manual input | Usefulness claims judges have heard 50 times |
| Mental-health / journaling / therapy chatbot | Sensitive domain + LLM | Wrapper + judges uncomfortable |
| Resume / cover-letter / interview coach | Career + LLM | Wrapper; irrelevant to all four tracks |
| Note summarizer, lecture-to-flashcards, "study buddy" | Education + LLM; campus-adjacent | Wrapper; campus-only feel |
| Bolted Auth0 ("users log in") | Sponsor appears only in beat 1 | Fails bolt test; MLH judges see 20 of these |
| Bolted Mongo ("we store it in Atlas") | Sponsor never on screen | Fails bolt test |
| Blockchain for supply-chain / provenance / certificates with no adversary | No reason state must be shared or trustless | Solana judges want tx that matter |
| Crypto tipping / token rewards for X | Token as points system | Same as above; gamification veneer |
| Voice assistant that reads LLM output aloud | ElevenLabs in beat 5 only | Fails "give the project a voice" |
| "Deployed on Vultr" | Sponsor is a URL | Hosting-only; weak by MLH's own note |
| Pokémon-Go / AR-scavenger for X | Location + camera + points | Common; hard to demo indoors |
| Smart-fridge / smart-kitchen IoT without hardware | Needs a device the team doesn't have | Fails hardware test |
| Generic dashboard / analytics for X | Charts of data the team made up | No transform; no need |
| AI-generated podcast / newsletter / story | Content generation as the product | Wrapper; no interactivity |
| Campus-anything (dining hall menus, class scheduler, dorm swap) | Needs CMU to be interesting | Excluded by team instruction |
| Security "password strength checker" / phishing quiz | Cyber + static rules | Sandia wants a real mechanism |
| "Agents that negotiate with each other" with nothing at stake | Multi-agent theater | Judges cannot verify anything happened |

Detection is by the agent (self-tag) and re-checked by red team. The parse script also greps developed one-liners for: `recipe, itinerary, planner, tracker, chatbot, assistant, summar, flashcard, resume, journal, dashboard, tipping, trivia` and flags for red-team attention (flag, not kill).

---

## 12. One-day scope estimator (agents run it; build-sim re-runs it)

Inputs per idea: components list (≤8), external services list, live dependencies list, team = 4 people, build window Fri 10:50pm → Sat 4:00pm = 17.2h, demo prep reserved 2h, sleep floor 3h per person.

**Hours**
1. For each component, estimate `h_i` = hours for one strong dev with Cursor to get it to demo quality (not production). Round up to 0.5h.
2. Hackathon tax: `h_i × 1.8`.
3. Integration tax: `+2h` per external service beyond the first, `+1h` for the first.
4. Unknown-tech tax: `+3h` per component using a technique nobody on the team has shipped before (`BR`).
5. `total_person_hours = Σ taxed h_i + integration + unknown`.
6. Capacity: 4 people × (17.2 − 3 sleep − 2 demo prep) = 4 × 12.2 = 48.8 person-hours, × parallelism efficiency 0.65 = **31.7 effective person-hours**. `total_person_hours > 31.7` → `SR = 5` and kill unless a named scope cut brings it under.
7. Critical path: longest dependent chain of taxed components. `> 11h` → kill (violates Sat-10am test).

**Demo failure probability**
Per live dependency, base `p_i`: hosted LLM call 0.05; wifi-dependent anything 0.10; a second device on stage 0.15; live multi-human (strangers/judges) 0.20; camera/mic capture in a new room 0.10; Solana devnet tx confirmation 0.10; GPU job finishing on cue 0.15; realtime sync between ≥3 clients 0.15; browser permission prompts 0.05. A named mitigation (cached result, pre-warmed state, recorded fallback clip ready, bot players) halves that dependency's `p_i`.
`p_demo_fail = 1 − Π(1 − p_i)`. `> 0.35` → `DR = 5`; kill unless a mitigation brings it under. `p_demo_ok = 1 − p_demo_fail`.

**Ship probabilities (build-sim only)**
`p_ship_core = clamp(1 − (critical_path / 11)², 0.1, 0.95)` adjusted −0.1 per `BR` component. `p_ship_polish = p_ship_core × 0.7`.

`ponytail:` linear taxes and independent failure events are the ceiling; upgrade is calibration against the team's actual Sat-10am checkpoint, which we record in `results/final_decision.md` for next time.

---

## 13. Failure modes of this orchestration, with mitigations

| Failure | How the night is wasted | Mitigation (already in plan) |
|---|---|---|
| Ideation overruns | Build starts at 1am; 14h left | Hard clock (§0); skip build-sim on ranks 16–30 and shrink jury before slipping build start |
| Mode collapse despite seeds | 300 ideas, 40 distinct | Obvious-dump, seed triple, forbid lists, cluster penalty; no relaunch, just penalize and proceed |
| Fast model writes shallow or malformed reports | Parse fails; rankings garbage | Strict JSON schema in a fenced block; validator; ≤10 re-runs; within-agent self-rank sanity check |
| Self-score inflation | Everyone is a 5 | Coarse buckets in round 1; red team replaces scores in round 2 |
| Sponsor Frankenstein | 4 integrations, 0 finished | Max 3 sponsors; each must pass bolt test with Q ≥ 3; final rule requires overall top-8 |
| Chasing thin-field prizes with no grand path | Win a Ledger, lose the room | Final pick requires top-8 overall ∩ top-8 P(any) |
| UNKNOWN treated as fact (K2 access, IFM track, Sandia rules) | Build on sand | Live verification table (§6.2) feeds jury; IFM ideas need Gemini fallback |
| Team hates the winner | Half-hearted 17h | `Y` score; human veto at top 3; runner-up named as pivot |
| Parent hallucinates rules while compiling packet | 100 agents inherit an error | Packet is compiled by copy-paste from the three source files, not paraphrased; one teammate diffs it against `competition_ground_truth.md` before launch |
| Rate limits / agent launch failures | Wave 3 never lands | 5 waves × 20; any agent not landed by 9:28pm is dropped, its cell noted in `results/rankings_round1.md`, no rerun |
| Humans steer wave 5 after seeing wave 1 | Correlation through the parent | Parent shows nothing until all 100 land |
| Red team kills everything | 50 → 4 | Red team must output a fix, not just objections; floor rules keep 30 |
| Recombination produces chimeras | Hybrid passes on paper, dies at 2am | Hybrids must re-pass bolt test and estimator and get their own build-sim |
| Demo room reality (3 rooms, wifi, projector) | Works at the table, dies on stage | Reset test, slow-LLM test, recorded fallback clip required by demo-sim |
| Pivot with no plan when Sat-10am checkpoint fails | Panic at 10am | Runner-up carried in `final_decision.md` with its build-sim |

---

## 14. Concrete artifacts

All paths under `/Users/nicholasmino/ProgrammingFiles/HackCMU/brainstorm/`.

**Parent writes before launch**
- `planning/fable_plan.md` — this file.
- `planning/shared_packet.md` — everything every agent reads (§6.1).
- `planning/seeds.csv` — `agent_id,cohort,home_track,domain,technique,twist,forbid_1,forbid_2,forbid_3,stack_pair`.
- `planning/agent_prompt_template.md` — the loop-1 prompt with `{{agent_id}}`, `{{cohort_brief}}`, `{{home_track}}`, `{{domain}}`, `{{technique}}`, `{{twist}}`, `{{forbid}}`, `{{stack_pair}}` slots.

**Loop 1 agents write** (one file each, nothing else)
- `agents/initial/NNN.md` for NNN = 001…100. Human-readable sections first, then one fenced ` ```json ` block that is the source of truth. Required JSON fields:

```json
{
  "agent_id": "001",
  "cohort": "TRACK",
  "home_track": "Optimization",
  "seeds": {"domain": "", "technique": "", "twist": ""},
  "obvious_dump": ["", "", "", "", ""],
  "raw": [{"n": 6, "one_liner": "", "why_not_obvious": "", "seed_used": "", "banned": false}],
  "developed": [
    {
      "idea_id": "001-A",
      "self_rank": 1,
      "name": "",
      "one_liner": "",
      "track": "Optimization",
      "track_why_50w": "",
      "core_tech_sentence": "",
      "before_after": {"before": "", "after": ""},
      "delete_llm_remains": "",
      "existing_products": ["", "", ""],
      "differentiator": "",
      "room_test_teams": 0,
      "sponsors": [
        {"name": "Solana", "role": "", "on_screen_moment": "", "bolt_substitute": "", "bolt_changes_demo": true,
         "scores": {"E": 0, "C": 0, "X": 0, "B": 0, "Q": 0}}
      ],
      "demo_script_6_beats": ["", "", "", "", "", ""],
      "slow_llm_fallback": "",
      "reset_seconds": 0,
      "components": [{"name": "", "hours": 0.0, "unknown_tech": false, "depends_on": []}],
      "external_services": [""],
      "live_deps": [{"name": "", "p_fail": 0.0, "mitigation": ""}],
      "estimator": {"total_person_hours": 0.0, "critical_path_hours": 0.0, "p_demo_fail": 0.0},
      "data_source_1h": "",
      "hardware_needed": [],
      "scores": {"U":0,"T":0,"O":0,"D":0,"F":0,"R":0,"P":0,"S":0,"N":0,"M":0,"J":0,"W":0,"A":0,"G":0,"H":0,"K":0,"Y":0},
      "risks": {"I":0,"API":0,"DR":0,"SR":0,"CR":0,"ER":0,"AR":0,"BR":0},
      "p_prize": {"grand":0,"track_1st":0,"track_2nd_or_3rd":0,"gemini":0,"elevenlabs":0,"solana":0,"vultr":0,"auth0":0,"mongo":0,"ifm":0,"cursor":0,"sandia":0,"peoples":0,"design":0},
      "kill_flags": [],
      "confidence": 0
    }
  ]
}
```

Validator rules: exactly 5 `obvious_dump`; `raw` has 15 entries numbered 6–20; exactly 3 `developed` with `self_rank` 1,2,3; all scores integers 1–5; `p_prize` values from the bucket set; sponsors listed only if `bolt_changes_demo` is true; `scores.Q` present per sponsor; `kill_flags` non-empty iff any §7.5 rule fires.

**Parent / tournament outputs**
- `results/initial_ideas.jsonl` — one developed idea per line, agent fields flattened.
- `results/oneliners.txt` — `idea_id | track | one_liner`.
- `results/obvious_dump_freq.md` — field estimate.
- `results/clusters.md` — from the clustering agent.
- `results/rankings_round1.md`, `results/rankings_round2.md`, `results/rankings_round3.md`, `results/rankings_jury.md` — five columns each plus kill/cluster notes.
- `results/parse_initial.py` — the validator/ranker (only script; stdlib only).
- `results/live_verification.md` — §6.2 table filled in.
- `agents/red_team/RT-01.md … RT-10.md`
- `agents/recombination/RC-01.md … RC-06.md`
- `agents/build_sim/BS-<idea_id>.md`
- `agents/demo_sim/DS-<idea_id>.md`
- `agents/jury/J-01.md … J-12.md`
- `results/finalists/<idea_id>.md` ×3
- `results/final_decision.md` — chosen idea, track, 50-word why, sponsors, roles, Sat-10am checkpoint, runner-up pivot.

---

## 15. Would I launch the 100 yet?

**Yes, at 9:00pm, with this allocation, without waiting on any UNKNOWN.** Reports are cheap; verification is slow; and every UNKNOWN in §6.2 changes *weights at the jury*, not *which cells to search*. Holding the launch to learn K2 access would cost 60 minutes of build time to save 6 agents' worth of reports.

Two things I want from the humans before 9:00pm anyway, because they change `F` for every idea: confirmed headcount (assume 4) and a one-line skill/hardware inventory (who has a GPU laptop or Apple Silicon, phones, webcam). If headcount is 3, cut STACK to 6 and PHYSICAL I/O to 3, add 3 to TRACK Optimization and 3 to SOLANA; the parent can do this by editing `seeds.csv` in two minutes.

UNKNOWNs that would change allocation *if known now*:
- K2 has **no** hosted/local access tonight → IFM 6 → 0; give 3 to SANDIA, 3 to SOLANA.
- Vultr code is **not** obtainable → VULTR 7 → 3; give 2 to AUTH0, 2 to TRACK Multiplayer.
- Cursor prize requires **Grok Imagine/Bot** in the product → add a 4-agent CURSOR cohort taken from ELEVENLABS (−2) and MONGO (−2).
- Sandia has a gate the team fails → SANDIA 6 → 0; give to TRACK Opt (3) and PHYSICAL I/O (3).

None of those are known at 8:35pm and none will be before the 9:00pm launch. Launch, verify in parallel, reweight at the jury.
