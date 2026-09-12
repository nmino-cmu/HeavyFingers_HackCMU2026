# HackCMU 2026 — competition ground truth

Recorded Fri Sep 11, 2026 ~8:30pm EDT, before hacking start (9:00pm).  
Confidence tags: **VERIFIED** (primary official source), **LIKELY** (strong inference), **UNKNOWN**.

Do not treat UNKNOWN as fact.

---

## Event

| Fact | Tag | Source |
|---|---|---|
| Name: HackCMU 2026 — Midnight Express | VERIFIED | Event site, opening deck, Devpost |
| 24 hours, beginner-friendly | VERIFIED | Opening, Devpost, event site |
| Venue: Tepper / TEP (Simmons, 1403) | VERIFIED | Opening, Devpost schedule |
| Dates: Fri Sep 11 – Sat Sep 12, 2026 | VERIFIED | All official hubs |
| Hacking **starts Fri 9:00pm EDT** | VERIFIED | Opening deck |
| Boarding Fri 5:00–6:00pm; Departure/opening 6:00–6:30pm (started ~6:15 delayed) | VERIFIED | Opening + Devpost |
| Do **not** start building or designing the project before the event. Brainstorm + teams beforehand OK | VERIFIED | Devpost rules |
| **Must be from scratch** | VERIFIED | Opening clarifications |
| Any language or AI; any kind of application | VERIFIED | Opening |
| Team size max **4** | VERIFIED | Opening, event FAQ |
| Eligibility (event): current CMU students | LIKELY | Event-site wording from earlier crawl; not re-fetched this hour |
| Eligibility (Devpost chips): US / age of majority | VERIFIED text, **conflicts** with “Anyone who can make it!” on same rules page | https://hack-cmu-2026.devpost.com/rules |
| Organizers: `acm-exec@cs.cmu.edu` | VERIFIED | Opening, event site |
| Devpost manager: `rachelto@andrew.cmu.edu` | VERIFIED | Devpost |
| Discord: **acmatcmu**; slides posted there | VERIFIED | Opening |
| MLH CoC applies | VERIFIED | MLH event pages |
| Hardware Lab at this event | LIKELY **no official lab** | MLH Hardware API inactive notice; opening did not ban bringing your own hardware |
| Pre-existing libraries, models, APIs | LIKELY allowed | “Any language or AI” + standard hackathon practice; **do not** bring a pre-built product |
| Pre-existing private codebase for *this* project | VERIFIED forbidden | Devpost: no building/designing before event |

---

## Deadline and format

| Fact | Tag | Source |
|---|---|---|
| **Baggage Check: Sat Sep 12, 4:00pm EDT** | VERIFIED | Opening, Devpost, event schedule |
| Submit: Google Form — description + **one track** + **50-word** why | VERIFIED | Opening, Devpost “What to Build” |
| Form URL | UNKNOWN | Not on public site; Discord / organizers |
| Devpost deadline: Sat Sep 12, 4:00pm EDT | VERIFIED | https://hack-cmu-2026.devpost.com/ |
| Devpost is **secondary**; opening said “submit google form” | VERIFIED | Opening final things |
| **Platform Showcase: Sat 4:00–6:30pm** | VERIFIED | Opening, Devpost |
| **3 min presentation + demo** | VERIFIED | Opening judging slide |
| 3 rooms of judges; spreadsheet for when/where | VERIFIED | Opening |
| Expo tables for submitted groups | VERIFIED | Opening |
| Arrival / winners: Sat 7:00–8:00pm | VERIFIED | Opening, Devpost dates (~7pm) |
| Dinner Sat 6:30–7:00pm | VERIFIED | Opening |

Effective build window: **Fri 9:00pm → Sat 4:00pm ≈ 19 hours**, then demo until 6:30pm.

---

## Tracks (pick exactly one)

Opening listed four themed tracks + **IFM (optional)** on the tracks slide. Prize list treats **Track Prizes** and **IFM Prize** as separate.

| Track | Opening one-liner | Tag |
|---|---|---|
| Optimization | “perhaps optimize something? 0.0” | VERIFIED |
| Traveling | “what does traveling mean to you? hm….” | VERIFIED |
| Multiplayer | “this is how you can meet people and touch grass :P” | VERIFIED |
| Food | “Yummy! :D” | VERIFIED |
| IFM (optional) | No blurb | VERIFIED listed; **UNKNOWN** whether the Google Form offers IFM as a fifth *track pick* |

Track prize **depth** scales with how many teams pick it: popular → 1st/2nd/3rd; sparse → maybe **1st only**. VERIFIED (Devpost + event FAQ). Opening still showed 1st/2nd/3rd objects.

Fits multiple tracks → pick one. Theme fit is **part of judging (Relevance)**. VERIFIED (opening).

Public 2026 site JS was still “coming soon” as of Fri evening (last-modified Sep 9). Opening overrides the site.

---

## Official judging (HackCMU track + grand)

Opening (authoritative tonight):

| Axis | Gloss | Tag |
|---|---|---|
| Originality | Entirely novel / fresh approach | VERIFIED |
| Technical Difficulty | Real technical challenges **vs ChatGPT wrapper** | VERIFIED |
| Demo Quality | Clear, understandable, **under 3 minutes** | VERIFIED |
| Usefulness | Practical, fulfills a real need | VERIFIED |
| Relevance | **Track only** — related to the track applied to | VERIFIED |

Devpost still lists only: real-life usefulness, technological complexity, originality, presentation/demo quality. Same idea minus named Relevance.

---

## Prize catalog (stackable)

Opening prize categories. You can win more than one. Sponsor prizes **not restricted to any track** (Devpost FAQ + opening).

### HackCMU (opening)

| Prize | Object | How | Tag |
|---|---|---|---|
| Grand Prize / Overall Winner | **HRT Poker Set** | All submits | VERIFIED opening; Devpost still says “Overall Winner” unnamed object |
| Track 1st | Mini projector + Jump AirPods Pro | One track | VERIFIED |
| Track 2nd | Visa swag bags | One track | VERIFIED |
| Track 3rd | Keyboard + keychain | One track | VERIFIED |
| IFM Prize | **IFM Kindle Lite** | Use IFM tools (K2 etc.) | VERIFIED object; bar = LIKELY “load-bearing K2/IFM”, not stated |
| Cursor Prize | **Cursor keyboards** | Unstated bar | VERIFIED object; eligibility **UNKNOWN** |
| Sandia Prize: Cybersecurity | AirPods with ANC | Cyber-themed | VERIFIED object; extra rules **UNKNOWN** |
| People’s Favorite | Ticket to Ride | Expo / audience | VERIFIED object; vote mechanic **UNKNOWN** |
| Best Design | Fujifilm QuickSnap | Design | VERIFIED object; rubric **UNKNOWN** |
| Raffle | Unnamed | Submit by deadline | VERIFIED event FAQ |

### MLH Best Use (HackCMU page + Devpost + opening — same six)

Devpost tags each **1 winner** = the team. Some blurbs say **per teammate**.

| Category | Prize | Who (blurb) | Eligibility bar (official) | Tag |
|---|---|---|---|---|
| Gemini API | Google Swag Kits | 1 team | Use Gemini API; pitch: chat, analyze, generate | VERIFIED. Distinctive-capability bar is **our** scoring, not written |
| ElevenLabs | Wireless earbuds | team | “Fully autonomous audio”; give the project a **voice** | VERIFIED |
| Solana | Ledger Nano S Plus | **each teammate** | Fast/cheap txs; games/social/consumer, DEX, supply/identity/payments. **devnet** in MLH partner docs | VERIFIED prize; cluster = VERIFIED partner docs |
| Vultr | Portable screens | team | Cloud compute / GPU / deploy; “infrastructure not the bottleneck” | VERIFIED. Hosting-only = weak **LIKELY** |
| Auth0 | Wireless headphones | **each teammate** | **Any Auth0 APIs**; login/MFA/passwordless **or** Auth0 for AI Agents. Free, no card, blurb 7,000 MAUs | VERIFIED |
| MongoDB Atlas | M5Stack IoT kit | **each teammate** | Build a hack **using Atlas** | VERIFIED. Persist-only = weak **LIKELY** |

Opening did **not** add Tiger Data, Presage, Gen AI, Backboard, DigitalOcean, Snowflake, .Tech, GoDaddy.

GitHub Copilot = workshop, not a prize. VERIFIED.

### Event-logo sponsors with **no opening prize**

Microsoft, Adobe, Jane Street, Citadel, Roblox, a16z, Bloomberg, DE Shaw, Garner Health, Jump, Lockheed Martin, Quadrature, Querit, SCM, Texas Instruments, Visa, HRT (HRT *is* the grand-prize object, not a Best Use).

| Sponsor | Opening role | Prize? |
|---|---|---|
| IFM (MBZUAI Institute of Foundation Models) | Platinum + workshop + IFM Prize | YES — Kindle Lite |
| SpaceXAI / Cursor | Tabling + workshop + Cursor Prize | YES — keyboards; bar UNKNOWN |
| Sandia | Tabling + Sandia Cyber prize | YES — ANC AirPods |
| Querit | Tabling: Web Search API for LLMs/agents | **No prize named** |
| MLH | Tabling | The six Best Use prizes |
| Jane Street, Citadel, Microsoft, Adobe, Roblox | Logos / recruiting | **No prize named** — do not invent |

---

## Sponsor products / resources (eligibility-relevant)

Full start links: `HACKCMU_RESOURCES.md`. Short:

| Tech | What to use | Credits | Distinctive (for scoring, not official) |
|---|---|---|---|
| Gemini | AI Studio key, first-call model **`gemini-3.8-flash`** | Free tier. $300 Cloud trial **cannot** pay AI Studio | Multimodal, long context, structured output, tools. `gemini-3.1-pro-preview` not Free Tier |
| ElevenLabs | `xi-api-key`, TTS / agents / STT | Free 10k/mo or MLH email → 3-month sub | Expressive / conversational voice, not a leftover MP3 |
| Solana | **devnet only** | Faucet / `solana airdrop 5` | Real tx / program / shared state |
| Vultr | VM / GPU / k8s | **$100**, code from **MLH Coach**, `mlh.link/vultr-giftcode` | Compute that is *visible*, not just a URL |
| Auth0 | Tenant signup auth0.com (not newsletter link) | No card. Blurb 7k MAU vs auth0.com 25k — conflict | Identity as primitive, or Token Vault / agents |
| Atlas | M0 free, no card | Optional $50 via GitHub Pack (card, 90-day unused expiry) | Evolving docs, geo, vectors, system of record |
| IFM | K2 (six open models), Jais, PAN | Workshop Fri 9–10pm TEP 1403. https://ifm.ai/ | K2 load-bearing, not a rename of Gemini |
| Cursor / Grok | Cursor, Grok Imagine, Grok Bot | Workshop Fri 10–10:30pm TEP 1403 | Bar UNKNOWN |
| Querit | Search API | No prize | Optional infra only |

---

## Tonight’s sponsor contact (information value)

| When | What | Where | Tag |
|---|---|---|---|
| Fri 7:00–9:00pm | Dinner + Sponsor Expo | Tepper Simmons | VERIFIED |
| Fri 9:00–10:00pm | IFM Workshop — how to use K2 | TEP 1403 | VERIFIED |
| Fri 10:00–10:30pm | Cursor / Grok Imagine / Grok Bot | TEP 1403 | VERIFIED |
| Sat 10:00am–1:00pm | Mentor OH | TEP Simmons B | VERIFIED |
| All weekend | Discord mentor tickets | FE/BE/mobile/ML/data/cloud | VERIFIED |

IFM workshop may change K2 integration cost. **UNKNOWN** whether they hand out keys/weights/hosted endpoints.

---

## Stacking rules

| Fact | Tag |
|---|---|
| One project, **one** track | VERIFIED |
| Grand + track + IFM + Cursor + Sandia + People’s + Design + any MLH Best Use can theoretically stack | VERIFIED categories exist independently; **UNKNOWN** if judges mentally double-count |
| MLH Best Use **not** track-locked | VERIFIED |
| List only sponsors you **actually** used and can demo | VERIFIED practice / opening “built with” |

---

## Field / competitor sophistication

| Fact | Tag | Source |
|---|---|---|
| Devpost shows **34 participants**, 7 non-cash prizes | VERIFIED snapshot | Devpost (likely undercount; Google Form is primary submit) |
| Actual team count tonight | UNKNOWN | Do not use 34 as the field |
| HackCMU 2025 grand: **Medicly** — phone video → clinician findings + 3D mesh + exercises; claimed 1/250+ teams | LIKELY useful prior | 2025 site + LinkedIn; **different year, different tracks/sponsors** |
| 2025 tracks (do not reuse as 2026): Games, Digital Media, Health & Sustainability, etc. | VERIFIED 2025 only | hackcmu2025 site |
| 2026 is beginner-friendly **and** CMU CS-heavy | LIKELY | Event copy + historical field |
| Many teams will ship Gemini chat “AI for X” | LIKELY | MLH season pattern + opening “vs ChatGPT wrapper” |
| Gemini MLH winners elsewhere: photo-validation (Impromptu), structured taste graphs (Taste Tape also won Vultr), voice agents booking IRL (DracoCare), Gemini-as-explainer around a real model (Aqua-Cult) | LIKELY analog | Public 2026 MLH writeups — **not this event** |

Judge listed on Devpost: Katie Wang. Other judges UNKNOWN.

---

## Conflicts (do not pick a winner)

1. Devpost eligibility chips (US / age) vs “Anyone who can make it!” vs event CMU-student wording.
2. Auth0 MAU 7,000 (prize blurb) vs 25,000 (auth0.com/pricing).
3. Demo length: opening **3 min**; older informal briefings said 2. Use **3**.
4. Grand prize object: opening **HRT Poker Set**; Devpost still unlabeled “Overall Winner”.
5. IFM as fifth track vs optional extra prize only.
6. Devpost participant count vs likely in-room attendance.

---

## Search constraints for this ideation phase (team instruction)

- **Ignore CMU-specific / “Only at CMU” idea cohort.** Do not force campus-only products.
- Team can execute ambitious ML/systems work. Do not self-censor to beginner CRUD.
- Optimize **P(at least one prize)** with a serious overall-win path. Not idea volume.

---

## Sources

- Opening Ceremony PDF (53 slides), Discord, Fri Sep 11, 2026
- https://www.acmatcmu.com/hackcmu2026/
- https://hack-cmu-2026.devpost.com/ + `/rules`
- https://www.mlh.com/events/hackcmu/prizes (re-fetched Fri night — still six MLH categories)
- https://www.mlh.com/partners/{gemini,elevenlabs,solana,vultr,auth0,mongodb}
- Local: `HACKCMU_PRIZES_TRACKS.md`, `HACKCMU_RESOURCES.md`, `MLH_OFFICIAL_TRANSCRIPT.md`
