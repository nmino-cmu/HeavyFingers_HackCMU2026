# HackCMU 2026 — resources you can use

Only sources confirmed as **this event / this MLH season** (Sep 11–12, 2026, Midnight Express).  
Did **not** copy HackCMU 2025 tracks, prizes, or leftover pages.

Official 2026 hubs:

- Event site: https://www.acmatcmu.com/hackcmu2026/
- Devpost: https://hack-cmu-2026.devpost.com/
- MLH prizes for **this** event: https://www.mlh.com/events/hackcmu/prizes
- MLH partner “Build with” pages: https://www.mlh.com/partners/{gemini,elevenlabs,solana,vultr,auth0,mongodb}
- MLH Software / Hardware / Learn tabs on the same site

Verbatim crawl: `MLH_OFFICIAL_TRANSCRIPT.md`. Prize/track rules: `HACKCMU_PRIZES_TRACKS.md`.  
Opening deck: Discord (slides posted there). Server: **acmatcmu**. Turn on announcement notifications.

---

## Tonight / Saturday (opening ceremony)

| When | What | Where |
|---|---|---|
| Fri 7:00–9:00pm | Dinner + Sponsor Expo | Tepper Simmons |
| Fri 9:00pm | Hacking starts | |
| Fri 9:00–10:00pm | **IFM Workshop** — K2 models | TEP 1403 |
| Fri 10:00–10:30pm | **Cursor Workshop** — Cursor, Grok Imagine, Grok Bot | TEP 1403 |
| Fri 12:00–1:00am | Midnight Cafe Halte | |
| Sat 10:00am–1:00pm | Mentor office hours | TEP Simmons B |
| Sat all weekend | Remote mentor tickets (Discord) | Fullstack / FE / BE / Mobile / ML / Data / Cloud |
| Sat 4:00pm | Baggage Check (Google Form) | Discord / organizers — URL not on the site |

---

## Create tonight (free or MLH-credited)

| What | Why | Start |
|---|---|---|
| Gemini API key | MLH Best Use + product brain | https://aistudio.google.com/api-keys → [get-started](https://ai.google.dev/gemini-api/docs/get-started). Use **`gemini-3.8-flash`**. |
| MongoDB Atlas M0 | MLH Best Use + persist demo data | https://www.mongodb.com/cloud/atlas/register — **no card**. One free cluster per project, 512 MB. |
| Auth0 tenant | MLH Best Use + real login | https://auth0.com/signup — **no card**. Do **not** use Software Lab `hackp.ac/auth0-signup` (newsletter). |
| Vultr account + $100 | MLH Best Use + public URL | https://mlh.link/vultr-signup → verify email → sign out/in via https://mlh.link/vultr-giftcode → **code from MLH Coach**. One account. |
| ElevenLabs | MLH Best Use + voice | Free tier (10k credits/mo) or MLH email promo → **3-month sub**. Key: https://elevenlabs.io/app/developers/api-keys |
| Solana **devnet** wallet | MLH Best Use | Browser [Playground](https://beta.solpg.io/) or Phantom on **devnet**. `solana airdrop 5` or https://faucet.solana.com/. **No mainnet money.** |
| GitHub Student Pack | Mongo $50 + Copilot + other tools | https://education.github.com/pack |
| IFM K2 (optional prize) | IFM Kindle Lite if you actually use it | https://ifm.ai/ — workshop Fri 9pm TEP 1403 |
| Shipping address | Swag / prize packages | Typeform at hackp.ac/address is **closed**. Use https://my.mlh.io/settings |

---

## MLH “Best Use” stack (judged if you demo it)

### Gemini API

- Docs: https://ai.google.dev/gemini-api/docs/get-started
- Cookbook: https://github.com/google-gemini/cookbook
- Partner hub: https://www.mlh.com/partners/gemini
- Student Google AI Pro (consumer Gemini app, **not** an API key): https://gemini.google/students/
- $10/mo Cloud credits: bundled with Google AI Pro → signed-in https://developers.google.com/program/my-benefits
- **$300 Cloud Welcome credit cannot pay Gemini API in AI Studio.** Use the API Free tier.

### ElevenLabs (TTS / agents / STT / music)

- Partner hub: https://www.mlh.com/partners/elevenlabs
- First TTS call: https://elevenlabs.io/docs/eleven-api/quickstart (`xi-api-key`)
- Agents: https://elevenlabs.io/docs/eleven-agents/overview
- Demo agents: https://mlh.github.io/elevenlabs-demo/
- Promo: MLH email the week of the event (ask the MLH table if missing)

### Solana (devnet only)

- Partner hub: https://www.mlh.com/partners/solana
- Quick start: https://solana.com/docs/intro/quick-start
- Playground: https://beta.solpg.io/
- Faucet: https://faucet.solana.com/
- Local install: `curl --proto '=https' --tlsv1.2 -sSfL https://solana-install.solana.workers.dev | bash`
- Anchor: https://www.anchor-lang.com/docs
- Agent skills: `npx skills add https://github.com/solana-foundation/solana-dev-skill`
- Templates: https://solana.com/developers/templates

### Vultr (cloud VM / GPU / k8s)

- Partner hub: https://www.mlh.com/partners/vultr
- Products: https://docs.vultr.com/products
- API: https://www.vultr.com/api/ · CLI: https://github.com/vultr/vultr-cli
- **$100** via MLH Coach gift code (MLH: no card)

### Auth0 (login / MFA / Auth0 for AI Agents)

- Weekend guide: https://developer.auth0.com/resources/get-started/mlh
- Quickstarts: https://auth0.com/docs/quickstarts
- AI Agents (Token Vault, CIBA, MCP): https://auth0.com/ai/docs/intro/overview
- Sample: https://github.com/auth0-samples/auth0-assistant0
- 10-minute MLH blog: https://blog.mlh.com/enable-user-authentication-for-your-hackathon-project-in-as-little-as-ten-minutes-05-12-2023

### MongoDB Atlas

- Register free: https://www.mongodb.com/cloud/atlas/register
- Student $50 (card/PayPal; 90-day unused expiry): https://www.mongodb.com/students
- First cluster (MLH): https://blog.mlh.com/read-and-write-to-a-mongodb-atlas-database-in-minutes-04-19-2023
- Docs: https://www.mongodb.com/docs/ · University: https://learn.mongodb.com/
- Node driver / PyMongo via Learn tab: `hackp.ac/mongodb-javascript-tutorials` · `hackp.ac/mongodb-python-tutorials`

---

## Also on the MLH site this weekend (not HackCMU prize categories)

**GitHub Global Campus / Student Pack** — https://www.mlh.com/resources/software  
Hello World: https://docs.github.com/en/get-started/using-github/hello-world  
Pack apply: https://education.github.com/pack  
Useful for Copilot, Mongo $50, and other student tools. Copilot is a workshop, not a judged prize.

**GoDaddy Registry free 1-year domain** — claim https://www.tech.study/  
On Software Lab + the **global** MLH prize page. **Not** on HackCMU’s prize list or Devpost. Fine to use as hosting; do not expect a HackCMU GoDaddy prize.

**Hardware Lab cards** (https://www.mlh.com/resources/hardware): Pico/RP2040, Arduino IDE, Echo Dot, Google Home Mini. API has an **inactive** “no Hardware Lab at this event” notice; visible copy still says visit the MLH table. Confirm before planning around hardware.

- Pico playlist: https://www.youtube.com/playlist?list=PLEBQazB0HUyQO6rJxKr2umPCgmfAU-cqR
- Arduino IDE: https://www.arduino.cc/en/software
- Home Mini setup: https://support.google.com/googlehome/answer/7029485

---

## Event / opening sponsors (not MLH Best Use unless listed above)

Opening **tabling** blurbs + event-site logos. Opening **did** give these extra judged prizes: **IFM**, **Cursor**, **Sandia (cybersecurity)**. Other logos are recruiting unless a table says otherwise.

### IFM — Institute of Foundation Models (platinum)

- https://ifm.ai/
- Global AI lab (MBZUAI, launched May 2025). Abu Dhabi, Silicon Valley, Paris.
- **K2** series: six fully open-source models. **Jais**: Arabic LLM. **PAN**: world model (embodied / simulation).
- Workshop: Fri 9:00–10:00pm TEP 1403 — how to use K2 on your hack.
- Prize: **IFM Kindle Lite** (optional; not a required track).

### SpaceXAI / Cursor

- Company behind Grok and SpaceXAI. One model family, one API. Chat, hard engineering, real-time voice, image and video.
- Workshop: Fri 10:00–10:30pm TEP 1403 — Cursor, Grok Imagine, Grok Bot (resume / portfolio / jobs).
- Prize: **Cursor keyboards**. Bar not stated on the slides.

### Sandia

- National security science/engineering lab (defense, biotech, energy, computer security, …).
- Prize: **Sandia Prize: Cybersecurity** — AirPods with noise cancellation.

### Querit

- Web Search API / search infra for LLMs, agents, in-app search. Multilingual index, structured extraction, source grounding.
- https://www.querit.ai/en — no opening prize named.

### Other site logos

a16z, Adobe, Bloomberg, Citadel, DE Shaw, Garner Health, HRT, Jane Street, Jump, Lockheed Martin, Microsoft, Quadrature, Roblox, SCM, Texas Instruments, Visa.

Links the 2026 page actually ships:

- DE Shaw: https://www.deshaw.com/ · https://www.youtube.com/@deshawgroup
- Roblox careers: https://careers.roblox.com/
- SCM intern: https://grnh.se/eyywl26a1us
- Visa students: https://www.visa.com/students

Sponsor Expo: Fri 7:00–9:00pm, Tepper Simmons.

---

## Do not mix these up

| Trap | What to do instead |
|---|---|
| `hackp.ac/auth0-signup` → Auth0 newsletter | https://auth0.com/signup |
| $300 Google Cloud trial for Gemini API | AI Studio free key / `gemini-3.8-flash` |
| Solana mainnet / real SOL | **devnet** only |
| Global MLH prizes (Tiger Data, DigitalOcean, Snowflake, .Tech, …) | Not on HackCMU’s list |
| HackCMU **2025** site / Devpost | Different year. Ignore. |
| `mlh.lin/mongodb-benefits` (typo on partner page) | https://mlh.link/mongodb-benefits |

---

## People / incidents

- Discord: **acmatcmu** (slides + announcements)
- Organizers: `acm-exec@cs.cmu.edu`
- Devpost manager: `rachelto@andrew.cmu.edu`
- MLH CoC incidents (NA): `+1 (409) 202-6060`, `incidents@mlh.io`
- Signup / tickets (2026 site): https://forms.gle/2ZbetvDn44GPYP6GA · FAQ ticket: https://forms.gle/XHyQMkiPM8SFS1ze6
- Saturday **Baggage Check** Google Form URL: not posted on the site. Discord / organizers.
