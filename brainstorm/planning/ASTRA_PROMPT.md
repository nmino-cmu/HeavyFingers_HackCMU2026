# CLI Astra — design the HackCMU 2026 ideation search (do not generate project ideas)

You are GPT-6-Astra via Codex CLI. **Planning only.** Do not invent 100 project ideas. Do not launch agents. Design the *search architecture* for a later 100-agent ideation phase.

Read (if you can access the filesystem):

- `/Users/nicholasmino/ProgrammingFiles/HackCMU/brainstorm/research/competition_ground_truth.md`
- `/Users/nicholasmino/ProgrammingFiles/HackCMU/brainstorm/research/prior_winners/notes.md`
- `/Users/nicholasmino/ProgrammingFiles/HackCMU/HACKCMU_PRIZES_TRACKS.md`

If you cannot read files, use the GROUND TRUTH SUMMARY below as complete.

Write a complete plan as markdown. If you can write files, save it to:

`/Users/nicholasmino/ProgrammingFiles/HackCMU/brainstorm/planning/astra_plan.md`

Otherwise return the full markdown in your reply (the parent will save it).

No TBD. Resolve choices. Ignore “Only at CMU” / campus-forced ideas.

---

## GROUND TRUTH SUMMARY (Fri Sep 11, 2026 ~8:30pm EDT)

HackCMU 2026 Midnight Express. 24h beginner-friendly. Team max 4. From scratch; no building/designing before Fri 9:00pm. Brainstorm OK. Any language/AI.

**Submit Sat 4:00pm EDT** Google Form: description + **one** track + 50-word why. Showcase 4:00–6:30pm. **3 min** talk+demo. 3 judge rooms. Winners ~7–8pm. ~19h build.

**Tracks (pick one):** Optimization / Traveling / Multiplayer / Food. Vague official blurbs. Theme fit = Relevance (track-only judging). Sparse track may only award 1st. **IFM (optional)** on tracks slide; separate IFM Prize. UNKNOWN if form lists IFM as a fifth track.

**Judging:** Originality, Technical Difficulty (real tech vs ChatGPT wrapper), Demo Quality (<3 min), Usefulness, Relevance (track only).

**HackCMU prizes (stackable):**
- Grand: HRT Poker Set
- Track 1/2/3: mini projector+Jump AirPods Pro / Visa swag / keyboard+keychain
- IFM: Kindle Lite (use K2 / IFM tools; bar not spelled)
- Cursor: Cursor keyboards (bar UNKNOWN)
- Sandia Cybersecurity: ANC AirPods (extra rules UNKNOWN)
- People’s Favorite: Ticket to Ride (vote UNKNOWN)
- Best Design: Fujifilm QuickSnap (rubric UNKNOWN)

**MLH Best Use (not track-locked, 1 team each on Devpost):**
- Gemini → Google swag. Use Gemini API (`gemini-3.8-flash` free). $300 Cloud ≠ AI Studio.
- ElevenLabs → earbuds. Live voice, not leftover MP3.
- Solana → Ledger Nano S Plus **each teammate**. Real **devnet** tx/program.
- Vultr → portable screens. Visible cloud/GPU, not “we have a URL.” $100 from MLH Coach.
- Auth0 → headphones **each teammate**. Any Auth0 API (login or agents). No card.
- MongoDB Atlas → M5Stack **each teammate**. Atlas as real data plane.

Opening did **not** add Jane Street / Citadel / Microsoft / Adobe / Roblox prizes. Querit has a search API, no prize. Copilot = workshop.

Workshops: IFM K2 Fri 9–10pm TEP 1403; Cursor/Grok Fri 10–10:30pm TEP 1403.

Field size UNKNOWN (Devpost 34 is undercount). 2025 grand Medicly = video→3D clinical mesh (visible transform). Many Gemini wrappers expected.

**Objective:** maximize P(≥1 prize) with a serious overall-win path. Not idea volume. Not trendy. Not consensus.

**Team:** can do ambitious ML/systems/CV/local models/realtime. Do not force those in. **Do not** design a CMU-campus-only idea cohort.

**Later execution (you are not doing this now):** 100 independent Grok 4.6 Extra High Fast agents, ≥15 raw concepts each, top 3 developed, structured reports; then recombination, red-team, build-sim, demo-sim, tournament, 12-person jury.

Default population (modify if you have something stronger; drop “Only at CMU” and reallocate those 5):
- 20 open-world overall
- 10 Gemini, 8 ElevenLabs, 8 Solana, 8 Vultr, 8 Auth0, 8 Mongo
- 10 multi-prize stack
- 5 anti-AI, 5 demo-first, 5 weird research-lab
- leftover 5: you choose (not campus-local)

Scoring later uses official U/T/O/D plus execution F/R/P/S, competitive N/M/J/W, per-sponsor E/C/X/B/Q, strategic A/G/H/K/Y, risks (higher=worse) I/API/DR/SR/CR/ER/AR/BR. Do not collapse to one score early. Five rankings: overall, P(any prize), sponsor-sniper, risk-adjusted, upside.

---

## Design these (required sections)

1. **Decomposition of idea search** — how 100 independent loops cover space without one mega-prompt.
2. **Diversity mechanisms** — priors, seeds, forbidden clichés, anti-mode-collapse.
3. **Prize targeting** — how specialists vs open-world vs stackers are weighted given 19h and stacking rules.
4. **Avoiding correlated agents** — information firewall; what is shared vs private.
5. **Scoring methodology** — how to use the rubric without fake precision; P(any prize) without naive sums.
6. **Information gathering** — what each agent must read; what to verify live (K2 access, Vultr code, etc.).
7. **Feasibility / sponsor-fit / novelty / demo assessment** — operational tests, kill rules.
8. **Expected-value reasoning** — prize weights you would use and why (per-teammate hardware vs swag vs grand).
9. **Selection + tournament architecture** — 100 → 50 → 30 → 15 → 8 → 1; recombination/red-team/build/demo/jury. When (if ever) agents inspect each other.
10. **Per-agent idea count** — defend ≥15 raw / top 3 or change it.
11. **Deceptively attractive bad ideas** — detection list (AI for X, Uber for X, bolted Auth0, etc.).
12. **One-day scope estimator** — algorithm/heuristic for hours and demo failure.
13. **Failure modes of this orchestration** — how the night gets wasted; mitigations.
14. **Concrete artifacts** — exact output filenames under `brainstorm/agents/initial/NNN.md` and JSON fields you require.
15. **Would you launch the 100 yet?** — yes/no + remaining UNKNOWN that would change allocation.

Be specific enough that a parent agent can execute without asking you again.
