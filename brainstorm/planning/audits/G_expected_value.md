# G — Expected-Value Auditor

Adversarial pass on whether the process maximizes **P(at least one prize)** rather than prestige, EV-of-hardware-stacks, or grand-or-bust.

Inputs only: `competition_ground_truth.md`, `fable_plan.md`, `astra_plan.md`, `synthesized_plan_v1.md`.  
No project ideas. No agents launched.

---

## Verdict

**No.** The files *say* P(≥1 prize) is the objective. The decision procedure maximizes something else: a prestige-feasible idea that can tell a P(any) story.

Ground truth’s team instruction is already a two-term objective: maximize P(≥1) *with* a serious overall path. That is a constraint, not a license to put grand potential in the overall ranking, require top-8 ∩ top-8, require `G ≥ 3`, staff a prestige jury, and break ties with a table that sets Grand = 10 because “reputation dominates object value.” That is four prestige filters plus a hardware-EV last mile. Fable even states the kill shot in plain language: a #1 sponsor-sniper that is #40 overall “does not win.”

Under realistic field math, that discarded sniper is often the **higher** P(any) object. One thin-field Best Use (Solana / Sandia / IFM if eligible) is a 1-of-few shot. Grand is 1-of-all-submits. Track 2nd/3rd in a deep track are extra slots the process treats as consolation. Positive correlation through project quality means P(union) sits near `max_k p_k`, i.e. near the sniper. The overall gate systematically prefers the *lower* of those numbers.

Astra’s hierarchy makes the substitution official: (1) ship, (2) overall path, (3) then P(any), (4) then utility. Synthesized claims to “keep both” Fable’s intersection and Astra’s gate. That is not a synthesis of P(any)-max. It is P(any) as a membership card for a prestige tournament.

---

## What is actually being optimized

| Surface | Claimed | Actual |
|---|---|---|
| Objective sentence | max P(≥1) + serious overall path | overall path is the binding constraint |
| `p_any` ranking | primary sort | one of five Borda lists, then intersected, floored, juried |
| EV table | tie-break only | last-mile pick among finalists who already cleared `p_any ≥ 0.5` and `G ≥ 3` |
| Sponsor-sniper ranking | exists | structurally cannot win the final pick |
| Allocation | search coverage | 10 STACK slots + Solana/Auth0 overweight justified by **per-teammate hardware** |
| Jury | pick a winner | 12 prestige/sponsor personas; **no juror whose only job is max P(any)** |
| Clock | ideation ≤ time that eats the prize | synthesized refuses to skip the 100; escape hatch drops **build-sim**, the only delivery multiplier |

---

## Ranked flaws

### 1. Final pick is prestige-gated, not argmax P(any) — **fatal**

Fable §3.2 / §9.5 / synthesized “Final pick rule”:

- Must be top-8 **overall** ∩ top-8 **P(any)** (Fable), or “overall-win gate **and** top-tier P(any)” (synthesized).
- Then `p_any ≥ 0.5`, then `G ≥ 3`, then **EV**, then `Y`.
- Humans veto. Jury Borda produces the three names.

P(any) is a **threshold and an intersection**, not the thing being maximized. Once three finalists clear 0.5, the sort is grand path, then hardware-weighted EV, then “would we enjoy this.” That is the opposite of P(any)-max at the only decision that matters.

Worse: synthesized **never translates** Astra’s overall-win gate onto the 0–10 user scale. Astra wants U,T,O,D each ≥ 3 **and** one of T/O/D = 4 on a 0–4 scale (harsh). Fable’s `G ≥ 3` is middling on 1–5. On 0–10, `G ≥ 3` is almost everyone; U/T/O/D ≥ 3 is a joke; scaling Astra to ≥7–8 with a 9+ is grand-or-bust. An undefined gate will be applied as whatever makes the pretty idea survive.

**Fix:** Parent sorts survivors by `p_any_adj` (flaw 2). Overall is a **soft** constraint: among ideas within a stated ε of the P(any) leader (e.g. 0.05), prefer higher G. Hard-kill only true joke-overall ideas (no before/after, wrapper-test fail, Rel stretch). Delete `G ≥ 3` until it is defined on 0–10. EV is not in the pick order at all unless two ideas have indistinguishable `p_any_adj` *and* G. Human veto may kill one finalist; it may not replace the sort.

---

### 2. `p_any` is the wrong random variable — **fatal**

Synthesized copies Fable:

```
p_max  = max_k p_k
p_rest = 1 - Π_{k ≠ argmax}(1 - p_k)
p_any  = p_max + 0.5 · (1 - p_max) · p_rest
```

Four independent defects, any one of which means the ranking is not P(≥1 prize).

**2a. Track 1st and track 2nd/3rd are mutually exclusive.** Ground truth: one track, depth is 1st or 1st/2nd/3rd. You cannot win both. Astra said this out loud. Synthesized kept Fable’s product anyway. An idea with `track_1st=0.20` and `track_2nd_or_3rd=0.35` gets fake residual credit. For exclusive placements, `p_track = p_1st + p_2nd_or_3rd` (capped at 1), **one** term.

**2b. Synthesized dropped `p_any_adj`.** Fable at least did `p_any_adj = p_any × p_ship_core × p_demo_ok`. That is the quantity that hits the expo floor. Synthesized’s P(any) ranking is paper eligibility × judge vibes, unconditional on shipping. An unshippable 0.50-bucket idea beats a boring shippable 0.35. Astra’s only correct equation in the whole stack is the one synthesized did not operationalize:

`P(any) = Σ_z P(z) P(D|z) P(∪ W_j | D, z)`

**2c. Global ρ = 0.5 is the wrong correlation.** People’s / Design / Grand / Demo-quality are almost the same 3-minute event. MLH Best Use can be a **different judge** (ground truth: categories exist independently; UNKNOWN if mentally double-counted). Treating Grand+People’s as half-independent **overstates** P(any) for wow-demo prestige plays and **understates** an orthogonal sponsor shot. Fable’s own `ponytail:` admits the upgrade is a per-pair table and then calls it unnecessary.

**2d. Astra’s scenarios are a “sensitivity column.”** A column that cannot change the pick is decoration. Ranking by one damped point estimate while field-size and operating-condition uncertainty sits unused is fake precision — the exact failure Astra warned against.

**Fix:**

1. Collapse exclusive track placements to one `p_track`.
2. Rank by `p_any_adj = P(D) · P(∪ W_j | D)` with `P(D) = p_ship_core × p_demo_ok` (crude is fine; omitting it is not).
3. Default union: `p_union | D = p_max` as the **conservative** number used for selection (positive quality-correlation ⇒ P(any) ≈ best single shot). Report Fable’s damped formula and the independence product as **bounds**, not as the sort key.
4. Raise correlation (use `p_max` only) inside the demo-tied bundle {grand, peoples, design}; allow more residual credit for an MLH/Sandia/IFM term that has a distinct judge path.
5. Scenarios (Astra’s 8, or synthesized’s 3) **must** be able to flip the leader. If the leader is not the leader in ≥2 of 3 field-size scenarios, it is not the leader. No decorative columns.

---

### 3. `p_k` are uncapped self-scores; the 0.5 gate is a self-score game — **high**

Buckets `{0, .02, .05, .10, .20, .35, .50}`. No mapping from U/T/O/D/Rel/E/C/X/B or from field size. Shared-packet prior (“random team ≈ 0.3, top quartile ≈ 0.6–0.7”) is a prompt hope. Parent does not compute `p_k` from anything official.

Field arithmetic the agents are not required to use (ground truth: do **not** use Devpost 34; Fable `ASSUME` ~60):

| Prize | Rough base if 60 submits | Closest honest bucket |
|---|---|---|
| Grand | 1/60 ≈ 0.017 | 0.02 |
| Track 1st, 15-team track | 1/15 ≈ 0.07 | 0.05–0.10 |
| Track place if 3 slots, 15 teams | ~0.20 | 0.20 |
| MLH Best Use, 25 Gemini wrappers | 1/25 = 0.04 | 0.02–0.05 |
| MLH Best Use, 4 real Solana | 1/4 = 0.25 | 0.20–0.35 |
| Sandia, 3 cyber teams | ~0.33 | 0.35 |

A serious overall path with `p_grand=0.10` and `p_track=0.10` has Fable `p_any ≈ 0.145`. A thin-field sniper at 0.35 has `p_any = 0.35`. The process will call the first “the objective” and reject the second.

The `p_any ≥ 0.5` finalist gate makes this worse. Under Fable’s damping:

- One 0.50 bucket → 0.50 (passes).
- Two 0.35s → ~0.46 (**fails**).
- Four 0.20s → ~0.40 (fails).

So the gate is “did you put 0.50 on your favorite category,” not “P(any) ≥ 0.5.” Agents will. Red team “replaces scores from round 2”; synthesized does not say red team replaces **`p_prize` buckets**. Round 1’s 300→50 P(any) ranking is then 300 vibes.

Overconfidence flag at `p_any > 0.8` almost cannot fire from the formula (a 0.50 + four 0.50 residuals still lands ~0.73). It polices a number agents are not even asked to output (parent computes `p_any`; agents output `A` / `p_prize`).

**Fix:** Parent computes `p_k`, not agents. Minimum recipe: `p_k = P(eligible) × 1 / max(1, n_competing_k)`, with `n_competing` a scenario variable (Gemini crowded, Solana/Sandia/IFM thin, track n from a stated prior). Agents supply only eligibility/centrality/bolt bits and a 1–3 “we are in the top third of this category” claim. Red team **must** overwrite `p_prize`. Delete the 0.5 numeric gate until `p_any_adj` is on a calibrated scale; if a gate is needed, use “not dominated on the conservative bound,” not 0.5.

---

### 4. Five rankings + floors + jury drown the one ranking that matches the objective — **high**

Fable round 1: keep top-50 in **≥2** lists **or** top-10 in any one, then cohort ≥2 and track ≥5, fill from risk-adjusted.  
Red team: each of {Solana, Auth0, Mongo, Vultr, ElevenLabs, Sandia, IFM} ≥1 if any survived.  
Synthesized: same floors; 20 recombiners; 12-persona jury; pairwise.

Effects:

- A boring high-P(any) track-place + one thin sponsor can miss top-10 P(any) *and* miss a second list (low G, low W, low upside) and die at 300→50.
- Track ≥5 of 50 is **40% reserved by geography**, not by P(any). A weak Food card displaces a stronger Opt card because of a floor. Ground truth: sparse tracks may award **1st only** — fewer slots, not automatic “cheap wins.” Fable’s “keep top 3 of a sparse track regardless of score” (dropped by synthesized, replaced by a blunter ≥5) never computes depth × field strength, which Astra correctly refused to assume.
- Sponsor floors keep snipers alive through mid-tournament so the final gate can kill them. Coverage theater.
- Jury personas: CS prof, HRT quant who hates wrappers, Jane Street systems, designer, audience, Sandia, Solana, ElevenLabs, Vultr, 3am selves. That committee picks impressive. It does not pick max P(any). Astra at least had a 3-seat prize-strategy panel and min-regret across rankings. Synthesized took Fable’s celebrity panel and “pairwise, no casual ties.”

Overall ranking itself includes **G** (synthesized: `U T O D M P R J W G Rel`). Prestige is inside “overall,” then required again as a gate, then again as the post-0.5 sort. Triple-counted.

Letter `A` (“multi-award surface”) is in the schema and in **none** of the five rankings. Dead.

**Fix:** P(any_adj) is the **only** advancement ranking after kill flags. Overall and risk-adjusted are **display columns** for humans. Upside and sniper are diagnostics. Floors: at most **one** reserved seat per track if that track’s leader would otherwise vanish **and** scenario `p_track` for that seat exceeds the displaced idea’s `p_any_adj`. No sponsor has a guaranteed seat (Astra was right; synthesized reverted). Jury: three reviewers score only “which of these has higher P(any_adj) under the packet priors”; they do not Borda prestige. If a 12-persona jury remains, it cannot change the parent’s P(any) order; it can only annotate.

---

### 5. Allocation and the EV table optimize hardware stacks the prose forbids — **high**

Synthesized: “EV would over-pick hardware stacks that slip” / “Use Fable’s weight table as tie-break only.”

Same file: Solana 8, Auth0 8, STACK 10. Fable’s justification for Solana 9 and Auth0 8 is **per-teammate Ledger / headphones**. That is `w_k`, not `p_k`. Thin field *is* a P(any) reason; multiplying by object value is EV. The allocation text does not separate them.

Fable weights: Grand 10 (explicit reputational premium), Solana 5, Auth0 5, Gemini 2, track 2nd/3rd 2, Best Design 1. Astra: Grand **20**, Solana `1+n`, Auth0 `2+n`, track **2nd = 1 < 3rd = 3**. Both tables encode prestige and swag, then get used when the 0.5 and G gates have already flattened P(any).

STACK’s 10 cells exist to hunt 2–3 prizes from one build. Under Fable’s own damping, extra prizes are half-credit residuals. Under quality-correlation, they are nearly **zero** extra P(any). Ten percent of the search is an EV machine.

Physical I/O (4) exists because 2025 grand was Medicly — different year, different tracks (ground truth forbids reuse). Research-lab (5) is “Grand via Technical Difficulty.” Those 9 slots are grand-or-bust search, not P(any) search.

Gemini-at-6 because “eligibility rides free” is the one allocation move that is actually P(any)-smart.

**Fix:** Allocate search by **expected impact on the P(any) frontier**, not by object value. Thin-field + distinct-judge categories (Solana, Sandia, IFM-if-access, maybe Auth0-as-primitive) earn specialists because `1/n_competing` is large. Per-teammate multipliers do not. Cut STACK to the assigned pairs that share a judge path only if a pair can raise `p_max` (not `H`). Physical I/O / research-lab fold into open-world with the same hard constraints; they do not get a grand-cosplay quota. EV table: delete Grand’s reputational 10/20 or move it out of any numeric pick. If a utility table remains, it is a footnote for humans who already picked the P(any) winner.

---

### 6. The process farms snipers, then refuses to hire them — **high**

53 specialist cells + STACK + a sponsor-sniper ranking + sponsor floors → the pipeline is built to *find* high `p_max` cards. Final rule: sniper #1 / overall #40 is recombined into a top-overall idea or discarded.

Recombination (synthesized: **20** agents) is offered as the patch. It is how you get **neither**:

- Bolt test + `Q` + max 3 sponsors + 3-minute story.
- Adding a load-bearing sponsor to a grand-path core raises `I`, `DR`, critical path — i.e. cuts `P(D)`.
- Fable only gives the added prize half residual credit even if `P(D)` holds.
- Hybrids must re-pass tests; chimeras die at 2am (both plans admit this).

Specialist briefs also fight P(any) at generation time: “Grand path first” for 18 open-world agents; specialists must invent a *reason to exist* that *is* the sponsor (high P(that prize), “lower grand path”). Then the tournament punishes that lower grand path. You paid 53 agents to generate the thing you forbade.

**Fix:** Allow a sniper to win. If conservative `p_any_adj` (≈ `P(D) · p_max`) is highest, that is the pick. Recombination is optional and only ships if the hybrid’s `p_any_adj` **beats both parents**. No “graft the Ledger onto the beautiful idea so we can sleep.” Specialist agents should maximize P(that prize)×P(D), not apologize for a weak G.

---

### 7. The 100-agent clock is not inside the objective — **medium-high**

Fable: ideation > 1h50m “is eating the prize”; build by 10:50pm, never past 11:15. Astra: 75 min target, 90 cap, commit by 10:30; **do not launch 100** if capacity cannot finish. Synthesized: run the **full** user pipeline, 20 recombiners, do **not** skip the 100; if overtime, skip build-sim on 16–30 and shrink the jury.

`P(any | pick)` dies when `P(D)` dies. The escape hatch discards the stage that estimates `P(D)` in order to protect search theater. Astra’s capacity note (four slots including parent ⇒ 100 reports may be fiction) is unresolved. A partial 100 that is still *called* a search, or a 100 that slips build start, is a direct P(any) loss. Neither `p_any` nor the estimator has a term for “hours already burned.” Fable’s 17.2h / 31.7 effective hours assume a 10:50pm start that synthesized’s pipeline may miss.

**Fix:** Hard cap commitment (Astra 10:30 or Fable 10:50 — pick one, write it). If the 100 cannot finish inside the cap, **do not launch 100** (Astra). If already launched and late, freeze the completed set, **keep** build-sim on the remaining P(any) leaders, drop floors/jury first. Never skip `P(D)` to save coverage. Put `H_remaining` into the estimator so a slipped start raises every critical-path kill.

---

### 8. No baseline, so “we maximized P(any)” is unfalsifiable — **medium**

The process never scores a default: one honest track, one distinctive core, one thin-field sponsor that passes the bolt test, Saturday-noon freeze, Astra’s last four hours reserved. That default may beat the tournament winner on `p_any_adj`. Without it, any finalist can be declared optimal.

Raffle correctly has weight 0 for concept choice (Astra). Cursor UNKNOWN will be scored as 0 by some agents and as a free rider by others; noise in `p_any` if “used Cursor” is actually free. People’s vote mechanic is UNKNOWN; demo-first’s 5 slots are a guess. Fine as uncertainty — not fine as an uncompared search tax.

**Fix:** Before loop 1, parent writes one **baseline card** (no new idea content in this audit; the card is a scoring fixture). Every ranking file includes `p_any_adj(finalist) − p_any_adj(baseline)`. If the winner does not beat baseline on the conservative bound, you did not earn the pipeline. Cursor: one packet rule, applied to all ideas, after the workshop fact lands — not per-agent invention.

---

### 9. Synthesized merge leaves the pick rule internally inconsistent — **medium**

Disagreement table says: primary sort is P(any) then overall gate; EV tie-break only; “both” Fable intersection and Astra min-regret.

Those three cannot be true together.

- Intersection **discards** the P(any) leader if it is 9th overall.
- Min-regret **averages** overall, P(any), and risk-adjusted regret — prestige again.
- “Primary sort is P(any)” is a third procedure.

Plus letter collisions already acknowledged (`R`, `H`, `A`, `Y` remapped) without remapping the **numeric gates** that still say `G ≥ 3`. Fable P(any) tie-break was higher `H` = stack count. Synthesized remapped `H` to “team advantage” and left the tie-break unspecified. Implementers will grab Fable §8 and re-inject stack EV into the P(any) list.

**Fix:** One numbered procedure in `final_ideation_plan.md`. Delete the others. Suggested:

1. Kill flags, exclusive-track collapse, parent-computed `p_k`, `P(D)`.
2. Conservative `p_any_adj ≈ P(D) · p_max` (with orthogonal-prize residual per 2c).
3. Drop dominated ideas (worse on conservative P(any) in ≥2 scenarios and not better on `P(D)`).
4. Soft overall: if #2 P(any) is within ε and clearly higher G/Rel, humans may take it; record the P(any) tax.
5. One backup with a **numeric** switch trigger (Sat-10am core loop missing), not a second build.

---

### 10. Demo-tied prestige prizes are over-counted; track depth is under-counted — **medium**

People’s Favorite and Best Design ride the same demo as Grand. Fable/Astra still give them separate `p_k` inside the product. That is how a “wow” overall card inflates `p_any` without adding a real second lottery.

Track 2nd/3rd are the opposite: extra official slots when the track is popular (ground truth: depth scales with how many teams pick it). Process culture (banned list, wrapper test, G, Technical Difficulty slide, “serious overall path”) treats place as failure. Astra’s utility even sets track 2nd < track 3rd. A good-not-great team’s highest P(any) may be **track place + one thin Best Use**. The overall gate is designed to throw that away.

**Fix:** Bundle {grand, peoples, design} for union math. Keep track place as first-class `p_track`. Do not require a grand-shaped story to collect a track medal. Sparse-track handling: compute `p_track = 1/n_track` if depth=1st-only, `(1+2+3)/n` style only if opening/FAQ still imply depth; **never** “keep regardless of score.”

---

## What is not wrong (credit, so the score is not zero)

- Stating P(≥1) instead of idea volume (ground truth + both plans + synthesized).
- Refusing `Σ p_k` and `Σ w_k p_k` as the **primary** ranking (Fable §8, Astra §8, synthesized disagreement table). Linearity of EV ≠ P(union). That sentence is correct.
- Bolt test → bolted sponsor `p=0`. Correct for both eligibility-competitiveness and not stuffing the union.
- Gemini specialist cut because eligibility rides free. Correct P(any) allocation instinct.
- Kill rules that protect `P(D)`: hardware-in-bags, paid-API, critical path > 11h, data-in-1h, wrapper test.
- Astra last-4-hours reserve (synthesized adopted). That is real P(any); a 4:00pm miss is P=0.
- Raffle excluded from concept choice.
- Live verification table: UNKNOWNs reweight p, not (mostly) cells. Right direction, if the jury is not the place those weights go to die.

These are slogans and guards. They do not survive contact with the pick rule.

---

## Score: **39 / 100**

| Band | Meaning |
|---|---|
| 80–100 | Sort key is calibrated `P(D)·P(∪W\|D)`; prestige is a disclosed soft tie-break |
| 60–79 | Formula issues but the parent would still pick a high-P(any) shippable idea |
| 40–59 | Right words; decision procedure still prestige-constrained |
| 20–39 | Objective captured, then inverted by gates, jury, EV, and floors |
| 0–19 | Pure hardware-EV or grand-or-bust with no P(any) object |

39: they wrote a correlation-aware formula and demoted EV on paper, then built a tournament that cannot select the P(any) leader if it looks like a sniper, a track-place card, or insufficiently grand. That is the band for “inverted.”

Not 25: bolt test, no-naive-sum, Gemini free-rider, and `P(D)` kill rules are real.  
Not 55: the final sort is G then EV then Y after a 0.5 self-score gate.

---

## Launch 100? **NO**

Do not launch on `synthesized_plan_v1.md` as written.

Launching 100 now freezes the inverted objective into 18 “grand path first” cells, 10 STACK cells, 12 prestige jurors, and a pick rule that cannot hire the P(any) winner. Reports are cheap; **wrong selection is not**. The formula, exclusive-track collapse, parent-computed `p_k`, `p_any_adj`, and a single pick procedure are document edits. They come before agents.

Launch only after `final_ideation_plan.md` contains:

1. Conservative `p_any_adj` as the advancement sort (flaw 2 + 4).
2. Snipers allowed to win (flaw 1 + 6).
3. Parent-computed `p_k`, red team overwrites buckets, no 0.5 self-score gate (flaw 3).
4. EV/hardware weights out of the pick order (flaw 5).
5. A commitment clock that will abort the 100 rather than skip `P(D)` (flaw 7).
6. One pick procedure, gates defined on 0–10 (flaw 9).

Preflight (model exists, headcount, 2-agent pilot) is necessary and not sufficient. This audit fails the process on the objective, not on runtime.

---

## One-line charge

You will spend the night searching for thin-field prizes, then pick the idea that looks most like a grand-prize demo, and call the max of a self-scored 0.50-bucket formula “P(any).”
