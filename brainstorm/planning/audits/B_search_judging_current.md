# Audit B — Judging and demo-quality review

**Worker:** /root/search_audit_judging  
**Verdict:** The search architecture is unusually well aligned with the official axes: usefulness, technical difficulty, originality, demo quality, and track relevance. Its strongest feature is that every finalist has a visible state transition rather than a feature list. It still needs hard build-time gates because several demos could look staged, sponsor-decorative, or like an LLM wrapper under a three-minute judge interaction.

## What is strong

- The plan correctly treats one track and a single primary sponsor as core constraints, and rejects cosmetic fit before scoring.
- Quality gates map directly to the official rubric: meaningful first-ten-second change, visible sponsor artifact, clear track explanation, prior-art boundary, and fallback.
- The 90-second simulations follow a judge path: painful before-state → causal action → changed result → proof artifact.
- Finalists expose non-LLM technical mechanisms: Ask Once uses constrained matching/value-of-information; CycleClear uses cycle optimization/atomic settlement; Bracket Patch uses unsat core/minimum repair; StaleMap makes evidence freshness change routing.
- The demos include skeptical branches: denied actions, negative sound clips, stale evidence, late-edit attempts, and uncertainty handling.
- Cards state modest novelty claims and explicit kill conditions.

## Systemic failure modes

1. **The official presentation is three minutes; current artifacts foreground ninety seconds.** A full run must also cover problem framing, technical/sponsor proof, track close, and interruption buffer.
2. **Sponsor centrality is not a substitute for HackCMU judging strength.** Sponsor usage helps a Best Use prize but cannot make a weak product beat a clear, useful track project.
3. **Seeded transitions can look pre-scripted.** Every finalist needs one credible adverse/alternate branch: a rejected CycleClear signer, a real requested Triangulate observation, a rerouting StaleMap report, a non-canned Bracket Patch repair, or a negative Sizzle Oracle clip.
4. **API proof and product proof are easy to conflate.** The provider artifact must change state: Gemini JSON affects an allocation, Auth0 denies before approval, Solana changes devnet state, Atlas changes a route.
5. **Time estimates are close to maximum capacity.** A 48–68 person-hour judge-ready plan must reserve integration, debugging, and rehearsal.
6. **Credibility boundaries must be product behavior.** Ask Once must visibly withhold uncertainty; Airlock must enforce a tool boundary; FairTable must not promise private on-chain data; Sizzle Oracle must not imply food-safety accuracy.

## Candidate-specific judge risks

| Candidate | Strong judge moment | Main way it loses |
|---|---|---|
| Ask Once | One staff answer visibly changes 1/4 to 4/4 eligible matches. | It sounds like allergy diagnosis or generic food-rescue matching. |
| CycleClear | Real all-or-nothing devnet settlement after a computed cycle. | Fixed cycle, wallet failure, or decorative hash. |
| Airlock | Forbidden action denied, then succeeds after approval. | Standard Auth0 login/RBAC sample with travel copy. |
| Triangulate | Conflicting multimodal reports lead to one discriminating next action. | It summarizes reports or overstates confidence. |
| StaleMap | New evidence changes recommended route. | Static map visualization with seeded pins. |
| Bracket Patch | Photographed board becomes an unsat core and minimal repair. | Manual correction precedes solver. |
| Sizzle Oracle | Threshold crossing causes concise voice intervention; noise stays silent. | Brittle classifier or prerecorded cue. |
| FairTable | Late edit cannot affect earlier commitment. | Chain adds no visible trust property. |

## Three binding safeguards

1. **H+2 sponsor-proof gate:** provider artifact must change application state, or switch.
2. **H+5 causal-value-and-boundary gate:** show measurable before/after plus adverse/uncertain branch with the same implementation, or kill.
3. **H+12 freeze and H+15 rehearsal:** freeze the 75–90 second proof path at H+12; at H+15 run a 2:35–2:45 full presentation: 15s problem, 90s demo, 35–45s technical/sponsor proof, 20s track/usefulness close, buffer for interruption. Fix the proof path before adding features.

## Conclusion

Advance Ask Once, CycleClear, Airlock, Bracket Patch, and StaleMap only if they clear the early sponsor-proof gate. For overall HackCMU judging, Ask Once and Bracket Patch have the clearest immediate transformations; CycleClear has stronger technical/sponsor proof but higher execution risk. The final decision should override numerical scores with the demonstrated gates.

