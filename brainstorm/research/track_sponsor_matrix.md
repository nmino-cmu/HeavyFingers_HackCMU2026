# HackCMU 2026 track × sponsor matrix

Status snapshot: September 11, 2026. The four named tracks below come from the locally preserved transcript of the official Discord opening deck (`MLH_OFFICIAL_TRANSCRIPT.md`, section K). The public event page still displayed generic Track 1–5 accordions when checked, so the deck is the current primary source capture. Scores are analytical estimates, not organizer claims.

## Reading the table

Each cell is `fit / sponsor depth / demo / build / field` on a 10-point scale. `Field` is inverse competitor density: higher means a better chance of avoiding a crowded category. `Forced` is the risk that the sponsor would become decorative. The strategic result accounts for the five scores plus the official judging axes: usefulness, technical difficulty, originality, demo quality, and track relevance.

| Sponsor prize | Verified eligibility / technical evidence |
|---|---|
| Gemini API | Use the Gemini API. Its documented video understanding, tool calling, and JSON-schema structured output make a visual or decision loop much stronger than text chat. [Gemini video](https://ai.google.dev/gemini-api/docs/video-understanding), [structured output](https://ai.google.dev/gemini-api/docs/structured-output) |
| ElevenLabs | Fully autonomous audio is the official ask; its realtime conversational and speech models are appropriate only when voice changes the interaction. [MLH prize page](https://www.mlh.com/events/hackcmu/prizes), [models](https://elevenlabs.io/docs/overview/models) |
| Solana | The official prompt explicitly calls out games, social/consumer products, high-frequency transactions, supply chains, identity, and payments. A visible devnet transaction/program is the reliable eligibility proof. [MLH prize page](https://www.mlh.com/events/hackcmu/prizes) |
| Vultr | The official prompt explicitly advertises scalable cloud compute and cloud GPUs. A hosted API alone is weak; a visible parallel or GPU workload is the defensible bar. [MLH prize page](https://www.mlh.com/events/hackcmu/prizes), [Vultr docs](https://docs.vultr.com/products) |
| Auth0 | Auth0 APIs, login/MFA/passwordless, and Auth0 for AI Agents are explicitly eligible. A scope boundary or delegated agent is materially stronger than a login screen. [MLH prize page](https://www.mlh.com/events/hackcmu/prizes), [Auth0 AI docs](https://auth0.com/ai/docs/intro/overview) |
| MongoDB Atlas | Atlas must be used. A geospatial, time-series, vector-search, or change-stream feature can make the data system visible and load-bearing. [MLH prize page](https://www.mlh.com/events/hackcmu/prizes), [Atlas docs](https://www.mongodb.com/docs/atlas/) |
| IFM / K2 | VERIFIED as a separate HackCMU prize from the opening deck; endpoint/access method and whether it is a submission track remain UNKNOWN. Treat all pairs as conditional. |
| Cursor | VERIFIED as a separate opening-deck prize; the eligibility bar is UNKNOWN. Do not target it until a representative states the rule. |
| Sandia cyber | VERIFIED as a cybersecurity prize from the opening deck; detailed rubric is UNKNOWN. A real threat model and demonstrated control are required for a conditional target. |

## Complete matrix

| Track | Sponsor | Fit | Depth | Demo | Build | Field | Forced | Strategic result and best mechanism |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Optimization | Gemini | 8 | 8 | 8 | 7 | 5 | 3 | **Attractive.** Video-to-process graph plus an explicit optimizer; avoid a generic operations chatbot. |
| Traveling | Gemini | 7 | 8 | 8 | 7 | 3 | 4 | **Conditional.** Multimodal ground-truth mismatch is credible; itinerary generation is crowded. |
| Multiplayer | Gemini | 6 | 7 | 8 | 7 | 6 | 4 | **Selective.** Camera-mediated physical play or live shared understanding, not a social chat. |
| Food | Gemini | 8 | 8 | 8 | 7 | 3 | 3 | **Attractive but crowded.** Food-state video, provenance, or constrained allocation can survive; recipe chat cannot. |
| Optimization | ElevenLabs | 5 | 6 | 6 | 8 | 7 | 6 | **Usually reject.** Voice is seldom essential to the optimization objective. |
| Traveling | ElevenLabs | 7 | 8 | 8 | 7 | 4 | 4 | **Selective.** Eyes-busy, interruption-sensitive interaction; translation alone is crowded. |
| Multiplayer | ElevenLabs | 8 | 8 | 9 | 7 | 6 | 3 | **Attractive.** Voice must be shared game/social state, not narration. |
| Food | ElevenLabs | 8 | 8 | 8 | 8 | 5 | 3 | **Attractive.** Hands-busy coordination is a natural loop; avoid Alexa-recipe clones. |
| Optimization | Solana | 3 | 5 | 6 | 6 | 7 | 8 | **Reject.** Ledger seldom improves an optimization system. |
| Traveling | Solana | 6 | 7 | 7 | 6 | 6 | 5 | **Selective.** Verifiable group commitments or delegated trip escrow; avoid payments cosplay. |
| Multiplayer | Solana | 9 | 9 | 9 | 7 | 7 | 2 | **Highly attractive.** Commit-reveal, common state, and fairness are native to the sponsor and track. |
| Food | Solana | 5 | 7 | 7 | 6 | 7 | 6 | **Selective.** Food rescue pickup commitments are credible; restaurant crypto payments are not. |
| Optimization | Vultr | 9 | 9 | 9 | 7 | 6 | 2 | **Highly attractive.** Parallel simulation / optimization job visibly needs cloud compute. |
| Traveling | Vultr | 8 | 8 | 8 | 7 | 6 | 3 | **Attractive.** Counterfactual route/crowd/weather simulations, not a hosted map. |
| Multiplayer | Vultr | 6 | 8 | 8 | 7 | 6 | 5 | **Selective.** Large shared simulations work; a normal game server is weak. |
| Food | Vultr | 7 | 8 | 8 | 7 | 5 | 4 | **Selective.** Kitchen-order or food-rescue dispatch simulation can earn the compute. |
| Optimization | Auth0 | 7 | 8 | 8 | 7 | 7 | 3 | **Attractive.** Safe delegated agents optimize work under scoped authority. |
| Traveling | Auth0 | 9 | 9 | 8 | 7 | 6 | 2 | **Highly attractive.** Travel delegation exposes a real, easy-to-understand permission boundary. |
| Multiplayer | Auth0 | 9 | 9 | 8 | 7 | 6 | 2 | **Highly attractive.** Consent and shared authority are part of the multiplayer experience. |
| Food | Auth0 | 6 | 8 | 7 | 7 | 7 | 5 | **Selective.** Dietary/privacy delegation can work, but ordinary restaurant login does not. |
| Optimization | MongoDB Atlas | 8 | 8 | 7 | 8 | 6 | 3 | **Attractive.** Live time-series/event data plus change streams makes Atlas visible. |
| Traveling | MongoDB Atlas | 9 | 9 | 9 | 8 | 6 | 2 | **Highly attractive.** Geo queries + expiring field reports + realtime route changes are a natural fit. |
| Multiplayer | MongoDB Atlas | 6 | 8 | 8 | 8 | 6 | 5 | **Selective.** Change streams can power presence, but generic chat/game state is insufficient. |
| Food | MongoDB Atlas | 8 | 9 | 8 | 8 | 6 | 3 | **Attractive.** Time-series cold chain or real-time surplus allocation has a genuine data spine. |
| Optimization | IFM / K2 | 6 | 6 | 6 | 5 | 8 | 5 | **Conditional only.** Access and judging bar are unknown; no critical-path dependency. |
| Traveling | IFM / K2 | 6 | 6 | 7 | 5 | 8 | 5 | **Conditional only.** Could support local multilingual operation, but tooling risk is too high. |
| Multiplayer | IFM / K2 | 5 | 6 | 6 | 5 | 8 | 6 | **Conditional only.** No strong unique interaction found under known constraints. |
| Food | IFM / K2 | 6 | 6 | 7 | 5 | 8 | 5 | **Conditional only.** Use only after a working endpoint is confirmed. |
| Optimization | Cursor | — | — | — | — | — | — | **Reject for now.** Prize rubric UNKNOWN. |
| Traveling | Cursor | — | — | — | — | — | — | **Reject for now.** Prize rubric UNKNOWN. |
| Multiplayer | Cursor | — | — | — | — | — | — | **Reject for now.** Prize rubric UNKNOWN. |
| Food | Cursor | — | — | — | — | — | — | **Reject for now.** Prize rubric UNKNOWN. |
| Optimization | Sandia cyber | 6 | 7 | 7 | 7 | 7 | 4 | **Conditional.** Security of an optimization control plane can be real, but rubric is unknown. |
| Traveling | Sandia cyber | 4 | 6 | 6 | 7 | 7 | 7 | **Reject.** Travel theme would likely be bolted on. |
| Multiplayer | Sandia cyber | 7 | 8 | 8 | 7 | 7 | 3 | **Conditional.** Anti-cheat / consent protocol can be compelling if security is substantive. |
| Food | Sandia cyber | 6 | 8 | 7 | 7 | 7 | 4 | **Conditional.** Protecting kitchen QR provenance is coherent but depends on rubric. |

## Strategic pair shortlist

1. **Optimization × Vultr** — visible cloud-scale simulation is both technical substance and the user-facing answer.
2. **Traveling × MongoDB Atlas** — a changing, evidence-weighted accessibility map makes geospatial data and realtime updates central.
3. **Traveling × Auth0** — scoped delegation for an agent or trusted companion has a crisp, sponsor-visible failure mode.
4. **Multiplayer × Solana** — commit-reveal fairness creates a natural on-chain reason, but must be framed around a real group decision.
5. **Optimization × Gemini** — process video becomes a constrained optimization model rather than chat.
6. **Food × ElevenLabs** — live roles and interruptible calls are defensible if the demo is an actual team cooking workflow.

## Explicit rejections

Do not target Cursor until the rule is stated. Do not make IFM/K2 a critical path until access is verified. Do not pick Solana for a single-user optimizer, Vultr for a conventional hosted web app, Auth0 for a login screen, Atlas for user/settings storage, Gemini for prompt-to-text, or ElevenLabs for post-hoc narration.

