# Auditor H — Red-Team of the Orchestration

**Scope:** Night-waste in the *search machine*, not in any project idea. No ideas. No agents launched.  
**Read:** `competition_ground_truth.md`, `fable_plan.md`, `astra_plan.md`, `synthesized_plan_v1.md` only.  
**When:** Fri Sep 11, 2026, ~8:42pm EDT. Hacking starts **9:00pm**. Build window after that is **≈19 hours** to Baggage Check (Sat 4:00pm).  
**Job:** Find every way this plan burns the clock: runtime limits, shallow Grok reports, parse failures, human steering, a fake 100, audit theater.

---

## Verdict

| | |
|---|---|
| **Score** | **28 / 100** |
| **Launch 100?** | **NO** |

The synthesized plan kept Fable’s 100-cell religion and Astra’s “don’t launch blind,” then resolved the conflict by adding *more* stages (8-auditor gate, 2-pilot, 20 recombiners, multi-role red team, pairwise 12-persona jury) and forbidding the only honest abort: **do not skip the 100**. That is how a 19-hour build becomes a 16-hour build with a folder of invalid JSON.

Fable already knew the night-killers (§13). Astra already knew the runtime cannot host this population (§9 capacity, §15). Synthesis scheduled both failures and named the result a pipeline.

**28** is not “the document is stupid.” Firewall, bolt test, no loop-1 web, overall ∩ P(any), and “UNKNOWNs reweight, they do not resize the search” are the right instincts. **28** is “as an executable night plan, this will eat the prize it exists to protect.”

---

## Honest clock (the plan will not keep)

Ground truth is not negotiable: **9:00pm start, 4:00pm submit, 3-minute demo, one track.** Workshops occupy humans **9:00–10:00pm (IFM)** and **10:00–10:30pm (Cursor/Grok)**.

What the three plans actually scheduled:

| Plan | Ideation + select done | Honesty |
|---|---|---|
| Fable | Build **10:50pm**, never past **11:15pm** | Already fantasy if 100 fat reports + ~90 tournament agents |
| Astra | **75 min**, **90 min cap**, commit by **10:30pm**; **do not launch 100** if capacity does not fit | The only adult clock |
| Synthesized | “User’s full pipeline” + **20** recombiners + fat red team + pairwise jury; escape = skip build-sim 16–30 and jury 12→8; **do not skip the 100**; **do not launch until 8 auditors + `final_ideation_plan.md`** | Fable’s hard stop deleted; Astra’s capacity veto deleted; a new pre-9:00 gate added |

It is already **~8:42pm**. The synthesized “not yet” list is: 8 audits → `audit_summary.md` → `final_ideation_plan.md` → 10-minute preflight that compiles packet + seeds + prompt + **writes and tests `parse_initial.py`** + 2-agent pilot + one prompt rewrite. That is **not** a 10-minute preflight. That is **9:00–10:00pm of more markdown** while hacking is legal and the IFM workshop is the one live UNKNOWN that actually moves K2 weight.

Then the 100 still has to run. Then the tournament. Fable’s 9:28pm drop deadline is already dead if launch is after 9:00. The 10:50 build start is dead if launch is after 9:20. The 11:15 hard stop plus “do not skip the 100” is a contradiction: the parent will either **slip the build** or **freeze a partial inbox and still say “the 100.”**

---

## Ranked flaws

Ranked by expected minutes stolen from a working core loop, not by cleverness.

### 1. The 100 does not fit the runtime — and the plan forbids admitting it

**Night kill:** You spend 60–180 minutes waiting on a queue, then rank whatever landed, then build late. Or you stop waiting and **fake the 100**.

Astra measured the constraint the others treat as flavor text: this environment exposes **four agent slots including the parent → ≤3 workers**. Conservative generation time:

`T ≈ ceil(97 / c) × t`

Two pilots that each take 6–8 minutes (synthesized developed section is *larger* than Fable’s “≤5k tokens”) at `c = 3` is **~3–4 hours of generation before any tournament**. Fable’s “5 waves × 20” assumes **20 concurrent** Extra-High-Fast jobs. That number is **unverified**. Synthesized preflight step 1 is “confirm the model *launches*” — one process ≠ twenty.

Synthesized then says launch “20 at a time **or whatever the runtime allows**” and, in the same breath, **do not skip the 100** and **never call a partial run “the 100.”** Those three sentences cannot be true together. The parent will pick a lie. The cheap lie is the fake 100: 100 IDs assigned, 20–40 files on disk, floors still force every cohort into the top 50.

Fable’s own drop rule (agent not landed by **9:28pm** is dropped, no rerun) is a **designed fake-100**. Synthesis kept the 100 and lost the 9:28 knife.

**Fix:** After the 2-agent pilot, compute `N = max(0, floor((25 min) / t) × c)` with **measured** `t` and **measured** `c` (a 6-wide probe, not a single launch). If `N < 20`, **do not run a tournament** — humans pick from the pilots plus a 15-minute structured dump. If `20 ≤ N < 100`, launch **N**, label the run `N-of-100`, freeze on time. **Never** pad IDs. Delete “do not skip the 100.”

---

### 2. Tournament mass is a second 100

**Night kill:** Loop 1 “finishes” at 10:20. Then the plan starts another model farm.

Fable already queued ~90 post-100 jobs: 1 cluster + 10 red + 6 recomb + ~30 build-sim + ~30 demo-sim + 12 jury, stuffed into **9:30–10:30**. That is one-minute-per-stage fiction.

Synthesis **increased** the farm:

- Recombination **6 → 20**. Twenty agents × ≤3 hybrids = up to 60 babies, then a cap of **15** new. **45 writes are born to be discarded.**
- Red team on ~30 with **advocate + judge + skeptics + sponsor + red team per idea**. Read as 5 roles × 30 = **150** reviews unless someone writes a staffing sentence that does not exist.
- Jury: **12 personas, pairwise, no casual ties**. Pairwise on 8 is 28 comparisons. Times 12 is **336** ballots, or 12 full rankings produced by pairwise theater. Fable gave this **15 minutes**.

Escape hatch skips build-sim on ranks 16–30 and shrinks jury 12→8. That saves the cheapest slice. It does not save 20 recombiners or a 5-role red team. It does not save parse. It does not save the 100.

**Fix:** After parse+cluster, **zero new agents** unless `t` and `c` still have 15 minutes of slack. Default tournament: scripted Borda on **three** letters (T, D, Rel) + one-liner clusters + **8 cards for humans**. If slack exists: **4** recombiners max, **one** red-teamer per surviving idea, **no** build-sim in the ranking (build-sim is fanfiction; keep it for the winner only). Delete pairwise jury. Delete 20 recombiners.

---

### 3. Fast Grok cannot fill this schema — reports will be shallow *and* unparsable

**Night kill:** 40 minutes of generation produce form-fill. Rankings become a random permutation of 7/10s. Humans either trust the number or ignore the search. Both waste the generation time.

The synthesized loop asks each of 100 fast agents for: 5 obvious-dumps + 15 raw in 3 batches + 3 **full** developed dossiers (identity / product / architecture / sponsor / feasibility / competition / kill-test) + Fable §14 JSON remapped onto a **different** 0–10 letter dictionary.

That is a clerk job. Extra-High-Fast will:

- Echo the banned list as the obvious-dump (not a field estimate).
- Rename the seed triple 15 times and call it batch diversity.
- Emit 0–10 integers with 20-word tautologies (“strong technical core because it is technical”).
- Stuff `p_prize` with 0.20/0.35 because those look “calibrated.”
- Drift between Fable’s 1–5 template, Astra’s 0–4, and the user’s 0–10.
- Break the fence: extra ``` , trailing commas, `R` as Relevance, `B` as “bar” not “bolted-on shamelessness.”

Fable’s mitigation is “strict schema + ≤10 re-runs + self-rank sanity.” Re-runs at 9:30 **are the tournament window**. Ten re-runs of a fast model still produce **shallow valid JSON**. Self-rank 1–3 does not create a technical core. Red team **replaces scores with the same model family** — correlated theater, not independent measurement. Astra said this out loud: *a hundred contexts using one model are not 100 observations.* Synthesis never operationalizes that sentence. Five Borda lists of the same vibes are one list.

**Fix:** One developed idea per agent, **≤15 JSON fields**, scores only U T O D Rel F DR, no `p_prize` from loop 1. JSON-only (Astra was right: do not author Markdown and JSON as two documents). Prompt forbids extra keys. If the pilot’s developed idea is a wrapper, **do not launch**; rewrite once, re-pilot **one** agent, then go. Depth beats 300 blurbs. Distinct winners come from distinct *cells that finish*, not from 3 stubs per cell.

---

### 4. Parser, packet, and letter remap do not exist — and they collide

**Night kill:** 9:35pm, `parse_initial.py` is still being written, or it runs and drops a third of the inbox, or it “succeeds” with `R` meaning two different things and the five rankings are garbage.

Facts:

- `parse_initial.py` is listed as “the only script.” It is **not in the plan as already written or tested**.
- Shared packet is “compiled by copy-paste” in a 10-minute preflight that also does seeds, prompt, pilots, and model check.
- Fable **R = track Relevance**. User/synth **R = Reliability**, relevance = **Rel**. Silent collision “would corrupt rankings” — synthesis *named* this and then said “schema in Fable §14, letters remapped.” That is two contracts, one file, a fast model, and a parser that has never seen Grok output.
- **B** flips meaning: Fable B = bar vs competitors; synth B = bolted-on penalty (10 = shameless). Same letter, inverted utility. Borda will promote bolted sponsors or kill organic ones depending on which dictionary the parent coded.
- Artifact names already disagree: Fable `results/final_decision.md`, Astra `selection/final_selection.md`, synth `FINAL_BRAINSTORM_DECISION.md`. Glue will write one path and the next stage will read another. Minutes die in “where is the file.”

Fable parse window is **5 minutes** (9:30–9:35) including clustering. That is not a window. That is a wish.

**Fix:** Write **one** `metric_dictionary` and **one** schema tonight. Delete Fable §14 as an executable contract; keep it as history. Parser: stdlib, extract last `json` fence, on failure keep the one-liner + track from a regex and mark `parse=degraded` — **do not re-run models**. Test the parser on the two pilots **before** wave 1. One output path: `results/final_decision.md`. If packet + parser + seeds are not ready at **9:10pm**, skip the 100 and pick manually. Do not compile under the tournament clock.

---

### 5. Audit theater is already eating 9:00pm

**Night kill:** The synthesized launch gate is “8 auditors → summary → `final_ideation_plan.md` → preflight → 100.” This file is part of that gate. Eight adversarial memos plus a merge pass is **the first hour of legal hacking**, spent re-planning a plan that already contains two full architectures.

If the merge is real, launch slips to **~10:00pm**, then generation, then tournament → build starts **near midnight**. If the merge is fake, the 8 audits were costume. There is no third option in which eight write-ups are both deep and free.

Fable §13 and Astra §13 already listed clock, rate limits, shallow reports, steering, and incomplete populations. Synthesis copied the tables and added auditors. That is a process that consumes the risk it claims to reduce.

**Fix:** This audit pass **ends at 9:00pm**. One human applies the clock/capacity/schema cuts below. No `final_ideation_plan.md` novel. No second auditor round. If a later auditor wants a new scoring theory, it waits until next year’s postmortem. **Planning after 9:00 is a prize-negative activity** unless it is the 10-minute measured preflight.

---

### 6. Escape hatch is too small; “do not skip the 100” removes the real hatch

**Night kill:** Stage runs 20 minutes late. Parent skips build-sim on ideas 16–30 (ideas that were already going to die) and cuts 4 jurors. The expensive work continues. Build start slips. Nobody is allowed to shrink N.

Fable: if any stage >15 min late, skip those sims, shrink jury; **never slip build past 11:15**. Synthesis kept the small skip and dropped the 11:15 commandment as a hard law (it is only in Fable). The user’s “full pipeline” plus “do not skip the 100” wins every argument against the clock, because the clock is not in the room — the checklist is.

**Fix:** Publish a degrade table the parent **must** execute without discussion:

| Wall clock | Action |
|---|---|
| 9:00 | Preflight starts or is already done |
| 9:10 | Packet/parser/seeds ready or **abort 100** |
| 9:15 | Generation starts at measured N |
| 9:40 | Generation **freezes**. Inbox = whatever parsed |
| 9:50 | Cluster + scripted rank done, or humans read one-liners |
| 10:00 | Humans have ≤8 cards |
| **10:15** | **`final_decision.md` exists. Build starts.** |
| 10:15+ | No more agents. Workshops are optional one-delegate only |

If a stage is late, **cut the next model stage**, not the sleep of the build. Never slip 10:15 for “almost all 100.”

---

### 7. Humans are double-booked — parent is a single point of failure — steering happens anyway

**Night kill:** The only person who can launch waves is also the only person who can notice they died. Everyone else is at TEP 1403. `live_verification.md` is empty at jury time. At 10:30 four people who did not watch the search veto a winner they do not understand, or rubber-stamp a number they did not read. Either the search was pointless or the pick is random.

Fable parks humans at IFM **9–10** and Cursor **10–10:30**, wants `live_verification.md` by **10:15**, and a human pick **10:30–10:50**. Those intervals overlap the entire tournament. Synthesis did not assign a parent who **stays**. Astra’s “one delegate with a narrow verification brief” was the correct staffing; it was not adopted as a named roster.

Firewall says no mid-wave steering and “parent shows nothing until 100 land.” Reality:

- Files appear on disk. Anyone with the repo can read `agents/initial/001.md` during wave 2.
- The **2-agent pilot is the highest-leverage steer** in the whole night: humans read two idea lists and “fix the prompt once.” That fix will be “less like these, more like that.” The other 98 agents inherit it. Synthesis forbids wave-to-wave edits and then schedules a pre-wave edit from live ideas.
- Packet compilation is “copy-paste plus one teammate diffs.” That teammate can “clarify” a sponsor bar toward a preference.
- Final **veto** can throw away 2 hours of search. Fine if the search was real. Expensive if the search was the reason build started at 11:30.

**Fix:** Named roles before 9:00: **Parent (does not leave the machine)**; **Delegate A (IFM, 5 questions, back by 10:05)**; **Delegate B (MLH/Vultr/Sandia/form URL, 15 minutes, not the whole expo)**; **Cursor workshop: skip or Delegate B after 10:05**. Pilot rewrite may change **schema/validation only**, not taste. Humans see **no initial reports** until freeze. Veto window is **10 minutes** (10:05–10:15) on 8 one-page cards, not 20 minutes of committee. Default if humans are missing: parent picks by T/D/Rel + bolt, writes the file, build starts.

`live_verification.md` ships at packet time with **defaults already filled** (K2 unknown → IFM `p=0` unless fallback holds; Vultr unknown → no GPU dependence; Sandia unknown → keep theme, prize conditional). Jury — if it exists — never waits on the workshop.

---

### 8. Ten-minute preflight is a lie that launches a broken machine

**Night kill:** Preflight “passes” because the model said hello. Then 100 agents get a half-written packet, an untested parser, and a seed file with a letter-remap bug. The failure is discovered at 9:40 when parse dies. Now you pay generation *and* a rewrite *and* you are late.

Synthesized preflight list:

1. Confirm model launches  
2. Headcount + hardware one-liner  
3. Compile packet + `seeds.csv` + prompt  
4. 2 pilots; if JSON invalid or wrappers, fix prompt **once**  
5. Launch 100  

Missing: measured `c`, measured `t` at intended width, parser test, packet diff against ground truth, Physical I/O hardware gate, “does 20-wide even start.” Astra’s launch conditions required **throughput**, not a ping. Synthesis cited Astra’s “no until preflight” and then emptied the preflight.

One prompt fix after two wrappers does not prove the 98 will not wrapper. Fast models wrapper **in specialist cells too**; that is why Astra required “≥5 raw that survive deleting the sponsor.” That check is not in the parser.

**Fix:** Preflight is **allowed to fail closed**. Pass criteria: (a) `c` and `t` measured at the intended width (if 20-wide fails, width becomes 3 and N shrinks); (b) parser accepts both pilots; (c) packet contains UNKNOWNs as UNKNOWN, not resolved; (d) inventory recorded; (e) N fits the 9:15–9:40 generation box. Fail any → **no 100**. Two-person pick from a 20-minute human session beats a 100-wide invalid run.

---

### 9. Invented probabilities get multiplied until they look like a decision

**Night kill:** Forty-five minutes of jury/build-sim/demo-sim exist to feed `p_any_adj = p_any × p_ship_core × p_demo_ok`. All three factors are Grok-issued. The parent then treats the product as the objective. Humans defer to the printout. You built the wrong thing with high confidence.

Fable’s `p_any` shortcut is labeled `ponytail:` — a fixed-ρ hack, fine at n=8 **if the p_k are adult**. They are not. Loop-1 buckets are self-scored. Overconfident flag at 0.8 almost never fires if the model sits on 0.35. Build-sim `p_ship_core = clamp(1 − (critical_path/11)², …)` is a curve fit to a **guessed** critical path. Demo-sim `p_demo_ok` is a story.

Astra refused decimal-point forecasts and refused to let initial agents emit prize percentages. Synthesis **kept Fable’s formula as primary P(any) ranking** and added Astra’s scenarios as a “sensitivity column.” Under clock pressure the column will not be read. The fake number will.

Five rankings on 10+ correlated letters do not hedge this. Borda of the same model’s U,T,O,D,M,P,R,J,W,G,Rel is **one** vibes ranking with extra arithmetic. “Top-50 in ≥2 rankings” is not a filter when the rankings move together.

**Fix:** Loop 1 emits **no** `p_prize`. Parent does not compute `p_any` until humans have 8 cards and fill buckets themselves in 3 minutes (or refuse). Build-sim/demo-sim **never** multiply into the rank; they are appendices on the final 2. Kill flags and bolt test stay; they are boolean. If you need a scripted sort: T then D then Rel, minus kill, minus bolted-sponsor claims.

---

### 10. Floors and 20 recombiners launder the allocation into the shortlist

**Night kill:** You reserved 5 IFM + 5 Sandia + 10 STACK cells “to search.” Then you **require** each cohort ≥2 and each track ≥5 in the top 50, and red-team floors keep ≥1 per sponsor “if any survived.” Weak specialist stubs occupy slots that a better open-world idea lost on score. Then 20 recombiners bolt those sponsor mechanisms onto grand-path ideas — the exact Frankenstein both plans warned about — and hybrids get their own sims. Clock gone, stack still bolted.

Fable at least capped hybrids at 15 and required bolt+estimator again. Synthesis kept the cap idea in Fable’s text but changed the agent count to **20** because “the user said 20.” User-pipeline fidelity is not a reason to run 20 concurrent remixers on a 3-wide runtime.

**Fix:** **No cohort floors.** Track floor at most “if a track has zero survivors, keep its single best as a note, not a finalist.” Recombiners: **0** by default; **4** only with slack. A hybrid that adds a sponsor must re-pass bolt in **one** paragraph, not a new 17-hour fanfic schedule.

---

### 11. Estimator disagrees with itself — kill rules will fire at random

**Night kill:** Two “feasible” ideas die or live because the parent used 31.7 vs 26 effective hours. Arguments at 10:40. No build.

Fable: 17.2h window, 3h sleep, 2h demo, 0.65 parallelism → **31.7**. Kill if over.  
Astra: reserve **last 4 hours** (freeze/rehearse/submit), plan as **two effective builders** when unknown.  
Synthesis: **adopt both** Fable taxes **and** Astra’s 4-hour reserve. Capacity becomes `4 × (H − 4 − 3) × 0.65`. For H≈17 that is **~26**, not 31.7. Demo-sim scripts are **90s** in synth, **165s** in Astra, **~180s six-beat** in Fable, **3 minutes official**. Agents will write the wrong show.

Staffing: synthesis assumes 4 and “if 3, edit seeds.” Astra’s default is **2 effective**. A no-show at 10pm does not get a seed edit; it gets a 4-body architecture and a 2-body team.

Physical I/O (4 cells) is not in the preflight reallocation table. Only K2 / Vultr / Sandia / Cursor are. If bags have no cameras, those 4 are dead cells — another fake-100 hole.

**Fix:** One capacity number, written in the packet: **2 effective builders, 4-hour tail reserved, Fable taxes, kill on critical path > 11h to a core loop.** Demo contract: **3 minutes**, 15s slack, one before/after. Reallocate Physical I/O to open-world at preflight if inventory fails. If headcount < 4 at 9:10, do not “edit STACK”; cut STACK and Research-lab first.

---

### 12. Same-model jury / red team / cluster is audit theater with extra steps

**Night kill:** 12 “personas” burn the last 20 minutes before the human pick. Output: a Borda list that matches the context-window order. You could have given humans the 8 cards at 9:50.

Astra: treat the jury as **simulated**, correlated, aggregate by panel, **randomize card order**. Synthesis: 12-persona pairwise, Fable filenames, no randomization stated. First idea in the prompt wins more than “Sandia security engineer” wins.

Clustering on **one-liners only** (Fable/synth) is cheap and wrong. Fast-model one-liners collide on track verbs. Cluster ≥4 → `CR=5` and only the representative advances: a whole mechanism family dies because the wording rhymed. Astra’s fingerprint (job / mechanism / input / loop / proof) was the anti-collapse tool. It was dropped for speed, then the saved minutes were spent on 20 recombiners.

**Fix:** If time exists for one extra model call, use it on **clustering fingerprints**, not on 12 cosplay judges. Humans *are* the jury. Card order randomized by `sort -R`. Red team: **one** pass, search allowed, on the **8** not the 50.

---

### 13. Workshop UNKNOWNs are on the critical path of the *pick*, not just the weights

**Night kill:** You correctly refuse to delay the 100 for K2. Then you put K2/Vultr/Sandia/Cursor answers on the jury’s required reading at 10:15 while the readers are in the workshop. Jury (or humans) pick an IFM-centric finalist on residual hope. 11pm: no endpoint. 11:30: pivot. That pivot was supposed to be the named runner-up; the runner-up’s build-sim was also Grok; you now have 16 hours and a hole.

Ground truth: IFM workshop **may** change K2 integration cost; access is **UNKNOWN**. Synthesis: mandatory Gemini fallback (good) + reweight at jury (good) + humans at the workshop (collides). Fable kill: core depends on UNKNOWN access with no fallback. Fast agents will claim a fallback in a sentence (“use Gemini if K2 missing”) that does not preserve the distinctive demo. Bolt test is not applied to the fallback.

**Fix:** IFM ideas **dead for ranking** unless the fallback **passes bolt as the demo**. Delegate A returns a yes/no by 10:05. If no, `p_ifm = 0` in the packet defaults (already). Do not wait. Cursor workshop does not block 10:15 pick; Cursor is UNKNOWN and stays a free-rider until proven otherwise.

---

### 14. “Obvious-dump + 20 raw” is token tax that buys echo, not coverage

**Night kill:** Fast model’s first 5 ideas are the banned list. The next 15 are the banned list with a twist word. Three developed are the least-banned of those. You paid for 2000 raw lines nobody will read (parent “does not manually read 1,500” — Astra). Parse still has to ingest them. Failures increase with file size.

Fable’s defense: dump is ~100 tokens and estimates the field; 15 real is where seeds appear; 3 developed keeps reports ≤5k. The synthesized developed **section list is longer than Fable’s**, so the 5k cap is already broken. Grep flags (`planner`, `tracker`, `assistant`) will light up half the open-world file and flood red team.

**Fix:** 8 raw, 1 developed, 3-line dump optional. Field estimate = human look around the room at 9:05, not 500 model clichés. Parser greps are **notes**, not a queue that expands red team.

---

## Fake-100 checklist (any one = do not say “we ran 100”)

1. `c × (9:40 − start) / t < 100`  
2. Drop-on-timeout / drop-on-parse without relabeling N  
3. Wave 4–5 never launched (rate limit)  
4. Re-runs counted as “100 cells searched”  
5. Pilots “count toward 100” after the prompt was rewritten from their ideas  
6. Cohort floors stuffing dead cells into the top 50  
7. Preflight reallocations change IDs but the writeup still shows the table above  
8. Same model, same packet, no fingerprint cluster — **≈15 modes, not 100 observations** (Astra §4). Even a complete inbox is not a 100-independent search.

If (8) is the only miss, you may still *use* the inbox. You may not treat consensus as evidence.

---

## Human-steering surface (complete)

| Surface | Why it correlates the search |
|---|---|
| 8-auditor merge into `final_ideation_plan.md` | Taste enters the packet before wave 1 |
| 2-pilot prompt rewrite | Two idea lists become the mode for 98 |
| Disk-readable `agents/initial/` during waves | Procedural firewall only (Astra admitted this) |
| Packet “clarifications” | Sponsor bars get silently stronger/weaker |
| Workshop Slack into the parent mid-wave | Fable forbids showing results; does not forbid the parent *hearing* humans |
| 20-min committee + veto | Search discarded or rubber-stamped |
| Wave-to-wave “just fix the schema” after seeing wave 1 content | Schema edits become content edits |

**Fix:** Parent-only machine until freeze. Packet frozen at launch. Prompt rewrite = schema only, and **re-pilot one**, not “launch 100 on the new taste.” Humans get cards at freeze, not a running commentary.

---

## What both source plans already confessed — and synthesis still scheduled

| Confession | Where | What synth did |
|---|---|---|
| Ideation overrun → 1am build | Fable §13 | Bigger tournament, weaker hard stop |
| Fast model shallow/malformed | Fable §13 | Fatter schema, 0–10, same re-run myth |
| Rate limits, wave 3 never lands | Fable §13 | “Whatever the runtime allows” + do not skip 100 |
| 4 slots, 100 will not fit | Astra §9, §15 | Launch 100 after a ping |
| Same-model agreement ≠ evidence | Astra §4 | 12-persona pairwise jury |
| Do not call a partial run the 100 | Astra §13 | Same sentence **and** “do not skip the 100” |
| Workshop fragments the team | Astra §13 | Still send the team to two workshops |
| Rubric administration > reasoning | Astra §13 | More letters, more rankings, more sims |
| Build-sim ≠ prototype | Astra §13 | `p_any_adj` multiplies it in anyway |

The failure tables are not mitigations. They are a prophecy the schedule fulfills.

---

## Fixes (minimum set — do these or do not run agents)

1. **Hard commit 10:15pm.** `final_decision.md` or it is a process failure. Build starts.  
2. **Measure `c` and `t`. Set N. Label N.** No 100-fiction.  
3. **One schema, 0–10, Rel ≠ R, B = bolted-on only, JSON-only, ≤15 fields, 1 developed idea.**  
4. **Parser exists and has eaten the pilots. Zero model re-runs after 9:15.** Degraded parse keeps one-liners.  
5. **Degrade table in §6 is law.** Cut model stages, not the build.  
6. **Named parent stays. One IFM delegate. Cursor workshop is optional.** Defaults in `live_verification.md` at t=0.  
7. **No 20 recombiners. No 12-persona pairwise. No `p_any_adj`.** Humans rank ≤8 cards.  
8. **Audit theater stops at 9:00.** One human applies this list. No second plan novel.  
9. **Pilot rewrite = validation only.** If pilots are wrappers after one fix, **abort the farm.**  
10. **No cohort floors. Physical I/O dies if bags are empty.** STACK dies first if headcount < 4.

That is a search. The synthesized file is a **search-shaped delay**.

---

## Score (why 28, not 50, not 10)

| Criterion | /100 | Why |
|---|---:|---|
| Clock honesty | 10 | Deleted Fable’s 11:15 law; rejected Astra’s 90-min cap |
| Runtime honesty | 8 | Astra’s slot math ignored; preflight is a ping |
| Anti-shallow-Grok | 25 | Knew the failure; shipped a fatter form |
| Parse / glue readiness | 15 | Script unwritten; three schemas; three output paths |
| Anti-fake-100 | 12 | “Do not skip the 100” + drop rules + floors |
| Human / workshop design | 30 | Firewall text is good; roster is not |
| Kill / bolt / no-web instincts | 75 | These parts should survive the rewrite |
| Self-awareness | 55 | §13 tables exist; the schedule contradicts them |

**Weighted toward night-waste (clock, runtime, fake 100, theater): 28.**

A 50 would require a measured N, a 10:15 hard stop, and a schema a fast model can finish. A 70 would require the parser to already exist and a named parent who is not in a workshop. This file is not that plan.

---

## Launch 100? **NO**

Not “no search tonight.” **No to this 100, on this schema, on this tournament, behind this audit gate.**

Launch is allowed only if **all** of these are true (they are not, at 8:42pm):

- 9:00 has arrived (rules).  
- Packet, one schema, parser, seeds exist and the parser has passed 2 pilots.  
- Measured `c`,`t` imply **N complete reports by 9:40**.  
- N is the number you will print. If N=100, fine. If N=24, you launch 24.  
- Tournament is the degrade table, not 20+12+build-sim ranking.  
- Parent is seated. Humans are not the runtime.  
- Commit file at **10:15**.

Until then, the 100 is a way to feel busy until the real work is late.

**Launch 100? NO.**
