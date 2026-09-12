# Search plan

## Objective

Select one project with exactly one primary HackCMU track and one primary sponsor prize. The objective is the probability of winning that pair, conditioned on a working, memorable three-minute demo, with overall-winner upside as a secondary tie-breaker. Sponsor stacking, idea count, and score theatrics are not objectives.

## Evidence and constraints

- The live opening-deck capture lists Optimization, Traveling, Multiplayer, and Food. One track and a 50-word justification are submitted; relevance is a judging dimension.
- Submission is at 4:00 p.m. EDT Saturday, with a three-minute presentation/demo. The usable build horizon is about 19 hours.
- Official judging names usefulness, technical difficulty, originality, demo quality, and track relevance.
- The only confirmed MLH sponsor prizes are Gemini, ElevenLabs, Solana, Vultr, Auth0, and MongoDB Atlas. IFM/K2, Cursor, and Sandia are separate event prizes with incomplete public criteria.

Sources: [Devpost](https://hack-cmu-2026.devpost.com/), [rules](https://hack-cmu-2026.devpost.com/rules), [MLH HackCMU prizes](https://www.mlh.com/events/hackcmu/prizes), locally preserved opening-deck transcript in `MLH_OFFICIAL_TRANSCRIPT.md` section K.

## Search design

1. **Establish ground truth.** Treat the public site, Devpost, MLH event page, and captured opening deck as separate sources. Mark a claim VERIFIED only when an official source supports it; label access, track-form, rubric, and field-size gaps UNKNOWN.
2. **Build the pair matrix.** Score all four tracks × six confirmed MLH prizes, and explicitly reject the incoherent cells before ideation. Track and sponsor are constraints, not tags added afterward.
3. **Generate independent cohorts.** Cover need-first, mechanism-first, non-LLM, demo-first, research-demo, practical, and sponsor-capability-first ideas. The provenance records include independent workers and prior work; no worker sees an emerging leaderboard.
4. **Filter before scoring.** Kill a candidate if its sponsor can be replaced by commodity infrastructure without changing the product, its track explanation is cosmetic, its demo needs a long explanation, or its closest implementation already provides the central experience.
5. **Research prior art twice.** Search exact wording and the broader underlying mechanism across product sites, GitHub, Devpost/MLH winners, and academic work. Classify NOVEL, DIFFERENTIATED, CROWDED, or ALREADY EXISTS. Eliminate ALREADY EXISTS; retain CROWDED only with a named, demo-visible distinction.
6. **Preserve raw scores.** Score the official axes, execution, competition, track, sponsor, strategic upside, and risk values separately. Do not create a misleading single probability ranking before adversarial review.
7. **Cluster and recombine.** Cluster by user job, core mechanism, input/data dependency, interaction loop, proof, and external dependency. High convergence triggers scrutiny. Recombine only when a mutation improves the winner's core loop without adding a second prize target.
8. **Red-team and simulate.** For semifinalists, independently ask advocate, HackCMU judge, sponsor judge, technical skeptic, product skeptic, novelty skeptic, and ruthless critic questions. Build a four-person hour-by-hour plan, a fallback, and a 90-second narrative before a finalist can advance.
9. **Fresh jury.** Give finalists and evidence to independent personas; require a full ranking and pairwise reasons. The jury cannot introduce new unresearched projects.

## Quality gates

| Gate | Advance only if |
|---|---|
| Pair integrity | One track and one sponsor are named; both would weaken materially if removed. |
| First-10-seconds | A judge sees a concrete input changing a meaningful visual or audible output. |
| Sponsor proof | The primary sponsor is visible in the core loop, with an artifact the judge can inspect. |
| Track proof | The same one-sentence product pitch answers the track question without a separate justification. |
| Prior art | The closest existing item and the material distinction are named. |
| Feasibility | The minimum winning version fits roughly 28–34 person-hours and has a tested fallback. |
| Demo reliability | A scripted demonstration works on known input and degrades honestly to a local/precomputed fallback. |

## Scoring dictionary

All positive dimensions use 0–10, where 10 is best. Risks use 0–10, where 10 is worst. `B` is the sponsor bolt-on penalty, also worse when higher.

| Category | Fields |
|---|---|
| Official judging | U usefulness, T technical complexity, O originality, D demo/presentation |
| Execution | F feasibility, R demo reliability, P polishability, S judge-visible value per engineering hour |
| Competition | N field-relative novelty, M memorability, J judge comprehension, W wow factor |
| Track | TF track fit, TC expected competitiveness in that track |
| Sponsor | E eligibility confidence, C centrality, X unique capability exploitation, Q sponsor-prize competitiveness |
| Strategic | G overall upside, H team advantage, K killer-demo density, Y story coherence |
| Risk | I integration, API external API, DR demo, SR scope, CR commodity/wrapper, ER explanation, AR prior-art, BR boredom, B bolt-on |

## Time-boxed execution model

The original task asks for broad search, but the build time is the dominant constraint. The search is therefore a completed research package, not a live prescription to delay implementation. In a live hackathon, freeze at the first credible ranked shortlist and start construction; do not wait for arbitrary idea-volume targets.

