# Auditor F — Demo Auditor

**Question:** Does scoring sufficiently reward an immediate visual/interactive holy-shit moment in 3 minutes, vs research-paper ideas that need a lecture?

**Answer:** **No.** The plans *name* wow, memorability, killer-demo density, and a 3-minute clock. They then **average those names to death**, give research-lab a dedicated escape ranking, and never kill “needs a lecture.” Official Demo Quality is “clear, understandable, under 3 minutes” (ground truth). That is comprehension, not spectacle. Our extra letters (`W`, `M`, `K`) were supposed to close that gap. They do not, because they are not gates.

Adversarial. No project ideas. Agents not launched.

---

## Score: **45 / 100**

Vocabulary of a demo-first search. Aggregation of a paper-review committee.

Enough machinery exists that a lucky wow can survive. Nothing *forces* the winner to be one. A CRDT/DSL/solver writeup with a slide of math and a one-sentence core will outrank a 20-second interactive transform whenever `T`/`O`/`G` are high and `D` is “clear enough.” That is the failure mode that loses 3-room judging to the team whose screen *does something* before the judge sits down.

---

## Launch 100? **NO**

Do not launch until the fixes below are in `final_ideation_plan.md` and the shared packet. Launching now burns 100 cells on a rubric that will promote lecture-tech into the top 50 via the Upside ranking and cohort floors, then ask a professor-heavy jury to pick among survivors that already selected for “a CS prof would respect.”

---

## Ranked flaws

### 1. `K` (killer-demo density) is scored and discarded

Synthesized letters invent `K` = killer-demo density — the only strategic letter that is *about* stage compression. It appears in **zero** of the five parent rankings.

- Overall-winner: `U T O D M P R J W G Rel`
- Upside: `T O G W N`
- P(any), sponsor-sniper, risk-adjusted: no `K`

So the one number that was supposed to punish “brilliant, please sit for a seminar” is a JSON ornament. Agents will still emit it. The tournament will not read it. This is the single most embarrassing demo bug in v1.

### 2. No demo gate. Research has two.

Synthesized final pick: overall-win gate **and** top-tier P(any). The inherited Astra gate is `U,T,O,D` each “strong” and **at least one of `T`, `O`, or `D` exceptional**.

Consequences:

- A lecture with exceptional `T` **satisfies the overall-win gate** with ordinary `D`.
- A 30-second holy-shit with middling `T` **fails** that same gate.
- There is **no** `D` floor, **no** `W` floor, **no** `K` floor, **no** “visible transform in the first 30s” kill.

Fable’s human pick is worse: `p_any ≥ 0.5`, `G ≥ 3`, then EV, then `Y`. Demo letters are not in the pick rule at all.

Ground truth: 3 minutes, 3 rooms, Demo Quality is an official axis equal to Technical Difficulty. A pick rule that can crown `G=4, D=3, W=2` is not optimizing the event you are entering.

### 3. Upside ranking is a research-paper on-ramp

`top-10 in any one ranking` (Fable, kept in spirit by “user’s full pipeline”) plus Upside = `T O G W N` means a paper-core idea that is merely *fine* on wow still **auto-advances** if it ranks on technical ambition.

`W` is 1 of 5 letters there. `D`, `M`, `J`, `K` are absent. There is **no symmetric Stage ranking** (`D W M J K`). Lecture-tech has a VIP door. Spectacle does not.

Cohort floors compound it: each cohort keeps ≥2 into the top 50. Research-lab is **guaranteed two seats** even if every entry is a chalkboard. Demo-first also gets two — then equal-weight Borda and the Upside door let the chalkboard overtake them.

### 4. Equal-weight overall Borda treats “wow” as 1/11th of winning

v1 overall: eleven letters, equal Borda. Demo-adjacent: `D M J W` (4). Lecture-adjacent: `T O G` (3). That looks almost fair until you notice:

- Official `D` (ground truth gloss) scores **clarity and time-fit**, not a holy-shit moment. A well-narrated paper demo is `D=8`.
- `J` is “one-sentence core” / comprehension. Papers can have a crisp sentence and still need two minutes of setup to *see* anything.
- `W` is a 0–10 with a ≤20-word justification and **no operational test**. Inflated by construction.
- `T` and `O` and `G` also dominate Upside. Research double-dips; wow does not.

Net: a research idea can be mid-pack on the only letters that measure the 3-minute *feeling* and still win Overall + Upside + the gate.

### 5. The 6-beat script is a TED talk, not a demo

Fable §7.4 (schema still used by v1): hook 15s, before 30s, transform 60s, **technical core 20s**, **sponsor moment(s) 30s**, close+track 25s.

That is **60s of visible change and 120s of narration**. The schema *requires* a lecture beat and a sponsor beat. Agents who write a 90-second interactive loop with no seminar will look “incomplete” against the contract.

v1 then says demo-sim is **90s scripts**. Official slot is **3 minutes**. A 90s wow plus 90s of unexplained leftover time is how you ship a research talk with a gif in the middle. The sim never scores minutes 1:30–3:00, which is where lectures go to die in room 3.

Astra’s 165s split (70s live interaction) is better and was not adopted as the contract.

### 6. “Wow exists” is not a test

Fable `W` = “wow moment exists.” v1 `W` = wow, `M` = memorability. Neither plan requires:

- timestamp of first *visible or interactive* state change
- whether a stranger understands the change **without the spoken sentence**
- whether the judge’s hands or phone do something (vs watching a slide)
- a cold-start in a new room (ground truth: 3 rooms + expo)

Missing before/after in Fable only caps `D ≤ 2`. That is not a kill. v1’s explicit kill list **drops even that cap**. “Keep both plans” is not an operational rule. The listed kills are wrapper/bolt/hardware/data/11h/API/stall/reset. **“Needs a lecture to land” is legal.**

Astra *does* kill “cannot explain the core contribution within the demo budget” and “impressive model with no usable loop.” v1 cites “keep both” and then omits those kills from the bullet list the parent will actually implement.

### 7. Jury composition will vote for the paper

Fable’s 12 personas: CMU CS professor; HRT quant who hates wrappers; Jane Street–style systems engineer; skeptical senior who has seen 200 demos; Sandia engineer; plus sponsor specialists. That is a **faculty seminar** with two design/audience seats (product designer, beginner student).

Borda over that room **averages toward respected difficulty**. The beginner’s “I felt it in 20 seconds” is 1/12th.

Astra’s 3+3+3+3 panels (merit / demonstration / execution / prize) are more balanced. v1 says “12-persona jury, pairwise” and Fable filenames — it does **not** adopt Astra’s demonstration panel or panel-then-compare aggregation. Pairwise among professor-shaped personas still elects the lecture.

People’s Favorite and Best Design are the official spectacle prizes. Fable EV weights them **2 and 1** — the floor of the table. P(any) will not steer toward them. Demo-first is told to hunt them; the pick rule will discard that hunt.

### 8. Demo-sim is late, optional, and disconnected from `p_any`

Fable’s only numerical demo teeth are `p_demo_ok` and `p_any_adj = p_any × p_ship_core × p_demo_ok` at **round 3** (30→15→8). By then lecture ideas have already used Upside + equal Borda + cohort floors to occupy the pool.

v1 lists demo-sim as a stage toward 8 battle cards and **does not restate the `p_any_adj` multiply**. If the parent implements the v1 tournament literally, demo-sim is prose for the jury, not a rank input.

Clock escape hatch: skip build-sim on ranks 16–30. Demo-sim is not protected. If the night slips, the one remaining demo instrument is the first to get thin.

### 9. Search allocation hunts respect, not stage

| Cohort | n | Demo posture |
|---|---:|---|
| Open-world | 18 | “Visible before/after” — good, still not timed |
| Research-lab | 5 | “Hard core a systems/ML person respects; still demoable” |
| Demo-first | 5 | “30s wow, then product. **Substance required.**” |
| Physical I/O | 4 | Sensor→spatial — visual, can still be a SLAM lecture |
| Anti-AI | 5 | No demo constraint |

“Still demoable” is a weasel. A compiler with a terminal screenshot is demoable. “Substance required” on demo-first is the instruction that will bury the wow under a technical core so `T` doesn’t kill them at the overall-win gate.

5% of agents design the stage first. 5% are told to impress a professor. The scoring then prefers the professor. Physical I/O is the 2025 Medicly pattern (ground truth: phone video → visible 3D transform) and is **smaller than research-lab**.

Recombination (v1: **20 agents**) is specified as grafting a sponsor mechanism onto a grand-path idea. That adds explanation burden and sponsor beats. It does not ask “did we make the first 30 seconds worse.”

### 10. Letter collisions will mis-score demo if anyone implements the wrong plan

| Letter | Fable | Astra | v1 |
|---|---|---|---|
| `W` | wow moment | **competitor strength** | wow |
| `M` | mode-collapse inverted | replication resistance | **memorability** |
| `R` | track relevance | reliability | reliability (`Rel` = track) |
| `K` | kill-switch / fallback | prize-path coherence | **killer-demo density** |
| `BR` | build-blocker (unknown tech) | runtime fragility | **boring** |
| `ER` | eligibility/rules | eligibility ambiguity | **explanation** |
| `DR` | live demo failure | **data** risk | demo |

If packet, schema, or a later auditor copies Astra’s dictionary, `W` stops meaning wow and `DR` stops meaning the stage dies. v1 already remapped; the Fable JSON schema in §14 still uses the old letters. Loop-1 reports will write `K` as kill-switch and `BR` as “we never used SLAM,” while rankings interpret `K` as killer-demo and `BR` as boring. **Demo ranks will be garbage on collision.** This is a launch blocker by itself.

### 11. Fallbacks can fake the holy-shit, and honesty rules are soft

Fable requires a recorded fallback clip and treats cached/pre-warmed state as passing the slow-LLM test. Astra correctly forbids using prerecorded output as proof of live behavior.

v1 keeps the stall/reset tests and “keep both.” Agents will write a cinematic clip, score `W=9`, and call it a demo. In a 3-room showcase that clip is a video essay — the research-paper failure mode with better production.

Ground truth Demo Quality is *understandable in 3 minutes*, not *a trailer exists*.

### 12. Time-to-first-pixel is unmeasured; 3 rooms make that fatal

No score, kill, or schema field is “seconds until a stranger sees or does the transform.” Fable hook is 15s of talk, then 30s of before-state — **45 seconds of setup** before the only visual beat.

Judges rotate. Expo is noisy. People’s Favorite is audience walk-by. A idea that is holy shit at 2:10 after a problem statement is a research talk. Medicly-class wins (ground truth prior) land the transform **on the device in the first beat**. Nothing in the rubric measures that.

---

## Fixes

Mapped to flaws. Do these in `final_ideation_plan.md` + packet + schema + `parse_initial.py`. Still no project ideas.

1. **Put `K` in Overall and create a Stage ranking.** Overall must include `K`. Add ranking 6 (or replace Upside’s lecture bias): Stage = `D W M J K` with tie-break lower `DR`. Apply the same “top-10 in any one” rule to Stage so spectacle has the door research already has.

2. **Hard demo gates, symmetric to the overall-win gate.** Finalists require `D ≥ 7`, `W ≥ 7`, `K ≥ 6` (0–10), **and** a filled `t_first_visible_s ≤ 30` (first judge-visible or judge-interactive state change). Fail any → cannot be the pick, cannot occupy a research-lab floor seat in the last 8. Astra’s “at least one of T/O/D exceptional” stays, but **`D` exceptional cannot be skipped because `T` is exceptional.**

3. **Kill “needs a lecture.”** New kill (round 1, not jury): if the 6th-grade stranger test fails — delete the spoken script; if the screen/audio/haptics loop no longer communicates the before→after, `kill_flags += lecture_required`. Re-run in red team and demo-sim. This is the wrapper test for talking.

4. **Replace the TED-talk beat contract.** Schema: beat 1 is the live transform or interaction (target ≤30s, hard cap 45s). Explanation and sponsor proof are *inside* that loop or after it, not instead of it. Demo-sim is a **full 180s** script with a required 90s *silent-watch* pass (no voiceover). `D` and `W` are scored from the silent pass first. 90s-only sims are banned.

5. **Operationalize `W` / `M` / `K` or delete them.**  
   - `W`: 10 only if a first-time viewer gasps or leans in *before* the technical sentence. Evidence: timestamp + what is on screen/hands.  
   - `M`: what the judge repeats to the next judge, ≤12 words, no jargon.  
   - `K`: count of distinct holy-shit beats that survive wifi-down and 60s reset. `K=1` if there is one; `K=0` if the only beat is a spoken claim.  
   No 20-word vibe scores.

6. **Fix letter collisions before one agent writes JSON.** One dictionary in the packet. Fable §14 field names must match v1 meanings or be renamed (`wow`, `killer_demo`, `boring`, `demo_risk`). Reject reports that use Astra’s `W`=competitor or Fable’s `K`=kill-switch under v1 names.

7. **Reweight the jury and the pick.** Minimum 4 of 12 ballots are demonstration-only (first-time comprehension, hands-on, expo walk-by, silent-screen). Aggregate that panel *before* mixing with professor ballots (Astra’s panel-then-compare). Human pick order: pass demo gates → pass overall-win gate → `p_any_adj` → EV. A teammate may veto a finalist that “needs the speech.”

8. **Multiply demo into P(any) from round 1, not as late flavor.** Keep Fable `p_any_adj = p_any × p_ship_core × p_demo_ok`, but compute a cheap `p_demo_ok` at parse time from: `t_first_visible_s`, lecture-kill, stall test, reset test. Demo-sim *revises* it; it must exist before the 50-cut. Do not skip demo-sim in the clock hatch; skip recombination volume first.

9. **Close the research escape hatch.** Research-lab floor applies only to ideas that also clear the demo gates. “Still demoable” is deleted; the constraint is “silent-screen pass ≥7.” Demo-first “substance required” may not be satisfied by adding a lecture-only core; substance must be *visible in the loop*. Recombination must re-score Stage and is rejected if `t_first_visible_s` gets worse.

10. **Stop faking wow with a trailer.** Cached/recorded output may save the explanation; it **cannot** raise `W` or `K`, and it cannot be the silent-screen evidence. Astra’s honesty kill stays in the *implemented* kill list, not in “keep both.”

11. **Raise spectacle prizes in calibration, not in EV fantasy.** People’s / Design stay low-object. Agents still must not set `p_peoples=0` by default on any idea with `W≥8`. That is a calibration instruction, not a new prize.

---

## What is already non-stupid (does not salvage the score)

- Official 3-minute constraint is believed (ground truth conflict #3 resolved).
- Open-world asks for visible before/after; bolt test asks “does the judge *see* the sponsor.”
- Wrapper kill, stall test, 60s reset, demo-sim stage, Physical I/O / Demo-first cohorts exist.
- Astra’s 70s live-interaction budget and “no usable loop” ban are the right ideas — **not the v1 contract.**

Those are ingredients. The recipe still bakes a paper.

---

## Launch checklist (all required)

- [ ] `K` in Overall; Stage ranking `D W M J K` exists and can auto-advance
- [ ] Finalist floors: `D,W ≥ 7`, `K ≥ 6`, `t_first_visible_s ≤ 30`; `T` cannot substitute for `D`
- [ ] `lecture_required` kill + silent-screen 180s sim
- [ ] One letter dictionary; Fable JSON remapped; collisions fail validation
- [ ] `p_demo_ok` in the 300→50 cut; demo-sim not in the skip table
- [ ] Jury ≥4 demo ballots, panel-aggregated; pick rule includes demo gates
- [ ] Recorded fallback cannot inflate `W`/`K`

Until every box is checked: **Launch 100? NO.**
