# Astra plan: HackCMU 2026 ideation search architecture

**Scope:** Planning architecture only. No project ideas, agent launches, implementation, or account provisioning were performed.

**Delivery:** Full markdown returned here because the workspace is read-only. Intended destination: `brainstorm/planning/astra_plan.md`.

**Objective:** Maximize the probability of winning at least one judged prize while retaining a credible overall-win path. Idea volume, sponsor count, and agent consensus are not objectives.

**Evidence basis:** The September 11, approximately 8:30pm EDT snapshot in [competition ground truth](/Users/nicholasmino/ProgrammingFiles/HackCMU/brainstorm/research/competition_ground_truth.md), [prior-winner notes](/Users/nicholasmino/ProgrammingFiles/HackCMU/brainstorm/research/prior_winners/notes.md), and [prizes and tracks](/Users/nicholasmino/ProgrammingFiles/HackCMU/HACKCMU_PRIZES_TRACKS.md). Also read: [resources](/Users/nicholasmino/ProgrammingFiles/HackCMU/HACKCMU_RESOURCES.md) and [sponsor research](/Users/nicholasmino/ProgrammingFiles/HackCMU/brainstorm/research/sponsor_research/mlh_and_opening.md). These are supplied research snapshots, not live verification performed during this planning task.

Operating constraints:

- Hacking starts Friday, September 11 at **9:00pm EDT**. Run the developed-concept and project-design phases only after that time.
- Submission is Saturday, September 12 at **4:00pm EDT**: approximately **19 hours** after hacking starts.
- Maximum team size is four; actual staffing must be recorded.
- Submit one project under **one track**. Prepare an exactly 50-word track justification.
- The presentation and demo together must fit **three minutes**.
- Grand, track, and sponsor awards may stack. Multiple track entries are not a strategy.
- IFM’s relationship to the track selector remains unresolved.
- Do not infer prizes from sponsor logos, import last year’s tracks, or use Devpost’s 34 participants as the field size.
- Do not create a campus-only cohort or force a literal interpretation of “Midnight Express.”
- Official eligibility requirements and our stronger standards for competitiveness must remain separate.

## 1. Decomposition of idea search

### Population

Run **100 independent logical searches** using the requested Grok 4.6 Extra High Fast configuration, after verifying that the parent can actually access that configuration. Do not silently substitute another model or reasoning setting.

A logical search is a fresh context with its own assignment and report. It does not require a dedicated simultaneous process.

| IDs | Count | Search responsibility |
|---|---:|---|
| 001–020 | 20 | Open-world searches for overall-winning quality |
| 021–028 | 8 | Gemini specialists |
| 029–036 | 8 | ElevenLabs specialists |
| 037–044 | 8 | Solana specialists |
| 045–052 | 8 | Vultr specialists |
| 053–060 | 8 | Auth0 specialists |
| 061–068 | 8 | MongoDB Atlas specialists |
| 069–078 | 10 | Coherent multi-prize searches |
| 079–083 | 5 | Anti-AI searches: no generative model in the essential product loop |
| 084–088 | 5 | Demo-first searches |
| 089–093 | 5 | Research-oriented searches with a bounded technical unknown |
| 094–097 | 4 | Conditional IFM specialists |
| 098–100 | 3 | Sandia cybersecurity specialists |
| **Total** | **100** | |

This reduces Gemini from ten specialists to eight and combines the released two slots with the five unallocated slots to fund IFM and Sandia exploration.

### Assignment structure

Each initial agent receives five small inputs:

1. A shared competition fact packet.
2. One cohort-specific objective.
3. One private seed card.
4. A fixed local search procedure.
5. A report contract.

Do not give every agent the entire orchestration document. In particular, initial agents do not need allocation totals, tournament mechanics, other agents’ assignments, or expected tournament favorites.

Each private seed card contains:

- A user or operating-context lens.
- A technical-mechanism lens.
- An interaction or demonstration lens.
- One constraint that exposes a different part of the search space.
- One assumption the agent must challenge.
- A soft track lens.

These are search directions, not project briefs. They must not prescribe a product.

### Local search procedure

Every agent:

1. Reads the common packet and its private assignment.
2. Writes **15 genuinely distinct raw concepts** in three batches of five.
3. Checks whether the batches changed the underlying mechanism and user interaction, rather than merely renaming the audience.
4. Rejects obvious constraint violations.
5. Develops its top three.
6. Nominates one primary candidate.
7. Records why its strongest rejected alternative lost.
8. Seals its report.

Specialists must include at least five raw concepts whose useful core survives removal of the target sponsor, even if removing that sponsor weakens implementation or prize eligibility. This exposes concepts whose only justification is the prize.

The output is:

- At least **1,500 raw concepts**.
- **300 developed candidates**.
- **100 primary nominations** for the first tournament stage.

The parent reads structured summaries first. It does not manually read 1,500 concepts.

## 2. Diversity mechanisms

### Stratified private seeds

Create separate balanced decks for:

| Axis | Lenses |
|---|---|
| Operating context | Individual workflow; small-team operations; creative practice; scientific work; accessibility; social interaction; household decisions; trust and security |
| Technical mechanism | Optimization; simulation; computer vision; signal processing; distributed state; information retrieval; identity and permissions; language or multimodal reasoning |
| Observable interaction | Direct manipulation; spatial output; live audio; multi-user state; measurable transformation; physical interaction using available equipment |
| Constraint | Intermittent network; limited setup; minimal data; bounded latency; no generative model; constrained compute |
| Track lens | Optimization; Traveling; Multiplayer; Food |

Use run seed `hackcmu2026-astra-v1`.

For each axis, repeat its values to fill 100 positions as evenly as possible, then shuffle deterministically using that run seed, the axis name, and a version counter. Assign one position from each deck to each agent. Resolve duplicate complete seed tuples by deterministic swaps.

Cohort requirements override incompatible seed values. For example, a Gemini specialist does not receive a mandatory “no generative model” constraint. Record each adjustment.

The track lens is advisory. A candidate must eventually have natural relevance to one official track, but the lens must not force an implausible justification.

### Three batches, three priors

The 15 raw concepts must cover:

- **Batch A — need first:** Start from a concrete user difficulty.
- **Batch B — mechanism first:** Start from a technical capability and identify where it changes an outcome.
- **Batch C — assumption reversal:** Challenge a dependency, interaction convention, or expected implementation.

At least one developed finalist must come from outside the agent’s initially preferred batch.

### Cliché rule

The following patterns require a specific rebuttal before advancement:

- Generic “AI for X.”
- General-purpose chat over uploaded documents.
- Another conversational planner or recommender.
- Marketplace or “Uber for X” dependent on attracting both sides.
- A dashboard whose only substantial behavior is displaying API output.
- Blockchain added to a workflow that gains nothing from shared verification.
- Sponsor integrations added only to increase the claimed prize count.

These are diagnostic patterns, not absolute bans on entire domains. Advancement requires a concrete technical and user-visible distinction.

### Detect collapse after reports are sealed

Cluster developed candidates using a fingerprint containing:

- User job.
- Core technical mechanism.
- Essential input and data dependency.
- Interaction loop.
- Visible proof.
- External dependency pattern.

Names and domains alone do not establish diversity.

At the 50-candidate stage, normally retain no more than two candidates from one mechanism-and-interaction cluster. Allow up to four only when their differences materially change feasibility, demonstration, or prize exposure. Record the exception.

Do not send “the pool has too many examples of X” messages to unfinished initial agents. That would turn independent exploration into coordinated convergence.

## 3. Prize targeting

### Weighting the search

The population deliberately contains:

- **35 searches without a sponsor mandate:** open-world, anti-AI, demo-first, and research-oriented.
- **48 searches across the six established MLH categories.**
- **10 searches for coherent stacking.**
- **7 searches for event-specific IFM and Sandia opportunities.**

These are search investments, not reserved finalist seats.

Equal MLH specialist counts avoid pretending that unknown participation levels or hardware preferences justify precise allocation differences. Gemini receives no additional allocation because the supplied research already suggests a crowded wrapper-heavy field.

### Limits on stacking

Default project scope:

- One core technical contribution.
- One primary sponsor-prize thesis.
- At most one deliberately added secondary sponsor-prize thesis.

A third integration is permitted only when all of the following hold:

1. It is already required by the useful product.
2. Incremental work is at most 45 minutes.
3. It adds no new unverified critical dependency.
4. Its contribution can be demonstrated inside the existing three-minute story.
5. Removing its prize eligibility would not cause the team to remove the underlying capability.

There is no reward for a longer “built with” list.

For each proposed integration, require three answers:

- What capability does the product need?
- What does this sponsor contribute to that capability?
- What evidence will a judge see?

A provider need not be irreplaceable. The test is meaningful use, not artificial vendor lock-in.

### Track strategy

Choose a track by relevance first, then credible competition information.

Do not assume a sparse track is easier: it may have fewer prize positions. Compare plausible field strength and award depth together.

Do not create a fifth IFM track allocation until the submission form or organizers resolve its status. Until then, IFM is modeled as a conditional additional prize.

### Event-specific prizes

- **IFM:** Four conditional specialists because a working access path could create differentiated opportunities. Unsupported access assumptions do not survive feasibility review.
- **Sandia:** Three specialists because the category is confirmed, while extra requirements are not.
- **Cursor:** No dedicated cohort before its eligibility bar is known.
- **Best Design and People’s Favorite:** Cross-cutting evaluation opportunities, not feature requirements.
- **Raffle:** Excluded from project-selection probability. Timely submission captures this opportunity without affecting concept choice.

## 4. Avoiding correlated agents

### Shared information

All agents receive the same versioned:

- Rules, schedule, and judging criteria.
- Prize catalog.
- Official-versus-internal eligibility distinctions.
- Team capability and equipment inventory.
- Confirmed API access facts.
- Prior-winner calibration notes.
- Output schema.
- Prohibited assumptions.

### Private information

Each initial agent receives only its own:

- Seed card.
- Cohort assignment.
- Research notes.
- Raw concepts.
- Self-critique.
- Candidate nominations.

Initial agents cannot read:

- Other initial reports.
- Shared brainstorm documents.
- A live leaderboard.
- Parent-generated example concepts.
- Aggregate themes emerging from the population.
- Other agents’ self-scores.

### Firewall implementation

The parent owns the shared manifest and submission inbox. Initial workers receive only their permitted packet and assignment.

Where the runtime supports file or tool restrictions, prevent workers from reading the initial-report directory. Otherwise, the prompt must forbid it, access must be logged, and the parent must acknowledge that the isolation is procedural rather than enforced.

Completed outputs remain sealed until the initial phase closes.

Factual corrections are allowed during generation:

- Broadcast the exact correction to every affected worker.
- Increment the fact-packet version.
- Require acknowledgement in the report.
- Do not attach any concept, recommendation, or emerging preference.

### Limits of independence

A hundred contexts using one model remain correlated. The plan reduces shared prompt and information effects; it does not treat their agreement as 100 independent observations.

The same limitation applies to the later jury.

## 5. Scoring methodology

### Fix the metric dictionary

The source prompt lists abbreviations without definitions. This plan establishes the following schema rather than implying those definitions were official.

All merit scores use integers **0–4**, where higher is better:

- **0:** Absent, contradicted, or unusable.
- **1:** Weak; major unresolved problems.
- **2:** Credible but ordinary or incompletely supported.
- **3:** Strong and supported by concrete reasoning or evidence.
- **4:** Exceptional relative to the expected event field, with a specific justification.

Use `null` when unassessed. Unknown does not equal zero.

| Group | Fields |
|---|---|
| Official | `U` usefulness; `T` technical difficulty; `O` originality; `D` demo quality |
| Track-specific | `Rel` relevance to the single nominated track |
| Execution | `F` feasibility; `R` reliability; `P` parallelizability; `S` scope controllability |
| Competitive | `N` distinction from likely field; `M` resistance to superficial replication; `J` judge comprehension; `W` strength against plausible competitors |
| Per sponsor | `E` eligibility evidence; `C` centrality; `X` depth of capability use; `B` benefit relative to incremental effort; `Q` clarity of sponsor proof |
| Strategic | `A` robustness of at-least-one-prize case; `G` overall-winning headroom; `H` upside available after the minimum build; `K` coherence across prize paths; `Y` diversity of credible award channels |

`M` measures the depth visible in the hackathon submission, not startup defensibility.

`Y` does not count sponsor logos. Several prizes dependent on the same fragile demonstration may provide little additional robustness.

Sponsor `E` has specific anchors:

- `0`: Known contradiction or ineligibility.
- `1`: Eligibility unresolved.
- `2`: Documented plausible eligibility path.
- `3`: Access and intended usage verified.
- `4`: Implemented usage and reproducible evidence available.

An unbuilt concept cannot receive `E=4`.

Risk scores also use **0–4**, but higher is worse:

| Field | Risk |
|---|---|
| `I` | Integration complexity |
| `API` | External service access, quota, latency, or availability |
| `DR` | Data acquisition, quality, or suitability |
| `SR` | Scope growth |
| `CR` | Competition and crowding |
| `ER` | Eligibility ambiguity |
| `AR` | Adoption, participant, or network-effect dependency |
| `BR` | Build, deployment, device, or runtime fragility |

Every assessed score includes a rationale, evidence references, and an evidence-strength label. Do not add these scores together during initial screening.

### Score in stages

**Initial agents:** Assess official merit, execution, track relevance, target-sponsor fit, and the three largest risks.

**Independent reviewers:** Complete competitive and strategic assessments after reports are sealed.

**Finalist assessors:** Revise scores using access checks, dependency schedules, novelty research, and demo simulations.

Preserve all revisions. Never replace an initial optimistic score without recording why it changed.

### Five separate rankings

| Ranking | Ordering principle |
|---|---|
| Overall | Official merit profile, technical and original contribution, usefulness, and clarity; use execution as a viability gate |
| P(any prize) | Conservative joint prize case under successful delivery and adverse scenarios |
| Sponsor-sniper | Strongest single sponsor case using eligibility, centrality, capability depth, and visible proof |
| Risk-adjusted | Strongest deliverable result under stressed schedule and dependency assumptions |
| Upside | Best credible ceiling after a complete minimum build, with additional work explicitly bounded |

Track relevance affects track prospects. It does not become an invented fifth grand-prize criterion.

### Serious overall-win gate

For final selection, require:

- `U`, `T`, `O`, and `D` each at least 3.
- At least one of `T`, `O`, or `D` equal to 4.
- A specific explanation of the contribution beyond ordinary API assembly.
- A complete useful minimum version that fits the schedule.

These are internal selection standards, not official score thresholds.

If no candidate qualifies, record that failure explicitly. Allow one bounded repair pass inside the search deadline, then select the strongest feasible candidate with the shortfall disclosed. Do not fabricate a qualifying score.

### Model P(any prize) jointly

Let:

- \(z\) be a field-and-operating scenario.
- \(D\) mean timely submission and a usable judging demonstration.
- \(W_j\) mean winning eligible prize \(j\).

Then:

\[
P(\text{any prize})
=
\sum_z P(z)\,P(D\mid z)\,
P\left(\bigcup_j W_j \mid D,z\right)
\]

This separates shared delivery failure from judging uncertainty.

Do not use:

\[
\sum_j P(W_j)
\]

as the probability of any prize. Do not use the independence product \(1-\prod_j(1-p_j)\) without evidence that the relevant events are independent.

Evaluate eight scenarios formed from:

- Lower versus higher sponsor crowding.
- More favorable versus less favorable relevant-track competition and award depth.
- Nominal versus degraded live operating conditions.

These are stress scenarios, not claims about actual attendance or infrastructure. Apply a consistent interpretation across candidates.

When only marginal probability intervals are defensible, use bounds. Conditional on delivery and a scenario:

\[
\max_j l_j
\le
P\left(\bigcup_j W_j\right)
\le
\min\left(1,\sum_j u_j\right)
\]

Do not narrow those bounds merely to produce a ranking. Treat track placements as mutually exclusive outcomes within one chosen track, not separate stackable awards.

For finalists:

- Estimate broad subjective intervals only where evidence supports them.
- Record assumptions about field strength and judging.
- Preserve uncertainty about scenario weights.
- Use ranges and sensitivity results, not decimal-point forecasts.
- Allow `[0,1]` when evidence cannot support a narrower interval.
- Label estimates as elicited judgments, not statistically calibrated probabilities.

Initial agents produce no prize percentages.

## 6. Information gathering

### Required reading

Every initial agent reads:

1. `brainstorm/research/competition_ground_truth.md`
2. `brainstorm/research/prior_winners/notes.md`
3. `HACKCMU_PRIZES_TRACKS.md`
4. The parent’s versioned corrections and team inventory.
5. Its assignment and output schema.

Sponsor specialists additionally read the relevant sections of:

- `HACKCMU_RESOURCES.md`
- `brainstorm/research/sponsor_research/mlh_and_opening.md`
- The relevant official sponsor documentation, as needed.

The parent may provide faithful extracts to reduce context size. Preserve qualifiers, conflicts, dates, and source references.

Prior winners establish examples of visible technical contribution. They do not establish a winning domain, a current field size, or causal evidence that one interface style wins.

### Verification ownership

Use one central verification queue for common facts. Do not let 100 agents independently troubleshoot the same account setup.

The parent handles public read-only research. Assign one team member to obtain in-person organizer or sponsor clarification. This plan does not authorize automated messages to organizers or others.

| Unknown | Verification | Default if unresolved |
|---|---|---|
| Requested model configuration and capacity | Inspect actual runtime and measure pilot completion | Do not claim the requested 100-agent run is ready |
| Actual builders, equipment, and availability | Team inventory | Estimate using two effective builders and existing equipment only |
| Submission form and IFM selector | Inspect form or obtain organizer clarification | Nominate one of the four confirmed tracks; treat IFM as conditional extra |
| Separate MLH submission requirements | Inspect current event instructions and Devpost flow | Prepare both Google Form and Devpost materials |
| K2 access, hosting, memory, and latency | Official documentation and a successful minimal call or load after 9pm | Reallocate IFM cohort; exclude unverified IFM eligibility from conservative prize estimates |
| Vultr credits and provisioning | Confirm code redemption and usable capacity | No reliance on unfunded resources or speculative GPU availability |
| Gemini model identifier and quota | Verify the documented endpoint and successful call | Treat recorded `gemini-3.8-flash` as an unverified snapshot value until checked |
| ElevenLabs entitlement and live latency | Verify credentials, quota, and a live interaction | Exclude concepts needing unavailable capabilities |
| Solana devnet access | Confirm faucet/RPC access and a real devnet transaction | No mainnet fallback; prune dependent paths if access fails |
| Auth0 access | Verify tenant and required API flow | Distinguish ordinary login eligibility from stronger competitive use |
| Atlas availability | Verify cluster connection and required operation | Prune paths that depend on unavailable features |
| Cursor eligibility | Obtain current prize requirements | No dedicated allocation; no claimed probability contribution |
| Sandia extra requirements | Obtain current requirements | Keep only clear cybersecurity fit; mark prize conditions unresolved |
| Design and audience voting | Inspect judging or voting instructions | Treat as secondary upside |
| Field and track participation | Reliable in-room or organizer information | Retain scenario uncertainty; do not substitute Devpost’s 34 |
| Library/model reuse rules | Check current event rules if a finalist depends on disputed reuse | No prebuilt project or project-specific pre-event work |

Smoke tests occur only after the permitted start and within existing authorized access. Default infrastructure spending is zero beyond confirmed free resources or credits.

### Research limits

- Initial workers: at most two narrowly scoped external checks each, only when they change feasibility.
- Central verification: deduplicate common API and rule questions.
- Novelty checks: focus on the 30-candidate stage and investigate shared clusters together.
- Finalist research: resolve the decision-changing uncertainty first.

Do not spend time resolving inconsequential pricing-copy discrepancies when the demonstrated usage is safely inside confirmed access.

## 7. Feasibility, sponsor fit, novelty, and demo assessment

### Feasibility tests

Every developed candidate must specify:

1. The one technical claim whose failure would invalidate the project.
2. A smallest experiment that could falsify that claim.
3. The required input and how the team obtains it.
4. A complete useful minimum version.
5. One stretch feature that can be removed cleanly.
6. A dependency and owner schedule.
7. What still works when the weakest external dependency fails.

A candidate may contain one substantial unresolved technical problem. Multiple unknowns on the same critical path require a simpler minimum version before advancement.

### Sponsor-fit tests

Apply four tests to each targeted sponsor:

- **Eligibility:** Does documented use plausibly satisfy the official requirement?
- **Removal:** What useful capability disappears if the integration is removed?
- **Depth:** What actual computation, state, identity decision, transaction, or interaction uses the sponsor?
- **Proof:** What trace or visible behavior demonstrates that use?

Separate outcomes:

- Eligible and competitive.
- Eligible but ordinary.
- Potentially competitive but eligibility unresolved.
- Ineligible.

Internal competitiveness standards are not invented official rules. For example:

- Ordinary Auth0 login can satisfy the documented API-use requirement.
- Straightforward Atlas persistence can satisfy basic usage.
- Hosting on Vultr may satisfy basic usage while producing a weak “Best Use” story.

Live voice, visible compute, real state changes, and meaningful identity boundaries are internal evidence standards where the official bar is broader.

### Novelty tests

At the 30-candidate stage, identify:

- The nearest existing product or project.
- A nearby hackathon implementation.
- The closest candidate elsewhere in the internal pool.

Record the distinction in mechanism, interaction, or demonstrated outcome.

Rules:

- A changed audience label is insufficient.
- A new combination must produce a new behavior, not just a longer stack.
- A familiar problem may still support an original implementation.
- “No search result found” is not evidence of unprecedented novelty.
- Prior winners are comparisons, not templates to reproduce.

### Demo test

Use a **165-second target**, leaving 15 seconds of margin:

| Segment | Time |
|---|---:|
| User need and stakes | 20 seconds |
| Starting condition or baseline | 20 seconds |
| Live core interaction | 70 seconds |
| Result and technical explanation, including sponsor proof | 35 seconds |
| Value and close | 20 seconds |
| **Total** | **165 seconds** |

Require one sentence for each:

- What goes in?
- What changes?
- Why is that technically meaningful?
- Why does the change help someone?

Sponsor proof must fit inside the core story. Do not append a separate mini-demo for each sponsor.

### Kill rules

Reject or materially rescope candidates that:

- Violate event timing, reuse, team-size, or submission requirements.
- Lack natural relevance to any confirmed track.
- Require unavailable hardware, inaccessible data, or unconfirmed funding.
- Depend on collecting users, building a marketplace, or obtaining external cooperation during the event.
- Cannot show useful behavior without a perfect live generative response.
- Require more critical-path time than the remaining build budget.
- Need hidden manual intervention presented as automation.
- Use prerecorded or cached output while claiming it proves live behavior.
- Depend on more than one unresolved research breakthrough.
- Cannot explain the core contribution within the demo budget.

Do not kill ambitious technical work merely because it is ambitious. Kill unsupported dependencies and unbounded experiments.

## 8. Expected-value reasoning

Use the objective hierarchy:

1. Deliver a valid, useful submission.
2. Preserve a serious overall-win path.
3. Prefer a robust probability of at least one judged prize.
4. Use prize utility to distinguish otherwise close alternatives.

This prevents the physical value of sponsor hardware from overriding the stated overall ambition.

### Default utility weights

These are decision-policy units, not resale prices or factual valuations.

Let \(n\) be confirmed team size.

| Prize | Utility |
|---|---:|
| Grand | 20 |
| Track first | 7 |
| Track second | 1 |
| Track third | 3 |
| IFM | 3 |
| Cursor | 3 |
| Sandia | 4 |
| People’s Favorite | 2 |
| Best Design | 2 |
| Gemini | 1 |
| ElevenLabs | 3 |
| Solana | \(1+n\) |
| Vultr | 5 |
| Auth0 | \(2+n\) |
| MongoDB Atlas | \(1+n\) |
| Raffle | 0 for project selection |

Rationale:

- Grand receives a substantial prestige weight.
- Confirmed per-teammate hardware gains value with team size.
- Swag receives a modest weight.
- Unspecified prize quantities are valued as one team award, not multiplied by four.
- Track second and third need not have utility in rank order because the physical objects differ.
- Team preference can replace these weights before launch; absent such input, use this table.

Expected utility can legitimately use:

\[
E[V]=\sum_j w_j P(W_j)
\]

Linearity of expectation does not require independence. This is different from adding prize probabilities to estimate P(any prize).

Use consistent marginals and mutually exclusive track placements. Report expected utility as a range when probabilities or prize conditions are uncertain.

### Integration decision

Add an integration only when its useful contribution and credible prize opportunity outweigh:

- Incremental implementation work.
- Shared demo-failure risk.
- Lost time for the core contribution.
- Extra explanatory burden.

An extra prize route that damages every existing route has negative strategic value even if its isolated prize probability is positive.

## 9. Selection and tournament architecture

### Clock budget

Target completion in **75 minutes**, with a **90-minute absolute cap**.

Let `T0` be the start of execution, no earlier than Friday 9:00pm EDT.

| Time from T0 | Stage |
|---|---|
| 0–10 minutes | Preflight and pilot |
| 10–40 minutes | Complete initial independent searches |
| 40–48 minutes | Normalize and select 100 → 50 |
| 48–55 minutes | Recombination and select 50 → 30 |
| 55–61 minutes | Red-team and select 30 → 15 |
| 61–68 minutes | Build/demo simulations and select 15 → 8 |
| 68–75 minutes | Twelve-reviewer jury and final selection |

Up to 15 additional minutes may absorb measured execution delays. Do not spend that allowance on another open-ended ideation round.

The latest permitted commitment time for this full process is **Friday 10:30pm EDT**. If starting late, reduce the available search budget accordingly. If the requested full population cannot fit, do not launch it under the fiction that it can.

### Capacity check

Pilot agents `001`, `021`, and `037` retain their outputs and count toward the 100.

Measure:

- Completion time.
- Output size.
- Schema validity.
- Useful distinctions among the 15 concepts.
- Rate-limit or context failures.

For `c` available worker slots and conservative measured report duration `t`, estimate:

\[
T_{\text{remaining generation}}
\approx
\left\lceil\frac{97}{c}\right\rceil t
\]

Add allowance for retries and reserve capacity for later review stages.

The current environment exposes four total agent slots including the parent, so a native implementation would ordinarily have at most three workers. Do not assume that this supports 100 completed searches within the budget. A separate verified runtime may have different capacity.

### Before the tournament

All 100 agents seal:

- Fifteen raw concepts.
- Three developed concepts.
- One nominated primary.

The 100 primaries enter the tournament. The other 200 developed candidates remain available as a recovery and recombination archive.

If an agent’s primary is invalid, replace it with its highest valid developed alternative before tournament scoring.

### 100 → 50: broad independent screening

Use concise candidate cards with names, cohort identity, and self-scores hidden.

Obtain two independent screens per candidate. Reviewers see the candidate, rules, and evidence—not other reviews.

Construct the five rankings.

Selection:

1. Take eight unique candidates from each ranking, cycling through rankings in a fixed order until 40 unique candidates are selected.
2. Fill ten additional positions using the most underrepresented credible mechanism-and-interaction clusters.
3. Apply the cluster cap from Section 2.
4. Resolve identical merit and diversity cases using stable candidate ID.

No sponsor receives a guaranteed seat.

### 50 → 30: controlled recombination

This is the first stage where designated agents may inspect multiple initial reports.

Create at most **12 challengers**:

- Up to eight recombinations.
- Up to four rescues from the developed-alternative archive.

A recombination must:

- Name its parents.
- Identify one coherent useful core.
- State what was removed from each parent.
- Explain the new behavior.
- Recompute scope and dependencies.
- Survive the same eligibility and demo tests.

Combining two sponsor stacks is not sufficient.

Evaluate the 50 incumbents and the challengers. Select:

- Five unique candidates from each of the five rankings, producing 25.
- Five additional candidates for credible diversity or major unresolved upside.

At most six of the final 30 may be challengers. If necessary, replace lower-ranked challengers with the next eligible incumbents.

### 30 → 15: adversarial review

Assign two independent reviews to each candidate:

- **Build skeptic:** Find the most likely implementation or schedule failure.
- **Judge skeptic:** Find the most likely reason the project fails to win despite working.

The author or a defender gets one response, limited to:

- Evidence.
- A scope reduction.
- A corrected claim.

No unlimited debate or late feature expansion.

Select two unique candidates from each ranking, then fill five positions with nondominated candidates that best preserve credible diversity and upside.

### 15 → 8: build and demo simulations

Give each candidate:

- One dependency-and-staffing simulation.
- One three-minute demo simulation.
- A nearest-neighbor novelty check.
- An updated sponsor eligibility assessment.
- An eight-scenario prize assessment.

These are analyses, not instructions to build 15 prototypes. Share reusable access-check results.

Select eight using the five rankings. Preserve at least two candidates from the leading overall group and two from the leading P(any prize) group when qualifying candidates exist; overlap is allowed.

A candidate that fails a hard gate cannot be retained to satisfy a quota.

### 8 → 1: twelve-reviewer jury

Use twelve fresh, independent reviewer contexts:

| Panel | Three reviewer responsibilities |
|---|---|
| Overall merit | Technical contribution; practical usefulness; originality |
| Demonstration | First-time comprehension; interaction/design; expo appeal |
| Execution | Dependency schedule; integration reliability; data/model skepticism |
| Prize strategy | Sponsor evidence; track relevance; adversarial field assumptions |

Each reviewer receives all eight cards in a deterministically randomized order and returns:

- A complete ordering.
- Top-three reasoning.
- One decisive concern per finalist.
- Confidence and evidence gaps.
- A statement of what could reverse its first choice.

The reviewers do not see prior rankings, other ballots, or persuasive defenses.

Treat this as a **simulated jury**, not twelve human judges or twelve independent empirical observations. Aggregate each three-reviewer panel before comparing panels.

### Final decision rule

1. Remove candidates failing hard constraints.
2. Prefer candidates satisfying the serious overall-win gate.
3. Remove candidates confidently dominated in P(any prize) across the scenario analysis.
4. Among the remainder, minimize worst-case rank regret across overall, P(any prize), and risk-adjusted rankings.
5. Resolve ties by panel-majority head-to-head preference.
6. Then use conservative P(any prize), overall rank, sponsor utility, upside, stressed critical-path time, and stable ID—in that order.

For a ranking with `m` eligible candidates, normalized rank regret is:

\[
\frac{\text{rank}-1}{m-1}
\]

Use zero when `m=1`.

Record one winner and one backup. The backup gets a precise switch trigger; it does not become a second project under parallel development.

Stage counts are targets. If too few valid candidates survive, advance the valid set and record the shortfall. Do not invent filler or relax hard rules to preserve the diagram.

## 10. Per-agent idea count

Keep **15 raw concepts and three developed candidates**.

Fifteen is enough to force several search directions without turning each worker into its own sprawling tournament. Three developed candidates expose local tradeoffs and preserve an alternative to the agent’s favorite.

Require each raw entry to identify:

- User and need.
- Core mechanism.
- Visible proof.
- Plausible track.
- Largest dependency or failure condition.

Limit each raw entry to approximately 55 words.

Developed entries add feasibility, sponsor use, differentiation, and demonstration details. The worker should spend more reasoning effort on selecting and falsifying its top three than on polishing all fifteen.

Do not reward exceeding fifteen. If duplicate checking leaves fewer than fifteen distinct entries, replace the duplicates within the original time budget. If the worker cannot do so, mark its report incomplete.

Generate canonical JSON once and render Markdown from it. Do not ask the model to independently author two potentially inconsistent reports.

## 11. Deceptively attractive bad ideas

| Pattern | Why it is tempting | Detection |
|---|---|---|
| Generic AI for a domain | Fast to describe and scaffold | Remove the chat interface; identify the remaining technical contribution |
| Document upload plus conversation | Easy apparent usefulness | Require a consequential transformation, decision, or workflow beyond retrieval and prose |
| “Uber for X” | Large apparent market | Test value with zero external users and no marketplace liquidity |
| Many sponsors | Appears to diversify prizes | Draw shared dependencies and identify how one failure affects all prize paths |
| Bolted-on Auth0 | Low integration cost | Separate basic eligibility from a competitive identity story |
| Atlas as a nominal users table | Easy database claim | Identify useful state behavior and observable Atlas operations |
| Vultr as an invisible URL | Easy hosting claim | Show where cloud capability affects the demonstrated result |
| Decorative Solana | Distinctive branding | Require real devnet state change and a reason for shared verification |
| Voice as an ending flourish | Produces a polished clip | Test whether live audio contributes to the essential interaction |
| IFM without access | Attractive perceived scarcity | Require a verified execution path, not workshop optimism |
| Cursor used during coding | May seem automatically eligible | Verify the actual prize bar |
| Impressive model with no usable loop | Technical novelty | Require a complete interaction and visible consequence |
| Fragile physical demonstration | Strong spectacle | Verify equipment availability, setup, reset, and cold-start behavior |
| Huge training or data plan | Signals ambition | Check data arrival, preparation, training, and fallback times separately |
| Regulated-domain authority claims | Creates apparent seriousness | Require a useful bounded demonstration without unsupported real-world claims |
| Sparse-track speculation | Looks like easy probability | Account for reduced award depth and unknown competitor strength |
| Last year’s winner with a new label | Familiar winning pattern | Compare mechanism and interaction, not name or audience |
| Beautiful mockup | Strong presentation | Identify which important behavior actually runs |
| Large numeric self-score | Appears rigorous | Demand anchors, evidence, and independent review |

## 12. One-day scope estimator

### Available time

Let:

- `selection_time` be the actual commitment time.
- `deadline` be Saturday 4:00pm EDT.
- `H` be the hours between them.

Reserve the final **four hours**:

| Period | Purpose |
|---|---|
| Saturday 12:00–1:30pm | Feature freeze, failure handling, evidence capture |
| 1:30–2:30pm | Demo rehearsal and comprehension checks |
| 2:30–3:15pm | Submission materials and uploads |
| 3:15–4:00pm | Submission confirmation and contingency |

Submit by **3:15pm** when the form permits. The official deadline remains 4:00pm.

Earlier completion creates extra polish time, not permission to add another subsystem.

### Task model

For every required work package, record:

- Owner and necessary skill.
- Dependencies.
- Optimistic, expected, and stressed duration.
- Whether it can proceed in parallel.
- External waiting time.
- Verification step.
- Whether it survives scope reduction.

Use:

\[
\mu_i=\frac{o_i+4m_i+p_i}{6}
\]

as a planning estimate, not a measured distribution.

Calculate a resource-constrained schedule, not merely the sum of estimates. Enforce one person’s available attention across overlapping tasks.

Include:

- Access and setup.
- Core algorithm or system.
- Data preparation.
- User interaction.
- Sponsor-specific work.
- Integration.
- Deployment.
- Reset and recovery.
- Demonstration preparation.

Include explicit break and reduced-availability blocks. When exact availability is unknown, plan with two effective builders. Do not assume four people provide 76 uninterrupted engineer-hours.

### Stress cases

Recompute the schedule under:

1. The hardest technical package taking its stressed duration.
2. A shared API or deployment problem delaying all dependent work.
3. One contributor being unavailable for two hours.
4. One integration requiring rework.
5. Failure of the first intended data or device path.

Correlated failures belong in the same scenario. Do not assume every work package’s overrun is independent.

Acceptance requires:

- The expected schedule reaches feature freeze comfortably.
- The stressed schedule reaches a useful, integrated minimum version before feature freeze.
- Sponsor work does not displace required demonstration or submission work.

If simulation software is available, a sampled 80th-percentile finish time may supplement this analysis. Label it **modeled P80**; it is not empirically calibrated.

### Milestones after selection

| Deadline | Required evidence |
|---|---|
| Selection + 45 minutes | Highest-risk dependency tested; keep/rescope/switch decision |
| Selection + 3 hours | Thin end-to-end useful interaction |
| Selection + 6 hours | Core technical contribution and primary sponsor path demonstrated |
| Saturday noon | Feature freeze |
| Saturday 1:30pm | Failure handling and truthful fallback validated |
| Saturday 2:30pm | Three-minute presentation rehearsed |
| Saturday 3:15pm | Submission complete when possible |

At the 45-minute gate, switch to the backup only for its recorded trigger or an equivalent critical failure. Otherwise cut scope.

A failed milestone triggers scope reduction before additional feature work.

### Demo failure assessment

Map failure points across:

- Input acquisition.
- External response.
- Computation.
- State transition.
- Rendering.
- Reset.

For the selected project, perform:

- Three ordinary complete runs.
- One cold-start run.
- One run with the highest-risk dependency degraded or unavailable.
- One run using an input not used during development.

Record actual failures and recovery time. These checks are useful evidence, not proof of a precise reliability percentage.

A fallback can preserve the explanation, but cached or recorded output must be identified honestly and cannot prove current live API use.

## 13. Failure modes of the orchestration

| Failure | Mitigation |
|---|---|
| Generation consumes the night | Pilot throughput, capacity gate, 75-minute target, 90-minute cap |
| Claimed concurrency exceeds actual capacity | Count worker slots including coordinator overhead |
| All workers anchor on the same examples | Private seeds, no parent-generated ideas, sealed outputs |
| Workers browse each other’s files | Restricted packet access or explicit procedural firewall with logs |
| Same-model agreement looks like evidence | Treat consensus as correlated; preserve dissent and scenario sensitivity |
| Self-scores become rankings | Hide them from independent screeners |
| Rubric administration exceeds reasoning time | Stage the scoring; generate structured data once |
| API research is repeated 100 times | Central verification queue and reusable factual checks |
| Sponsor count substitutes for strategy | Two intentional integrations by default; marginal-cost test |
| Recombination creates oversized projects | One coherent core; explicit deletions; complete re-estimation |
| Tournament rewards persuasive names | Anonymous candidate cards and randomized display order |
| Ranking averages hide fatal weaknesses | Hard gates before ranking |
| Novelty searches become endless | Search nearest neighbors for survivors and clusters only |
| Workshop attendance fragments the team | One delegate with a narrow verification brief |
| New workshop information restarts ideation | Update eligibility or scope; do not rerun the full search |
| Build simulations are mistaken for prototypes | Label simulated versus measured evidence |
| Jury voting becomes groupthink | Independent sealed ballots and panel aggregation |
| The backup becomes a second build | One selected project; one explicit switch condition |
| All finalists fail | One bounded repair pass; then select the strongest feasible result and disclose the shortfall |
| Worker failures make the population incomplete | One retry if the deadline permits; record missing IDs honestly |
| Late delivery is disguised as a complete run | Freeze the actual completed set and report coverage |
| Submission work is treated as an afterthought | Prepare materials early and reserve the final four hours |

No phase extends itself because its output is “almost ready.” The parent owns the clock and records every extension.

## 14. Concrete artifacts

All paths below are relative to `/Users/nicholasmino/ProgrammingFiles/HackCMU/`.

### Planning and shared inputs

```text
brainstorm/planning/astra_plan.md
brainstorm/planning/run_manifest.json
brainstorm/planning/agent_schema.json
brainstorm/planning/metric_dictionary.json
brainstorm/planning/seed_manifest.json

brainstorm/research/fact_packet.md
brainstorm/research/live_verification.md
brainstorm/research/live_verification.json
brainstorm/research/team_inventory.json
```

### Initial assignments and reports

For every zero-padded ID from `001` through `100`:

```text
brainstorm/agents/assignments/001.json
brainstorm/agents/initial/001.json
brainstorm/agents/initial/001.md
```

Continue exactly through:

```text
brainstorm/agents/assignments/100.json
brainstorm/agents/initial/100.json
brainstorm/agents/initial/100.md
```

Raw candidate IDs use:

```text
001-c01
001-c02
...
001-c15
```

The three developed candidates retain their raw IDs. Do not assign new identities when a concept is expanded.

Recombinations use `r01` through `r08`, with explicit parent IDs.

### Aggregation and tournament outputs

```text
brainstorm/selection/raw_index.jsonl
brainstorm/selection/developed_index.jsonl
brainstorm/selection/primary_100.json
brainstorm/selection/clusters.json
brainstorm/selection/shortlist_050.json
brainstorm/selection/recombination.json
brainstorm/selection/shortlist_030.json
brainstorm/selection/red_team.json
brainstorm/selection/shortlist_015.json
brainstorm/selection/build_simulations.json
brainstorm/selection/demo_simulations.json
brainstorm/selection/prize_scenarios.json
brainstorm/selection/shortlist_008.json
brainstorm/selection/rankings.json
brainstorm/selection/elimination_log.jsonl

brainstorm/jury/01.json
...
brainstorm/jury/12.json
brainstorm/jury/aggregate.json

brainstorm/selection/final_selection.json
brainstorm/selection/final_selection.md
brainstorm/selection/build_handoff.md
```

### Initial JSON contract

The following is a field contract for JSON, not a filled concept report.

**Root object: all fields required**

| Field | Type and requirement |
|---|---|
| `schema_version` | String, fixed to `astra-search-v1` |
| `run_id` | String |
| `agent_id` | Three-digit string |
| `cohort` | Assigned cohort enum |
| `model_config` | Object containing requested and actual model, reasoning mode, and runtime |
| `seed_id` | String matching the assignment manifest |
| `fact_packet_version` | String |
| `source_refs` | Array of source records |
| `started_at` | ISO-8601 timestamp with offset |
| `finished_at` | ISO-8601 timestamp with offset |
| `status` | `complete`, `incomplete`, or `failed` |
| `raw_concepts` | Array of at least 15 raw objects for a complete report |
| `developed_concepts` | Exactly three developed objects for a complete report |
| `primary_candidate_id` | ID of one developed candidate |
| `strongest_rejected_alternative` | Object with candidate ID and rejection reason |
| `assignment_deviations` | Array; empty when none |
| `unresolved_facts` | Array of fact IDs and their operational consequences |
| `access_declaration` | Object recording which permitted inputs were read and whether peer outputs were accessed |

**Source record**

```text
source_id: string
path_or_url: string
source_kind: official | local_snapshot | observation | inference
observed_at: timestamp | null
claim: string
confidence: verified | likely | unknown
```

**Raw concept object**

```text
candidate_id: string
batch: need_first | mechanism_first | assumption_reversal
label: string
user: string
need: string
mechanism: string
visible_proof: string
plausible_track: Optimization | Traveling | Multiplayer | Food
largest_dependency: string
kill_condition: string
fingerprint:
  user_job: string
  technical_mechanism: string
  interaction_loop: string
  input_dependency: string
  demo_transformation: string
disposition: developed | rejected
disposition_reason: string
```

**Developed concept object**

```text
candidate_id: string
summary: string
user_value: string
core_technical_claim: string
minimum_complete_scope: string[]
stretch_scope: string[]
explicitly_excluded_scope: string[]
inputs_and_access: Dependency[]
architecture_steps: string[]
falsification_test: TestSpec
track:
  primary: Optimization | Traveling | Multiplayer | Food
  justification_50_words: string
  relevance_score: Score
sponsor_cases: SponsorCase[]
nearest_neighbors: Comparison[]
novelty_claim: string
demo:
  beats: DemoBeat[]
  total_seconds: integer
  live_steps: string[]
  fallback: string
  fallback_limitations: string[]
  reset_seconds: integer | null
work_packages: WorkPackage[]
scores:
  official: U, T, O, D
  execution: F, R, P, S
  competitive: N, M, J, W
  strategic: A, G, H, K, Y
risks: I, API, DR, SR, CR, ER, AR, BR
assumptions: Assumption[]
kill_conditions: string[]
strongest_objection: string
response_to_objection: string
evidence_status: proposed | simulated | access_tested | implemented
```

**Supporting object contracts**

```text
Score:
  value: integer 0..4 | null
  rationale: string
  evidence_refs: string[]
  evidence_strength: low | medium | high | unassessed
  assessed_by: string
  assessed_at: timestamp

Dependency:
  name: string
  category: data | api | hardware | account | compute | people
  required_for_minimum: boolean
  access_status: verified | plausible | unavailable | unknown
  evidence_refs: string[]
  fallback: string
  failure_consequence: string

SponsorCase:
  sponsor: confirmed sponsor enum
  official_requirement: string
  requirement_source_refs: string[]
  eligibility_status:
    documented_possible | access_verified | implemented | ineligible | unknown
  intended_use: string
  removal_test: string
  capability_depth: string
  demo_proof: string
  incremental_hours_expected: number
  incremental_hours_stressed: number
  additional_failure_modes: string[]
  scores: E, C, X, B, Q
  conditional_facts: string[]

WorkPackage:
  id: string
  description: string
  owner_role: string
  dependencies: string[]
  optimistic_hours: number
  expected_hours: number
  stressed_hours: number
  external_wait_hours: number
  required_for_minimum: boolean
  completion_evidence: string

TestSpec:
  hypothesis: string
  procedure: string[]
  timebox_minutes: integer
  pass_condition: string
  failure_action: string
  status: planned | simulated | passed | failed
  evidence_refs: string[]

DemoBeat:
  start_second: integer
  duration_seconds: integer
  purpose: string
  visible_behavior: string
  proof_refs: string[]

Comparison:
  name: string
  source_refs: string[]
  similarity: string
  material_difference: string
  verification_status: checked | unverified

Assumption:
  fact_id: string
  statement: string
  confidence: verified | likely | unknown
  consequence_if_false: string
  default_action: string
```

All eight risk fields use the `Score` structure with the reversed risk direction specified in the metric dictionary.

Unassessed later-stage scores are `null` with a reason. That is a declared absence of evidence, not an unfinished planning choice.

### Final selection JSON

Require:

```text
schema_version
run_id
selected_candidate_id
backup_candidate_id
backup_switch_trigger
chosen_track
track_justification_50_words
committed_prize_targets
conditional_prize_targets
overall_gate_result
five_rankings
scenario_results
probability_method
probability_intervals
uncertainty_and_sensitivity
expected_utility_range
jury_panel_results
selection_rule_trace
rejected_finalists_with_reasons
minimum_complete_scope
scope_cut_order
critical_path
staffing_plan
first_45_minute_test
milestones
submission_requirements
remaining_unknowns_with_default_actions
decision_timestamp
```

### Validation rules

Reject or mark incomplete reports with:

- Duplicate candidate IDs.
- Fewer than 15 distinct raw entries.
- A developed candidate not present in the raw set.
- A primary not present in the developed set.
- Missing score rationale or unsupported evidence claims.
- A track outside the four confirmed choices.
- A track justification other than 50 whitespace-delimited words.
- A demo plan exceeding 165 seconds.
- Negative work estimates or stressed durations below expected durations.
- Unknown sponsor categories.
- Eligibility claims without source references.
- Unassessed fields filled with invented numbers.
- Recombination without parent IDs.
- Implemented or tested status without corresponding evidence.

Store secrets outside reports. Reports contain access status and evidence references, never API keys or tokens.

The elimination log records candidate ID, stage, reason, decisive evidence, and whether a recoverable alternative remains.

## 15. Would I launch the 100 yet?

**No. The architecture is ready, but the supplied evidence does not establish that the requested runtime, throughput, and resource assumptions are ready for a complete launch.**

The present task also explicitly prohibits launching agents. None were launched.

For the later execution, perform the ten-minute preflight and pilot, then apply these rules without waiting indefinitely for clarification.

### Mandatory launch conditions

- The permitted hacking/design start has arrived.
- The requested model configuration is actually available.
- Pilot reports demonstrate adequate quality and throughput.
- The full initial phase plus review stages fit before the commitment deadline.
- The fact packet, private assignments, schema, and report isolation are ready.
- Actual staffing is recorded, or the two-effective-builder fallback is used.

Missing sponsor access does not block the whole population. It changes assignments.

### Allocation-changing unknowns and fixed responses

| Finding before assignments freeze | Action |
|---|---|
| K2 access or feasibility unverified at preflight close | Reassign `094–095` to open-world and `096–097` to demo-first |
| Vultr cannot provision required resources within confirmed credits | Reassign `045–048` to open-world and `049–052` to demo-first |
| Sandia requirements exclude the team or cannot support a credible eligible path | Reassign `098–100` to open-world |
| Another MLH sponsor is inaccessible | Reassign the first four IDs in that cohort to open-world and the remaining four to demo-first |
| Cursor requirements are confirmed, feasible, and require a distinct search direction | Reassign `077–078` from stackers to Cursor specialists, preserving their IDs |
| Cursor merely requires documented use during development | Keep allocation unchanged and capture the required evidence during the selected build |
| IFM occupies the only track selection and prevents ordinary track entry | Retain IFM only as an explicitly competing track strategy; remove assumed IFM-plus-themed-track stacking |
| Reliable field information arrives | Update scenario assessments; do not infer easy wins from headcount alone |
| Verified capacity cannot complete the requested population in time | Do not launch the full 100; record the capacity failure and use a separately labeled reduced run if the parent must proceed |
| Too little time remains for this pipeline | Prioritize commitment and building; never describe partial coverage as the completed 100-agent search |

Freeze assignment changes at the start of the main generation phase. Later factual discoveries may invalidate eligibility, reduce scope, or alter finalist rankings; they do not restart the population.

The final handoff must contain **one selected candidate, one conditional backup, one track, a bounded prize strategy, a staffed build schedule, and the first falsification test**.
