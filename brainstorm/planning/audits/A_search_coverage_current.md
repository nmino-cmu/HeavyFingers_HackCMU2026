# Audit A — Current search-space coverage and mode-collapse check

**Independent scope:** audit the completed search artifacts, not generate projects. Reviewed `search_plan.md`, `all_candidates.json`, `idea_clusters.md`, the semifinal slate, and the event ground truth on Sep. 11, 2026.

## Verdict

The present pool is substantially better defended against late-stage duplication than a raw idea dump: it clusters on mechanism, names a single leader, uses a sponsor-removal test, and has first-hours kill gates. It is not yet evidence of broad *generation* coverage. The result is a high-quality short list whose search provenance and numerical diversity claims are thinner than the brief asks for.

## What it covers

- All four official tracks have survivors: Optimization 7, Traveling 7, Multiplayer 8, Food 12.
- Five of six MLH sponsors appear in every track; Food × Solana is the sole empty primary-pair cell. The matrix may make that cell unattractive, but the candidate record does not say that it was searched and rejected.
- The sponsor mechanisms are mostly genuinely different: atomic settlement (Solana), authorization (Auth0), voice loop (ElevenLabs), visible compute (Vultr), durable/evolving state (Atlas), and multimodal structured extraction (Gemini).
- The clustering pass catches obvious near-duplicates. In particular, it limits multiple constraint-repair, evidence-routing, food-intake, and atomic-exchange variants.

## Blind spots and collapse risks

1. **The requested breadth is not met numerically.** The pool has 34 candidates, below the target floor of 15 per track (and therefore below 60 total). “Up to 100, not a quota” protects against padding, but it does not make the missing coverage invisible. Record this as a conscious quality-over-volume waiver or run a targeted backfill round.
2. **The generator provenance is not auditable.** `all_candidates.json` has no cohort, worker/prompt, seed, or independent-search field. The manifest shows one ideation-worker archive plus review workers. The claim that cohorts were independent cannot be tested from the retained candidate records.
3. **Several leaders share one latent shape:** uncertain evidence → model/optimizer → one recommended action. That is a good demo primitive, but it couples F13 Ask Once, M1 Triangulate, M2 RumorClock, T4 StaleMap, and O2 ConstraintLens. Different nouns do not make them independent discoveries.
4. **Food is overrepresented, yet narrow.** Four food candidates use Atlas and three use Gemini; much of the track concentrates on intake, batch/process evidence, and safety-adjacent constraints. It has less coverage of non-inference, non-operations Food experiences.
5. **Prior-art discipline is good for obvious categories but not consistently reproducible.** The decision ledger centralizes examples, while most candidate cards make qualitative classifications. Retain a query/source/closest-mechanism row for every advancing candidate, especially the “DIFFERENTIATED” ones.

## Three safeguards before treating the shortlist as exhaustive

1. **Publish a coverage ledger.** For each of 4 tracks × 6 MLH sponsors, state `searched`, `survived`, or `rejected`, with the rejection mechanism. Add candidate provenance: worker/cohort, input modality, user job, computation primitive, and prior-art query set. Do not manufacture an F×Solana finalist merely to fill a box.
2. **Run a bounded anti-convergence backfill.** Use independent, blinded prompts aimed only at under-covered mechanism families (local/offline, design/interaction-first, non-LLM algorithmic, physical I/O, and boundary-track work). Require no evidence-routing / “ask next question” core loop. Keep only items that pass the same prior-art and sponsor tests; otherwise document no survivor.
3. **Cap the final slate by fingerprint.** Use `user job + input dependency + core mechanism + state transition + visible proof` rather than title/theme. Permit at most two semifinalists and one finalist from the uncertain-evidence/next-action fingerprint; require a distinct counterfactual sponsor proof for each.

## Bottom line

The existing clustering makes the *selection* credible. A small, documented coverage/provenance correction would make the claim of broad independent search credible as well.
