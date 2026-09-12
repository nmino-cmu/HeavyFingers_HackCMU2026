# Auditor D — Feasibility

**Question:** Does this architecture systematically reject projects that four people cannot build and demo in ~19h (Fri 9:00pm → Sat 4:00pm Baggage Check, then a 3-minute stage demo)?

**Answer:** No. It systematically *describes* rejection. It does not systematically *do* it.

It will catch cartoon infeasibility (no hardware in the bag, paid API, “we’ll find a dataset,” delete-the-LLM-and-nothing-remains). It will not catch the projects that actually burn a hackathon: underestimated hard cores, two load-bearing sponsor integrations, a pick that happens after midnight with an estimator still assuming a 10:50pm start, and a live demo whose only survival plan is a cached clip.

---

## Score: 41 / 100

**Launch 100? NO**

| Band | Meaning |
|---|---|
| 80–100 | Clock, capacity, and kills are mechanical, conservative, and bind the final pick |
| 60–79 | Honest 2-builder schedule + independent hour audit; residual gaming |
| 40–59 | Checklist theater: self-scored kills, optimistic capacity, pipeline uncapped |
| 0–39 | Ambition cohorts with no real filter |

41 is not “they forgot feasibility.” Fable §0/§7/§12 and Astra §7/§9/§12 are real apparatus. Synthesis then **loosened the clock, dropped the ship-probability coupling, remapped the build-blocker letter, kept ambition floors, and expanded the tournament.** The dangerous set gets through.

---

## Ground-truth budget (the only clock that matters)

From `competition_ground_truth.md`, VERIFIED:

- Build window: Fri 9:00pm → Sat 4:00pm ≈ **19 hours**, then showcase to 6:30pm.
- Team ≤ 4. From scratch. No building or **designing** the project before 9:00pm. Brainstorm/teams beforehand OK.
- Submit Google Form (URL **UNKNOWN**) + Devpost by 4:00pm. **3 min** talk+demo. Three judge rooms.
- IFM workshop Fri 9–10pm; Cursor/Grok Fri 10–10:30pm. Those hours are not four-person build hours.
- Search instruction in the same file: do not self-censor to beginner CRUD. That instruction is load-bearing: it is why Research-lab / Physical I/O / “training during the hackathon” exist, and why the filter has to be stricter than vibes.

Fable already spends 1h50m of the 19h on ideation and starts build at 10:50pm (**~17h** left), never later than 11:15pm. Astra caps commitment at **10:30pm** and will not launch 100 if measured throughput cannot fit. Synthesized v1 **runs the full user pipeline**, calls Fable’s tournament “too shallow,” forbids calling a partial run “the 100,” and **does not skip the 100**. That is a feasibility decision, and it is the wrong one.

---

## Ranked flaws

Ranked by how many impossible (or un-demoable) projects survive, or how many build hours the pipeline itself destroys.

### 1. The pipeline is uncapped and is allowed to eat the prize

**Where:** Synth “Disagreements / Pipeline duration,” “Tournament,” “Would we launch”; Fable §0 vs Astra §9 clock/capacity.

Synthesized v1 resolves the clock debate by taking the **longer** search: full user pipeline, **20** recombination agents (Fable had 6), richer red team, 12-persona pairwise jury, plus an 8-auditor pass + `final_ideation_plan.md` + 10-minute preflight + 2 pilots **before** the 100. Escape hatch: skip build-sim on ranks 16–30 and shrink jury to 8. Explicit: **do not skip the 100.** Fable’s “never slip 10:50 past 11:15” is **gone**. Astra’s “latest commitment 10:30; do not launch 100 under the fiction that it fits” is **gone**.

Loop 1 after 9:00pm is legal brainstorming, but every minute is subtracted from the 19h. Developed dossiers with architecture/components/demo scripts are **design**. After 9:00pm they are on the clock; before 9:00pm they are a rules problem. The plan treats 300 designed concepts as free.

Fable’s own tournament schedule is already fiction: 100 full reports by 9:30, then parse, then 10 red-teamers, then **6 recomb + 30 build-sims + 30 demo-sims in 25 minutes**, then 12 jurors. Astra’s capacity note (coordinator + ~3 worker slots in the native runtime) makes 100×deep-report in 30–75 minutes a fantasy unless a separately verified wide runtime exists. Synthesized says “waves of 20 or whatever the runtime allows” and then **still forbids aborting the 100**.

If loop 1 takes 2–5h (the plausible band), commit is midnight–2am. Remaining feature time is ~10–12h before Astra’s last-4h reserve, not 17h. The estimator and the 11h critical-path kill still assume the 10:50pm world. **The search procedure is itself an infeasible project.**

**Fix:** Hard `T_commit ≤ 22:30`. If loop-1 files are not sealed by 21:50, freeze the completed set, pick from primaries in 15 minutes, start build. Never finish the 100 after 22:00. Pilot must measure `t` and concurrency `c` and refuse 100 unless `ceil(100/c)*t + tournament ≤ 90 min`. Cut recombination to ≤6 agents, not 20. If the clock dies, drop recombination and jury personas **before** dropping build-sim on anything that can be a finalist. Record coverage; do not call a partial run the 100.

---

### 2. Capacity math is optimistic and internally inconsistent (~20–40% too loose)

**Where:** Fable §12 (31.7 effective PH); Astra §12 (2 effective builders, last 4h, PERT, resource-constrained); Synth “Scope estimator.”

Fable:

- Window 10:50pm→4:00pm = 17.2h
- Minus 3h sleep and **2h** demo prep → 12.2h × 4 × 0.65 = **31.7**
- Kill if taxed person-hours exceed 31.7 unless a named cut saves it

Astra:

- Reserve **Saturday noon–4:00pm** (feature freeze, rehearsal, submit, contingency)
- When staffing is unknown, plan **two effective builders**
- Do not treat 4 names as 76 engineer-hours
- Resource-constrained schedule (one person’s attention), not a sum of `h_i`

Synthesized **adopts both**: Fable’s ×1.8 / +integration / +unknown **vs 31.7**, and Astra’s last 4 hours, then writes `4 × (H − 4 polish − 3 sleep) × 0.65`.

That formula does not yield 31.7:

| H | Meaning | 4 × (H−7) × 0.65 |
|---|---|---|
| 19.0 | 9:00pm→4:00pm | 31.2 |
| 17.2 | Fable 10:50 start | **26.5** |
| 15.0 | Commit ~midnight | 20.8 |

They kept the **kill threshold from the generous story** and the **reserve from the honest story**. Workshops (1–2 people, 9:00–10:30) are not subtracted. Sleep test in Fable §7.1 says “4 × 14 usable hours”; the estimator uses 12.2 — the sleep test is the weaker one and is **not even in the synthesized kill list**.

Four named people ≠ four parallel engineers. One serial technical core plus three people blocked on it is the default hackathon shape. 0.65 on four people still prices that as ~2.6 full-time equivalents after sleep/polish. Astra’s two-builder default is the one that matches a workshop-split, tired, from-scratch team.

**Fix:** One published capacity, computed at commit time:

`capacity = N_eff × (H − 4 polish − sleep_hours − workshop_hours) × 0.60`

`N_eff = 2` unless inventory names four people who can each own a workstream on the critical path (not “we have four laptops”). Recalc `H` from actual `T_commit`. Kill if post-cut person-hours exceed that number. Delete the naked “31.7” constant.

---

### 3. Every number that triggers a kill is written by the agent who wants the idea to live

**Where:** Fable §7.5, §12, §14 validator; Synth “Kill / bolt / demo tests,” agent loop step 4–5.

Kill inputs are all self-reported: `critical_path_hours`, `total_person_hours`, `data_source_1h`, `hardware_needed`, `unknown_tech`, `live_deps` + mitigations, per-sponsor `Q`, `kill_flags`. Validator rule: `kill_flags` nonempty **iff** a §7.5 rule fires — the agent is the rule. Parse greps banned tokens and **flags, does not kill**. Red team re-runs wrapper/bolt, not a unit-cost rebuild of the hour model. Independent re-estimate is build-sim, which is late, scheduled impossibly tight in Fable, and **skippable** in the synthesized escape hatch.

Named scope cut that “brings it under” is a free action. Every ambitious idea will include one.

**Fix:** `parse_initial.py` mechanical kills, ignoring `kill_flags` text:

- `critical_path_hours > min(11, hours_until_Sat_10am)`
- `total_person_hours > capacity` after applying only cuts listed as `required_for_minimum = false`
- `hardware_needed` not ⊆ `team_inventory.json`
- any `paid` / non-free external service
- empty or “TBD/find/scrape later” `data_source_1h`
- `unknown_tech` on a component that is on the critical path **and** not in the skill inventory, unless a 45-minute falsification exists

Agent `h_i` is advisory. Parent (or one build-skeptic) recomputes hours from a **published unit-cost table** on component class + unknown flag. No idea enters the top 8 without that recompute.

---

### 4. Synthesis dropped Fable’s only real coupling of “can we ship?” to “should we pick it?”

**Where:** Fable §9.3 `p_any_adj = p_any × p_ship_core × p_demo_ok`; Synth scoring / P(any).

Fable’s useful move: after build-sim and demo-sim, prize probability is multiplied by ship and demo survival. An elegant infeasible idea gets crushed even if `p_prize` buckets are drunk.

Synthesized keeps Fable’s correlation formula on self-bucketed `{0,.02,.05,.10,.20,.35,.50}` and Astra’s field-size sensitivity. It does **not** restore `p_any_adj`. Build-sim is listed as a stage (~15 ideas) with no effect on the ranking that final pick uses.

Final pick in synth: overall-win gate **and** top-tier P(any), human veto, one backup. Overall ranking is `U T O D M P R J W G Rel` — **no F, no S, no estimator**. Astra’s “complete useful minimum that fits the schedule” is not restated as part of that gate (the disagreement table uses “overall-win gate” to mean “not a sniper-only winner”).

So the ranking the plan **requires** the winner to be high on is the ranking that **ignores feasibility**. High-T research-shaped ideas are favored twice (overall + upside) and only die if their author confesses.

**Fix:** Restore `p_any_adj`. No top-8 seat without build-sim + demo-sim. Overall-win gate must include `F` at least 6/10 **and** “stressed 2-builder schedule reaches a useful integrated minimum before Saturday noon.” Put `F` and `S` in the overall ranking.

---

### 5. Floors and ambition cohorts re-inject the exact projects the kills exist to stop

**Where:** Ground truth search constraints; Fable §1.1 RESEARCH-LAB / PHYSICAL I/O / VULTR “training-during-the-hackathon” / IFM LoRA / STACK; Astra “do not kill ambitious work merely because it is ambitious”; Synth allocation + “floors: each track ≥5, each cohort ≥2.”

The filter is asked to be harsh while the search is asked to generate:

- Research-lab: SLAM, CRDT, custom DSL/compiler, differentiable X, novel solver
- Physical I/O: camera/mic → spatial/realtime/3D, three rooms, no purchased hardware
- Vultr: visible GPU/job, including training during the event (Fable; synth still says visible compute/GPU/job)
- IFM: K2 load-bearing, including fine-tune/LoRA in Fable’s hard constraint
- STACK: **two** sponsors that both pass the bolt test (i.e. both load-bearing)

Astra says hard gates cannot be kept to satisfy a quota. Synthesized says “Astra’s no filler if short” in a header and then **writes cohort/track floors** on the 300→50 cut. Red-team failure mode in Fable is “kills everything → floors keep 30.” Floors fight kills.

Unknown-tech tax is **+3h** per new technique. That is not a tax; it is a permission slip. `h_i` is “hours for one strong dev **with Cursor** to demo quality,” then ×1.8. First-time Solana program, first-time LoRA, first-time SLAM-class work, overnight training — all can clear 31.7 and 11h on paper.

**Fix:** Bind Astra’s sentence to the floor line: a hard kill **cannot** occupy a floor seat. Technique floors before tax (examples, not ideas): first-time on-chain program ≥6h; training/fine-tune on the critical path → **kill** (off-path toy job only); SLAM/custom compiler/novel solver on the critical path → kill unless the 45-minute falsification already passed. STACK: one load-bearing integration by default; a second only if incremental work ≤45 minutes, not on the critical path, no new unverified dependency (Astra §3). Q hours **add** into `total_person_hours` in the parser, not as a separate vibe score.

---

### 6. The 11h / Saturday-10am kill does not track remaining time

**Where:** Fable §7.1, §12; Synth kill bullet “critical path > 11h.”

Saturday 10:00am is 13h after 9:00pm and ~11h after 10:50pm. The constant 11h **is** that second number. If commit is 1:00am, Saturday 10:00am is 9h away; an 11h critical path still “passes” and the 10am checkpoint is already a failed milestone.

Synthesized kill list is the 11h constant only. It does not say “recompute against remaining time.” Fable’s Saturday-10am test is not restated. Astra’s “more critical-path time than the **remaining** build budget” was the correct rule and was not the one copied.

**Fix:** `cp_kill = min(11h, t(Sat 10:00) − T_commit)`. Recompute at parse, at red team, and at commit. If commit slips, previously “feasible” ideas die without a meeting.

---

### 7. Letter remap deleted build-blocker from the risk ranking

**Where:** Fable §5.1 `BR` = tech nobody on the team has shipped (`+3h`, `p_ship_core −0.1`); Synth risks: `BR` = **boring**. Also Fable `H` = stack count vs synth `H` = team advantage.

Risk-adjusted ranking is one of five. After remap it no longer punishes “nobody here has touched this.” The unknown-tech boolean can still feed the estimator **if agents set it**. They will not.

Fable `DR` was live-demo failure; synth `DR` is still “demo,” luckily. Eligibility risk (`ER`) and track-ambiguity (`AR`) also vanished into “explanation” and “already-exists.” Those are other auditors’ problems except where eligibility UNKNOWN becomes a build (K2, Vultr credits, Sandia gate). Synth allocation has fallbacks; synth **kills** do not include Fable’s “core depends on UNKNOWN access with no fallback.”

**Fix:** Keep the user rubric letters if required, but add `BB` (build-blocker) back into risk-adjusted. Restore UNKNOWN-without-fallback as a kill (IFM already requires a Gemini fallback that **keeps the demo** — enforce it in the parser: missing fallback → kill). Vultr ideas that need an unredeemed GPU credit are UNKNOWN-without-fallback until preflight says otherwise.

---

### 8. Demo survival is a named-mitigation form, not a filter; synth demo-sim is 90s

**Where:** Fable §7.4, §12 `p_demo_fail`; Astra §7 demo + “cached cannot prove live”; Synth “demo-sim 90s scripts,” “survive 20s stall and reset ≤60s.”

Official demo is **3 minutes**, three rooms, then expo. Fable six-beat script is ~3 minutes. Astra targets 165s with margin. Synthesized tournament says **90s scripts**. That under-tests talk+demo and under-tests setup/reset across rooms.

`p_demo_fail > 0.35` kills unless a mitigation brings it under. A named mitigation **halves** each `p_i`. Cached result / pre-warmed state / recorded clip are always available as text. Independent-event `Π(1−p_i)` is already marked `ponytail:`. Result: almost nothing dies on demo math.

Physical I/O and camera/mic get `p_i = 0.10` for capture in a **new** room. Three rooms. Setup time is not on the critical path. Expo is a fourth environment. Hardware-in-bags is necessary, not sufficient.

Astra’s honest rule: fallback may preserve explanation; cached/recorded output **cannot** prove live sponsor use. Synthesized does not make that a kill.

**Fix:** Demo-sim is 180 seconds, plus a 60-second reset, plus a 3-room setup line on the critical path for any second device / camera / mic / physical output. Mitigations that are cached or recorded **do not** reduce `p_i` for any prize that needs a live trace. `p_demo_fail` computed by the parent from a fixed table, not from agent-supplied `p_fail`. Restore Fable’s “>2 live humans, no bot fallback → kill.”

---

### 9. Synthesized kill list is a subset, and the missing rows are the 2am rows

**Where:** Fable §7.5; Astra §7 kill; Synth “keep both plans” then seven bullets.

Operational synth kills: bolt; wrapper; CP>11h; data 1h; hardware in bags; paid API; 20s stall + 60s reset; banned-list union.

Dropped from the **operational** list even if “keep both” is wished into existence:

| Missing kill | Why it matters tonight |
|---|---|
| Sleep / 2-builder stress | 31.7 assumes four usable bodies |
| >2 live humans, no bots | Multiplayer / audience-in-the-loop dies on stage |
| UNKNOWN core, no fallback | K2 / Vultr / Sandia / Cursor-bar |
| From-scratch / no private prebuilt | Rules, not just taste |
| Marketplace / external cooperation during the event | Banned table helps; not a numeric kill |
| Hidden human presented as automation | Will be used to fake “core loop by Sat 10am” |
| Cached output claimed as live | Sponsor + demo judges |
| >1 unresolved research breakthrough | Research-lab’s entire purpose |
| Cannot explain core inside the 3-minute budget | High-T sludge |
| Remaining-budget CP (not constant 11h) | See flaw 6 |
| Unconfirmed funding | Vultr $100 is from a coach, not a promise |

“Keep both” without a merged, parser-enforced list means agents implement the short list.

**Fix:** One kill table in `shared_packet.md`, copied into the validator. Union of Fable §7.5 + Astra §7 + the rows above. Short list in v1 is not the spec.

---

### 10. Preflight does not test the thing this auditor cares about

**Where:** Synth “Preflight”; Astra §9 capacity check / 45-minute post-selection gate.

Preflight: model slug launches, headcount one-liner, compile packet, 2 pilots, rewrite prompt once if JSON is junk or ideas are wrappers. That tests **format and wrapper-taste**, not hour honesty, not tournament duration, not 2-builder schedules.

If headcount is 3, parent “edits seeds.” Allocation changes; **31.7 and F do not automatically change** unless someone remembers Fable §6.2 (“F scores re-weighted”). Inventory is optional in practice: Fable will launch without it and reweight later; synth records it in 10 minutes if someone is not at the IFM workshop.

Astra’s selection+45-minute falsification of the highest-risk dependency is the best feasibility control in any of the three plans. Synthesized tournament does not include it. Backup “switch trigger” without a 45-minute test is a paragraph, not a gate.

**Fix:** Pilot 2 is not done until one developed idea is run through the **parent** estimator + 2-builder stress and a human says “this hour model is not fanfic.” After pick: 45-minute dependency test with keep / rescope / switch. No parallel second project.

---

### 11. Recombination (especially ×20) is a scope-growth engine

**Where:** Fable §9.3 hybrids; Astra §9 50→30 (≤12 challengers, ≤8 recomb, must delete from each parent); Synth 20 recombination agents.

Hybrids exist to bolt a sponsor mechanism onto a grand-path idea. They must “re-pass” bolt + estimator — the same gamed estimator. Twenty agents produce up to a pile of new candidates (Fable capped hybrids at 15 and pool ≤45; synth does not restate a hard cap). Glue time is the work that blows 2am. Fable failure table already names chimeras; synthesis **increased** chimera production.

**Fix:** ≤6 recombination agents, ≤8 hybrids, each hybrid’s critical path = **worse parent + 2h glue** (parent-computed). If that exceeds `cp_kill`, the hybrid is dead. Combining two sponsor stacks is not a candidate (Astra).

---

### 12. Integration tax and sponsor `Q` are not the same ledger

**Where:** Fable §3.2 (~2h per extra load-bearing integration, `Q≤2h` or primary); §12 (+1h first external, +2h each additional); Synth STACK + bolt.

A STACK idea with two bolted-test-passing sponsors is two load-bearing integrations. Estimator may count them as two “external services” (+1+2=3h) while the policy text says ~2h **each**. `Q` is a 1–5 (Fable) or 0–10 (synth) score, not added to `total_person_hours` by the parser. Agents can set `Q` “cheap” and `external_services` short.

ElevenLabs character budgets, Gemini free-tier quotas, Solana faucet/RPC, Auth0 tenant, Atlas M0, Vultr code-from-coach are **credit/quota** problems, not only paid/free. Paid-API kill is binary. Rehearsal can exhaust a free voice quota before Saturday 4pm. Not modeled.

**Fix:** Parser adds `max(policy_hours, Q_hours, unit_table_hours)` per external service into PH. Quota-sensitive services require a rehearsal budget line; if unbudgeted, `API` risk maxes and the idea cannot sit in top 8. Vultr without a redeemed code: compute-on-laptop fallback or kill.

---

## What already works (why this is 41, not 25)

- Hardware-in-bags, paid-API, 1h data, wrapper, and banned-list **ideas** are written down and will kill the dumbest class if anyone enforces them.
- Bolt test is the right sponsor-feasibility test (delete → cheapest substitute → does the 3-minute change?).
- Fable’s numeric estimator + Saturday-10am / 11h idea is the right *shape*.
- Astra’s last 4 hours, 2-builder default, PERT+stress, 45-minute falsification, capacity check, “hard gate beats quota,” and “do not launch 100 if it cannot finish” are the right *honesty*.
- Mandatory K2→Gemini fallback that keeps the demo is correct (access is UNKNOWN).
- Backup with a named switch trigger is correct **if** a 45-minute test exists.
- Workshop-parallel verification (Fable §6.2) is the right split **if** the parent is not also the only person who can launch waves.

None of that is systematic rejection until the parent owns the clock and the arithmetic.

---

## Fixes (do these before any 100)

1. **Hard clock:** `T_commit ≤ 22:30`. Abort the 100 rather than the build. Measure `c` and `t` in preflight; refuse 100 if the inequality fails.
2. **One capacity number** at commit: 2 effective builders default; `H` from commit; minus 4h polish, sleep, workshops; ×0.60. Delete 31.7.
3. **Mechanical kills** in `parse_initial.py` from inventory + unit-cost table + remaining-time CP. `kill_flags` is diagnostic, not authority.
4. **Restore `p_any_adj`.** No top-8 without parent build-sim + 180s demo-sim.
5. **Overall-win gate includes schedule fit** (`F`, stressed 2-builder min-version before noon). Overall ranking includes `F` and `S`.
6. **Floors cannot override hard kills.** Training/fine-tune and first-time “research-lab core” on the critical path die unless the 45-minute falsification already passed.
7. **`cp_kill = min(11h, Sat 10:00 − T_commit)`**, recomputed when commit moves.
8. **Restore build-blocker** (`BB`) in risk-adjusted. UNKNOWN-without-fallback is a kill.
9. **Demo math owned by parent.** Cached/recorded does not prove live use and does not halve those `p_i`. Physical second-device setup is on the CP. Restore live-human kill.
10. **Merged kill table** in the packet = Fable 7.5 ∪ Astra §7 ∪ the missing 2am rows. “Keep both” is not a spec.
11. **Pilot tests the estimator**, not only JSON. Post-pick 45-minute dependency test with keep/rescope/switch.
12. **Recombination ≤6**, hybrids inherit worse-parent CP + 2h glue, hard cap on new candidates.
13. **Q/integration hours add in the parser.** Quota budget required. Unredeemed Vultr/K2 ≠ full-weight feasibility.
14. **Inventory before launch** or force 2-builder + no GPU + phones-only. Headcount 3 changes capacity, not just seeds.
15. **Sleep test is a kill**, not a paragraph: 3h sleep floor each; if the plan only works with four all-nighters, it is already over scope.

---

## Launch 100? NO

Not because idea search is illegal after 9:00pm. Because **this** 100 + this tournament + this estimator is an infeasible use of the 19h, and the filter at the far end will promote the impressive-unshippable set.

Launch a 100 only after:

- preflight proves the 90-minute inequality,
- mechanical kills and parent unit-costs exist,
- `p_any_adj` and schedule-fit are back in the pick rule,
- capacity is the 2-builder remaining-time number,
- `T_commit` is a hard abort.

Until then, a 2-agent pilot plus a human pick from a short, estimator-audited list wastes less of Saturday than a theatrical 100.

**Launch 100? NO**
