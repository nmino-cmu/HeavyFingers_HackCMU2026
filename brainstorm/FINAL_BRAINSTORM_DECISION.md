# HackCMU 2026 — final prize-optimized decision

## Decision

**Build Ask Once.**  
**Declared track:** Food  
**Primary sponsor target:** Gemini API  
**One-line pitch:** A pantry worker photographs an ambiguous donation label; Ask Once turns it into an evidence-tagged ingredient graph and asks the one staff question that unlocks the most policy-eligible portions without guessing.

The decision optimizes for a credible overall/track-winning demo while keeping a real Gemini Best Use path. It does not assume sponsor prizes stack, invent eligibility bars, or treat “uses an API” as a sponsor case.

This choice is conditional on an early technical proof. If the proof fails, the first fallback is **StaleMap — Traveling × MongoDB Atlas**; the high-upside non-Gemini fallback is **CycleClear — Optimization × Solana**, but only after its devnet atomic settlement works.

## Constraints that shaped the decision

The authoritative local opening-deck record says the build window is about 19 hours, teams pick one track, Baggage Check is Saturday 4:00pm EDT, and judges score originality, technical difficulty, demo quality, usefulness, and track relevance. The presentation/demo is three minutes. Sponsor prizes are not track-locked, but projects should use and demonstrate the sponsor they name. See [competition ground truth](research/competition_ground_truth.md) and the official [Devpost rules](https://hack-cmu-2026.devpost.com/rules).

The relevant verified prize surface is Gemini, ElevenLabs, Solana, Vultr, Auth0, and MongoDB Atlas. The opening deck also lists IFM, Cursor, Sandia cybersecurity, People’s Favorite, and Best Design prizes, but their additional qualification bars are partly unknown. No prize was invented for logo sponsors such as Microsoft, Adobe, Jane Street, Citadel, or Roblox.

The full 4-track × sponsor assessment, including caveats for non-MLH prizes, is in [track_sponsor_matrix.md](research/track_sponsor_matrix.md). The highest generic pair score is not automatically the best project: it can lack a defensible candidate, a demo transformation, or a sponsor-central mechanism.

## Why Ask Once wins

Ask Once is the rare finalist whose single action makes all five primary judging axes visible:

| Axis | Judge-visible evidence |
|---|---|
| Usefulness | Staff stop discarding or underusing an ambiguous donation because they learn exactly what clarification matters. |
| Technical difficulty | Multimodal evidence extraction, typed uncertainty/provenance, constrained bipartite allocation, and expected-information-gain question selection all interact. |
| Originality | The narrow interaction is not “scan food” or “match donated food”; it is selecting the one staff-confirmable fact that changes the allocation. |
| Demo quality | A red/uncertain graph and 1/4 eligible allocation become green and 4/4 after a single answer. |
| Food relevance | The user, input, constraint, and outcome are all food-handling decisions. |
| Gemini centrality | Gemini extracts structured visual evidence from a label. Remove that visual-evidence primitive and the product loses its intake interaction. |

The fresh jury’s required-perspective aggregate ranked Ask Once first on 89 Borda points and as the Condorcet winner. It beat StaleMap 10–2, CycleClear 9–3, and Airlock 11–1 in the jury’s explicit pairwise comparisons. Read the complete independent simulation in [fresh_jury.md](agents/jury/fresh_jury.md).

## Exact product boundary

**User:** a food-pantry or community-kitchen worker receiving ambiguously labeled donated food.  
**Moment:** the worker must decide whether a portion can be allocated under recorded household constraints, but a label leaves one or more ingredients uncertain.  
**Outcome:** the system withholds uncertain allocations, identifies the question with the largest expected allocation gain, records a staff-confirmed answer, and recomputes eligible portions.

**Draft Food-track statement (46 words):** Ask Once helps pantry workers allocate ambiguously labeled food under recorded household constraints. It turns a label into an evidence graph, identifies the one clarification that unlocks the most policy-eligible portions, and shows transparent reasoning rather than guessing. The food-intake and allocation workflow is the product.

Ask Once must say **“eligible under recorded policy after staff confirmation.”** It must not infer allergens as facts, diagnose users, certify food, promise safety, or replace local food-handling policy. That boundary is essential both ethically and competitively.

The closest prior art includes mature food-rescue matching and routing systems such as [RescueRoute](https://rescueroute.org/), [Replate](https://blog.replate.org/blog/a-major-milestone-replate-receives-patent-for-food-recovery-technology), and [Knead](https://kneadtech.com/). Visual food-recognition is also crowded. Those findings kill a generic “AI food-rescue matcher.” They do not establish that the narrower evidence-to-one-human-question interaction is already a product; it remains a conditional differentiation claim, recorded in [decision_evidence.md](research/prior_art/decision_evidence.md).

## Product and technical flow

~~~mermaid
flowchart LR
  I[Ambiguous label photo] --> G[Gemini structured evidence]
  G --> E[Evidence graph: fact / uncertainty / source]
  E --> M[Conservative allocation solver]
  M --> Q[Expected-information-gain question selector]
  Q --> H[Staff confirms one fact]
  H --> M
  M --> R[Policy-eligible allocation + audit]
~~~

1. Capture one controlled donation-label photo.
2. Gemini returns schema-validated evidence objects: ingredient candidate, confidence/uncertainty, visible source fragment, and status.
3. The app turns those objects into an explicit graph. Unknown hard constraints remain blocked.
4. A matching solver assigns portions only where all recorded constraints pass.
5. For each allowed clarification question, the app estimates the number/value of allocations it could unlock and chooses the highest-value question.
6. A staffer confirms or declines the answer. The graph, matching result, and audit update visibly.

This leaves a real non-LLM technical core on screen. Gemini is not asked to decide who can receive food or to supply an allergy judgment.

Gemini supports structured output, which makes schema-constrained evidence extraction feasible; see the official [Gemini structured-output documentation](https://ai.google.dev/gemini-api/docs/structured-output). The design should display the extracted evidence alongside the original label so judges can see what the model did and what it did not know.

**Why now:** community food programs already receive ambiguous donations, while current multimodal APIs can turn messy visual evidence into a constrained schema quickly enough for a live intake interaction. The opportunity is not a claim that food-rescue software is absent; it is that current systems make it practical to put uncertainty and a value-of-information question on one worker-facing screen.

## Build gate and minimum winning version

Run the following test before committing past the first two hours:

1. Use a prepared handwritten label whose uncertainty is real but controlled.
2. Get valid Gemini structured output with source-linked evidence.
3. Render four household cards with explicit recorded constraints.
4. Show only one policy-eligible allocation.
5. Have the app ask a single question, such as “Does the sauce contain sesame?”
6. Enter a human-confirmed response and show the eligible count change to four.

**Minimum winning version:** one item, two uncertain facts, four household constraints, one question, one numerical before/after allocation change.  
**Do not build:** a marketplace, driver routing, accounts, health profiles, recipe suggestions, generalized OCR, a recommendation chatbot, or automated safety scoring.

| Time | Owner focus | Deliverable |
|---|---|---|
| H0–H2 | A: Gemini, B: graph/matching, C: before/after UI, D: fixture/policy | Valid visual-evidence JSON and static 1/4 state |
| H3–H5 | A+B | Live question selection and 1/4 → 4/4 allocation proof |
| H6–H11 | C+D with A+B hardening | Guided flow, provenance, refusal case, cold 90-second run |
| H12–H15 | Whole team | Scope freeze, fallback artifact, explanation of policy limits |
| H16–H19 | Whole team | Demo rehearsal, backup capture, submit, three-minute presentation |

The full hour-level plan for Ask Once and all 11 alternatives is in [top_12_build_simulations.md](agents/build_sim/top_12_build_simulations.md).

This selection uses technical strengths only where they create a judge-visible edge: one person owns multimodal schema grounding, one owns graph/matching/value-of-information logic, one owns the decisive visual flow, and one owns fixtures, safety boundary, and rehearsal. It does not require hardware, model training, a marketplace, or an external partner.

## Ninety-second proof sequence

| Seconds | What the judge sees | What it proves |
|---:|---|---|
| 0–10 | A label photo and four household cards; only 1/4 is eligible. | Real food-handling constraint and a clear bad before-state. |
| 10–25 | Gemini evidence graph marks a sauce attribute uncertain, with source evidence. | Gemini does structured extraction, not a chat response. |
| 25–40 | The system asks one highlighted question and displays its expected allocation gain. | The algorithm selects an information-rich human interaction. |
| 40–60 | Staff confirms a fact; graph and allocation animate to 4/4. | The central transformation is measurable and immediate. |
| 60–78 | Each allocation has a policy/evidence explanation; blocked alternatives remain blocked. | Conservative behavior and technical rigor. |
| 78–90 | A second ambiguous item is shown only as a queued next case; close with the audit. | The product is a repeatable workflow, not a staged answer. |

Use a controlled fixture and retain a source-visible cached Gemini response as a network fallback. Do not fake a live answer or hide a model failure. The complete semifinal demo stress test is in [semifinal_90s.md](agents/demo_sim/semifinal_90s.md).

### Failure points, fallback, and stretch

| Risk | Mitigation / decision |
|---|---|
| Gemini fails to produce grounded structured evidence | Use a pre-warmed response tied to the visible controlled label; if the result cannot be source-linked, do not claim live extraction. |
| Ambiguous phrasing drifts into an allergen/safety claim | Constrain vocabulary to evidence, uncertainty, recorded policy, confirmation, and eligibility. Add an explicit refusal path. |
| The selected question does not materially change matching | Use a fixture engineered around a real hard-constraint branch; if no allocation flips at H5, abandon the project. |
| Scope expands into marketplace/routing/account features | Freeze at one item, one question, and four allocations. |

**Fallback:** source-visible cached model output for the same controlled input; graph, allocation, and question-ranking logic remain live.  
**Stretch only after H15:** second item queue; clarification-cost weighting; bilingual label evidence; a second, non-allergen policy class. None may replace the core one-question transformation.

**Strongest competing project:** a polished CycleClear or StaleMap demo could exceed Ask Once in technical spectacle or sponsor specificity.  
**Strongest reason not to build Ask Once:** the food-rescue category is crowded and an unsafe-sounding pitch can disqualify its credibility.  
**Why it still wins this selection:** the narrow evidence-to-question-to-allocation change is unusually compact, humane, and demonstrable, while its safety boundary is a visible product behavior rather than a disclaimer.

## Probabilities and score interpretation

The candidate database uses explicit ranges rather than fabricated precision. They are decision heuristics, not independent event probabilities; sponsor and track outcomes correlate with demo quality.

| Metric | Ask Once estimate |
|---|---:|
| P(credible MVP) | ~68–82% |
| P(polished demo) | ~54–69% |
| P(demo works live) | ~75–88% |
| P(Food track prize) | ~14–25% |
| P(Gemini prize) | ~12–23% |
| P(at least one of track/sponsor) | ~25–42% |
| P(overall win) | ~6–12% |
| P(no prize) | ~58–75% |

The full 31-dimension vector for F13 is in [all_candidates.json](results/all_candidates.json). Its strong dimensions are demo transformation, track fit, sponsor centrality, technical substance, and low build risk relative to high-upside alternatives. Its weak point is not a number: the team must earn the safety/credibility framing by showing uncertainty rather than hiding it.

## Portfolio leaderboard

This is a project-level ranking after ground truth, prior-art filtering, deduplication, adversarial elimination, build simulation, and the fresh jury. It is deliberately not a list of prize names.

| Rank | Candidate | Track × primary sponsor | Why it remains | Main gate |
|---:|---|---|---|---|
| 1 | **Ask Once** | Food × Gemini | Best overall before/after, human value, and Gemini-evidence use. | One human answer must change conservative allocation. |
| 2 | **StaleMap** | Traveling × MongoDB Atlas | Strong fallback; fresh evidence visibly changes an accessible route. | An Atlas-backed report must reroute live. |
| 3 | **Airlock / Proxy Passport** | Traveling × Auth0 | Security is the product, not a login screen. | A protected action must deny, then approve and audit. |
| 4 | **CycleClear** | Optimization × Solana | Strongest sponsor proof and algorithmic wow when atomicity works. | Four-way devnet settlement and reject branch. |
| 5 | **Bracket Patch / ConstraintLens** | Optimization × Gemini | Most feasible polished visual optimization demo. | Photo-to-unsat-core-to-minimal-repair without retyping. |
| 6 | **Triangulate** | Multiplayer × Gemini | Active evidence gathering is deeper than summary. | It must assign and resolve a discriminating observation. |
| 7 | **Sizzle Oracle** | Food × ElevenLabs | Memorable sound-to-action event. | A real acoustic state must beat noise and trigger one intervention. |
| 8 | **FairTable** | Multiplayer × Solana | Private commitment has a tangible trust property. | Commit/reveal must prevent a demonstrated edit attack. |
| 9 | **Resilience Canvas** | Optimization × Vultr | Robust plan under failure can create a powerful visual. | Remote computation must change the chosen allocation. |
| 10 | **RumorClock** | Multiplayer × MongoDB Atlas | Shared confidence decay is intuitive if genuinely multi-user. | Another user’s evidence must update all views. |

**Pareto frontier:** Ask Once is the best balance. CycleClear leads on sponsor-specific technical proof. StaleMap leads on immediate public usefulness and demo clarity outside Gemini. Airlock leads on security/authorization depth. Bracket Patch is the safest polished build. No single point dominates all of those dimensions.

### Numeric leaderboard scorecard

The score legend is: official judging U/T/O/D; track fit/competitiveness TF/TC; sponsor eligibility/centrality/exploitation/competitiveness/bolt-on E/C/X/Q/B; execution feasibility/reliability/polish/value-per-hour F/R/P/S; competition novelty/memorability/comprehension/wow N/M/J/W. Higher is better except B and risk fields. The primary prior-art risk below is the AR score, where higher is worse.

| Rank | Project | U/T/O/D | TF/TC | E/C/X/Q/B | F/R/P/S | N/M/J/W | Prior-art risk | P(demo) | P(track) | P(sponsor) | P(either) | P(overall) | Primary risk |
|---:|---|---|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | Ask Once | 9/9/9/10 | 10/8 | 9/10/10/8/2 | 8/7/8/10 | 8/10/9/10 | 5 | 75–88% | 14–25% | 12–23% | 25–42% | 6–12% | safety framing / label grounding |
| 2 | StaleMap | 9/8/8/9 | 10/8 | 9/10/9/9/1 | 7/8/8/9 | 8/8/9/9 | 5 | 76–88% | 12–23% | 13–25% | 24–41% | 5–10% | evidence must reroute live |
| 3 | Airlock | 9/8/8/9 | 10/8 | 8/10/10/9/1 | 7/7/8/9 | 8/9/9/9 | 4 | 72–86% | 12–22% | 15–27% | 24–40% | 5–10% | auth sample / external action setup |
| 4 | CycleClear | 8/9/9/9 | 10/8 | 9/10/10/9/1 | 7/8/7/9 | 9/9/8/9 | 3 | 75–88% | 14–24% | 16–28% | 26–42% | 5–10% | devnet and wallet variance |
| 5 | Bracket Patch | 8/8/7/9 | 10/7 | 9/9/9/7/2 | 9/8/8/9 | 7/8/9/9 | 5 | 78–90% | 10–20% | 8–16% | 17–31% | 4–8% | crowded scheduling/OCR neighborhood |
| 6 | Triangulate | 8/9/9/9 | 10/8 | 9/9/10/8/2 | 7/7/7/9 | 9/9/8/9 | 4 | 70–84% | 12–22% | 11–21% | 21–37% | 5–10% | could become a summary wrapper |
| 7 | Sizzle Oracle | 8/8/8/9 | 10/7 | 9/10/9/8/2 | 7/7/8/8 | 8/9/9/9 | 5 | 70–84% | 9–18% | 10–20% | 18–34% | 3–8% | acoustic robustness / voice-cooking prior art |
| 8 | FairTable | 7/8/9/9 | 10/7 | 9/10/10/9/1 | 6/7/8/8 | 9/9/9/9 | 4 | 70–84% | 10–20% | 12–23% | 21–37% | 4–9% | wallet friction / low user stakes |
| 9 | Resilience Canvas | 8/9/8/9 | 9/8 | 9/10/9/8/2 | 5/6/6/8 | 8/8/8/9 | 6 | 60–78% | 10–19% | 11–21% | 18–34% | 5–11% | scope and cloud integration |
| 10 | RumorClock | 7/8/9/8 | 9/7 | 9/9/8/8/2 | 9/8/8/8 | 9/7/7/8 | 4 | 78–90% | 8–16% | 9–18% | 16–30% | 3–7% | insufficiently compelling shared outcome |

## Best track × sponsor pairs

The matrix produces attractive pairs only when a candidate makes the sponsor’s distinctive behavior visible.

| Pair | Best retained mechanism | Why it is strategically attractive | Constraint |
|---|---|---|---|
| Food × Gemini | Ask Once | Structured visual evidence can unlock a constrained human decision with an immediate before/after. | Avoid all generic food scanning or safety claims. |
| Traveling × MongoDB Atlas | StaleMap | Time-decaying field evidence and route recomputation make data persistence/realtime state legible. | Accessibility maps are close prior art; rerouting is mandatory. |
| Traveling × Auth0 | Airlock | Scoped delegated action has a natural high-stakes travel failure mode. | Must prove protected denial/approval, not login. |
| Optimization × Solana | CycleClear | Atomic cycle settlement maps directly to a constrained exchange outcome. | A devnet program must settle real reservation rights. |
| Optimization × Gemini | Bracket Patch | Image-to-constraint extraction makes an optimization repair intuitive. | Limit to a fixed board grammar and a minimal patch. |
| Multiplayer × Gemini | Triangulate | Multimodal evidence can direct a teammate to collect the next fact. | It must not become a group-summary interface. |
| Optimization × Vultr | Resilience Canvas | Parallel failure-world simulation can visibly change a robust allocation. | Hosting is insufficient; remote compute must alter the answer. |

## Why the near-winners are not the recommendation

| Candidate | Why it is strong | Why Ask Once is ahead |
|---|---|---|
| StaleMap | Great route-change demo, credible Atlas role, meaningful travel/accessibility use case. | Its data/evidence story is harder to ground in a 90-second controlled fixture, and accessibility mapping has closer established alternatives. |
| Airlock | Auth0 can be visibly load-bearing through denied actions and approvals. | It risks reading as an authorization demo with a travel skin; external-action scope can consume the build. |
| CycleClear | Atomic multi-party settlement is technically impressive and a clean Solana case. | Anchor/wallet/network variance and the need to explain why a ledger is necessary lower the chance of a polished overall demo. |
| Bracket Patch | Easiest route to a crisp visual repair and an Optimization fit. | Whiteboard/schedule tooling is crowded, and its novelty ceiling is lower. |
| Triangulate | Strong Gemini multimodal mechanism and authentic multiplayer transition. | Its user/stakes take longer to explain; it can devolve into an evidence-summary wrapper. |
| Sizzle Oracle | High sensory memorability and strong voice use. | Sound classification robustness and voice-cooking prior art leave less room for error. |
| FairTable | Clear Solana manipulation-defense proof. | Wallet friction and a small decision domain weaken usefulness. |

## Immediate pivot packets

### StaleMap — Traveling × MongoDB Atlas

Build a two-route accessibility fixture, a timestamped-report document model, a freshness/conflict score, and a deterministic route-cost recomputation. The 90-second path is green route → outage report → red confidence → alternate route → restoration evidence. Start only if an Atlas write and second-client update work by H2. The minimum winning version has one elevator edge and three reports; the full implementation adds a map and photo provenance. It is the preferred pivot when Ask Once’s Gemini evidence gate fails.

### Airlock — Traveling × Auth0

Build a protected first-party mock-airline API, Auth0 scopes for search/hold/cancel, a permission card, and an audit view. The 90-second path is request → allowed hold → real denied cancellation → user approval → protected success → audit. Start only if an unauthorized request is denied by H2. The minimum winning version has one traveler, one allowed action, one denied action, and one approval; do not integrate a real airline.

### CycleClear — Optimization × Solana

Build a fixed four-person reservation graph, a cycle solver, a minimal Anchor program, pre-funded devnet wallets, and a state transition view. The 90-second path is failed bilateral exchanges → highlighted 4-cycle → all approvals → one devnet settlement → rejection leaves all original rights intact. Start only if a program invocation yields a confirmed transaction at H2. The minimum winning version is a fixed cycle and rejection branch; no marketplace, token, or open matching.

## Do-not-build list

These are eliminated mechanisms, not merely lower-ranked ideas. Reversing the decision would require new evidence of a materially different core interaction.

| Do not build | Reason | Evidence |
|---|---|---|
| Generic food-rescue matching, donor/driver routing, or surplus marketplace | Mature products already match, route, and coordinate the exact multi-sided loop. | [RescueRoute](https://rescueroute.org/), [Replate](https://blog.replate.org/blog/a-major-milestone-replate-receives-patent-for-food-recovery-technology), [Knead](https://kneadtech.com/), [evidence ledger](research/prior_art/decision_evidence.md) |
| Generic visual food recognition, nutrition log, or food-safety scanner | Visual-food-recognition research and products are crowded; adding a model does not create a decision workflow. | [Large Scale Visual Food Recognition](https://arxiv.org/abs/2103.16107) |
| Voice recipe assistant / narrated cooking guide | Voice-first cooking tools and research already cover the basic experience. | [AskChef](https://www.ask-chef.com/), [Heard Recipes](https://heardrecipes.com/), [VoiceCookingAssistant](https://aclanthology.org/2021.icnlsp-1.30/) |
| Video-to-time-study or process-mining app | Existing products already turn work video into process steps and time studies. | [Process Study](https://process.study/), [SHOWHOW](https://showhow.emplif.ai/en), [Proxima](https://proxima.vision/) |
| Camera board-game referee/rules assistant | Camera identification, live tracking, and rule assistance already have close products and contest projects. | [Board Law](https://ai.google.dev/competition/projects/board-law), [Start2Play](https://www.start2play.app/), [KnightVision](https://www.knightvision.app/) |
| Generic board-game rules chatbot | Rulebook-grounded assistants already exist. | [Board Game Genie](https://www.boardgenie.app/), [Game Guru](https://gameguruapp.com/) |
| Generic Gemini itinerary generator | Gemini multi-agent itinerary projects and commercial planners cover the core product. | [TripCraft](https://github.com/mtwn105/TripCraft) |
| Generic travel translation / voice concierge | Translation and voice-assistant products make the premise crowded. | [prior-art ledger](research/prior_art/decision_evidence.md) |
| General crowd-flow digital twin | Recent research and platforms already cover real-time crowd simulation and camera-fed crowd systems. | [micro-modelling study](https://www.sciencedirect.com/science/article/pii/S219643862500734X), [Kobe digital twin](https://link.springer.com/article/10.1007/s10015-024-00941-y) |
| “Deploy on Vultr” as the whole sponsor argument | Hosting alone is unlikely to make a distinctive Best Use case. | [Vultr matrix assessment](research/track_sponsor_matrix.md) |
| Auth0 social login pasted into an otherwise unrelated app | It fails the sponsor-removal test. | [Auth0 AI-agent overview](https://auth0.com/ai/docs/intro/overview) |
| Atlas as a conventional CRUD datastore | It fails the sponsor-removal test unless durable live state, geo, vector, or evidence history changes the product. | [MongoDB Atlas docs](https://www.mongodb.com/docs/atlas/) |
| Solana token, NFT, or wallet veneer | It fails unless a real settlement/commitment property visibly changes trust. | [Solana docs](https://solana.com/docs) |

## Audit trail and artifact index

| Requirement | Artifact |
|---|---|
| Verified / likely / unknown event and prize facts | [research/competition_ground_truth.md](research/competition_ground_truth.md) |
| Full track × sponsor matrix | [research/track_sponsor_matrix.md](research/track_sponsor_matrix.md) |
| Search plan and eight independent audits | [planning/search_plan.md](planning/search_plan.md), [planning/search_plan_audit.md](planning/search_plan_audit.md), [planning/audits](planning/audits) |
| Coverage and candidate provenance | [research/search_coverage_ledger.md](research/search_coverage_ledger.md), [results/candidate_provenance.md](results/candidate_provenance.md) |
| Prior-art evidence and decisions | [research/prior_art/decision_evidence.md](research/prior_art/decision_evidence.md) |
| All 34 structured candidates | [results/all_candidates.json](results/all_candidates.json) |
| Deduplication/convergence analysis | [results/idea_clusters.md](results/idea_clusters.md) |
| Semifinalists and battle cards | [results/semifinalists.md](results/semifinalists.md), [results/finalists.md](results/finalists.md) |
| Recombination / second novelty pass | [agents/recombination/mutations.md](agents/recombination/mutations.md) |
| Independent adversarial elimination | [agents/red_team/adversarial_elimination.md](agents/red_team/adversarial_elimination.md) |
| Build and demo simulations | [agents/build_sim/top_12_build_simulations.md](agents/build_sim/top_12_build_simulations.md), [agents/demo_sim/semifinal_90s.md](agents/demo_sim/semifinal_90s.md) |
| Fresh final jury | [agents/jury/fresh_jury.md](agents/jury/fresh_jury.md) |

## Source note

Competition facts come from the local opening-deck transcript and the official [HackCMU Devpost](https://hack-cmu-2026.devpost.com/), [rules](https://hack-cmu-2026.devpost.com/rules), [ACM@CMU event page](https://www.acmatcmu.com/hackcmu2026/), and [MLH prize page](https://www.mlh.com/events/hackcmu/prizes). Sponsor claims should be verified against the linked official Gemini, Auth0, Solana, Vultr, ElevenLabs, and MongoDB documentation immediately before submission if the team changes the selected project.
