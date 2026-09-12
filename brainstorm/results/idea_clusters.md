# Candidate clustering and convergence review

This is a deduplication pass over the 34 candidates in [all_candidates.json](all_candidates.json), after each was forced into exactly one 2026 track and one primary sponsor. A cluster is a shared mechanism, not merely a shared theme. The leader is the only version permitted to survive unless its proof gate fails.

| Cluster | Members | Strongest distinct mechanism | Leader / disposition | Why the variants merge or diverge |
|---|---|---|---|---|
| Atomic exchange under scarce capacity | O1 CycleClear, O8 Entitlement Auction | Find a mutually acceptable cycle and settle every leg together | **O1 final**; O8 cut | O8 becomes a speculative market. O1’s reservation-rights ledger makes atomicity legible and useful. |
| Constraint repair from a messy plan | O2 ConstraintLens, O3 Resilience Canvas, O4 ConsentSolver, O5 UndoPoint, O6 LineCheck | Convert a plan into explicit constraints and expose a justified repair | **O2 final**, O3 semifinal; O4–O6 cut | O2 has a before/after visual. O3 is a different robust-planning route and stays only as the Vultr option. The rest have a less visible primary-sponsor role. |
| Delegated travel action | T1 Proxy Passport, T7 DetourPact | A traveler grants narrow, expiring authority for a disruption | **T1 final**; T7 cut | T7 adds a ledger without solving the authority boundary. T1 is distinguished only if a disallowed action is visibly blocked by Auth0. |
| Decaying travel evidence and recovery | T2 Delayscape, T3 Arrival Witness, T4 StaleMap, T5 LostLoop, T6 RepairRelay | Freshness-weighted facts change what a traveler should do | **T4 final**; T2/T3/T5/T6 cut | T4 makes a concrete route change caused by a report. The others drift toward generic status boards, proof capture, lost-and-found, or voice concierge. |
| Shared evidence under uncertainty | M1 Triangulate, M2 RumorClock, M6 Cross-Modal Commons | A group gathers the next fact that resolves disagreement | **M1 final**, M2 semifinal; M6 cut | M1 assigns a discriminating next observation. M2 keeps only evidence decay and needs a stronger physical interaction. M6 lacks a sufficiently constrained outcome. |
| Multiplayer mediation and sensing | M3 Babel Relay, M4 Consent Relay, M5 ManySight, M7 NoiseFloor | Shared state changes because multiple people contribute | all cut after first pass | Translation, consent settings, generic camera rooms, and sound visualizers do not show a prize-worthy irreversible state transition. |
| Private group choice | M8 FairTable | Commit, reveal, and compute a group choice without exposing individual constraints | **M8 final** | It has no duplicate in the set. It remains conditional on a real devnet commit/reveal changing trust rather than decorating a poll. |
| Food intake with uncertainty | F6 Allergrant, F9 Traceplate, F13 Ask Once | Represent a food-related fact as bounded evidence rather than a confident guess | **F13 final**, F6 semifinal, F9 cut | F13 chooses the one staff question with measurable allocation impact. F6 risks looking like ordinary authorization; F9 risks becoming a traceability dashboard. |
| Acoustic cooking intervention | F1 Sizzle Oracle, F8 KitchenHandoff | A sound event triggers one well-timed action | **F1 final**; F8 cut | Existing voice cooking products make F8 untenable. F1 survives only as pan-sound-to-action, not recipe narration. |
| Food visual / operations analysis | F2 Heat Witness, F4 RoleTestbench, F5 ChillChain, F10 MiseStorm, F11 Ferment Falsifier | Images or operations data become a food decision | all cut | Visual food recognition, food workflow analytics, cold-chain monitoring, and fermentation trackers have too much direct prior art or too little demo transformation. |
| Parallel-batch learning | F3 BatchBraid | Align multiple batches to locate the first divergent condition | **F3 semifinal** | It is sufficiently different from a single-batch tracker, but must show causal assistance rather than a chart. |
| Group food coordination | F12 Hot Together | Coordinate several diners or cooks | cut | The outcome is too close to group planning and has no sponsor-specific technical proof. |

## Convergence flags

High convergence is a reason to demand a stronger proof, not automatically to eliminate a concept.

1. **Food rescue / donation handling:** mature matching and routing tools already exist. The retained F13 scope is intake clarification before allocation, not donor-driver-recipient logistics. See [the prior-art ledger](../research/prior_art/decision_evidence.md#prior-art-evidence-ledger).
2. **Travel assistance:** itinerary chat and accessibility maps are crowded. T1 must show authorization enforcement; T4 must show confidence decay that reroutes a traveler.
3. **Gemini evidence graphs:** several teams could build a multimodal summary. M1 and F13 survive only because they select an action or question and visibly update a constrained state.
4. **Solana social products:** polling and tokenized marketplaces are common hackathon shapes. O1 requires actual atomic reservation settlement; M8 requires actual commit/reveal.
5. **Voice cooking:** ordinary TTS or spoken recipes are explicitly excluded because established products already do that.

## Portfolio rule used after clustering

Retain a leader when it can satisfy all four conditions:

1. its central state transition takes less than 20 seconds to show;
2. removing the primary sponsor would remove a user-visible property rather than a logo;
3. its closest prior art lacks the stated interaction, or the candidate narrows itself until that is true;
4. its smallest credible version fits the effective 19-hour build window.

The retained portfolio therefore contains 8 finalists and 4 contingencies. It is intentionally not a volume leaderboard.

