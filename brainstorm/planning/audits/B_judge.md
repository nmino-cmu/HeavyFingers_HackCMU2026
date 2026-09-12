# Auditor B — Hackathon-Judge Auditor

Adversarial read of `competition_ground_truth.md`, `fable_plan.md`, `astra_plan.md`, `synthesized_plan_v1.md`.  
Question: would this process select what judges reward, or what engineers find intellectually appealing?  
No project ideas. No agents launched.

---

## Verdict

**Engineers.** The pipeline is excellent at not shipping a ChatGPT wrapper. It is structured to prefer a load-bearing sponsor stack, a “systems/ML person respects” core, and a calibrated `p_any` over the five axes on the opening slide.

Official track + grand axes (VERIFIED, opening): **Originality, Technical Difficulty vs wrapper, Demo Quality under 3 minutes, Usefulness, Relevance (track only).** Devpost is the same minus named Relevance. That is the whole game for HackCMU prizes. MLH Best Use, IFM, Sandia, Cursor, People’s, Design are stackable sideshows with weaker or UNKNOWN bars.

The synthesized plan stores those letters, then drowns them. Overall rank is an 11-factor stew. Primary sort is `P(any prize)` built from sponsor buckets. 63/100 cells are sponsor- or prize-shaped. Tournament floors keep a Solana idea and a K2 idea alive because the cohort exists, not because a room judge would score them. `BR` is remapped to **boring**. Research-lab’s success criterion is a CS prof, not Katie Wang in a 3-minute room. Demo-sim is cut to **90 seconds** against a VERIFIED 3-minute clock. The “overall-win gate” is named in the disagreement table and **never defined on the 0–10 scale**.

A tired judge who has already seen eight wrappers will reward: a real need they can repeat, a fresh approach, a technical core that is visibly not a prompt, a demo that finishes clean, and a track story that does not stretch. This process will hand that judge a hybrid that passed the bolt test, the wrapper test, and a Jane Street persona, and lost the room.

---

## Score of synthesized plan

**42 / 100**

Credit: banned list + wrapper kill + bolt test + honest Rel letter + 50-word why + stall/reset tests will correctly execute the one sentence on the judging slide that engineers already believe (“vs ChatGPT wrapper”). That is necessary. It is maybe 15 points.

The other 58 points are selection pressure. Allocation, floors, `p_any`, undefined gate, engineer jury, technique seeds, Medicly cargo-cult, 90s scripts, and `BR=boring` will systematically promote intellectually hot, prize-catalog-shaped builds over useful, original, demo-clear, track-true ones. You cannot jury your way out of that prior.

---

## Launch 100?

**NO**

Not because K2/Vultr/Sandia are UNKNOWN (Fable is right that those reweight later). Because launching this allocation and this ranking contract produces 300 developed ideas drawn from the wrong objective. Red team and a 12-persona jury cannot recover a biased search. Fix the judge-objective, the gate, the floors, the demo clock, and the jury, then launch. The synthesized file already says “not until auditors + `final_ideation_plan.md`.” Keep that. Do not launch on v1.

---

## Ranked flaws

Ranked by how hard they push the final pick away from official U / T / O / D / Rel.

### 1. Usefulness is a spectator letter; “real need” has no kill

Official Usefulness: practical, fulfills a real need. Weight on the slide: one of five.

Operational kills in v1: delete LLM, delete sponsor, hardware not in bags, data not in 1h, paid API, critical path >11h, banned pattern. All of those are engineer/feasibility/sponsor tests. None ask whether anyone needs the thing.

Fable’s before/after and six-beat script are present as artifacts, not as gates. Astra required four sentences (in / change / why technical / why it helps someone) and a useful minimum that fits the schedule. v1 says “keep both plans” and then lists only the engineering kills.

Result: a SAT/CRDT/SLAM/devnet toy that “deletes the LLM and something remains” survives. That is Technical Difficulty theater. Judges score it U=low, D=confused, Rel=stretched, and you lose the room while the spreadsheet still shows T=9, G=8, `p_solana=0.35`.

### 2. `P(any prize)` is the real objective; official axes are a constraint you forgot to write down

Stated goal: maximize P(≥1 prize) with a serious overall path. v1’s final rule is “overall-win gate AND top-tier P(any).” Astra defined that gate (`U,T,O,D` each ≥3 on 0–4, one of T/O/D = 4). v1 **does not translate it to 0–10**. The scoring section has five rankings and no floors on U, T, O, D, or Rel.

`p_any = p_max + 0.5*(1-p_max)*p_rest` over grand + track + six MLH + IFM + Cursor + Sandia + People’s + Design. A mediocre-useful Auth0+Solana+Mongo stack with three mid buckets beats a high-U, high-D, high-Rel idea with only grand+track mass. EV is “tie-break only,” but `P(any)` *is* the hardware-stack objective under another name. Astra warned that isolated prize probability can have negative strategic value. v1 did not implement that warning.

Sponsor-sniper is a first-class ranking. Combined with 63 sponsor cells, it is the search.

### 3. 63 sponsor/prize cells + cohort floors = the pool is not a judge pool

Allocation: 6+8+8+7+8+6+10+5+5 = 63 cells whose hard constraint is a sponsor or a dedicated prize (IFM, Sandia). Open-world is 18. Demo-first is 5. Research-lab + Anti-AI + Physical I/O (14) are “be technically interesting” cells, not “be useful” cells.

Tournament: each cohort ≥2 into the 50; Fable also floors surviving sponsor categories into the 30. That is how a weak-U K2 idea and a weak-D Solana idea stay alive: the org chart requires them.

Grand + track judges do not score Gemini, Ledgers, or Atlas features. MLH Best Use is a different panel and a different sentence. Optimizing the search for stackable eligibility is engineer prize-catalog reasoning. It is not the opening rubric.

### 4. Research-lab, technique seeds, and “CS prof would respect” are the intellectual-appeal prior

Fable research-lab: realtime SLAM, CRDT, custom DSL/compiler, differentiable X, novel solver; “Grand via Technical Difficulty.” v1 keeps the cohort: “one hard core a systems/ML person respects; still demoable.”

Fable seed techniques include SLAM, CRDT, ILP/SAT, RL, diffusion, ZK, fuzzing, on-device models — and the agent must use a seed in at least 10 raw ideas. v1 inherits the seed triple as the private card.

Official Technical Difficulty is “real challenges vs ChatGPT wrapper,” not “a paper a prof would cite.” Official Demo Quality is “clear, understandable, under 3 minutes.” A differentiable core that cannot be explained in 20 seconds fails D and often U, even when T is real.

Astra’s anti-pattern table already named this: “Impressive model with no usable loop”; “Last year’s winner with a new label.” v1 kept the cohort anyway.

### 5. Overall ranking dilutes the official five to 1/11 each

v1 overall: `U T O D M P R J W G Rel` (11 letters, equal implied).

Official five are 5/11. The other six are engineer-adjacent: memorability, polishability, reliability, judge comprehension, wow, grand potential. G inside an overall-winner rank is circular. W and M promote spectacle. T, G, W, M will correlate on research-lab / Physical I/O / stacked-sponsor demos.

Astra treated execution as a **viability gate**, not an average, and refused to invent Relevance as a fifth *grand* criterion. v1 puts Rel in the overall stew (wrong for grand) and still has no U/D floor (wrong for both).

### 6. Demo clock is wrong, and Demo-first optimizes wow, not “clear and understandable”

VERIFIED: 3 min presentation + demo. Older 2-min rumor is discarded. Astra: 165s + 15s margin, sponsor proof inside the story. Fable: 180s six-beat with before/after required or D≤2.

v1: “demo-sim **90s** scripts.” That is half the official allowance. It selects punchy W/K moments and starves before-state, track why, and a judge-repeatable sentence. Fable’s “one sentence a judge repeats to another judge” does not appear in v1.

Demo-first cohort: “Design the **30s wow**, then the product.” People’s Favorite and Best Design have UNKNOWN rubrics. Official D is clarity inside 3 minutes, not a trailer. `K` = killer-demo density. Spectacle is now a strategic letter.

Under the escape hatch, build-sim and jury shrink first. Those are the stages that could have caught “works on paper, dies in a room.” Generation of the 63 sponsor cells is what you refuse to skip.

### 7. Jury is a faculty + sponsor review, not a HackCMU room

Fable’s 12: CS professor, MLH rep, HRT quant who hates wrappers, Jane Street systems, product designer, beginner audience, skeptical hacker, Sandia, Solana ecosystem, ElevenLabs, Vultr infra, 3am selves. v1: “12-persona jury, pairwise.”

At most three of those people resemble a 3-room HackCMU judge scoring the opening slide. Four are sponsor-ecosystem. Three are “smartest person in the trading/CS room.” Borda over that panel elects engineer-legible, sponsor-proofed finals.

Astra’s panel split (overall merit / demonstration / execution / prize strategy, then aggregate panels) at least let U/T/O and demo vote as blocks. v1 did not keep that. Pairwise + no casual ties is more tournament, not more judge-fidelity.

Ground truth: judges mostly UNKNOWN except Katie Wang. Do not simulate Jane Street.

### 8. Track Relevance is a `mod 4` rotate plus a prize floor, not a honesty gate

Relevance is judged, track-only, 50-word why. Fits multiple → pick one. Sparse tracks may pay 1st only.

v1: home track = `id mod 4`, “soft lens; Relevance must still be honest.” Then **each track ≥5** in the 50. Fable further assumed Food/Traveling absorb wrappers and overweighted Opt/Multi in TRACK because those “reward Technical Difficulty natively.” That is engineer track-shopping: pick the tracks that sound like problem sets.

A Solana or Vultr specialist whose id lands on Food will write a 50-word metaphor. Judges notice. Rel is in the 11-way average, so a 4/10 Rel still ranks if T/W/G are high. There is no “if the why needs a metaphor, you are not in this track” kill.

Track floors keep weak-Rel ideas to hunt sparse-track firsts. That is P(prize) logic, not Relevance logic.

### 9. `BR = boring` encodes engineer taste as a risk letter

Fable `BR`: build-blocker (tech nobody has touched). Astra `BR`: build/deploy/device/runtime fragility. v1 risks: `BR boring`.

Higher = worse, and risk-adjusted rank subtracts this. The process literally penalizes “boring.” To a CMU systems student, a useful, clear, track-true tool is boring. To a hackathon judge, that is often the winner. Official Originality is a fresh *approach*, not an un-boring mechanism.

This is the cleanest single tell that v1 selects intellectual appeal.

### 10. Physical I/O / Medicly is last-year cargo cult

Ground truth: 2025 grand Medicly is LIKELY useful prior and **different year, different tracks/sponsors**. Do not reuse 2025 tracks. Astra: last year’s winner with a new label is a deceptive pattern; prior winners are comparisons, not templates.

v1: 4 Physical I/O slots because “2025 grand was visible sensor→spatial transform.” Phone→3D on Optimization/Traveling/Multiplayer/Food is either a Rel stretch or a tech demo. Visible I/O can be a *demo tactic*. It is not a 2026 judging axis and not a reason to reserve 4% of the search.

### 11. Twenty recombinations will bolt prizes onto useful cores (or cores onto prizes)

User pipeline wants 20 recombination agents. Fable’s recipe: grand-path idea + a sponsor idea’s load-bearing mechanism. Astra: at most 12 challengers, one coherent core, explicit deletions, combining stacks is not enough; extra prize route that damages existing routes has negative value.

v1 keeps the bolt test (“would a judge *notice*”) and raises recombination to 20. Noticing a chain moment can *hurt* D and U by eating 30s of a 3-minute story. There is no kill for “this hybrid made the official-axis demo worse.” Bolt-pass + `p_any` up is enough to promote it.

### 12. Originality is optimized as “not the room’s wrapper,” not “fresh approach to a need”

Banned list + obvious-dump + CR/N are good and judge-aligned against the default field (recipe, itinerary, Kahoot, bolted login). Then the escape from the mode is a hard technique or a sponsor primitive. That is how you get original-*feeling* systems work that is not an original *product*.

Official Originality: entirely novel / fresh approach. A novel need-meeting interaction can win O with ordinary parts. v1’s upside rank is `T O G W N` — three of five letters are engineer-wow. Combined with anti-boring, simple-original dies in the 300→50 cut.

---

## Specific fixes

Do these in `final_ideation_plan.md` before any launch. Still no ideas.

1. **Write the overall-win gate on 0–10.** A finalist must have U, T, O, D, Rel each ≥6, plus at least one of {U, D} ≥8 and at least one of {T, O} ≥8. Fail the gate → cannot be selected, cannot be rescued by `p_any`, sponsor-sniper, cohort floor, or recombination. If nobody passes, disclose the shortfall and pick the closest *on official axes* (Astra), do not invent scores.

2. **Add a Usefulness kill, same hardness as wrapper/hardware.** After the 3-minute script: a stranger cannot name user + need + before/after in one sentence → kill. Delete the clever mechanism; if no reason to exist remains → cannot enter research-lab/anti-AI/Physical I/O rescue. “We’ll find users at expo” = marketplace kill (already in both parent plans); apply it.

3. **Overall rank = official five only, equal weight.** `U T O D Rel` for track-path ranking. Grand-path ranking = `U T O D` only (Astra: do not invent Rel as a fifth grand criterion). Move M, P, R, J, W, G to diagnostics or a secondary column. J≥6 is a *gate* (illegible → kill), not an average.

4. **Subordinate `P(any)` and kill sponsor-sniper as a finalist path.** After the official-axis gate, `p_any` may break ties among ideas that already clear U/T/O/D/Rel. An idea that is #1 sponsor-sniper and not top-tier on official overall cannot be a finalist. Recalibrate `p_grand` / `p_track` from official-axis scores, not from agent vibes about Ledgers.

5. **Remove cohort floors.** Track floors only if Rel is honest (see 8). No guaranteed seats for Solana, IFM, Sandia, research-lab, or Stack. Search investment ≠ reserved finalist seats (Astra already said this; v1 violated it).

6. **Rebalance the 100 toward judge axes, not catalogs.** Open-world / need-first ≥40. Sponsor specialists may remain, but every developed idea — including specialists — must pass the U/D/Rel gate to enter the 300→50. If that empties a cohort, the cohort empties.

7. **Delete “CS prof / systems person respects” from the packet and from research-lab.** Hard technical cores are allowed only if J≥7 and the 20-second technical-core beat is understandable to a non-specialist judge. Kill “grand via Technical Difficulty” as a standalone theory.

8. **Seeds: need/user-job first; techniques are optional.** Drop any “must use the technique seed in N raw ideas” rule. Keep obvious-dump (that one is judge-aligned). Prefer Astra’s Batch A (need first) as the source of at least one developed idea per agent.

9. **Demo-sim is 180 seconds (or 165+15), never 90.** Restore Fable’s six beats including visible before/after or D≤3. Require the judge-repeat sentence. Sponsor moments ≤30s total, inside the story (Astra). Wow/hook ≤15–20s. Missing track-why beat → Rel≤4. Escape hatch: **do not** drop demo-sim before you drop recombination count.

10. **Rebuild the jury as a HackCMU room.** ≥8 of 12 ballots score *only* U, T, O, D, Rel. ≤2 sponsor-ecosystem personas, and their ballots cannot move a candidate that the official-axis panel ranked bottom-half. Drop HRT/Jane Street/CS-prof as controlling Borda voters; if kept, isolate them as an “engineer appeal” score that is **not** used for selection. Read `live_verification.md`; do not read `p_any` or sponsor lists on the first ballot.

11. **Redefine `BR`.** Restore build-fragility / unknown-tech (Fable/Astra). “Boring” is not a risk. If you must keep a boring flag, it is informational and cannot change rank.

12. **Rel honesty kill.** 50-word why is scored as Rel. If it needs a metaphor, a second track, or “traveling means X philosophically,” Rel≤4 and the idea cannot take a track floor. `id mod 4` is a search hint, not an assignment of prize category.

13. **Kill dedicated Physical I/O / Medicly cohort.** Sensor→spatial is a legal open-world tactic when U and Rel hold. Do not reserve cells because 2025 won that way.

14. **Recombination cap = 8, with a demo-damage kill.** A hybrid that lengthens the 3-minute script, lowers U, or adds a sponsor the official-axis story does not need is discarded even if bolt-pass is true and `p_any` rises. One coherent core; name what was deleted (Astra).

15. **Human pick is a mock official ballot.** Top 3 are scored by humans on U/T/O/D/Rel *before* anyone sees `p_any`, EV, or the sponsor list. Veto stays. Backup switch trigger stays. If humans and the model jury disagree on official axes, humans win.

16. **Clock: protect judge stages, not generation vanity.** If wall-clock dies, cut recombination from 20→6 and skip sponsor-sniper ranking. Do not skip demo-sim. Never call a partial run “the 100.”

---

## What v1 already gets right (so you do not “fix” it into wrappers)

- Wrapper test, banned list, obvious-dump, no loop-1 web search: these are the correct defense against the field the opening already named.
- Bolt test as eligibility hygiene: keep it; stop using it as a reason to *select*.
- One track, 50-word why, from-scratch, 19h window, stacking allowed: factually aligned with ground truth.
- Live UNKNOWNs reweight at jury, not by rerunning the 100: correct.
- Human veto + one backup: keep, after fix 15.

---

## Bottom line

v1 would pick a project a strong CMU team is proud to defend in Discord and a sponsor table. Official judges are scoring five words: useful, original, technically real, 3-minute-clear, on-track. Those words are in the schema. They are not what the tournament maximizes.

**42. Launch 100? NO.**
