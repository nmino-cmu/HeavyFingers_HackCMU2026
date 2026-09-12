# Auditor A — Search-Theory Audit

**Target:** `synthesized_plan_v1.md` allocation and coverage design.  
**Question:** Is the 100-agent allocation actually likely to cover idea space effectively?  
**Lenses:** mode collapse, correlated cells, missing regions, over-allocated prizes.  
**Constraint:** architecture only. No project ideas. No agents launched.

**Verdict:** The 100 is a labeled grid, not 100 independent searches. Same model + same packet + abandonable seeds + soft tracks + prize-weighted specialist mass ⇒ effective coverage is closer to ~25–35 constrained modes. Sponsor intersections are over-searched; grand-path volume is under-searched; the distinctive cohorts sit in the last waves and die first if the runtime sheds agents.

---

## 1. Flaws (ranked)

### CRITICAL — Same-model draws are not independent cells

Fable’s load-bearing claim: “100 cells each constrained by cohort + track + seed triple make the mode unreachable in most cells.” That is false.

All 100 loop-1 workers are one model (`cursor-grok-4.6-xhigh-fast`) reading one `shared_packet.md`. A constraint does not delete the prior. It relocates the mode: you get the modal *Solana+Food+twist* idea, not an open draw from Solana+Food+twist. Astra stated this and the synthesized plan dropped it. Agreement across 8 Solana reports is one observation, not eight.

Implication: advertised N=100 is a vanity count. Intra-cohort cosine will be high. Tournament stages using the same model will *confirm* the collapse because they share the prior.

### CRITICAL — Seeds do not bind the only ideas that matter

The developed 3 (300 candidates, the actual pool) may abandon the seed triple if the agent “says why.” The only hard seed rule is “use at least one of three in at least 10 of 15 raw.” Raw ideas are discarded after development.

So the coverage instrument is optional on the objects that enter ranking. Unique modular triples (`domain[i mod 40]`, `technique[(i*7) mod 30]`, `twist[(i*3) mod 20]`) are real — `lcm(40,30,20)=120`, so no two of 100 agents share a full triple — and then get thrown away. Forbids (2 techniques + 1 domain) are a 6.7% / 2.5% ban and are not stated as binding on developed ideas in the synthesized file.

This is the single cheapest reason the grid fails: the cells are painted on and then the paint is allowed to wash off.

### CRITICAL — Wave order = cohort order = systematic hole if anything drops

Synthesized launch is waves of 20, IDs 001–100, “retry once, then drop the cell.” Fable already planned to drop anyone not landed by a cutoff, no rerun.

Cohorts are contiguous ID blocks. Wave 1 is almost all open-world. Wave 5 is research-lab + physical I/O + IFM + Sandia — the only cohorts that are actually orthogonal to “sponsor-shaped hackathon product.” Rate limits, schema failures, and clock kills hit later waves first. You will lose the rare regions and keep 18 correlated open-world reports plus the MLH specialist blob.

A dropped cell is not a random missing ticket. It is a missing *region*, and the regions you lose are the ones the allocation claimed were the diversity hedge.

### HIGH — Allocation is prize-EV, not search-volume

The grid spends **63 / 100** agents on sponsor-shaped search (Gemini 6 + Eleven 8 + Solana 8 + Vultr 7 + Auth0 8 + Mongo 6 + Stack 10 + IFM 5 + Sandia 5). Open / style / mechanism search is **37** (open-world 18 + anti-AI 5 + demo-first 5 + research 5 + physical 4).

Idea-space volume is the opposite shape. “Identity is a primitive,” “visible devnet state,” “Atlas feature on screen,” “voice is the loop,” “K2 in a way Gemini cannot” are *small* manifolds. Open-world / research / anti-AI are *large*. Search theory allocates hunters to unexplored volume × P(find a buildable, prize-relevant point), not to Ledger replacement value. Fable’s Solana-9 / Auth0-8 story is EV. The synthesized 8/8/6 split kept that story and only shaved the edges.

STACK makes it worse. Effective sponsor hunters after pair overlap:

| Sponsor | Dedicated | Also in STACK | Effective |
|---|---:|---|---:|
| Solana | 8 | 063, 067, 069, 071 | **12** |
| Auth0 | 8 | 062, 067, 068 | **11** |
| ElevenLabs | 8 | 064, 068, 071 | **11** |
| Mongo | 6 | 062, 063, 066, 070 | **10** |
| Vultr | 7 | 065, 066, 069 | **10** |
| Gemini | 6 | 064, 065, 070 + “rides free” on ~60 | **9 dedicated, ~60 free-riders** |

Gemini-rides-free is correct for *eligibility*. It is fatal for *dedicated Gemini cells*: the multimodal corner is maybe 3–4 disjoint capabilities. Six generalists with an OR-list (“image/video/audio / ≥100k / structured+tools”) all pick the easiest (structured output + tools). The five other Gemini bullets go unsearched while the count says 6.

Mongo’s own rationale says the differentiated Atlas feature set is narrow. Then the plan puts 10 hunters on ~5 features.

STACK 10 sits in *intersections* of already-narrow sets. Intersection volume is tiny. Ten agents there is not coverage; it is ten draws from three tropes.

IFM 5 searches a set that may be empty (K2 access UNKNOWN). Mandatory Gemini fallback means successful reports are allowed to be Gemini-adjacent. That is five more Gemini-ish cells, not five K2 cells.

### HIGH — Soft home track + `id mod 4` undoes track strategy

Synthesized: “Home tracks rotate Opt / Multi / Travel / Food by `id mod 4`. Soft lens.”

Fable’s TRACK cohort was hard-assigned and tilted 5/5/3/3 Opt/Multi because Food/Traveling are the wrapper sinks (ground truth: those tracks’ default products are in the banned list; popular tracks get 1st/2nd/3rd, sparse may get 1st only). The synthesized plan flattened *every* cohort, including open-world, to a soft rotating lens.

Population track tickets happen to land 25/25/25/25. That is not coverage. A soft lens plus a model that likes games and demos will convert Food/Traveling tickets into Multiplayer/Optimization submissions with a strained 50-word why — or into “clever food that is not a recipe generator,” which is itself a collapsed region. You will *assign* 25 Food cells and *search* maybe a dozen honest ones.

Tournament floors (each track ≥5 of the 50) then **keep** the weak Food/Traveling residue so the funnel looks balanced. That is anti-coverage: a fifth-best collapsed-track idea occupies a slot a unique mechanism lost.

### HIGH — Specialist prompts are one cell copied n times

Every Solana agent gets the same hard constraint: “Devnet state change the judge can see.” Every Auth0 agent: “Identity changes behavior.” Every ElevenLabs agent: “Voice is the loop.” Every Vultr agent: “Visible compute.” Every Mongo agent: “Atlas feature on screen.”

That is 8 copies of one instruction, not 8 regions. Partition the constraint or you have n=1 per sponsor with extra adjectives. Combined with optional seeds, intra-cohort collision is the default, not a failure mode.

Physical I/O is worse: four agents, one pattern (phone/cam/mic in, spatial/realtime out). Fable named it “the Medicly pattern.” The synthesized brief removed the name and kept the template. The shared packet still carries 2025-winner notes. Open-world, Gemini-multimodal, research-lab (SLAM/pose/CV are on the technique list), and demo-first will all fall into the same attractor. Predicted largest cluster: sensor → spatial transform → 3-minute wow. Four dedicated cells plus leakage from four other cohorts is overfit to one prior year, which ground truth itself warns not to reuse as 2026 structure.

### HIGH — Collapse detection cannot see the collapse

- Clustering is on **one-liners**. Mechanism-identical ideas with different nouns will not group. Astra’s fingerprint (user job, mechanism, input, interaction, proof, deps) was the correct object. Synthesized kept Fable’s one-liner pass.
- Obvious-dump is **contaminated by the banned list**. All 100 agents read the same §11 table, then are asked for “the five things most teams build tonight.” The dump frequency table will recover the packet, not the field. Developed ideas that avoid those strings look diverse while sitting on the model’s *second* layer of clichés. The `CR=5` if “within one edit of a dump item appearing ≥8 times” rule only catches people who failed to read the banned list.
- No relaunch if `>30%` of developed ideas sit in clusters of size ≥4. Fable already budgeted “300 ideas, 40 distinct” as an acceptable night. That is a failed search they planned to *penalize and ship*.
- Cohort floors (≥2 per cohort into the 50) **force** collapsed sponsor duplicates through the funnel. Diversity theater at the cost of unique open-world / research ideas.
- Recombination (20 agents) interpolates the pool it is given. It cannot invent an unsearched region. Twenty recombiners on a 40-distinct-idea pool produce more 40.

### HIGH — Missing first-class regions

The factorization is cohort × (soft) track × (optional) seed. That is not a covering design of the space that matters tonight.

Absent as hard cells:

1. **Grand-path technical volume that is not Medicly and not a sponsor.** Research-lab is 5%. Anti-AI is 5%. Ground truth: beginner-friendly *and* CMU-CS-heavy. The competitive moat is “executable by this team, not by the wrapper field.” That region is 10 agents, then the tournament floors dilute it with sponsor seats.
2. **Assumption-reversal / packet-inversion.** Astra’s Batch C exists as a *within-agent* ritual (3 batches of 5). There is no cohort whose job is to break a packet assumption. The packet becomes law; 100 workers optimize it.
3. **Architecture / deployment class.** Local-only, p2p, browser extension, on-device, no-cloud. Offline appears as one optional twist among 20, not a cohort. Ground truth: 3 judge rooms, wifi, projector. A no-cloud region is prize-relevant (demo risk) and almost unsearched except as a seed someone may abandon.
4. **Honest dual-track / boundary ideas.** One home track per agent, Relevance scored against that track. Boundary volume (optimization-of-multiplayer, food-as-logistics, etc.) is systematically under-sampled. Submission still picks one track; *search* should not.
5. **Cursor / Grok Imagine-Bot.** Bar UNKNOWN; 0 dedicated cells unless preflight steals 070–071 from STACK. If those IDs already ran as stack, you cannot “steal” them. Post-hoc reallocation of completed cells is a fiction. People’s Favorite and Best Design are dumped on demo-first (5), which is a *method* (design the wow first), not a region, and not two different judge optima.
6. **Demo-first is not a region.** Five agents re-search open-world with a stage prior. They will collide with open-world and physical I/O.

Domain list internal correlation (not missing, but fake spread): ~6/40 travel-adjacent, ~6/40 food-adjacent, ~5/40 games. Technique list is heavy on CV/audio/ML (~10/30), which feeds the Medicly attractor. Twist list is ~50% stage tricks, which feeds demo-first. The decks look like 40×30×20. They are lumpier.

### MED — Shared packet is a mode injector

Correct firewall (no peer files, no web, no wave-to-wave edits). Incorrect contents: banned list + prior-winner patterns + “distinctive” sponsor column + field prior + the full test battery, identical for all 100.

The banned list is useful as a kill filter and poisonous as a *generator*. “Build the opposite of a row” is itself a mode (20 specified attractors → 20 specified anti-attractors). Prior-winner notes in the packet teach the model what “winning” looks like. Distinctive-capability bullets teach every specialist the same three talking points.

Astra: initial agents must not see allocation totals, tournament favorites, or parent examples. Synthesized agrees. The packet still contains enough “what good looks like” that you do not need those.

### MED — Tournament floors fight the cluster cap

50-cut: each cohort ≥2, each track ≥5. If specialists collapsed, you keep two near-duplicates per sponsor cohort (14 cohorts × 2 = 28 of 50) before quality. Track floors add more residue. Astra’s “no sponsor guaranteed seat” + “≤2 per mechanism×interaction cluster” was the coverage-preserving rule. Synthesized picked Fable’s floors. That is prize-ticket insurance, not search.

### MED — Preflight cannot measure collapse

A 2-agent pilot (one open-world, one specialist) can catch invalid JSON and wrapper-shaped output. It cannot estimate intra-cohort collision. You need ≥2 agents *in the same specialist cohort* to see whether the hard constraint is one cell. The plan will greenlight 100 on “the reports parsed.”

### MED — Capacity vs claimed N

Astra: do not launch 100 under the fiction the runtime can finish them; native slot count may be ~3 workers. Synthesized: launch 100 after a 10-minute preflight, never call a partial run “the 100,” drop failed cells.

If throughput is low, you get a *biased* subset (early ID blocks) and are forbidden to name the hole. Search-theoretically a planned 36-cell covering design that finishes dominates a random 60/100 of a bad design, especially when the missing 40 are the last waves.

### LOW — `id mod 4` couples track to specialist ID block

Within a contiguous cohort the rotation is fine (most size-8 cohorts get 2/2/2/2). Size-7 Vultr is Food-short (1). Size-6 Mongo is Multi/Travel-short (1). Size-5 cohorts are 2-on-one-track / 1-on-others. This is minor next to soft-track abandonment, but if you ever make tracks hard, fix assignment so mechanism-partition and track are independent. Do not let “Solana escrow” lock to Optimization because that ID landed on `id ≡ 1 (mod 4)`.

### LOW — Reallocation rules are timed wrong

K2 dead → 091–092 open-world, 093–095 demo-first. No Vultr code → 041–043 open-world, 044–047 demo-first. Sandia gate → 096–100 open-world. Cursor Imagine → steal 070–071.

These only help if they fire *before* assignment freeze. Synthesized puts them at preflight, which is correct *if* preflight actually resolves those UNKNOWNs. Ground truth: K2 workshop is 9–10pm, Cursor workshop 10–10:30pm — **after** a 9:00pm launch. Fable was honest: those UNKNOWNs will not be known at launch. Synthesized “if K2 is dead at preflight” pretends a 10-minute preflight starting after audit can learn workshop facts that do not exist yet.

So IFM 5 and Vultr 7 and the Cursor steal are allocated into fog. That is over-allocation of possibly-empty regions, not a live reweight.

---

## 2. Specific fixes

Do not launch the current 100. Change the rules, then the counts, then the wave schedule.

### Rule changes (do these even if you refuse to move seats)

1. **Bind seeds on developed ideas.** Each developed idea must use **≥2 of {domain, technique, twist} in a load-bearing way** (delete it and the demo changes). One-sentence abandonment is illegal. If a seed is impossible under the cohort constraint, replace it with `list[(index + 17) mod n]` and record the swap — do not free-choose.
2. **Bind forbids on developed ideas.** Raise to **2 domains + 2 techniques + 1 twist**, none equal to the assigned seeds, and they cannot appear as the core mechanism/domain of a developed idea.
3. **Hard home track.** Soft lens is cancelled. Open-world tilt: **10 Opt / 9 Multi / 5 Travel / 4 Food** (or whatever the open-world *n* is, same 2:2:1:1 shape). Food/Traveling are collapsed regions; do not give them equal search mass.
4. **Partition every specialist constraint into disjoint subcells.** One mandatory mechanism per agent, not an OR-list. Examples of the *rule* (not ideas): Gemini 3 = {multimodal-in, long-context, structured+tools} one each; Solana 5 = five disjoint on-chain jobs; Auth0 5 = five disjoint identity jobs; Mongo 4 = four Atlas features; ElevenLabs 5 = five disjoint voice jobs; Vultr 5 = five disjoint visible-compute jobs. STACK pairs must not duplicate a specialist’s exact subcell.
5. **Cluster on fingerprints, not one-liners.** Fingerprint = user-job + mechanism + input-dependency + interaction-loop + visible-proof. At the 50-cut: **≤2 per cluster.** Cohort floor **≥1** (not ≥2). Track floor **≥3** (not ≥5). No sponsor is owed two seats.
6. **Interleave waves by cohort, not by ID.** Each wave of 20: ~6 open-world, ~8 mixed specialists, ~3 style (anti-AI / research / physical / offline), ~3 IFM/Sandia/stack. If agents drop, holes are uniform. Never put all rare cohorts in wave 5.
7. **Strip winner-templates from specialist briefs.** Packet may say “do not copy a prior mechanism.” Physical I/O brief must not encode the 2025 sensor→spatial template as the cohort definition. Banned-list stays a *kill filter* in the validator, not a “write the opposite” generator in the prompt.
8. **Obvious-dump before the banned list.** Agent writes 5 dumps, *then* receives the banned table to tag them. Otherwise the dump is a packet echo and the field-frequency table is junk.
9. **Pilot 6, not 2.** Two open-world + two of the *same* specialist cohort + two of a second specialist. Kill criterion: if the pair in one cohort is mechanism-duplicates, rewrite that cohort’s partition (rule 4) once. JSON-valid wrappers are not a pass.
10. **Capacity gate.** Measure `t` on the pilots. If `ceil(100 / workers) * t` plus tournament does not fit the ideation budget, **do not launch 100**. Launch a labeled reduced covering (below, or a 60-cell subset with the same proportions) or abort to build. A biased 60 of this grid is worse than a finished 36 of a covering.
11. **Reallocation only before freeze.** IFM/Vultr/Sandia/Cursor changes apply to `seeds.csv` before wave 1. After launch, jury reweights `p`; they do not restripe cells. Cursor steal of 070–071 after those agents ran is deleted as a plan step.
12. **If a second model exists, give it 8–12 seats** in open-world + research + anti-AI only. Same-model 100 cannot be debiased by more Grok.

### Exact reallocation (100, search-volume first)

Sponsor-shaped dedicated mass **40** (was 63). Open / orthogonal mass **60** (was 37).

| IDs | n | Cohort | Binding rule |
|---|---:|---|---|
| 001–028 | 28 | Open-world | Grand path. Hard track 10/9/5/4 Opt/Multi/Travel/Food. No sponsor required. Seeds bind. |
| 029–031 | 3 | Gemini | One capability each: multimodal-in / long-context / structured+tools. Not an OR. |
| 032–036 | 5 | ElevenLabs | Five disjoint voice-loop subcells. Voice is the product loop. |
| 037–041 | 5 | Solana | Five disjoint visible-devnet jobs. |
| 042–046 | 5 | Vultr | Five disjoint visible-compute jobs. Hosting = fail. |
| 047–051 | 5 | Auth0 | Five disjoint identity-as-primitive jobs. Login gate = fail. |
| 052–055 | 4 | Mongo | Four Atlas features, one per agent. Persist-only = fail. |
| 056–061 | 6 | Stack | Pairs only: Auth0+Solana, ElevenLabs+Gemini, Vultr+Mongo, Solana+Vultr, ElevenLabs+Auth0, Gemini+Mongo. Drop Auth0+Mongo, Solana+Mongo, Vultr+Gemini, ElevenLabs+Solana (near-duplicates of specialist intersections). |
| 062–069 | 8 | Anti-AI | No LLM in the essential loop. Hard tracks even. |
| 070–073 | 4 | Demo-first | Stage-first *method*, substance still required. Do not treat as a region. |
| 074–081 | 8 | Research-lab | One hard core; still demoable. This is the CMU-moat volume. |
| 082–085 | 4 | Physical I/O | Sensors you already have; **not** a restatement of 2025. |
| 086–089 | 4 | Offline / local-first | Demo survives dead wifi without a recorded fake. Missing region vs 3 rooms. |
| 090–092 | 3 | IFM / K2 | K2 load-bearing; Gemini fallback required. If access unverified at *true* freeze, these three → open-world before launch, not after. |
| 093–096 | 4 | Sandia | Real mechanism on stage; no live third-party targets. |
| 097–100 | 4 | Assumption-reversal | Hard job: invert one packet assumption (a test, a sponsor “distinctive,” a field prior). Not a sponsor hunt. |

**STACK effective sponsor counts after this cut:** Solana 5+2=7, Auth0 5+2=7, Eleven 5+2=7, Vultr 5+2=7, Gemini 3+2=5, Mongo 4+2=6. Still more than mechanism volume, but no longer 10–12.

**Open-world 28 + research 8 + anti-AI 8 + offline 4 + assumption-reversal 4 + physical 4 + demo-first 4 = 60** on large or orthogonal manifolds.

If the capacity gate forbids 100, scale this table by 0.6 and keep the same ratios (17 open-world, 2 Gemini, 3 per fat specialist, 4 stack, 5 anti-AI, 5 research, 2 each small cohort). Do not scale by dropping the last IDs.

### What not to do

- Do not add more STACK to “raise P(any).” That is EV cosplay on a tiny intersection.
- Do not “fix collapse” with 20 more recombiners. Interpolation ≠ coverage.
- Do not keep 100 and “rely on CR penalties.” You will detect (badly) and then ship the collapsed set.
- Do not move seats back to Solana/Auth0 because the objects are per-teammate. That is Auditor E’s problem. This audit is coverage.

---

## 3. Quality score (synthesized plan)

**52 / 100**

| What is real | Why it is not enough |
|---|---|
| Cells beat one mega-prompt | Cells are abandonable |
| Firewall (no web, no peers, no mid-wave edits) is correct | Packet still injects one mode |
| Unique modular seed triples | Developed-3 may drop them |
| Specialist bolt tests are the right *filter* | Specialist *search* is n copies of one filter |
| Reallocation table exists | It fires after workshops, or after the cell already ran |
| Pilot + “don’t call a partial run the 100” | Pilot cannot see collapse; drops are biased by wave order |
| Anti-AI + research as orthogonal cohorts | 10% of N for the largest non-sponsor volume |
| Honest “not yet” on launch | The thing they would launch next is still this grid |

This is not a 30: they did not fire 100 copies of “give me 300 ideas.” It is not a 70: the independence claim is false, the mass is inverted (63 sponsor vs 37 open), collapse instrumentation is one-liners, and floors preserve duplicates. A 52 is “right vocabulary, wrong measure, several self-inflicted correlation bugs.”

---

## 4. Launch the 100 yet?

**NO.**

Not because audits are unfinished (they are; that alone is enough under the synthesized file’s own gate). Because **this allocation will not cover idea space if it launches unchanged**.

Launching 100 now would lock in: one-model correlation, abandonable seeds, soft tracks, 12-deep Solana/Auth0/Eleven overlap, Medicly-attractor leakage, one-liner clustering that cannot see it, cohort floors that keep it, and a wave order that deletes research/IFM/Sandia/physical if the runtime blinks.

Fix the bind rules and the table in §2, interleave waves, run a 6-agent same-cohort pilot, apply the capacity gate, *then* launch a labeled population. If the clock forbids that work, launch a **reduced covering** with the same ratios — do not launch the current 100 “because reports are cheap.” Cheap correlated reports are how you spend 90 minutes to search 30 cells and believe you searched 100.

**Do not launch agents from this audit.**
