# Raw worker output archive — /root/adversarial_jury

Captured from the completed worker response. This is retained separately from the synthesis and was not used as a reason to overwrite candidate records.

Ground truth: use the local opening notes as authoritative. The public site’s stale placeholder tracks are a source limitation, not a contradiction. This is a ~19-hour build for four people, one declared track, a ≤50-word track statement, and a three-minute judged demo. Judges score originality, technical difficulty beyond a wrapper, demo quality, usefulness, and track relevance.

## Red-team critiques and search strategy

1. **Coverage:** Do not generate twelve variations of “AI assistant for X.” Cover distinct mechanisms: active information acquisition, minimum-edit optimization, capability authorization, conditional contracts, real-time distributed state, and voice-driven state simulation.
2. **Judging:** Every candidate needs a visible proof event: unknown → verified allocation, attack → denied, 8 schedule moves → 2, or claimant no-show → backup settled. A judge should see the result before hearing the architecture.
3. **Sponsor depth:** Apply the removal test: if the sponsor is removed, does a core user capability disappear? Gemini must parse unstructured evidence; Auth0 must enforce scoped action approval; Solana must settle a real devnet transaction; ElevenLabs must run live conversation; Atlas must drive live state via change streams.
4. **Track depth:** Pick the track the product serves directly, not the sparsest presumed pool. A sparse track may only award one prize; a popular one may award multiple. Food is especially strong only when food is the product’s real user workflow.
5. **Feasibility:** Treat the first 45–90 minutes as a technical gate. No deployed Solana program, live Auth0 authorization primitive, Gemini structured-output parse, ElevenLabs conversation, or Atlas event stream by that point means kill or reframe.
6. **Demo:** Script a controlled fixture and a boring fallback. Live demos should use one input, one decision, one visual transition, one verified payoff. Do not depend on arbitrary handwriting, open-ended voice, network luck, or real external booking.
7. **Novelty:** Search both the user journey and the mechanism. Kill crowded ideas: group dining selector, suitcase-packing vision, generic group travel, voice cooking, AI murder mystery, queue vision, accessibility route scanner. The surviving ideas below have narrower mechanisms.
8. **Expected value:** Optimize the chance of winning either the chosen track or sponsor prize, not the count of prizes listed. A project with a 35% chance of a compelling demo and 25% conditional prize chance loses to a project with a 75% demo chance and 20% conditional prize chance.
9. **Credibility:** Never infer an allergen as fact, fake a blockchain settlement, or hide a security failure behind slides. Put uncertainty and safeguards in the product’s visible behavior.

Search sequence: generate mechanism-first cards for each sponsor/track pair; score and dedupe to 20–25; prior-art-kill at least half; run sponsor technical spikes on the top six; choose the project with a working primitive plus a 90-second proof event by the early-morning cutoff. Do not enter Vultr merely because the app is hosted there; the camera/GPU candidates were both crowded and risky.

## Twelve independent concepts

| Concept | Track × sponsor | Worker status |
|---|---|---|
| Ask Once | Food × Gemini | Finalist / #1 |
| Airlock | Traveling × Auth0 | Finalist / #2 |
| Bracket Patch | Optimization × Gemini | Finalist / #3 |
| Last Plate | Food × Solana | Finalist / #4 |
| Dispatch | Multiplayer × ElevenLabs | Finalist / #5 |
| Pulse Pantry | Food × MongoDB Atlas | Finalist / #6 |
| SourceSeal | Traveling × Sandia | Fold into Airlock; better as a feature |
| LineCraft | Optimization × Vultr | Kill: queue-vision market and feed/GPU risk |
| Passage | Traveling × Vultr | Kill: close accessibility-mapping prior art |
| LuggageFit | Optimization × Gemini | Kill: PackPilot-like prior art |
| Tableau | Food × Gemini | Kill: crowded group-dining products |
| Tether | Traveling × Atlas | Kill: crowded group-travel/navigation products |

## Worker finalist cards

### Ask Once — Food × Gemini — clear #1

Pitch: A pantry volunteer photographs an ambiguously labeled food donation. The system creates an evidence-tagged ingredient graph, then asks the single staff/donor question that will unlock the most safely eligible portions across households with hard dietary restrictions. Unknown facts never become “safe” through AI inference.

Why it wins: Gemini is visibly useful but the core technical value is a custom allocation and value-of-information solver. The before/after payoff is immediate and humane.

90-second route:

- 0–10: Show four household cards and a vague “red curry, six portions” donation. Only one household can be matched safely.
- 10–25: Scan the label. Gemini extracts structured evidence and marks sesame as unknown.
- 25–40: Solver selects: “Does the sauce contain sesame? Expected effect: +3 safely placeable portions.”
- 40–60: Volunteer confirms the fact. The allocation graph moves from 1 / 4 households safely served to 4 / 4.
- 60–78: Show why each match is permitted, with evidence provenance and blocked alternatives.
- 78–90: Show a second intake card and total verified meals unlocked.

Four-person / 19-hour plan:

- A: Gemini image/text-to-schema extraction with provenance.
- B: bipartite matching/min-cost solver plus question-ranking heuristic.
- C: intake, evidence graph, household cards, animated allocation UI.
- D: fixture data, safety rules, fallback responses, pitch and integration.
- Gate: working structured parse plus allocation flip by hour 2–3.

Prior-art risk: Menu/allergen scanners and food-rescue matchers exist. The differentiator is not scanning or matching alone; it is choosing the one verified question with the highest expected allocation gain.

Killer objection: “You are making unsafe allergy recommendations.”  
Answer: The product must visibly withhold a match unless a hard constraint is explicitly verified. It reports evidence and uncertainty, never medical or safety certainty.

### Airlock — Traveling × Auth0

Pitch: A travel agent that cannot silently access or transmit a traveler’s data or book something. Every external action becomes a purpose-, scope-, and expiry-limited consent card. Auth0 authorization/Token Vault keeps credentials out of the agent and requires human approval for sensitive actions.

90-second route:

- 0–10: User asks for an accessible Denver flight under $250 and says not to share passport data.
- 10–25: Auth0 sign-in and scope card show only calendar-read access.
- 25–40: A simulated malicious airline-page instruction tries to exfiltrate itinerary/calendar data. The tool proxy denies it for lack of scope.
- 40–62: Agent finds a qualifying flight and opens an approval card: “Hold one $238 flight for five minutes.”
- 62–78: User approves; the scoped action completes and the audit records it.
- 78–90: Show capability graph: itinerary accessible, passport sealed, booking action separately approved.

Killer objection: “This is an Auth0 sample with a travel skin.”  
Answer: The demo must begin with an actual attempted data leak and visibly deny it; then show a legitimate travel action succeeding only after granular approval.

### Bracket Patch — Optimization × Gemini

Pitch: An organizer photographs a real, scribbled tournament bracket. When a court closes or team arrives late, the app generates the minimum-disruption repair while preserving results, rest periods, and fairness.

90-second route:

- 0–10: Photograph a paper eight-team bracket.
- 10–25: Gemini produces an editable structured bracket with confidence flags.
- 25–38: Trigger “Court 2 unavailable” or “Team 6 arrives 20 minutes late.”
- 38–57: Compare naïve reschedule: eight moved matches; Bracket Patch: two moves, no rest violation.
- 57–75: Add a constraint and recompute.
- 75–90: Show flagged parsing correction and objective score.

Killer objection: “Use a spreadsheet.”  
Answer: Make the solver’s reduction in moved matches/rest violations the centerpiece, not OCR novelty.

### Last Plate — Food × Solana

Pitch: Surplus food often goes unclaimed after someone reserves it. A time-limited devnet pickup pledge automatically advances food to a ranked backup claimant after a no-show; QR pickup attestation settles the pledge.

Worker’s qualifier: food-rescue and blockchain food-chain products are close. The narrow differentiator is conditional no-show handoff rather than generic food provenance. Wallet friction is a major objection.

### Dispatch — Multiplayer × ElevenLabs

Pitch: Four people rehearse event-volunteer coordination through browser radio roles. A formal incident state machine assigns required tasks; an ElevenLabs dispatcher speaks to the right role, handles interruption, and reassigns work after a failure.

Worker’s qualifier: voice agents and training simulations are crowded. A visible interdependent human-role state machine, not expressive audio, would have to carry the case.

### Pulse Pantry — Food × MongoDB Atlas

Pitch: Multiple pantry volunteers enter batches, household constraints, claims, and expirations simultaneously. Every durable change reruns allocation and updates all stations live, preventing double allocation of scarce food.

Worker’s qualifier: food-rescue and real-time inventory systems are close. It survives only when durable live change/replay and conflict prevention are unmistakably more than CRUD.

## Worker ranking

1. Ask Once — Food × Gemini  
2. Airlock — Traveling × Auth0  
3. Bracket Patch — Optimization × Gemini  
4. Last Plate — Food × Solana  
5. Dispatch — Multiplayer × ElevenLabs  
6. Pulse Pantry — Food × MongoDB Atlas

Clear #1: Ask Once. The worker found it strongest on usefulness, technical substance, sponsor depth, demo clarity, safety-conscious credibility, and 19-hour feasibility. The live 1 safely matched household → 4 transition is stronger than an explanation of a model.

