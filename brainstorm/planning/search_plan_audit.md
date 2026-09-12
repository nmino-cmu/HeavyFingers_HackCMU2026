# Search-plan audit

Eight independent critiques were preserved in `brainstorm/planning/audits/` and are summarized here. They were written before the present finalist selection and retain minority views rather than being overwritten.

| Critique | Core finding | Design response |
|---|---|---|
| A — search-space coverage | Mechanism labels can still collapse into renamed AI-for-X. | Stratify by user job, interaction, input modality, compute shape, and non-LLM mechanisms; cluster after generation. |
| B — judging | A clever system loses if the judge cannot understand its consequence immediately. | Require a first-10-second visual transformation and a three-minute script at semifinal stage. |
| C — sponsor specialization | Sponsor checkboxes are likely common and weak. | Require a counterfactual: remove the sponsor and the central product capability must break, not merely deploy differently. |
| D — feasibility | A 19-hour window rewards one hard, visible core over a complete platform. | Record critical path, account risk, task ownership, fallback, and minimum winning version for each semifinalist. |
| E — novelty | Related products are often found after a flattering first search. | Perform both exact-concept and mechanism-level prior-art checks; classify and kill mature overlaps. |
| F — demo | A live model/API creates avoidable failure modes. | Use deterministic demo data, prewarm services, prove the live integration early, and retain a labeled fallback. |
| G — expected value | Thin fields are not automatically attractive if track work becomes contrived. | Rank pair integrity and conditional demo success ahead of assumed competitor counts; treat field size as uncertain. |
| H — orchestration red team | Running a nominal 100-agent pipeline can consume the build window and produce false independence. | Retain broad research in this artifact, but time-box any live use; do not make agent count a gate to coding. |

## Current required coverage audit register

The following register explicitly maps the completed work to the eight search-plan dimensions in the brief. The two files marked current were independently re-run by fresh Codex workers against the final artifacts; the other files preserve earlier separate critique lenses.

| Critique | Source | Core finding | Binding response |
|---|---|---|---|
| A — search-space coverage | [A_search_coverage_current.md](audits/A_search_coverage_current.md) | A high-quality short list is not automatically broad generation coverage; evidence-to-action mechanisms converge. | Publish pair coverage and provenance; use fingerprint caps; do not manufacture filler. |
| B — HackCMU judging | [B_search_judging_current.md](audits/B_search_judging_current.md) | A state transition must be useful, causal, and credible in a three-minute slot. | H+2 sponsor proof, H+5 adverse branch, H+15 timed rehearsal. |
| C — sponsor specialization | [C_sponsor.md](audits/C_sponsor.md) | Sponsor checkbox use is common and weak. | Remove the sponsor: the central capability must break. |
| D — track specialization | [I_track_specialization_current.md](audits/I_track_specialization_current.md) | Broad tracks invite cosmetic topical fit. | Opening sentence and visible counterfactual must name a track outcome. |
| E — build feasibility | [D_feasibility.md](audits/D_feasibility.md) | A 19-hour window rewards one hard, visible core. | Record accounts, owner, H5 breakage, fallback, and minimum version. |
| F — demo quality | [F_demo.md](audits/F_demo.md) and current Audit B | Live APIs create avoidable stage failures. | Fixture, early live proof, adverse branch, labeled fallback, full rehearsal. |
| G — novelty | [E_novelty.md](audits/E_novelty.md) | Related products surface after a flattering first search. | Exact and mechanism-level searches; classify and kill overlap. |
| H — expected value | [G_expected_value.md](audits/G_expected_value.md) | Sparse or unknown prize fields do not make a contrived pair attractive. | Rank pair integrity and conditional demo success ahead of assumed density. |

## Auditor dissent that changed the decision

- The red-team audit correctly rejected sponsor stacking as a selection objective. Every finalist targets one sponsor only.
- The feasibility audit made the fallback a required build artifact rather than a reassuring sentence.
- The novelty audit moved generic itinerary generators, accessibility narrators, and food-recognition assistants to the do-not-build list despite their superficial sponsor fit.
- The expected-value audit prevented a recommendation based solely on perceived low competition for an unspecified prize.

## Audit conclusion

The plan is adequate only if it keeps the engineering clock visible. Its output must be a short ranked set with buildable demonstrations, not a menu of clever concepts. The earlier planning exercise described a broader 48-card exploration; this completed run preserves **34** structured candidates after duplicate and prior-art consolidation, then advances only 12 semifinalists into simulations.
