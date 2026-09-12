# Brief for planners (Fable + CLI Astra)

HackCMU 2026 Midnight Express. Now: Fri Sep 11 ~8:23pm EDT. Hacking starts Fri 9:00pm. Submit Sat 4:00pm EDT. ~19h build. Team max 4. From scratch. 3 min demo. Discord acmatcmu.

## Prize list (must target ≥1)

| id | prize | object | enter |
|---|---|---|---|
| grand | Grand Prize | HRT poker set | all submits |
| track_opt | Optimization 1st/2nd/3rd | mini projector+Jump AirPods / Visa swag / kb+keychain | pick this track |
| track_travel | Traveling 1st/2nd/3rd | same | pick this track |
| track_multi | Multiplayer 1st/2nd/3rd | same | pick this track |
| track_food | Food 1st/2nd/3rd | same | pick this track |
| ifm | IFM Prize | Kindle Lite | optional; use K2 / IFM tools (MBZUAI). Not a required 5th track |
| cursor | Cursor Prize | Cursor keyboards | bar unstated; Cursor / Grok Imagine / Grok Bot |
| sandia | Sandia Cybersecurity | AirPods ANC | cyber-themed |
| people | People’s Favorite | Ticket to Ride | expo/audience |
| design | Best Design | Fujifilm QuickSnap | design |
| mlh_gemini | Best Use Gemini API | Google swag | Gemini visible in demo |
| mlh_11labs | Best Use ElevenLabs | wireless earbuds | live voice |
| mlh_solana | Best Use Solana | Ledger Nano S Plus **each teammate** | real **devnet** tx |
| mlh_vultr | Best Use Vultr | portable screens | actually hosted on Vultr |
| mlh_auth0 | Best Use Auth0 | headphones **each teammate** | real Auth0 login |
| mlh_mongo | Best Use MongoDB Atlas | M5Stack **each teammate** | Atlas persist |

Track FAQ: sparse track may only award 1st. Popular → 1st/2nd/3rd.

Judging: Originality, Technical Difficulty (real tech vs ChatGPT wrapper), Demo Quality (clear, <3 min), Usefulness, Relevance (track only).

MLH bar: load-bearing integration shown on stage. Checkbox import loses.

Stack notes: Gemini `gemini-3.8-flash` free AI Studio. Atlas M0 no card. Auth0 no card. Solana **devnet only**. Vultr $100 from MLH Coach. IFM: ifm.ai K2 (six open models), Jais, PAN. Do not invent extra MLH prizes.

## What we will launch after this plan is audited

Exactly **100** Cursor agents, model **cursor-grok-4.6-xhigh-fast**. Each does its **own** big internal brainstorm loop (many ideas → score → kill → deepen winner). Each **must** target at least one specific prize; may stack if the story stays coherent.

They must not all invent the same travel-planner / food-app / generic chatbot.

## What the plan must specify (no TBD)

1. **Metrics schema** — feasibility + win-likelihood split (sponsor depth, judge axes, competition, demo, hours). Numbers with defined scales. Expected-value / pick ranking fields.
2. **100 unique briefs** — agent_id 001–100, primary prize, optional secondaries, unique constraint/angle seed so ideas do not collide.
3. **Agent prompt template** — the loop (how many rounds, kill rules), output JSON schema, 50-word track blurb, 3-min demo script beats, build slice for 19h.
4. **Anti-collision + anti-wrapper rules**
5. **How the parent aggregates** 100 JSON files into a ranked shortlist (top 10 / top 3) without another 100-agent pass.
6. **Output path:** `brainstorm/raw/NNN.json` only. Agents do not edit other files.

Return the FULL plan in your reply. Do not write repo files.
