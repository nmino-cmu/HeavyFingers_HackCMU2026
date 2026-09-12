# Finalist battle cards

All eight cards below have one track and one primary sponsor. A sponsor is named only where it powers the core proof. The allowed novelty claims are intentionally modest and are grounded in [the evidence ledger](../research/prior_art/decision_evidence.md).

## 1. Ask Once — Food × Gemini

**Opening scene:** A volunteer photographs a handwritten donation label. The screen draws uncertain ingredient nodes and shows only 1 of 4 household allocations as policy-eligible. It asks: “Does the sauce contain sesame?” A staff-confirmed answer unlocks 4 of 4.

**Proof to show:** Gemini multimodal structured output; a visible evidence graph; conservative matching; an expected-information-gain calculation choosing that question; a before/after allocation.

**Boundary:** Food-rescue networks exist. This may claim a narrow intake-clarification workflow, not food-rescue matching, allergy assessment, or food-safety certification.

**Kill condition:** Any inferred allergen shown as fact, or no measured change after the answer.

## 2. CycleClear — Optimization × Solana

**Opening scene:** Four people each want a different constrained reservation. A graph finds one 4-way exchange. All approve. Four reservation rights move together in one devnet transaction.

**Proof to show:** objective/constraint display, cycle finder, actual program state, explorer signature, then a declined participant leaving everyone unchanged.

**Boundary:** Dynamic barter and atomic-swap research exist. The claim is a small, concrete reservation-rights clearing interaction with visible all-or-nothing settlement.

**Kill condition:** A central server settles the cycle, or the program merely records a decorative hash.

## 3. Airlock (Proxy Passport) — Traveling × Auth0

**Opening scene:** A stranded traveler gives an assistant a passport card: search and hold are allowed; cancel is forbidden. The assistant finds a replacement. It can hold, but cancel is denied until the traveler approves.

**Proof to show:** Auth0 identity and scoped authorization protect every mock-airline action; a denied response and an approval event are both visible; audit log shows the reason.

**Boundary:** Agent delegation is already an Auth0-supported capability and travel role controls exist. The claim is a traveler-facing, per-trip action contract.

**Kill condition:** A role dropdown substitutes for a real enforcement check.

## 4. Triangulate — Multiplayer × Gemini

**Opening scene:** Three teammates disagree about a live observation through a photo, a voice note, and text. The app marks a contradiction and sends one teammate to get the photo that resolves it. The group state changes.

**Proof to show:** source-linked Gemini structured claims, shared claim graph, a discriminating observation request, and a conservative confidence update.

**Boundary:** Crisis reporting systems collect evidence. The claim is active, multimodal disambiguation that directs the next group action.

**Kill condition:** It only summarizes submitted reports.

## 5. StaleMap — Traveling × MongoDB Atlas

**Opening scene:** An accessible route is green. A report says the elevator is unavailable. Its confidence and freshness shift red, and the route changes. A new photo can restore the route.

**Proof to show:** timestamped claims, conflict/freshness rule, Atlas-backed evidence history, and real route recomputation.

**Boundary:** Accessibility maps and transit alerts exist. The claim is that uncertain, expiring evidence drives routing rather than merely appearing as a map pin.

**Kill condition:** Reporting does not change the recommended route.

## 6. Bracket Patch (ConstraintLens) — Optimization × Gemini

**Opening scene:** A phone looks at a messy sticky-note schedule. The app finds a red unsatisfiable core and animates the smallest two-task repair.

**Proof to show:** Gemini produces a typed constraint JSON; a solver identifies the conflict; minimal repair changes the board.

**Boundary:** Whiteboard digitizers and scheduling tools exist. The claim is image-to-constraint-to-explainable-minimal-repair in one interaction.

**Kill condition:** Manual re-entry is needed to make the solver work.

## 7. Sizzle Oracle — Food × ElevenLabs

**Opening scene:** A real or pre-recorded pan sound crosses a cooking-state threshold. A voice interrupts only once: “Turn it now.” The cook replies “done.”

**Proof to show:** signal trace, state transition, concise responsive voice, and spoken confirmation changing the state.

**Boundary:** Voice cooking is crowded. The retained claim is an acoustic event intervention, not a conversational recipe guide.

**Kill condition:** It cannot distinguish a meaningful sound transition from generic kitchen noise.

## 8. FairTable — Multiplayer × Solana

**Opening scene:** Four people privately set price, dietary, and cuisine constraints. Commitment dots lock before any preference reveals. The group gets one deterministic choice and aggregate reasons only.

**Proof to show:** devnet commit/reveal, hidden individual inputs, deterministic social-choice result, and a demonstrated prevention of preference editing after disclosure.

**Boundary:** Polls and secret ballots are established. The claim is a narrowly scoped private dining decision whose trust property is visible in the demo.

**Kill condition:** The Solana step changes nothing a regular group poll cannot provide.

## Full tournament scorecards

The card numbers above identify the original finalist set rather than final rank. Person-hour estimates assume four capable builders working in parallel and include only a bounded demo, not a production service. Probability ranges are copied from the canonical candidate database.

### Ask Once — Food × Gemini

| Dimension | Battle-card assessment |
|---|---|
| Why it wins | Clear food workflow; a one-question 1/4 → 4/4 transformation; Gemini produces visible evidence while an algorithm does the decision work. |
| Why it loses | Food-rescue prior art is close; safety language can destroy credibility; label grounding can fail. |
| 30-second judge experience | See ambiguous label → uncertain graph → selected question → human answer → allocation changes. |
| Technical core | Schema-validated multimodal evidence, provenance graph, hard-constraint matching, and expected-information-gain question selection. |
| Sponsor / track fit | Gemini makes image evidence structured; Food is the actual intake and allocation workflow. |
| Prior art / allowed claim | Rescue networks and visual food tools exist. Claim only a staff-confirmed clarification loop, never automated safety or food rescue logistics. |
| Build / critical path | 40–48 person-hours MVP; 60–68 judge-ready. Gemini evidence → conservative matching → question/rerun. |
| Top risks | unsafe phrasing; inconsistent model evidence; no meaningful allocation flip. |
| Probabilities | MVP 68–82%; demo 75–88%; Food 14–25%; Gemini 12–23%; either 25–42%; overall 6–12%. |
| Minimum winning version | One item, two uncertainties, four household constraints, one staff answer, one visible allocation flip. |
| Maximum upside version | Evidence-cost weighting, multilingual labels, second intake item, and richer audit—only after scope freeze. |

### CycleClear — Optimization × Solana

| Dimension | Battle-card assessment |
|---|---|
| Why it wins | Strong optimizer; actual atomicity is visually memorable; Solana is plainly irreducible. |
| Why it loses | Wallet/program setup risk; blockchain necessity must be explained; a simple fixture can feel contrived. |
| 30-second judge experience | Graph shows impossible bilateral swaps, finds 4-cycle, all approve, all reservation rights settle together. |
| Technical core | Top-trading-cycle variant, preference constraints, Anchor/Rust program, multi-party all-or-none state transition. |
| Sponsor / track fit | Devnet settlement proves a Solana trust property; maximizing feasible exchanges is exact Optimization. |
| Prior art / allowed claim | Barter/atomic exchange research exists. Claim concrete reservation-rights clearing, not novel blockchain or cycle theory. |
| Build / critical path | 48–60 person-hours MVP; 68+ judge-ready. Deploy program → actual transaction → four-party UI. |
| Top risks | Anchor deployment; wallet/network delay; decorative-chain criticism. |
| Probabilities | MVP 65–80%; demo 75–88%; Optimization 14–24%; Solana 16–28%; either 26–42%; overall 5–10%. |
| Minimum winning version | Fixed 4-cycle, pre-funded wallets, settle branch, rejected-consent branch. |
| Maximum upside version | Multiple cycle choices, scarcity graph animation, real reservation import—only after devnet proof. |

### Airlock / Proxy Passport — Traveling × Auth0

| Dimension | Battle-card assessment |
|---|---|
| Why it wins | High-stakes travel problem; a denied action is a compelling security moment; Auth0 protects the actual action boundary. |
| Why it loses | Can look like an Auth0 sample; Token Vault/external OAuth can consume the night; mock travel fixture must feel real. |
| 30-second judge experience | Travel agent can hold a new option, cannot cancel, then can cancel only after traveler approval. |
| Technical core | Scoped authorization, protected tool proxy, approval state, token boundary, and immutable audit. |
| Sponsor / track fit | Auth0 is required for tool-level enforcement; the boundary matters specifically during travel disruption. |
| Prior art / allowed claim | Auth0 itself supports agent delegation and travel role controls exist. Claim a traveler-facing per-trip contract. |
| Build / critical path | 48–60 person-hours MVP; 68+ judge-ready. Protected mock API → denial → approval → audit. |
| Top risks | sponsor setup; role-toggle substitute; external-provider dependency. |
| Probabilities | MVP 60–75%; demo 72–86%; Traveling 12–22%; Auth0 15–27%; either 24–40%; overall 5–10%. |
| Minimum winning version | One traveler, hold allowed, cancel denied, one approval, one audit record. |
| Maximum upside version | Token Vault connection, scoped expiry, attack-path visualization. |

### Triangulate — Multiplayer × Gemini

| Dimension | Battle-card assessment |
|---|---|
| Why it wins | True multiplayer dependency; mixed evidence creates a visible contradiction; next-observation selection is a real technical mechanism. |
| Why it loses | Stakes can feel abstract; model confidence is easy to overstate; it may resemble a report-summary tool. |
| 30-second judge experience | Three reports conflict; graph asks one teammate for a photo; submitted evidence resolves shared state. |
| Technical core | Multimodal claim extraction, provenance/confidence graph, contradiction detection, information-gain task choice, synchronized room. |
| Sponsor / track fit | Gemini processes multiple evidence modalities; group members are the sensor network, making Multiplayer central. |
| Prior art / allowed claim | Crisis maps collect reports. Claim active disambiguation and tasking, not first crowdsourced verification. |
| Build / critical path | 48–60 person-hours MVP; 68+ judge-ready. Valid claim schema → task choice → cross-client update. |
| Top risks | grounding; API latency; user story/purpose ambiguity. |
| Probabilities | MVP 60–75%; demo 70–84%; Multiplayer 12–22%; Gemini 11–21%; either 21–37%; overall 5–10%. |
| Minimum winning version | Three staged reports, one contested claim, one requested observation, one confidence transition. |
| Maximum upside version | Live device capture, richer roles, calibrated evidence history. |

### StaleMap — Traveling × MongoDB Atlas

| Dimension | Battle-card assessment |
|---|---|
| Why it wins | Immediate useful map transformation; evidence life cycle is easy to understand; Atlas history/live update has a natural role. |
| Why it loses | Accessibility-map prior art is close; map UI can consume time; seeded reports can feel artificial. |
| 30-second judge experience | Green route → elevator outage report → confidence decay/red edge → alternate route. |
| Technical core | Timestamped documents, freshness/conflict scoring, evidence provenance, routing over a changing graph, realtime update. |
| Sponsor / track fit | Atlas is the evidence system of record; Traveling is embodied in route choice under live conditions. |
| Prior art / allowed claim | Accessibility directories and transit alerts exist. Claim evidence decay/conflict actively changes routing. |
| Build / critical path | 40–52 person-hours MVP; 60–68 judge-ready. Atlas write → route-cost update → visible reroute. |
| Top risks | generic map appearance; routing not visibly causal; data-quality discussion dominates demo. |
| Probabilities | MVP 62–78%; demo 76–88%; Traveling 12–23%; Atlas 13–25%; either 24–41%; overall 5–10%. |
| Minimum winning version | Two routes, one elevator edge, old/outage/restoration reports, deterministic reroute. |
| Maximum upside version | Photo provenance, live field report intake, full base map. |

### Bracket Patch / ConstraintLens — Optimization × Gemini

| Dimension | Battle-card assessment |
|---|---|
| Why it wins | Fastest likely polished build; visual before/after is exceptional; deterministic solver prevents wrapper criticism. |
| Why it loses | OCR/scheduling neighborhood is crowded; source board grammar needs careful control; novelty ceiling is lower. |
| 30-second judge experience | Photograph a scribbled schedule, reveal red impossible core, animate two-note patch to feasible. |
| Technical core | Gemini image schema extraction, satisfiability/ILP or CP-SAT, unsat core, minimum-edit repair. |
| Sponsor / track fit | Gemini makes board constraints machine-readable; solving feasibility is directly Optimization. |
| Prior art / allowed claim | Digitizers and schedulers exist. Claim photo-to-explainable-minimal-repair, not generic planning. |
| Build / critical path | 32–44 person-hours MVP; 52–60 judge-ready. Photo schema → core → repair animation. |
| Top risks | manual re-entry; extraction error; generic-scheduler critique. |
| Probabilities | MVP 75–88%; demo 78–90%; Optimization 10–20%; Gemini 8–16%; either 17–31%; overall 4–8%. |
| Minimum winning version | One photographed board, one core, one three-change-or-fewer repair. |
| Maximum upside version | Court/team constraints, user correction loop, alternate repair comparison. |

### Sizzle Oracle — Food × ElevenLabs

| Dimension | Battle-card assessment |
|---|---|
| Why it wins | Sensory, memorable event; voice is a timely intervention rather than narration; Food use is intuitive. |
| Why it loses | Voice-cooking prior art; acoustic classifier can be brittle; real usefulness needs credible sound data. |
| 30-second judge experience | Pan signal crosses threshold, says “turn it now,” cook confirms, false/noise clip remains quiet. |
| Technical core | Audio features/state classifier, threshold calibration, responsive voice output and confirmation state machine. |
| Sponsor / track fit | ElevenLabs provides the real-time voice action; food-state detection defines the Food interaction. |
| Prior art / allowed claim | Voice cooking exists. Claim a narrow acoustic state-to-action interruption, not a better recipe assistant. |
| Build / critical path | 40–52 person-hours MVP; 60–68 judge-ready. Prepared sound classifier → low-latency voice → confirmation. |
| Top risks | noise false positives; latency; generic-assistant framing. |
| Probabilities | MVP 60–75%; demo 70–84%; Food 9–18%; ElevenLabs 10–20%; either 18–34%; overall 3–8%. |
| Minimum winning version | One clean prepared transition, one intervention, one confirmation, one negative clip. |
| Maximum upside version | Live microphone, adaptive thresholds, multiple cooking states. |

### FairTable — Multiplayer × Solana

| Dimension | Battle-card assessment |
|---|---|
| Why it wins | Private group choice has a neat commitment-based trust proof; social choice and devnet state are both judge-visible. |
| Why it loses | Wallet friction; decision domain may feel small; generic polls/secret ballots are close prior art. |
| 30-second judge experience | Four private constraints lock, a late edit becomes a new commitment, reveal yields one aggregate decision. |
| Technical core | Commitment/reveal program, deterministic social-choice algorithm, private input boundary, attack demonstration. |
| Sponsor / track fit | Solana enforces timing/integrity of commitment; the result cannot exist as a single-user feature, so Multiplayer is central. |
| Prior art / allowed claim | Polls and private social-choice research exist. Claim a demonstrated prevention of post-reveal manipulation. |
| Build / critical path | 48–64 person-hours MVP; 68+ judge-ready. Commit transaction → attack branch → reveal and result. |
| Top risks | explaining why a chain is needed; wallet UX; product stakes. |
| Probabilities | MVP 55–70%; demo 70–84%; Multiplayer 10–20%; Solana 12–23%; either 21–37%; overall 4–9%. |
| Minimum winning version | Four fixed preference records, actual commitment/reveal, one attempted late edit, deterministic result. |
| Maximum upside version | Selective disclosure proofs, richer group objective, multi-device reveal. |
