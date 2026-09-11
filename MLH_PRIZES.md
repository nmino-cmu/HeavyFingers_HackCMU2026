# HackCMU 2026 — MLH prize briefing

**Use this file as source of truth for another Cursor session.** Paste or `@`-mention it. Do not treat the global MLH prize catalog as HackCMU's list; only the categories below were in the official MLH email and on the HackCMU Devpost.

Event: **HackCMU 2026 — Midnight Express** (Carnegie Mellon, 24 hours, beginner-friendly).  
Dates: **Fri Sep 11 – Sat Sep 12, 2026**.  
Submission: **Sat Sep 12, 4:00pm EDT** (Google Form, "Baggage Check") then **Platform Showcase 4:00–6:30pm**.

Official pages:

- Event site: https://www.acmatcmu.com/hackcmu2026/
- Devpost: https://hack-cmu-2026.devpost.com/
- MLH global prize catalog (superset, not HackCMU-specific): https://www.mlh.com/events/prizes
- Organizer email: rachelto@andrew.cmu.edu

Source of this briefing: forwarded MLH email to `ahuynh@andrew.cmu.edu` dated Thu Sep 10, 2026, cross-checked against HackCMU Devpost on Sep 11, 2026.

---

## How prizes work at this event (read this first)

There are **three independent prize layers**. One project can compete in all three.

1. **HackCMU track prizes** — You pick **one track** at submit time plus a **50-word** "why this track" blurb. Tracks are announced at **Opening Ceremony, Fri 6:00–6:30pm**. Prize depth scales with how many teams pick that track (popular track → 1st/2nd/3rd; sparse track → maybe only 1st).
2. **HackCMU overall winner** — One grand prize across all projects.
3. **MLH sponsor "Best Use of X"** — **Not restricted to any track.** Separate from HackCMU judging. You win by actually using that sponsor's tech in a way that is demoable and more than a checkbox import.

HackCMU judging criteria (track + overall): **real-life usefulness, technological complexity, originality, presentation/demo quality.**

MLH "Best Use" judging is typically: did you use the product for real, is it central to the demo, and is it more interesting than a login button / a single TTS line / a hello-world insert. One winning team per category is the usual pattern; some prizes are **one unit per teammate**, some are a **kit for the team**. Brands of earbuds/headphones/screens were not named.

**You can stack.** A project that talks, stores data, logs people in, and calls Gemini can be entered for multiple MLH categories at once. Do not add a sponsor just to "be eligible" if it will not show in the 2-minute demo.

GitHub Copilot is a **workshop / mini-event**, not a prize category. See the last section.

All participants are under the [MLH Code of Conduct](https://mlh.io/code-of-conduct). Incidents: on-site MLH rep, `+1 (409) 202-6060`, `incidents@mlh.io`.

---

## At-a-glance

| Category | Prize | Who gets it (as worded) | What you must actually use | Typical "this is real" bar |
|---|---|---|---|---|
| Best Use of **ElevenLabs** | Wireless earbuds | Winning **team** | ElevenLabs voice / audio API | The project *has a voice* in the demo (talks, narrates, or is a voice agent) |
| Best Use of **Gemini API** | Google swag kits | 1 winner (Devpost) | Google Gemini API | Gemini does something the user can see (chat, analyze, generate) — not just a hidden call |
| Best Use of **Solana** | Ledger Nano S Plus | **Each teammate** | Solana (on-chain tx, program, or Solana-backed flow) | A live or recorded tx / wallet interaction, not a mocked "crypto" screen |
| Best Use of **Vultr** | Portable screens | Winning **team** | Vultr cloud (compute / GPU / deploy) | The demo is served from Vultr, or a model/job actually runs there |
| Best Use of **Auth0** | Wireless headphones | **Each teammate** | Any Auth0 API (login, MFA, passwordless, or Auth0 for AI Agents) | Real Auth0 login or agent-consent flow, not a fake email/password form |
| Best Use of **MongoDB Atlas** | M5Stack IoT kit | **Each teammate** | MongoDB Atlas (cloud DB) | App reads/writes Atlas in the demo; data persists |

Per-person hardware (Solana / Auth0 / MongoDB) is the higher-value MLH stack if the team is 3–4 people. Swag / one-kit-for-the-team prizes are still worth stacking if the integration is cheap.

---

## 1. Best Use of ElevenLabs — wireless earbuds

**What ElevenLabs is:** Text-to-speech and voice-AI platform. Human-sounding, emotionally expressive voices. Used for companions, narration, voice-enabled apps, conversational agents. No actors / studio audio required.

**What MLH wants:** "Fully autonomous audio experiences." The project should *have a voice*, not just play a pre-recorded MP3.

**Prize:** Wireless earbuds for the winning team. Brand/model not specified.

**Promo:** Email says claim an **ElevenLabs Q4 2025 – Q4 2026 promo code** from the MLH email (link was in the original message). If the link is dead, get it from the MLH table. Separate from that, ElevenLabs' hackathon program is often **1 month of Creator** (~100k credits). Free tier may be enough for a weekend demo; claim the promo anyway.

**Docs / start:** https://elevenlabs.io/docs — Speech (TTS), Conversational AI / agents, voice cloning (use only voices you have rights to).

**What "best use" looks like in 24 hours:**

- A character or assistant that *speaks* replies (TTS on Gemini/LLM output).
- A story / tour / accessibility narrator the user can trigger live.
- A voice-in / voice-out agent (STT elsewhere or ElevenLabs conversational, then TTS back).
- Multi-voice scenes (two characters) if you have time.

**What looks weak:** one hardcoded "hello" clip, or TTS that is never played in the showcase.

**Combo:** ElevenLabs + Gemini is the default weekend stack (Gemini thinks, ElevenLabs speaks). Auth0 if the agent acts as a user. MongoDB if it remembers.

---

## 2. Best Use of Gemini API — Google swag kits

**What Gemini is:** Google's multimodal LLM API (text, and depending on model: images, audio, video, long context). Good for chat, summarization, extraction, code/script/creative generation.

**What MLH / Google pitch:**

- Chatbot that gives personalized advice
- App that summarizes / analyzes complex material
- Creative generation (code, scripts, music, etc.)

**Prize:** Google swag kits. Devpost lists **1 winner**. This is merch, not hardware-per-person.

**Start:** https://aistudio.google.com/ — get an API key, then [Gemini API docs](https://ai.google.dev/gemini-api/docs). Free / student-friendly for a hackathon if you stay on flash-class models.

**What "best use" looks like:**

- Gemini is the *brain* of the product, visible in the demo (user asks → useful answer / artifact).
- Structured output that drives UI (it extracts fields, plans a trip, grades something, etc.).
- Multimodal if it helps: photo in → analysis out.

**What looks weak:** a single prompt hidden in a script that the demo never shows.

**Combo:** Almost every other MLH prize pairs with this. Do Gemini first if the project is AI-shaped; add voice/auth/db/cloud around it.

---

## 3. Best Use of Solana — Ledger Nano S Plus (each teammate)

**What Solana is:** High-throughput L1 blockchain. Fast confirmation, very cheap txs. Used for consumer apps, games, social, payments, DeFi (DEX / lending / trading), identity, supply-chain prototypes.

**What MLH wants (their examples):**

- Game / social / consumer product with instant, high-frequency txs
- Trading, lending, or DEX
- Supply chain, identity, or payments that could scale

**Prize:** **Ledger Nano S Plus** — a USB hardware wallet (stores crypto keys offline; you confirm txs on-device). Worded as **one for each teammate**. This is the most "real product" MLH prize on the list.

**Start:** https://solana.com/docs — Solana Playground / `npx create-solana-dapp` for a weekend web wallet flow. Use **devnet** (fake SOL). Do not put real funds on a hackathon laptop.

**What "best use" looks like:**

- User connects a wallet (Phantom / Solflare / wallet adapter) and a **devnet tx** happens in the demo (tip, mint, vote, pay, write a memo, hit your program).
- A tiny on-chain program (Anchor) if someone on the team already knows it; otherwise a client-side transfer / memo / existing program is enough if it is *load-bearing*.
- Identity: wallet login that actually gates something.

**What looks weak:** a landing page that says "powered by Solana" with no tx.

**Combo:** Hardest to fake, highest per-person prize. Only take it if someone will own the wallet/demo path. Pairs with Auth0 poorly unless you have a clear "web2 login + web3 action" story. Pairs with MongoDB if you index off-chain state.

**Safety:** Hardware-wallet prize does not mean you need Ledger in the hack. Do not collect seed phrases. Devnet only.

---

## 4. Best Use of Vultr — portable screens (team)

**What Vultr is:** Cloud provider. VMs, one-click deploy, object storage, **Cloud GPUs** for AI. Pitch: "infrastructure is no longer the bottleneck."

**Prize:** Portable screens for the winning **team**. Brand/size not specified (think USB-C travel monitor).

**Credits:** Email: sign up and claim **free cloud credits** (MLH table / email link). Do this early; new-account + billing quirks eat hours.

**Start:** https://www.vultr.com/ — deploy the smallest Ubuntu/Docker instance that can serve the app, or a GPU instance only if you actually need a local model.

**What "best use" looks like:**

- Production URL of the hack is a Vultr VM / app, shown in the demo.
- A job that needs a server (websocket game, inference, scraper, always-on agent) actually runs there.
- GPU used for something you could not run well on a laptop (optional, higher wow).

**What looks weak:** localhost-only demo with "we have a Vultr account."

**Combo:** Cheap if you were going to deploy anyway. Use it as the host for Gemini/ElevenLabs backends. Do not spend the night fighting GPU drivers unless the model is the product.

---

## 5. Best Use of Auth0 — wireless headphones (each teammate)

**What Auth0 is:** Hosted identity. Social login, email/password, MFA, passwordless. Free trial, **no credit card**, **up to 7,000 monthly active users**, unlimited logins.

They also push **Auth0 for AI Agents**: identity for agents — user login, consent, **Token Vault** (agent calls Google/GitHub/etc. *as the user* without you storing OAuth tokens), and async / human-in-the-loop approval (CIBA) for high-stakes actions.

**HackCMU wording (follow this):** use **any Auth0 APIs**. AI Agents is a bonus path, not the only path. (Some other 2026 MLH events narrowed it to Auth0 for AI Agents; HackCMU's email did not.)

**Prize:** Wireless headphones, **one pair per teammate**.

**Start:**

- App login: https://auth0.com/signup — Regular Web App / SPA quickstart for your stack.
- Agents: https://auth0.com/ai — Token Vault, Connected Accounts, async authorization.

**What "best use" looks like:**

- Real Auth0-hosted login in the demo (Google/GitHub social is fastest).
- MFA or passwordless if it is part of the story (less necessary than a working login).
- Stronger: an agent that can only do X after the user consents, tokens live in Token Vault (e.g. "email this for me" / "add a calendar event").

**What looks weak:** a custom `/login` form that never hits Auth0.

**Combo:** Highest-leverage "each teammate" prize if the app has users. Add it in the first hours, not at 3pm Saturday. Pairs with Gemini agents and ElevenLabs companions.

---

## 6. Best Use of MongoDB Atlas — M5Stack IoT kit (each teammate)

**What Atlas is:** MongoDB as a hosted cloud database. Document model, good for messy hackathon schemas. **Free forever tier, no credit card.** Students can also get **$50 Atlas credit** via GitHub Student Developer Pack ([mongodb.com/students](https://www.mongodb.com/students) / pack perk). Credit redeem often wants a card or PayPal even though the free cluster does not.

**Also:** [MongoDB University](https://learn.mongodb.com/) if someone is new.

**Prize:** **M5Stack IoT kit** for **each teammate**. MLH has also called this the **M5GO IoT Starter Kit** at other events. Typical kit (M5GO v2.7, ~confirm at prize table): ESP32 core (Wi-Fi), battery/charge dock, plus units such as ENV (temp/humidity/pressure), PIR motion, angle/rotary, IR, RGB LED, hub — i.e. a real hardware toy, not a sticker.

You do **not** need to use M5Stack in the hack. The kit is the prize, not the required platform.

**Start:** https://www.mongodb.com/atlas/database — M0 free cluster, get a connection string, `mongodb+srv://...`. Any official driver or Mongoose.

**What "best use" looks like:**

- Create / read / update that you can show ("I saved this, refresh, it's still there").
- Atlas is the system of record (users, sessions, generated content, game state).
- Bonus: Atlas Search / Vector Search if you are doing RAG — only if it is visible.

**What looks weak:** seed data in a local JSON file and "we would use Mongo."

**Combo:** Default backend for everything else. Easiest "each teammate" prize to honestly qualify for.

---

## GitHub Copilot — mini-event, not a prize

MLH is running a **GitHub Copilot "Flight Deck"** session this weekend (workshop / demo, not a judged category in the email).

Free Copilot for students: **[GitHub Student Developer Pack](https://education.github.com/pack)** — also the path to MongoDB's $50 credit.

Use Copilot if you want. It does not win an MLH prize by itself.

---

## Not at HackCMU (do not plan around these)

The global MLH prize page also lists Tiger Data, Presage, a generic GenAI category, Backboard, DigitalOcean, Snowflake, .TECH domains, GoDaddy. **None of these were in the HackCMU email or on HackCMU Devpost.** Ignore unless the on-site MLH table or opening ceremony adds them.

---

## Practical weekend plan (if the next session is picking a stack)

Cheap to qualify, high demo value, can stack:

1. **MongoDB Atlas** — free cluster, persist something. (~30–60 min)
2. **Auth0** — social login on the web app. (~1–2 hr first time)
3. **Gemini API** — the actual product intelligence.
4. **ElevenLabs** — speak the model's output. (hours, plus promo)
5. **Vultr** — deploy Friday night / Saturday morning so the showcase URL is live.
6. **Solana** — only if a teammate will own a wallet + one real devnet action.

If the team is 3–4 people and wants hardware: prioritize **Auth0 + MongoDB + (Solana if feasible)**. Those are the per-person prizes.

If the product is a talking agent: **Gemini + ElevenLabs + Auth0 + MongoDB** is the intended MLH combo.

---

## Submission notes for MLH categories

- Put every sponsor you actually used in the Devpost / Google Form "built with" list.
- Demo the integration on stage, not only in the writeup. Judges will not grep your repo.
- Keep API keys out of the public repo; use `.env`.
- Be ready to show the Auth0 tenant, Atlas cluster, Vultr instance, a Solana tx signature, or an ElevenLabs voice in dashboard if asked "did you really use it?"

---

## Unknowns to confirm on site (do not invent)

- Exact earbud / headphone / portable-screen models.
- Exact M5Stack SKU (M5GO vs another kit).
- Whether MLH wants a separate prize-claim form vs Devpost tags.
- ElevenLabs promo URL (clipped in the forwarded email).
- Vultr credit amount and claim URL.
- Whether any extra MLH categories get added at opening ceremony.

---

## Prompt you can paste into the next Cursor session

```
Read @MLH_PRIZES.md first. It is the source of truth for HackCMU 2026 MLH prizes.

We are at HackCMU (24h, submit Sat 4pm EDT). MLH "Best Use" prizes are separate from HackCMU tracks and can be stacked.

When proposing or building, tell me which MLH categories we are honestly qualifying for, which integrations are load-bearing in the demo, and which we should skip. Do not add a sponsor as a checkbox.

Prefer stack: MongoDB Atlas + Auth0 + Gemini, then ElevenLabs if the product should talk, Vultr if we need a public URL, Solana only if someone owns a real devnet tx in the demo.
```
