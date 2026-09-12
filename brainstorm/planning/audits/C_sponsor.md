# Auditor C — Sponsor-Prize Audit

Adversarial. No project ideas. Sources: `competition_ground_truth.md`, `mlh_and_opening.md`, `fable_plan.md`, `astra_plan.md`, `synthesized_plan_v1.md` only.

**Question:** Does the process optimize *real* sponsor eligibility **and** depth (bolt test), including IFM / Cursor / Sandia UNKNOWN bars? Stacking vs API soup?

**Answer:** It optimizes an internal “distinctive use” aesthetic. It does **not** model official eligibility as a separate fact. UNKNOWN event bars are invented, clock-mismatched, or both. Assigned STACK pairs plus 20 recombiners are a soup factory with a self-reported bolt checkbox.

---

## Verdict

| | |
|---|---|
| **Score** | **56 / 100** |
| **Launch 100?** | **NO** |

MLH six: the distinctive constraints (devnet state, voice-as-loop, visible compute, identity-as-primitive, Atlas feature, multimodal Gemini) match `mlh_and_opening.md` and will beat checkbox wrappers *if* those categories are judged on depth. Official bars are weaker than that. The plan treats “our bar” as if it were the prize rule, then zeros `p` for anything that merely meets the written rule. That is not eligibility optimization. That is taste.

IFM / Cursor / Sandia: objects VERIFIED, bars UNKNOWN or LIKELY-unstated. The synthesized plan still allocates 10 cells to IFM+Sandia, 0 to Cursor, and writes allocation branches that fire at **preflight** — before the workshops that could answer the UNKNOWNs.

Stacking: “max 3 + bolt” is the right slogan. The mechanism (pre-assigned pairs, Gemini-rides-free, cohort floors, 20 recombiners, undefined `SponsorWinScore_p`, hours-gate deleted) produces API soup.

---

## What is actually true (do not upgrade)

Ground truth, not the plans:

- Sponsor prizes are **not track-locked**. Grand + track + IFM + Cursor + Sandia + People’s + Design + any MLH Best Use can theoretically stack. UNKNOWN whether judges mentally double-count.
- Official MLH bars are thin: Gemini = use the API; Auth0 = **any** Auth0 API (login counts); Atlas = build using Atlas; Vultr = cloud compute/deploy (hosting-only = weak, **LIKELY**, not illegal); ElevenLabs = autonomous audio / a voice; Solana = real **devnet** tx/program.
- Distinctive-capability columns are **our scoring**, not written rules. Ground truth says this out loud for Gemini.
- IFM: use IFM tools (K2 etc.). Bar = **LIKELY** load-bearing, **not stated**.
- Cursor: object VERIFIED; eligibility **UNKNOWN**. Do not assume “we coded in Cursor” wins.
- Sandia: cyber-themed; extra rules **UNKNOWN**.
- IFM as fifth *track* vs optional prize: **UNKNOWN** (conflict #5).
- List only sponsors actually used and demoable.
- Logo sponsors with no opening prize: do not invent. Querit has no prize.
- Workshop clock: IFM 9–10pm TEP 1403; Cursor/Grok 10–10:30pm; expo 7–9pm. K2 access method UNKNOWN.

Astra kept official vs internal standards separate and gave `E` anchors (`1` = unresolved). Synthesized dropped both and kept Fable’s binary bolt.

---

## Ranked flaws

### 1. Official eligibility and competitive depth are one knob

**Rank: 1 — fatal to the question**

Fable §5.3 / synthesized: any sponsor that is not load-bearing gets `p = 0`. Bolt fail → `B = 10`, that `p = 0`. Cohort hard constraints fail login-gate, persist-only, hosting-URL, text-chat at **search** time.

Official world:

| Sponsor | Written bar | Plan’s kill / zero |
|---|---|---|
| Auth0 | Any Auth0 API, including login | Login gate = fail |
| Atlas | Using Atlas | Persist-only = fail |
| Gemini | Use Gemini API (chat/analyze/generate are the official examples) | Text chat = fail |
| Vultr | Compute / deploy; hosting-only weak LIKELY | Hosting URL = fail |

Those kills are reasonable *win* filters in a crowded checkbox field. They are false as *eligibility*. A thin Auth0 field can still award headphones to ordinary login. Hosting-only Vultr is weak, not `p = 0`. Gemini chat is the official example and the judging-slide loser for **HackCMU Technical Difficulty**, not automatically a Gemini Best Use loser.

Astra’s four outcomes (eligible+competitive / eligible+ordinary / unresolved / ineligible) were the correct instrument. Synthesized deleted them. `E` is listed and undefined against the official sentence. `SponsorWinScore_p` is named and never specified. Fable’s sponsor-sniper used `E+C+X+B` with `Q ≥ 3` hours. Synthesized remapped `Q` to “competitiveness” and deleted the hours gate. Agents can now claim three “deep” sponsors with no integration-time check.

**Effect:** Rankings will (a) throw away officially eligible ordinary use that wins a thin checkbox category, and (b) treat distinctive use as if it were required by the sponsor. Neither is “real eligibility AND depth.” It is depth-only, mislabeled.

**Fix:** Every claimed sponsor stores two fields, not one vibe:

- `official_eligibility`: `ineligible | official_met | unknown` with a quote of the written bar and a source.
- `competitive_depth`: bolt + named proof (Fable §7.2 name-the-thing list is mandatory, validator-enforced).

`p_k` priors:

- `ineligible` → 0
- `unknown` → cap 0.05 (see #2)
- `official_met` + bolt fail → small nonzero (0.02 or 0.05), never 0, unless the category is known-crowded *and* judges are known-depth (we do not know that)
- `official_met` + bolt pass → full bucket set

Define `SponsorWinScore_p` before launch or delete the ranking. Suggested: hours gate first (incremental > 2h → ineligible for sniper), then `(E_official_mapped) + C + X + (10−B) + Q` or any fixed formula written once. Never average sponsors. Restore Fable’s `Q`-as-hours as a **separate** letter (`Qh`) so competitiveness and cost are not one integer.

---

### 2. UNKNOWN bars are not capped; agents will invent `p`

**Rank: 2 — IFM / Cursor / Sandia**

`p_prize` includes `ifm`, `cursor`, `sandia` in the same `{0, .02, .05, .10, .20, .35, .50}` set as Solana. Overconfidence flag is only `p_any > 0.8`. An agent can put 0.35 on Cursor with a straight face.

Astra: Cursor “no claimed probability contribution” until the bar is known; `E = 1` when unresolved; unbuilt concepts cannot get `E = 4`. Synthesized dropped the anchors.

**Fix:** Packet-hard rule: if ground truth tag is UNKNOWN or LIKELY-unstated, `p_k ≤ 0.05` and `E ≤ 2` until `live_verification.md` contains a **verbatim** sponsor/organizer sentence. Red team must overwrite agent `p_k` for those three. Jury may raise the cap only after that sentence exists.

---

### 3. Cursor: zero search, wrong clock, two bad stories

**Rank: 3**

Verified prize. Bar UNKNOWN. Synthesized allocation: **0 Cursor cells**. Only branch: “If Cursor bar requires Grok Imagine/Bot in-product: steal 070–071 from stack.”

That branch is timed at **preflight**, before the 10:00–10:30pm Cursor workshop. Preflight cannot know the bar. The 100 will not search Grok-in-product. If the bar is “built with Cursor,” every finalist may already be eligible and `p_cursor` is a crowded lottery / documentation contest — not a cohort, not a 2h integration. The plan has no evidence checklist (usage log, screenshots, “built with” honesty) and no calibration for “everyone qualifies.”

Fable at least sent humans to the workshop and said: IDE-use → free rider on every finalist; Grok-required → 2h at recombination. Synthesized kept only the steal-two-stack-IDs line, which will not fire with information.

If they guess Grok and bolt Imagine onto a finished idea at 10:30pm, that is API soup on a prize whose rule they still have not heard.

**Fix:** No Cursor cohort in the 100. No preflight steal. Three **jury/recombination** branches after a human writes one sentence:

1. IDE / “built with Cursor” → evidence checklist on the chosen build; `p_cursor` = crowded-lottery bucket (0.02–0.05), not a search cell.
2. In-product Grok Imagine/Bot required and feasible in ≤2h → at most two recombination challengers; bolt substitute = generic image/video API; if demo unchanged, `p = 0`.
3. Still unknown at jury start → `p_cursor = 0` for all ideas. Do not steal STACK IDs.

---

### 4. IFM: bolt and Gemini fallback contradict; preflight will delete the cohort before the workshop

**Rank: 4**

Official: use IFM tools. Bar unstated. Access UNKNOWN (keys / weights / hosted). Workshop 9–10pm.

Synthesized requires **both**:

- K2 load-bearing (delete K2 → demo must change), and
- “mandatory Gemini fallback that keeps the demo.”

If Gemini keeps the demo, K2 fails the bolt test → `p_ifm = 0` while sitting in the IFM cohort. Unless the fallback is **visibly worse or different** and labeled as fallback, the two constraints cancel.

Fable distinctive K2 uses (local/offline, logits, LoRA, K2-as-judge) are **assumed capabilities**. Ground truth does not verify any of them. Five agents will hunt a model-internals prize that may be a hosted chat endpoint.

Clock: “Do not wait on K2” **and** “If K2 is dead at preflight: 091–092 → open-world, 093–095 → demo-first.” Preflight is before the workshop. K2 will look dead. The plan reallocates the only IFM-shaped search, then a hosted endpoint may appear at 9:30pm into a population with no IFM cells.

IFM-as-track (conflict #5): Fable/synthesized ASSUME prize-not-track and “no allocation changes; only the 50-word field.” Astra: if IFM occupies the only track slot, you **cannot** stack IFM + themed track. Synthesized dropped that. If the form is a single track pick and IFM is a fifth option, `p_ifm` and `p_track_*` are mutually exclusive. The P(any) formula does not know that.

**Fix:**

- Keep 5 IFM cells through launch. Do **not** reallocate at preflight-before-workshop.
- Fallback must be explicitly degraded or capability-different; demo-sim must show the K2 beat and the fallback beat. Same-looking Gemini ≠ fallback, it is a bolt fail.
- `p_ifm ≤ 0.05` until `live_verification` records a successful allowed call (or weights/endpoint in hand).
- Distinctive search constrained to **verified** K2 properties after the workshop note, not a pre-written LoRA/logit wishlist.
- Packet: if Google Form makes IFM a fifth *track*, IFM and themed-track placements are mutually exclusive; do not add those `p_k`. If IFM is an extra prize, keep current stack assumption.

---

### 5. Sandia: invented genre, 5 cells, tournament floor

**Rank: 5**

Official: cybersecurity-themed, extra rules UNKNOWN. Synthesized hard constraint: “Real security mechanism on stage.” Fable goes further: attack→detect→explain, defensive/educational. Banned password-checker is fine as a *weak idea* filter. It is not the Sandia rubric.

Unknown extra rules can be citizenship / US-person, writeup-only, a prescribed challenge, critical-infrastructure theme, or “any cyber sticker.” Five agents overfitting a stage-demo genre either miss the real bar or burn 5% of search. Fable §6.2 mentions a citizenship gate; synthesized only “if Sandia gate fails us → open-world” at **preflight**. Expo is 7–9pm. If that table is missed, the gate is still UNKNOWN at launch and at jury unless someone asks.

Tournament: synthesized “each cohort ≥2” at the 50-cut **forces** Sandia ideas forward. Fable also floors ≥1 Sandia if any survived red team. Astra: no guaranteed sponsor seats. Floors turn UNKNOWN-bar sketches into recombination parents.

**Fix:** Cohort constraint = cyber theme + one real mechanism (not a prescribed three-act). `p_sandia ≤ 0.05` until extra rules are a verbatim sentence in `live_verification`. If still unknown at jury, keep the idea only as overall/track; Sandia `p = 0`. **No sponsor cohort floors.** Track floors can stay. Human: one question at Sandia table or Discord before jury, not “preflight magic.”

---

### 6. STACK pairs + 20 recombiners = designed soup

**Rank: 6**

STACK IDs 062–071 are **assigned** pairs (Auth0+Mongo, Solana+Mongo, ElevenLabs+Gemini, …). The agent’s job is to invent a product in which both sponsors pass bolt. That is sponsor-first search, the definition of soup. Astra: a third integration only if the product already needs it, ≤45 min, no new unverified critical dep, proof inside the existing 3-min story, and removing the *prize* would not remove the capability. Synthesized STACK ignores all five.

Fable anti-leak: if >40% of developed ideas list ≥3 sponsors, STACK leaked — cap and re-rank. Synthesized dropped the check. Kept “max 3.”

Gemini “rides free” across LLM ideas. Unspecified whether free-rider Gemini counts toward the 3. STACK already has two; Gemini-as-third + Cursor-as-fourth is the default claim pattern. Bolt substitute for Gemini must be **another model**, not `print`. If another model leaves the demo unchanged, Gemini is bolted even when “used.” Wrapper test (delete LLM entirely) is a different test. The plan runs both without defining the Gemini substitute. Agents will pick whichever keeps the sponsor.

Recombination: synthesized **20** agents (user count; Fable had 6) gluing “grand-path + a sponsor’s load-bearing mechanism.” That is how you get a coherent core wearing two extra APIs. Astra: combining two sponsor stacks is not sufficient; at most 12 challengers, at most six in the 30. Synthesized has no cap on sponsor-adding hybrids.

Demo: Fable reserves 30s for “sponsor moment(s).” Astra: proof inside the core story, no per-sponsor mini-demo. Synthesized “90s scripts” vs official **3 min**. A 90s sim that still tries to show two sponsor miracles is soup theater. Official judging is one 3-minute demo, not a highlight reel of logos.

**Fix:**

- Delete assigned pairs. Ten “stack” cells become “one primary sponsor thesis; second only if the product needs it before the prize is named.”
- Restore the >40% ≥3-sponsor leak check.
- Gemini third-sponsor default = banned unless bolt substitute is a non-Gemini model **and** the demo changes (modality / tools / structured constraint a generic chat model lacks).
- Cursor IDE-use does not occupy a sponsor slot.
- Recombination: ≤6 hybrids may *add* a sponsor; each must re-pass bolt, incremental ≤2h, no new UNKNOWN dependency, proof inside the existing transform. 20 recombiners can exist for *mechanism* hybrids; they do not all get to add APIs.
- Final pick: **one** committed primary sponsor + at most **one** committed secondary. Everything else is conditional and does not get a demo beat. Restore Astra’s `committed_prize_targets` / `conditional_prize_targets`.
- Demo-sim must be a full 3-minute script (165s target + 15s margin is fine). 90s is a compression, not a second official format. At most one dedicated sponsor proof beat.

---

### 7. Self-reported bolt is gamed; “judge would notice” ≠ depth

**Rank: 7**

Validator: sponsors listed only if `bolt_changes_demo === true`. Claiming a prize requires checking the box. The substitute is agent-written. Red team re-runs bolt — necessary, not sufficient — then 20 recombiners add more checks.

“Does the 3-minute demo change in a way a judge would notice?” is theater. A change-stream that increments a counter is noticeable and still persist-adjacent. A role that greys a button is noticeable and still login-adjacent. Structured Gemini filling a form is noticeable and still a wrapper.

Astra’s four tests (eligibility / removal / depth / proof) asked for computation, state, identity decision, transaction, or interaction — and a **trace**. Synthesized collapsed to bolt + letters.

**Fix:** Bolt remains a kill for *sniper* claims, not a checkbox. Require Fable’s per-sponsor name-the-proof or reject the JSON:

- Solana: on-chain state + who reads it + signature/program the judge sees
- Vultr: job + what the audience sees that a laptop cannot fake
- Auth0: identity decision that changes behavior
- Atlas: named feature + query
- ElevenLabs: who speaks to whom, live
- Gemini: modality or tool a chat box lacks
- K2: verified property Gemini cannot substitute
- Sandia: mechanism, not sticker
- Cursor: the actual bar’s evidence, or no claim

Red team classifies each claim into Astra’s four outcomes and **replaces** `p_k` and `B`.

---

### 8. Live-verification clock does not match UNKNOWN resolution

**Rank: 8**

| UNKNOWN | When it can be answered | When the plan acts |
|---|---|---|
| Sandia extra rules / gate | Expo 7–9pm, table, Discord | Preflight reallocate; may already have missed expo |
| Vultr $100 code | MLH table / Coach / Discord | Preflight reallocate |
| K2 access | Workshop 9–10pm | Preflight “if dead” **and** “don’t wait” |
| Cursor bar | Workshop 10–10:30pm | Preflight steal (too early); jury 10:15 (Fable) starts before workshop ends |
| IFM as track / form URL | Organizers / Discord | “Nothing changes” — wrong if it is a track |

Synthesized adopted Fable’s “UNKNOWNs change weights not cells” for launch, then wrote cell-changing preflight branches that cannot see the answers. Humans: IFM workshop vs loop-1 vs Cursor workshop vs jury overlap is underspecified. Missing Auth0 newsletter trap and ElevenLabs quota from the synthesized preflight list (they exist in Fable §6.2 / sponsor research).

**Fix:** Launch cells do not change at preflight for K2 / Cursor / Sandia. Humans: one delegate, written questions, one sentence each into `live_verification.md`. Jury reads it; `p` caps lift only then. Cursor note may arrive mid-jury — late addendum, not a new cohort. Auth0 signup path and ElevenLabs quota stay on the human checklist.

---

### 9. Specialist track rotation fights Relevance and banned attractors

**Rank: 9**

Home track = `id mod 4` across Opt / Multi / Travel / Food. MLH prizes are not track-locked, but **Relevance is judged for the one named track**. Forcing Food/Travel onto Auth0/Solana/Gemini specialists pushes stretch “why” or the banned recipe/itinerary basin. Track prize depth (1st only if sparse) is modeled in prose, not in `p_track_*`.

**Fix:** Specialists pick the track the mechanism is honestly relevant to. Rotation is a soft prior, not a hard constraint (synthesized already says “soft lens” — then make the validator accept any of the four and reject a 50-word stretch). `p_track_2nd_or_3rd = 0` unless the packet has evidence that track will award depth.

---

### 10. Per-teammate hardware and EV vs P(any)

**Rank: 10 — smaller, still real**

Objective is P(≥1), not hardware EV. Fable weights Solana/Auth0 at 5 because of per-teammate objects; synthesized correctly demotes EV to tie-break. Good.

Residual: STACK and floors still over-sample per-teammate categories (Auth0 8, Solana 8, Mongo 6, plus STACK pairs that include them). That is search investment, not a reserved win. Acceptable if floors die (flaw 5–6). Do not let EV sneak back in via human “we want the Ledgers” at the veto step without writing it down — if the team prefers hardware, say so before launch so A/G do not lie.

Raffle: Astra excludes from concept selection. Synthesized silent. Fix: `p` unused; submit on time.

People’s / Design: UNKNOWN mechanics. Demo-first is enough. Do not invent rubrics. `p` stay low.

---

## What is not wrong

- Not inventing Tiger Data / Presage / logo-only prizes. Querit = no prize.
- Solana = visible devnet state. Matches partner docs.
- ElevenLabs official bar is already close to “voice is the loop.” Least broken specialist.
- Wrapper test, hardware/data/paid-API kills, “list what you can demo.”
- Specialists must write ≥5 raw ideas that remain a product if the sponsor is deleted (Astra, kept). That is the right anti-shell device — if the rest of the scoring does not zero official-ordinary use.
- One track. MLH not track-locked. Max team 4. 3-minute official demo.
- Cursor not assumed to be “we used the IDE.”
- IFM treated as extra prize until the form says otherwise — *as an assumption*, if the mutual-exclusion branch is restored.

---

## Stacking vs API soup (direct)

| Control | Status |
|---|---|
| Max 3 sponsors | Written |
| Bolt test | Written, self-scored, theater-threshold |
| Assigned STACK pairs | **Soup** |
| Gemini rides free as 3rd | **Soup** |
| 20 recombiners adding mechanisms | **Soup** unless capped |
| Cohort floors for sponsors | **Soup / UNKNOWN pollution** |
| Hours gate on sniper rank | **Deleted** |
| >40% ≥3-sponsor leak check | **Deleted** |
| Committed vs conditional prize lists | **Deleted** (Astra had them) |
| Official-easy `p > 0` | **Deleted** (everything non-bolt → 0) |

Net: the process will produce fewer *honest* checkbox claims and more *narrated* multi-API cores. Judges still see one 3-minute demo. Three load-bearing integrations is still three live deps. Estimator taxes exist; the selection rule does not force them to win.

---

## Fixes (do these before any 100)

1. Split official eligibility vs depth; write `SponsorWinScore_p`; restore hours as its own gate.
2. Cap `p_ifm`, `p_cursor`, `p_sandia` at 0.05 until a verbatim bar/access sentence exists.
3. Cursor: no cohort, no preflight steal; three post-workshop branches only.
4. IFM: keep 5 cells; degraded/labeled fallback; no preflight death; IFM-as-track mutual exclusion.
5. Sandia: no genre fiction; no sponsor floors; `p` capped.
6. Kill assigned STACK pairs; restore leak check; cap sponsor-adding recombinations; committed ≤2 prize targets.
7. Enforce name-the-proof in JSON; red team replaces `p_k` with four-way eligibility class.
8. Fix verification clock to workshops/tables, not preflight fantasy.
9. Specialist track is chosen, not `id mod 4` forced.
10. Packet copy-paste from ground truth: UNKNOWN stays UNKNOWN; distinctive column labeled **internal**.

---

## Score (56)

| Slice | /100 | Why |
|---|---:|---|
| MLH six: official vs depth | 62 | Right distinctive hunts; wrong eligibility zeros; Gemini/Auth0/Atlas official bars ignored |
| Bolt test integrity | 58 | Exists, operational, gamed, notice ≠ depth |
| IFM / Cursor / Sandia UNKNOWNs | 34 | Invented bars, contradictory IFM fallback, Cursor unsearched, wrong clock |
| Stacking discipline | 47 | Slogan good; pairs + recombiners + floors + free-rider Gemini |
| Packet honesty (no invented prizes) | 85 | Clean on logo-only and Querit |

**56** is “the slogans are correct and the instrument is not.” Not launch-ready.

---

## Launch 100? **NO**

Not because runtime/pilot (out of scope here). Because a 100-agent run with this sponsor instrument will:

1. Search the wrong object (internal distinctive-use, not official ∩ depth).
2. Burn or delete IFM/Sandia cells on a clock that cannot know the bars, and never search Cursor.
3. Manufacture STACK/recombination soup that the bolt checkbox will stamp as organic.
4. Rank with an undefined `SponsorWinScore_p` and `p_k = 0` for legally eligible ordinary use.

Launch after the ten fixes are in `final_ideation_plan.md` and the packet states official vs internal bars in two columns. Do not wait on K2/Cursor/Sandia *answers* to start — wait on *rules for what UNKNOWN means* in `p`, allocation, and floors. Those rules can be written now.

Do not launch agents.
