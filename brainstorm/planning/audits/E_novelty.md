# Auditor E — Novelty

**Question:** Will 100 agents still converge on generic AI wrappers / itinerary / recipe / Kahoot? Are seeds + bans + firewall enough? Independent discovery vs obviousness.

**Inputs (only):** `competition_ground_truth.md`, `prior_winners/notes.md`, `fable_plan.md`, `astra_plan.md`, `synthesized_plan_v1.md`.

**Stance:** Adversarial. No project ideas. No agents launched.

---

## Verdict

| | |
|---|---|
| **Score** | **41 / 100** |
| **Launch 100?** | **NO** |

**Direct answers**

1. **The four named clichés, as names:** mostly no. The banned table plus wrapper-kill plus `obvious_dump` will keep most *developed* rows from saying “recipe generator,” “trip planner,” or “Kahoot clone.” That is lexical hygiene, not novelty.
2. **The four clichés, as products:** yes. Expect the next ring: multimodal pantry → meal, voice trip agent, on-chain trivia, solver-scheduled calendar, camera-to-mesh in a new noun. Those pass self-tag, grep, and “I used a seed.” They are what this field already builds when someone says “don’t make a ChatGPT wrapper.”
3. **Seeds + bans + firewall:** necessary, not sufficient. Firewall buys *procedural* independence (no copying). It does not buy *statistical* independence. Seeds are optional on the only ideas the tournament sees. Bans are surface form.
4. **Independent discovery vs obviousness:** the pipeline discovers jitter around one posterior (same model, same packet, same winner templates, same negative space). That is not 100 independent observations. Astra said this out loud. v1 proceeds as if 100 cells make the mode unreachable. They do not.

Do not launch the 100 until the critical fixes below are in `final_ideation_plan.md`. Launching now spends the night minting well-formatted near-wrappers and winner-clones, then 20 recombiners will stack them and call the stack “original.”

---

## What the night actually selects for

Ground truth puts **Originality** on the official slide (“entirely novel / fresh approach”) and **Technical Difficulty** as “real technical challenges **vs ChatGPT wrapper**.” Traveling and Food are empty one-liners. The LIKELY field prior is Gemini chat “AI for X.” 2025 grand (Medicly) and the Gemini analogs in `prior_winners/notes.md` are *visible transform, not a chat box*.

So the losing mode is chat-wrapper. The *winning-looking* mode, once you ban chat-wrapper, is the notes file: camera/voice in, structured or spatial out, one-sentence core, demo that survives a slow LLM.

v1 puts that winning-looking mode in the **shared packet** (prior-winner patterns), in **Open-world** (“visible before/after”), in **Gemini** (multimodal / long context / tools), and in **Physical I/O** (“the Medicly pattern”). One hundred “independent” agents will rediscover the packet.

That is obviousness with a firewall.

---

## Ranked flaws

Severity: **C** = launch-blocking; **H** = will dominate the developed pool; **M** = silently inflates N/M and the 50-cut; **L** = residual.

### 1. [C] Seeds do not bind the ideas that enter the tournament

Fable §2.1 (inherited; v1 does not override): seeds are suggestions; use one of three in at least 10 of 15 *raw* ideas; **“may abandon them for the developed 3 if it says why.”**

The tournament is 300 developed ideas. Raw is discarded except as dump-frequency and color. An agent can satisfy the cell with ten strained one-liners, then develop the model’s mode plus a paragraph. The entire “100 cells make the mode unreachable” claim (Fable §1.2) dies in that clause.

Astra never granted this abandon. v1 took Fable’s `seeds.csv` and Astra’s batches and kept the leak.

### 2. [C] The shared packet is a second prompt, and it teaches the attractor

v1 firewall: everyone reads `shared_packet.md` only. Fable §6.1 compiles into that packet **prior-winner patterns**, the banned list, and the tests. `prior_winners/notes.md` is not an abstract rubric. It names:

- Medicly: phone video → findings + 3D mesh + exercises
- Impromptu: photo validation against prompts
- Taste Tape: structured JSON over a catalog
- DracoCare: voice agent that acts in the world
- Aqua-Cult: real model + Gemini as explainer
- Pattern: visible before/after, realtime/spatial, one-sentence core

Then v1 adds a **Physical I/O** cohort whose hard constraint is that pattern, and a **Research-lab** cohort whose brief *lists* the cores (SLAM, CRDT, DSL/compiler, differentiable X, solver).

That is assignment, not discovery. One hundred sealed contexts will still emit the same five “not-a-wrapper” templates with new nouns. Originality judges have seen those templates. Other teams in a CMU room remember Medicly.

**Keep the tests. Strip the implementations.** “Visible before/after” and “delete the LLM” are filters. Named 2025/2026 winners are recipes.

### 3. [C] Bans are lexical; the four clichés survive as shapes

Fable §11 (v1: union with Astra §11 + user heuristics):

| Banned string | Legal neighbor the model will emit |
|---|---|
| Recipe / fridge photo / meal planner | Constraint pantry, fermentation “optimizer,” dietary ILP, back-of-house prep sequencer |
| Itinerary / travel buddy / packing list | Voice “journey composer,” visa-paperwork agent, hostel matching with a map |
| Calendar / study-plan optimizer | SAT/CP-SAT over a personal schedule (technique list literally contains ILP/SAT/CP-SAT) |
| Kahoot / Jackbox / trivia | Party game, co-op puzzle, esports “knowledge duel,” board-game night with phones |

Detection: **self-tag**, red-team, and a parse grep of `recipe, itinerary, planner, tracker, chatbot, assistant, summar, flashcard, resume, journal, dashboard, tipping, trivia` — **flag, not kill**.

Fast models rename. “Cuisine sequencer” will not grep. Fable even invites “build the *opposite* of a row.” Opposite of Kahoot is still a scored room game. Opposite of itinerary is still a travel-planning loop.

Astra’s cliché rule (rebuttal, not ban) is weaker than Fable’s table. Unioning them without a precedence rule lets the agent pick the rebuttal path: “not a recipe, because there is a solver.”

### 4. [H] Food / Travel / Multiplayer × the domain deck recreates the basins

Ground truth: four tracks, Relevance is judged, one-liners are empty. Empty track + LLM = training-set default.

Fable knew this: TRACK weighted **5/5/3/3 toward Opt/Multi** because Food/Traveling absorb recipe/itinerary. v1 **dropped that weighting**. Home track is `id mod 4` across the population. ~25 Food homes, ~25 Traveling homes, plus Open-world may still pick those tracks.

Domain list (Fable §2.1, v1 seed triple) includes street food, fermentation/brewing, dietary medicine, dorm cooking, grocery, restaurants BOH, road trips, air travel, hostels, maps, translation on the move, tabletop, board-game night, esports, co-op puzzle, party games.

`domain[i mod 40]` assigns each of those to 2–3 agents. Food-home + cooking domain + any LLM-tolerant technique is a recipe-shaped cell. Travel-home + road-trips/air/hostels is an itinerary-shaped cell. Multi-home + party/tabletop/esports is a Kahoot-shaped cell.

Forbids are 2 unused *techniques* + 1 unused *domain*. They do not forbid product shapes. Forbidding OCR does not stop an itinerary. Forbidding hiking does not stop a meal planner.

### 5. [H] Same model, same packet, no statistical independence

Astra §4: “A hundred contexts using one model remain correlated. The plan reduces shared prompt and information effects; it does not treat their agreement as 100 independent observations.”

v1 keeps one executor, one packet, one banned list, one seed deck, no web (correct), no peer files (correct), no wave feedback (correct). Those stop *copying* and stop 100 agents googling “food hackathon ideas.” They do not stop 100 draws from `P(idea | Grok, packet, seed_i)`.

Seed assignment is modular, not a balanced design: `domain[i%40]`, `technique[(i*7)%30]`, `twist[(i*3)%20]`. Period `lcm(40,30,20)=120`. One hundred agents do not cover the triple space; many (domain, technique) pairs never appear; collisions do. Twists decorate the mode (“funny on stage” + Food, “audience phones” + Multiplayer, “single photo” + Food = fridge photo, which is *on the banned list*).

Consensus in the 50-cut is one model agreeing with itself.

### 6. [H] v1 recombines before a real novelty check

Fable order: cluster → 50 → **red team with search** → 30 → recombination.  
Astra order: 50 → recombination → 30 → red team.  
**v1 order: cluster → 50 → 20 recombiners → red team on ~30.**

Twenty recombiners (v1 raised Fable’s 6 to 20) will manufacture **stack novelty**: voice + itinerary + escrow + pose. Astra already forbade this (“a new combination must produce a new behavior, not just a longer stack”). v1 keeps the sentence and then funds 20 agents to violate it before anyone with search looks at nearest products.

Loop-1 `three-products` is unaided training-data theater. “No search result” is not novelty (Astra). Novelty search on 30 survivors is too late if the 50 is already next-ring cliché.

### 7. [H] Wrapper test and leftover theater

Kill: “Delete the LLM. What remains? Nothing → kill.” Applies to every cohort.

The model will always name a remainder: the solver, the scoreboard, the map, the mesh, the escrow. Then:

- If the remainder *is* the product, three-products should kill (solved app + “AI”). Agents will claim the differentiator is the remainder *and* the model.
- If the remainder is a stub, it still fills `delete_llm_remains` and survives parse.

Self-score, same model, fast executor. Red team is the same model family with search, later, on a subset. `CR` from dump-frequency uses “within one edit” — **undefined**. “Constraint-solved weekly menus from pantry photos” is not one edit from “what’s in my fridge” to a regex. It is the same product.

### 8. [H] Sponsor hard-constraints block chat and license the next cliché

Gemini: text-in/text-out = fail → photo/video food and travel.  
ElevenLabs: voice is the loop → spoken itinerary / spoken quiz.  
Solana: visible state → on-chain scoreboard, dinner escrow (split-the-bill adjacent).  
Auth0: identity changes behavior → login-gated Kahoot room.  
Mongo: Atlas feature on screen → vector search over menus / places.  
STACK (10) + Gemini-in-pairs: multimodal + something.

These constraints are correct for bolt-test honesty. They do **not** aim the search off the four basins. They aim it at the multimodal/voice/on-chain edition of the same basins. Gemini “rides free” across ~60 agents (Fable; v1 agrees). Six dedicated Gemini cells is extra pressure on the same corner.

### 9. [M] Clustering is on one-liners; floors protect the dangerous tracks

Fable §9.1: clustering agent reads `oneliners.txt` (id + one-liner + track). Size ≥4 → `CR=5`, one representative advances.

“Pantry ILP,” “dietary constraint engine,” and “fermentation scheduler” will not cluster. Astra’s fingerprint (user job, mechanism, input, interaction, visible proof, external deps) is the check that matters. v1 says “parse/dedupe/cluster” and does not adopt the fingerprint.

Then v1 **floors**: each track ≥5 in the 50, each cohort ≥2. That reserves ~20/50 for track coverage, including Food and Traveling, *especially if those tracks are wrapper-heavy and lose on merit*. Fable’s “sparse track keeps its top 3 regardless” was about prize EV, not about forcing track-default product shapes into the shortlist. v1 mixed those motives.

### 10. [M] Obvious-dump is a field estimator, not a mode flush

v1: 5 dump + 15 real. Claim: first five ideas *are* the field; write them down so they cannot contaminate.

Two different tasks were glued together.

- “What will the room build?” produces stereotypes (`AI chat for food`).
- “Get the mode out of *this* model” requires the model’s actual next tokens, which continue through ideas 6–20 with nicer nouns.

`why_not_obvious` in Fable is a **5-word tag**. That is a slogan, not a mechanism distinction. Astra’s raw row (user, need, mechanism, visible proof, dependency, ~55 words) is the stronger local check. v1 kept the dump and did not require Astra-strength raw rows.

Dump-frequency → `CR=5` only if a developed one-liner is “one edit” from a high-frequency dump string. Agents who read the rule will avoid the dump phrasing on purpose. The parse grep is the same game.

### 11. [M] Research-lab and Physical I/O are prompted clones

Research-lab n=5, brief enumerates the acceptable cores. Physical I/O n=4, “the Medicly pattern,” no bought hardware. Anti-AI n=5 is the only cohort that *structurally* leaves the LLM-wrapper basin.

Novelty budget that cannot emit a chat app: **5 + maybe 5 research + 4 I/O = 14/100**, and 9 of those 14 are told what to build in type. The other 86 are sponsor/track/demo cells whose easiest *legal* output is wrapper++.

### 12. [M] Pilot n=2 cannot see population collapse

v1 preflight: 2 pilots (one open-world, one specialist). If JSON is invalid or “ideas are wrappers,” fix the prompt **once**.

Two agents × 3 developed = 6 rows. A 40% next-ring-cliché rate can look like 0/6 in a lucky draw. Collapse is a *distribution* property. You cannot QA it with n=2, and you cannot fix a packet-level attractor with one prompt adjective.

### 13. [L] Twist deck is 20 gimmicks, reused 5×

Offline, one-button, no screen, funny, judges-as-players, model-as-villain, single photo, race-the-baseline. These are demo decorations. Assigned by `(i*3) mod 20`, they do not move user-job or mechanism. They make one-liners look diverse to a clustering agent that only reads one-liners.

### 14. [L] Fast executor + 20 raw favors rename-and-pad

v1 executor (from Fable): fast Grok, 20 raw, 3 developed. Fable’s own defense of 15 real is “the point where a fast model stops recombining its first ideas.” That is an aspiration. Fast models stay near mode and pad lists. Schema validity ≠ mechanism change across batches. v1 “force mechanism change across batches” has no validator: no fingerprint diff, no reject-and-rewrite if batch C is batch A with a new audience label (Astra §2 already named that failure).

---

## Independent discovery vs obviousness (the cut)

| Claim in the plans | What is actually true |
|---|---|
| 100 cells → mode unreachable | Mode moves from chat to anti-wrapper template + track defaults |
| Firewall → independent | Independent files, correlated weights and packet |
| Banned list → those ideas die | Those *strings* die; those *jobs* get a technique from the deck |
| Obvious-dump → field estimate and mode flush | Decent field stereotype table; weak flush |
| Cluster penalty → diversity | Diversity of titles, not of user-job × I/O loop |
| No web on loop 1 → less collapse | Correct vs googling; makes loop-1 “existing products” fictional |
| Red team + search → novelty | Too late in v1; same-model skeptic; 30 rows not 300 |
| Recombination → new ideas | New stacks of old jobs |
| Prior winners = calibration | Prior winners = shared examples; examples dominate |

**Independence** is a property of information flow. v1’s firewall is fine on flow.

**Discovery** is a property of search. Optional seeds + named winner patterns + enumerated research cores = interpolation.

**Obviousness** is a property of the room. Ground truth already says the room’s default is Gemini “AI for X,” and Food/Traveling absorb recipe/itinerary. A pipeline that equal-rotates those tracks and shares Medicly/Impromptu/DracoCare will hand humans a shortlist that looks original *inside the JSON* and ordinary *on stage*.

---

## Fixes (architecture only — apply before any launch)

Mapped to flaws. No products.

1. **Bind seeds on developed ideas.** A developed row must keep ≥1 of {domain, technique, twist} as a *load-bearing* mechanism or I/O constraint, not a flavor noun. “Abandoned seeds” is a kill flag unless the replacement still differs on Astra’s fingerprint (user job, mechanism, input, interaction, proof) from the agent’s own `obvious_dump`. (Fixes 1, 10, 14.)

2. **Strip implementations from the shared packet.** Packet keeps: judging axes, wrapper/bolt/room tests, banned *shapes*, prize bars, UNKNOWNs as UNKNOWN. Packet drops: Medicly / Impromptu / Taste Tape / DracoCare / Aqua-Cult writeups, “the Medicly pattern” as a cohort slogan, and the research-lab enumerated core list. Those stay in a **parent-only** file for *later* red-team nearest-neighbor checks, not in the 100. (Fixes 2, 11.)

3. **Ban product shapes, not just strings.** For each banned row, store a fingerprint: user job + essential I/O loop + “AI/chat/recommend/plan/quiz” as the verb. Self-tag on fingerprint. Parse-time kill (not flag) if developed fingerprint matches. Grep stays as a backstop, not the rule. “Opposite of a row” is deleted; it is a second mode. Astra rebuttal is allowed only when the *job* changes, not when a solver is bolted onto the same job. (Fixes 3, 7.)

4. **Restore Fable’s track weights and drop Food/Travel floors.** Open-world / TRACK: Opt/Multi heavy. Do not guarantee ≥5 Food and ≥5 Traveling in the 50. Sparse-track EV is a *later* ranking rule, not a novelty quota. Add a **shape ban** at assignment time: Food-home ∩ {street food, fermentation, dorm cooking, dietary, grocery, restaurants} and Travel-home ∩ {road trips, air travel, hostels, maps, packing/visa} require a **non-LLM** technique already in the raw set, or the cell is re-dealt. (Fixes 4, 9.)

5. **Cluster on fingerprints, on all 300, before the 50.** Adopt Astra §2 fingerprint. Cap: normally ≤2 per (job × mechanism × interaction); 3–4 only with a written feasibility/demo/prize difference. One-liner clustering is extra, not primary. Treat same-model cluster size as **correlation**, not as votes. (Fixes 5, 9, 13.)

6. **Put search-novelty back before recombination.** Fable order: 50 → red team + web (nearest product, nearest hackathon, nearest *internal* fingerprint) → 30 → then recombiners. Recombiners must name the **new behavior**; stack-only hybrids are kill. Cut recombiners from 20 toward Fable’s 6 unless the 30 is already fingerprint-diverse; 20 is a novelty-washing budget. (Fixes 6.)

7. **Make leftover theater fail.** Wrapper test is a kill only if remainder is nothing *or* remainder is a solved product whose differentiator is “AI” / “for X” / a sponsor. Three-products becomes: if you cannot name a differentiator that is visible after deleting both the LLM *and* the sponsor, kill. Red team, not the author, fills `existing_products` for anything that reaches 50. Undefined “one edit” is replaced by fingerprint match against dump-frequency ≥8 → `CR=5` **and** ineligible for overall top-8. (Fixes 7, 10.)

8. **Do not let sponsor constraints rewrite the basin.** Specialist prompts must say: passing Gemini-multimodal / voice-loop / visible-tx does **not** legalize the banned *job*. A photo meal-planner is still the Food default. A spoken itinerary is still the Traveling default. A scored-question room is still the Multiplayer default. (Fixes 8.)

9. **Pilot for collapse, not just schema.** After audit: ≥5 sealed pilots spanning Open-world, Gemini, Food-home, Travel-home, Multi-home. Parent (human) fingerprints the 15 developed rows against the banned shapes and against each other. If ≥5/15 are shape-matches or one cluster ≥4, rewrite packet + bind-seeds **once** and rerun the 5. n=2 is a JSON lint. (Fixes 12, 14.)

10. **Say the independence limit in the parent ranker.** Cluster agreement does not raise `N`, `M`, or `p_any`. It raises `CR`. Jury personas do not see “100 agents independently found this.” (Fixes 5.)

Hygiene already in v1 that should **stay**: no loop-1 web, no peer reads, no wave edits, no human steering mid-waves, obvious-dump as a *field table*, wrapper/bolt/hardware/data kills, Anti-AI cohort, bolt test, max-3 sponsors, “do not call a partial run the 100.”

---

## Score

| Slice | /100 | Why |
|---|---:|---|
| Surface chat-wrapper suppression | 72 | Banned verb list + wrapper kill + no-web + dump |
| Itinerary / recipe / Kahoot as *products* | 28 | Equal track rotate, domain deck, lexical grep, leftover theater |
| Winner-clone / anti-wrapper template | 22 | Packet examples + Physical I/O + Gemini constraints |
| Statistical independence | 30 | Firewall is real; one model + one packet is not 100 observations |
| Near-miss detection before it is too late | 34 | Self-score, late search, one-liner clusters, flag-not-kill |
| Ability to *discover* vs interpolate | 24 | Optional seeds, enumerated research cores, 20 recombiners |

**Weighted overall: 41.**

Better than one mega-prompt. Not enough to bet Originality and “vs ChatGPT wrapper” on. The residual mode is exactly what a CMU beginner-friendly field plus this packet will also invent.

---

## Launch 100?

**NO.**

Not because of K2/Vultr/Sandia (those reweight). Not because of runtime (other auditors). Because the novelty machinery as written will spend ~100 reports proving it avoided the words “recipe,” “itinerary,” and “Kahoot,” while the developed pool and the recombination layer refill those jobs.

Launch only after fixes 1–9 are in the final plan (10 can land in the ranker script). The 10-minute preflight does not substitute: a valid JSON wrapper++ still wastes the night.
