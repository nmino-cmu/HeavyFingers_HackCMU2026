# Top-12 19-hour build simulations

**Clock convention:** H0 is Friday 9:00pm, H5 is 2:00am, H15 is noon Saturday, and H19 is the 4:00pm Baggage Check. Each schedule assumes four people: A owns sponsor/backend, B owns algorithm/data, C owns interface/visuals, and D owns fixtures, narration, and QA. “Proof” means the on-screen event that a judge can verify, not a slide claim.

Every team should use the same stop rules:

- At **H2**, prove the sponsor integration on a disposable fixture.
- At **H5 (2am)**, decide whether the core state transition is real. Do not continue polishing a broken premise.
- At **H11**, run the full 90-second path without a developer explaining it.
- At **H15**, freeze scope, make the fallback demo independently runnable, and run a 2:35–2:45 presentation: 15 seconds problem, 90 seconds proof, 35–45 seconds technical/sponsor evidence, 20 seconds track/usefulness close, interruption buffer.
- At **H18**, submit the required form and capture the backup demo.

## Preflight inventory and probable H5 breakage

This inventory makes hidden dependencies explicit before a team spends the night on an idea. A “fixture” is a controlled demo input prepared after hacking begins; it is not a pre-built product.

| Candidate | Required account/key or unfamiliar primitive | Fixture / data / model | Deployment and test artifact | Most likely broken at H5 (2am) |
|---|---|---|---|---|
| Ask Once | Gemini API key; structured-output schema | handwritten label, four policy cards, evidence JSON | browser app; schema-validation log and allocation test | grounded extraction or a question with no measurable allocation gain |
| CycleClear | Solana devnet, funded wallets, Anchor/Rust | four reservations, approvals, reject branch | deployed program ID and explorer transaction | program deployment, signer flow, or atomic rollback |
| Airlock | Auth0 tenant/application, protected mock API | disruption itinerary, allowed/denied actions | protected-request log and audit | actual policy enforcement versus a cosmetic role toggle |
| Triangulate | Gemini API key; shared-room mechanism | photo, audio, text reports and resolving observation | schema fixture plus multi-browser test | action-selection logic degenerating into summary |
| StaleMap | Atlas project/URI and realtime/poll update | two-route graph, old/outage/restoration reports | Atlas event record and route regression test | report changes UI but not actual route cost |
| Bracket Patch | Gemini API key; solver library | photographed sticky-note board and expected patch | JSON-validation and satisfiability test | extraction requires manual cleanup |
| Sizzle Oracle | ElevenLabs key; audio I/O path | labeled pan/noise clips | signal-threshold trace and latency capture | noisy audio causes false intervention |
| FairTable | Solana devnet, wallets, commitment program | four preferences and late-edit attack | transaction/explorer proof and deterministic result test | commit/reveal complexity or unclear threat model |
| Resilience Canvas | Vultr account/credit/worker image | delivery graph, closure/no-show scenarios | remote job ID, baseline-versus-robust output | cloud job fails to change a recommendation |
| RumorClock | Atlas project/URI, two-browser sync | timestamped claim and refresh evidence | committed-event cross-client test | single-user state makes multiplayer value invisible |
| BatchBraid | Atlas project/URI; alignment code | three batch time-series/photo events | persisted event stream and divergence regression test | it only renders a chart, not an action |
| Allergrant | Auth0 tenant/application, protected kitchen API | minimal dietary constraint and expiry event | protected-read denial after expiry | revocation is only a front-end toggle |

## 1. Ask Once — Food × Gemini

| Hour | Concrete checkpoint |
|---|---|
| H0 | D writes one controlled ambiguous donation-label fixture and four policy-constrained household cards; C draws the before/after allocation scene. |
| H1 | A gets a Gemini image call working; B defines the evidence-node schema and matching inputs. |
| H2 | Sponsor gate: a label image produces valid structured evidence JSON with an uncertainty field and source quote/crop reference. |
| H3 | B renders an ingredient/allergen evidence graph from fixture JSON; C shows red uncertain nodes. |
| H4 | B completes conservative matching that refuses uncertain hard constraints; C displays 1/4 eligible allocations. |
| H5 | **2am break test:** enter “sesame confirmed” and prove a recomputation to 4/4. If Gemini is unstable, lock a clearly labeled precomputed response tied to the visible fixture. |
| H6–7 | A wires a real Gemini response with schema validation; B implements expected-information gain over the two or three candidate questions. |
| H8–9 | C builds capture, evidence, allocation, and question views as one guided flow; D tests hostile labels and declines unsafe wording. |
| H10–11 | A logs evidence provenance; D conducts a cold 90-second demo with someone uninvolved. |
| H12–13 | Add one failure case: inconclusive label → “ask staff / cannot allocate,” never a guess. |
| H14 | C adds large before/after counts and a compact “recorded policy” label. |
| H15 | Scope freeze: one fixture, one question, four allocations, one policy. |
| H16 | D records a backup run; A preserves raw model response and retry behavior. |
| H17 | Run demo in airplane-like conditions using cached fixture output; verify language says “eligible after confirmation.” |
| H18–19 | Submit, rehearse the three-minute version, and stop adding food or medical features. |

**Four-hours-behind route:** skip live camera capture and use one preloaded photo; retain live question selection and visible graph/matching.  
**Minimum winning version:** one ambiguous item, two uncertain attributes, one staff answer, a numerical eligible-allocation change.  
**Abandon at H5 if:** the answer does not materially change an allocation or the narrative implies inferred safety.

## 2. CycleClear — Optimization × Solana

| Hour | Concrete checkpoint |
|---|---|
| H0 | B fixes a four-person, four-reservation fixture; D writes a graph-to-settlement narration. |
| H1 | A creates devnet wallets and a minimal program/account model; C renders static exchange graph. |
| H2 | Sponsor gate: deploy or invoke a minimal devnet instruction and retrieve a transaction signature. |
| H3 | B implements fixed-cycle detection and preference feasibility with a unit fixture. |
| H4 | A adds reservation-right state and all-party approvals; C turns the solution cycle green. |
| H5 | **2am break test:** four approvals execute an all-or-none state change. A fifth declined path leaves every right unchanged. |
| H6–7 | A connects wallet/program state to UI; B adds one alternative cycle and objective explanation. |
| H8–9 | C makes each user’s old and new reservation visually unmistakable; D verifies explorer link and failure copy. |
| H10–11 | Cold run: four pre-funded wallets approve in sequence without shell commands. |
| H12–13 | Remove variable pricing, tokens, and marketplace features; strengthen the atomicity explanation. |
| H14 | Test network latency and prepare a live read of an already settled program state. |
| H15 | Scope freeze: fixed fixture plus one reject branch. |
| H16 | A captures program ID, explorer links, and reset accounts; D records backup. |
| H17 | C simplifies labels to “all four move / nobody moves.” |
| H18–19 | Submit and rehearse only the graph, approval, settlement, and rejection. |

**Four-hours-behind route:** fixed 4-cycle and generated demo wallets; do not build open matching or calendar integration.  
**Minimum winning version:** one computed cycle, actual devnet atomic settlement, actual refusal branch.  
**Abandon at H5 if:** program state cannot demonstrate all-or-nothing behavior.

## 3. Proxy Passport / Airlock — Traveling × Auth0

| Hour | Concrete checkpoint |
|---|---|
| H0 | D writes a two-action disruption script: hold allowed, cancel denied; B defines scope policy. |
| H1 | A creates Auth0 tenant/app and protected mock-airline API; C sketches the permission passport. |
| H2 | Sponsor gate: a request without correct Auth0 authorization receives a real protected-resource denial. |
| H3 | A maps search, hold, and cancel to scopes; B builds policy middleware and audit record. |
| H4 | C renders a replacement flight and action cards; D supplies a mock itinerary fixture. |
| H5 | **2am break test:** agent can hold but cannot cancel; traveler approval changes only the cancel result. |
| H6–7 | A attempts delegated token/Token Vault path; preserve RBAC-protected mock provider as the reliable fallback. |
| H8–9 | C shows allowed, denied, pending approval, and audit states in one linear screen. |
| H10–11 | Cold run uses an ordinary browser session and no hidden admin override. |
| H12–13 | Remove route recommendations, chat, real airline OAuth, and any unrelated booking interface. |
| H14 | D rehearses the “agent never sees credentials” explanation with a request log. |
| H15 | Scope freeze: one traveler, one tool, one denied action, one approval. |
| H16 | Capture a backup video from fresh login through audit. |
| H17 | Test authorization expiry or deliberate policy mismatch. |
| H18–19 | Submit and rehearse the denial before the approval; it is the story. |

**Four-hours-behind route:** use a first-party mock airline API under real Auth0 authorization; omit external OAuth connection.  
**Minimum winning version:** protected hold succeeds, protected cancel fails, approval changes it, audit persists.  
**Abandon at H5 if:** the interface is only a role toggle without a protected action failing.

## 4. Triangulate — Multiplayer × Gemini

| Hour | Concrete checkpoint |
|---|---|
| H0 | D creates three staged reports that conflict on one observable fact; B specifies three candidate claims. |
| H1 | A gets Gemini multimodal structured output with claim, evidence, confidence, and uncertainty fields. |
| H2 | Sponsor gate: photo, voice note, and text each produce schema-valid claims attached to original evidence. |
| H3 | B implements contradiction detection and a simple information-gain ranking for next observations. |
| H4 | C creates a shared claim graph; A adds a room/websocket or lightweight synchronized state. |
| H5 | **2am break test:** conflicting reports generate one actionable request, and the staged answer updates shared confidence. |
| H6–7 | Add source chips and conservative wording; do not let Gemini manufacture a resolved fact. |
| H8–9 | C stages three device panes and an obvious red-to-green claim transition. |
| H10–11 | D runs the room with three browsers and an uninvolved observer. |
| H12–13 | Trim to one claim conflict and one requested observation; remove broad incident-management features. |
| H14 | A prepares cached structured responses with the raw evidence still displayed. |
| H15 | Scope freeze: three reports, one request, one shared update. |
| H16 | Record the complete multi-device path. |
| H17 | Test without live webcam/audio; ensure fixture uploads preserve the visual story. |
| H18–19 | Submit and rehearse the point that it assigns verification rather than summarizing rumors. |

**Four-hours-behind route:** pre-stage the three files and use single-device tabs representing teammates; retain shared-state update.  
**Minimum winning version:** conflict graph, one information-gain request, one evidence-driven state change.  
**Abandon at H5 if:** it cannot name a next observation more informative than “tell me more.”

## 5. StaleMap — Traveling × MongoDB Atlas

| Hour | Concrete checkpoint |
|---|---|
| H0 | B makes a tiny graph with two routes and one elevator edge; D creates old, outage, and restoration reports. |
| H1 | A provisions Atlas and writes timestamped claim documents; C renders the two routes. |
| H2 | Sponsor gate: Atlas receives and retrieves a report with evidence metadata and time. |
| H3 | B implements freshness/conflict score and a deterministic route-cost adjustment. |
| H4 | C shows green accessible path with a confidence badge and an alternate route. |
| H5 | **2am break test:** submitting outage evidence lowers confidence and flips the recommended route. |
| H6–7 | A adds Atlas change-stream/poll update; B adds expiry timer and restoration evidence. |
| H8–9 | C makes provenance, recency, and route effect readable in a single screen. |
| H10–11 | Cold run from clean database: old report, outage, reroute, new photo, restoration. |
| H12–13 | Cut maps beyond the fixture; preserve only real graph/routing logic and evidence history. |
| H14 | D tests conflicting reports and explains conservative behavior when uncertain. |
| H15 | Scope freeze: two routes, one edge, three evidence events. |
| H16 | Capture backup and seed a fresh demo collection. |
| H17 | Verify UI still works if Atlas update is delayed; use an explicit refresh state. |
| H18–19 | Submit and rehearse the sentence “a pin is not evidence.” |

**Four-hours-behind route:** use a local graph and Atlas-backed report history; omit a geographic base map.  
**Minimum winning version:** two routes, evidence timestamp, confidence calculation, reroute.  
**Abandon at H5 if:** a new report does not deterministically alter the route.

## 6. ConstraintLens / Bracket Patch — Optimization × Gemini

| Hour | Concrete checkpoint |
|---|---|
| H0 | D prepares one sticky-note board photo with a deliberate impossibility; B encodes the expected constraints. |
| H1 | A proves Gemini image-to-JSON extraction; C draws board and repair panel. |
| H2 | Sponsor gate: photo returns typed tasks, people, availability, and dependency fields with validation. |
| H3 | B implements satisfiability check and extracts one minimal unsat core. |
| H4 | B computes smallest repair; C animates original notes to repaired board. |
| H5 | **2am break test:** photo directly causes a three-change-or-fewer repair with no manual retyping. |
| H6–7 | A builds correction affordances only for model uncertainty; B records explanation of why each change is needed. |
| H8–9 | C emphasizes red conflict, exact change count, and before/after feasibility. |
| H10–11 | D gives an outsider the photo and asks whether they can predict the result without explanation. |
| H12–13 | Remove natural-language planning, collaboration, and general calendar features. |
| H14 | Prepare one manually encoded fallback board, disclosed as a fixture only if API fails. |
| H15 | Scope freeze: one photo, one core, one minimal patch. |
| H16 | Video record the fastest clean path. |
| H17 | Test schema errors and show a non-deceptive “needs confirmation” state. |
| H18–19 | Submit and rehearse the repair as the climax. |

**Four-hours-behind route:** use a fixed photographed fixture with extracted JSON cached, but keep solver and repair live.  
**Minimum winning version:** camera input, typed constraint view, unsat core, minimal visual repair.  
**Abandon at H5 if:** user must construct the board manually before the optimization begins.

## 7. Sizzle Oracle — Food × ElevenLabs

| Hour | Concrete checkpoint |
|---|---|
| H0 | D collects three legal recorded clips: quiet, simmer, and frying/overheat; B labels time windows. |
| H1 | A proves ElevenLabs speech output and input/response latency; C builds one pan-state display. |
| H2 | Sponsor gate: a state transition produces concise ElevenLabs voice within an acceptable delay. |
| H3 | B implements a simple spectral/energy classifier or deterministic threshold over the known clips. |
| H4 | C maps threshold crossing to one action card and voice-confirmation state. |
| H5 | **2am break test:** the signal crosses once, speaks one instruction, and accepts “done.” |
| H6–7 | Improve clips/classifier robustness; A adds voice input or button fallback for confirmation. |
| H8–9 | C makes waveform, threshold, state, and action visible rather than hiding the technical mechanism. |
| H10–11 | D runs clips through speakers/microphone and direct upload to discover noise failures. |
| H12–13 | Cut recipes, free-form chat, timers, and multiple dishes. |
| H14 | Prepare direct-audio upload fallback if live microphone is unreliable. |
| H15 | Scope freeze: one pan transition, one terse intervention, one confirmation. |
| H16 | Record backup with clean audio. |
| H17 | Test a negative/noise clip and ensure it does not narrate falsely. |
| H18–19 | Submit and rehearse why audio, not a timer, caused the instruction. |

**Four-hours-behind route:** known audio file uploaded to the app, threshold classifier, ElevenLabs response; omit live microphone.  
**Minimum winning version:** signal trace, state change, one spoken action, confirmation.  
**Abandon at H5 if:** the classifier cannot distinguish the prepared transition reliably.

## 8. FairTable — Multiplayer × Solana

| Hour | Concrete checkpoint |
|---|---|
| H0 | B fixes four participant preferences and defines a tangible post-reveal edit attack; D scripts it. |
| H1 | A creates devnet wallets/program or hash commitment transaction; C draws private sliders and locked dots. |
| H2 | Sponsor gate: a devnet commitment transaction is confirmed and its input cannot be changed in place. |
| H3 | B implements deterministic aggregate choice from revealed constraints. |
| H4 | C hides individual values, shows commitment completion, and displays aggregate reasons. |
| H5 | **2am break test:** demonstrate an attempted late preference edit failing or becoming a new visible commitment. |
| H6–7 | A adds reveal verification; B checks results are deterministic across clients. |
| H8–9 | C stages four phones plus one shared result screen with no wallet jargon in the opening. |
| H10–11 | D cold-runs commit, reveal, attack, and result using pre-funded wallets. |
| H12–13 | Cut restaurant search, payments, token rewards, and generic social networking. |
| H14 | Test offline/reset plan and capture Explorer proof. |
| H15 | Scope freeze: four voters, one attack, one reveal, one result. |
| H16 | Record backup; seed pre-funded demo accounts. |
| H17 | Ask a skeptic whether a normal poll would be equivalent; clarify the attack proof. |
| H18–19 | Submit and rehearse the trust property in plain language. |

**Four-hours-behind route:** fixed preference fixture and one commitment/reveal pair; omit multi-device wallet UX.  
**Minimum winning version:** hidden inputs, actual commitment, attack prevention, deterministic reveal.  
**Abandon at H5 if:** the team cannot explain a real harm the commitment prevents.

## 9. Resilience Canvas — Optimization × Vultr

| Hour | Concrete checkpoint |
|---|---|
| H0 | B prepares small delivery graph, uncertainty inputs, and expected robust allocation; D scripts road closure. |
| H1 | A gets a Vultr compute job/VM container to execute a simple Monte Carlo run; C renders initial route. |
| H2 | Sponsor gate: a remotely executed job returns a scenario result visibly tied to the UI. |
| H3 | B implements baseline versus robust objective over a small scenario set. |
| H4 | C adds failure-world meter and allocation comparison. |
| H5 | **2am break test:** closure/no-show runs multiple worlds and selects a different, lower-regret allocation. |
| H6–7 | A parallelizes or batches scenarios; B adds one explanation of why sunny-day optimum loses. |
| H8–9 | C visualizes five mini-worlds converging on a robust decision. |
| H10–11 | D cold-runs with a new closure and checks remote job latency. |
| H12–13 | Cut geocoding, large maps, live fleet data, and arbitrary optimization parameters. |
| H14 | Prepare a fixed remote result fallback and make its source timestamp visible. |
| H15 | Scope freeze: one failure input, five scenarios, one allocation switch. |
| H16 | Record backup with job ID/metrics. |
| H17 | Test behavior when compute is delayed; show queued job rather than fake result. |
| H18–19 | Submit and rehearse why cloud computation changes the choice. |

**Four-hours-behind route:** five predeclared scenarios executed remotely; omit simulation editor.  
**Minimum winning version:** baseline, failure worlds, robust choice, visible remote compute evidence.  
**Abandon at H5 if:** the robust result equals a static heuristic with no meaningful scenario computation.

## 10. RumorClock — Multiplayer × MongoDB Atlas

| Hour | Concrete checkpoint |
|---|---|
| H0 | D writes a three-person claim timeline with evidence expiry; B formalizes state transition rules. |
| H1 | A provisions Atlas collection and change feed/polling; C creates shared room cards. |
| H2 | Sponsor gate: a new evidence event persists and appears in another browser. |
| H3 | B implements freshness decay and claim status transitions. |
| H4 | C makes verified, disputed, and stale states visibly distinct. |
| H5 | **2am break test:** no refresh causes a shared claim to decay; another participant’s evidence refreshes it everywhere. |
| H6–7 | A strengthens ordering/conflict handling; B adds one reason panel per state. |
| H8–9 | C stages three participant panes and time acceleration for the demo. |
| H10–11 | D cold-runs the participant handoff without narrative help. |
| H12–13 | Cut chat, general knowledge graphs, and incident feeds. |
| H14 | Prepare deterministic accelerated timestamps and a clean database reset. |
| H15 | Scope freeze: one claim, one decay, one refresh. |
| H16 | Record backup. |
| H17 | Test whether viewer understands why the claim changed state. |
| H18–19 | Submit and rehearse its multiplayer dependency. |

**Four-hours-behind route:** two browser clients with seeded Atlas events; retain live cross-client update.  
**Minimum winning version:** claim, timed decay, other-user evidence, shared refresh.  
**Abandon at H5 if:** a single person can fake the whole value proposition without shared state.

## 11. BatchBraid — Food × MongoDB Atlas

| Hour | Concrete checkpoint |
|---|---|
| H0 | D prepares three controlled batch timelines with one causal-looking divergence; B maps events. |
| H1 | A provisions Atlas time-series/normal collections; C draws braid timeline. |
| H2 | Sponsor gate: photos, temperatures, and observations persist as ordered batch events. |
| H3 | B implements alignment and earliest-divergence heuristic. |
| H4 | C lets the three lines braid, then split at a highlighted event. |
| H5 | **2am break test:** the system identifies the first divergence and produces one testable next trial. |
| H6–7 | A adds photo evidence links; B tests missing events and confidence labeling. |
| H8–9 | C emphasizes causal uncertainty rather than claiming proof from observational data. |
| H10–11 | D cold-runs with a changed batch fixture. |
| H12–13 | Cut recipe libraries, fermentation social feed, and predictive claims. |
| H14 | Seed reliable demo data and add a “hypothesis, not cause” label. |
| H15 | Scope freeze: three batches, one divergence, one next trial. |
| H16 | Record backup. |
| H17 | Ask an outsider whether it looks like a dashboard; tighten the intervention if so. |
| H18–19 | Submit and rehearse the controlled-experiment recommendation. |

**Four-hours-behind route:** seeded events and local alignment algorithm, with Atlas visibly holding event history.  
**Minimum winning version:** braided timeline, first split, evidence, next trial.  
**Abandon at H5 if:** it cannot give a decision better than “look at this chart.”

## 12. Allergrant — Food × Auth0

| Hour | Concrete checkpoint |
|---|---|
| H0 | D designs a non-medical dietary-constraint fixture and service expiry story; B defines minimal scopes. |
| H1 | A configures Auth0 app/protected kitchen API; C sketches diner and kitchen views. |
| H2 | Sponsor gate: kitchen cannot retrieve the constraint without valid authorization. |
| H3 | B models selective disclosure, acknowledgement, expiry, and audit events. |
| H4 | C makes diner disclosure smaller than a profile and kitchen acknowledgement visible. |
| H5 | **2am break test:** selected constraint reaches kitchen; acknowledgment logs; expiry removes access. |
| H6–7 | A adds actual revocation/expiry check; B tests unauthorized retrieval. |
| H8–9 | C removes medical language and makes “constraint reported by diner” unmissable. |
| H10–11 | D cold-runs the rights lifecycle. |
| H12–13 | Cut menu recommendation, health profiling, and generic account settings. |
| H14 | Prepare first-party protected mock kitchen fallback. |
| H15 | Scope freeze: disclose, acknowledge, expire. |
| H16 | Record backup. |
| H17 | Test expired-token/read denial. |
| H18–19 | Submit only if it clearly demonstrates an authorization primitive beyond login. |

**Four-hours-behind route:** first-party kitchen API protected by Auth0; no outside restaurant integration.  
**Minimum winning version:** minimal constraint, protected read, acknowledgement, real expiry denial.  
**Abandon at H5 if:** revocation is only a UI toggle or the pitch makes safety promises.
