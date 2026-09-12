# HackCMU 2026 — MLH official pages (verbatim source)

Crawled **Fri Sep 11, 2026** (prizes page + every chrome tab + each `Build with` partner page + linked docs + event site + Devpost). **Opening Ceremony deck** added the same night (Discord). For another Cursor session: this file is the **verbatim official wording**. Judging advice and weekend stack picks live in `MLH_PRIZES.md`.

`mlh.link/*` URLs return **HTTP 200** with a `<meta http-equiv="refresh">` (not a 3xx). Destinations below are the refresh targets.

---

## How this file is organized

1. Canonical **Prizes at HackCMU** page (API fields + visible copy)
2. Other pages linked from that site’s chrome (Software / Hardware / Learn / Address Form / global prize catalog)
3. One section per HackCMU MLH category: prize blurb → partner “Build with” page → access/credits → first-weekend start → destinations
4. Conflicts (pages disagree — do not invent a reconciliation)
5. Link map
6. Opening Ceremony deck (Fri Sep 11, 2026) — section K

Quotes are official. `UNKNOWN` means no fetched page stated it.

---

## A. Prizes at HackCMU (canonical)

**URL:** https://www.mlh.com/events/hackcmu/prizes  
**Component:** `HackathonPrizes`  
**Page title:** HackCMU Prizes  
**Subtitle:** Win awesome prizes, hacker gear, & swag by competing in one of these challenges and using new APIs.

**Event record (API):**

| field | value |
|---|---|
| name | HackCMU |
| slug | hackcmu |
| status | in_progress |
| startsAt | 2026-09-11T21:00:00Z |
| endsAt | 2026-09-12T22:00:00Z |
| dateRange | SEP 11 - 12 |
| location | Pittsburgh, PA |
| formatType | physical |
| websiteUrl | https://www.acmatcmu.com/hackcmu2026/ |
| region | AMER |
| hackathon_focus | Software |

**Visible chrome:** Prizes · Software · Hardware · Learn · Address Form · Resources · Hackathons. Footer: “Not at HackCMU? Switch to another event.” Same-weekend events in the switcher: HackKentucky, HackRice, HackMTY 2026, HackWesTX 26.

**`challengeClaimLinks`:** `{}` when signed out. Address Form in nav: https://hackp.ac/address → closed Typeform; live path is MyMLH settings (section B4).

**Active challenges at HackCMU (exactly these six):**

### A1. Best Use of Gemini API

- Sponsor window: **Gemini Prize Category Q1 2025 - Q1 2026**
- Prize: **Google Swag Kits**
- CTA: Build with Gemini → https://mlh.link/gemini → https://www.mlh.com/partners/gemini
- Challenge: https://www.mlh.com/challenges/01953de4-ee8b-0807-88b1-86bb6abbf410
- `hasDynamicPromoCodes`: false

> It’s time to push the boundaries of what's possible with AI using Google Gemini. Check out the Gemini API to build AI-powered apps that make your friends say WHOA. So, what can Gemini do for your hackathon project?
>
> - Understand language like a human and build a chatbot that gives personalized advice
> - Analyze info like a supercomputer and create an app that summarizes complex research papers
> - Generate creative content like code, scripts, music, and more
>
> Think of the possibilities… what will you build with the Google Gemini API this weekend?

Prize page does **not** say “each teammate.” Per-challenge URL (https://www.mlh.com/challenges/01953de4-ee8b-0807-88b1-86bb6abbf410) repeats this blurb only. `externalSubmissionUrl` / `surveyLink`: null. `settings`: `{}`.

### A2. Best Use of ElevenLabs

- Sponsor window: **ElevenLabs Q4 2025 - Q4 2026**
- Prize: **Wireless Earbuds**
- CTA: Build with ElevenLabs → https://mlh.link/elevenlabs → https://www.mlh.com/partners/elevenlabs
- Challenge: https://www.mlh.com/challenges/01999bc7-ad70-0ba6-f3ff-d7eb57ff56d1

> Deploy natural, human-sounding audio with ElevenLabs. Create realistic, dynamic, and emotionally expressive voices for any project, from interactive AI companions to narrated stories and voice-enabled apps. ElevenLabs will empower you to build rich, immersive experiences without the need for actors or complex audio production, using simply the power of AI.
>
> Integrate fully autonomous audio experiences into your hack with ElevenLabs and give your project a voice, along with giving your team the chance to win some wireless earbuds!

Wording: “your team.” Brand/model of earbuds: UNKNOWN. Challenge page settings: description required, project URL required, built-with optional. No separate MLH submit URL (`externalSubmissionUrl` null).

### A3. Best Use of Solana

- Sponsor window: **Solana Q4 2025 - Q4 2026**
- Prize: **Ledger Nano S Plus**
- CTA: Build with Solana → https://mlh.link/solana → https://www.mlh.com/partners/solana
- Challenge: https://www.mlh.com/challenges/019a2bd6-b180-c2c1-8b01-cd7998ac0c8d

> The world of development is evolving fast and Solana is leading the charge with a network built to handle all of your infrastructure needs. Forget high fees and slow confirmations, it’s time to build applications that are fast, efficient, and scalable.
>
> Harness Solana's core advantages like blazing fast execution and near-zero transaction costs to make your hackathon ideas become real world projects. With Solana, the possibilities are endless.
>
> - Create a game, social app, or consumer product that relies on instant, high-frequency transactions.
> - Design a sophisticated trading, lending, or decentralized exchange (DEX).
> - Build a prototype for supply chain, identity, or payments that can handle massive, real-world volume.
>
> Show us how you can innovate with Solana for a chance to win some cool prizes for you and each member of your team!

### A4. Best Use of Vultr

- Sponsor window: **Vultr Q4 2025**
- Prize: **Portable Screens**
- CTA: Build with Vultr → https://mlh.link/vultr → https://www.mlh.com/partners/vultr
- Challenge: https://www.mlh.com/challenges/019a0ccc-7154-9378-095c-2a7be06a0378

> Vultr empowers hackers to bring their high-performance projects to life instantly; providing everything from the speed of one-click deployment and scalable cloud compute, to specialized Vultr Cloud GPUs that can power AI-driven applications. We want you to push the limits of what can be built when infrastructure is no longer the bottleneck!
>
> Sign up for a Vultr account today and claim your free cloud credits! Take your next hack to the cloud with Vultr for a chance to win some awesome portable screens for you and your team!

Prize-page credit **amount** is not stated here. Amount is on the partner page ($100). Brand/size of screens: UNKNOWN.

### A5. Best Use of Auth0

- API `name` has a trailing space: `"Best Use of Auth0 "`
- Sponsor window: **Auth0 Q4 2025 - Q3 2026**
- Prize: **Wireless Headphones**
- CTA: Build with Auth0 → https://mlh.link/auth0 → https://www.mlh.com/partners/auth0
- Challenge: https://www.mlh.com/challenges/019b7272-8e91-7e01-f122-fd9c4c8da1e9
- Inline links: https://mlh.link/auth0-ai-agents · https://mlh.link/auth0-signup · https://mlh.link/auth0-docs

> Auth0 wants your applications to be secure! Why spend hours building features like social sign-in, Multi-Factor Authentication, and passwordless log-in when you can enable them through Auth0 straight out of the box? You can also secure your AI applications with Auth0 for AI Agents.
>
> Auth0 is free to try, doesn’t require a credit card, and allows for up to 7,000 free active users and unlimited log-ins. Make your new account today and use any of the Auth0 APIs for a chance to win a pair of wireless headphones for you and each member of your team!

### A6. Best Use of MongoDB Atlas

- Sponsor window: **MongoDB Q4 2024 - Q4 2025**
- Prize: **M5Stack IoT Kit**
- CTA: Build with MongoDB → https://mlh.link/mongodb → https://www.mlh.com/partners/mongodb
- Challenge: https://www.mlh.com/challenges/01952051-cd69-c851-c19b-592551464587
- Inline links: https://mlh.link/mongodb · https://mlh.link/mongodb-free · https://mlh.link/mongodb-university

> MongoDB Atlas takes the leading modern database and makes it accessible in the cloud! Get started with a $50 credit for students or sign up for the Atlas free forever tier (no credit card required). Along with a suite of services and functionalities, you'll have everything you need to manage all of your data, and you can get a headstart with free resources from MongoDB University! Build a hack using MongoDB Atlas for a chance to win a M5Stack IoT Kit for you and each member of your group.

Exact M5Stack SKU: UNKNOWN on this page.

---

## B. Same-site pages linked from the prizes chrome

### B1. Software Lab — https://www.mlh.com/resources/software

Not HackCMU-specific. Visible sponsor blocks:

**Google Gemini**

> Discover your AI superpowers and build mind-blowing apps that can understand language, analyze data, generate images, and more! Check out these resources to get started with the Google Gemini API.
>
> - Access the Google Gemini Quickstart guide → https://mlh.link/gemini-quickstart
> - Reference the Gemini API documentation → https://mlh.link/gemini-docs
> - Find Gemini API code Examples → https://mlh.link/gemini-cookbook
>
> CTA: Get Started with Google Gemini → https://mlh.link/gemini

**GitHub Global Campus**

> Millions of developers use GitHub to build personal projects, support their businesses, and work together on open source technologies. GitHub Global Campus helps students, teachers, and schools access the tools and events they need to shape the next generation of software development. You’ll also have access to the GitHub Student Developer Pack, featuring tons of useful resources for hackathons and beyond!
>
> - Learn to Use GitHub → https://hackp.ac/github-helloworld
> - Learn more about GitHub Global Campus → https://hackp.ac/github-global-campus
> - Signup for the GitHub Student Developer Pack → https://hackp.ac/github

GitHub Copilot is **not** named on this page.

**MongoDB Atlas**

> Redeem $50 in MongoDB Atlas Credits!
>
> MongoDB Atlas is more than a general purpose database, it’s a full developer data platform. Simplify the way you integrate database functionality into your hackathon project by starting a free cluster or using your introductory $50 Atlas credits.
>
> Deploy a database to the cloud in minutes and take your hack to the next level with MongoDB Atlas.
>
> - MongoDB Atlas Documentation
> - MongoDB Developer Center
> - MongoDB Startup Guides
> - MongoDB Atlas Free Tier → https://hackp.ac/mongodb-free
> - MongoDB GitHub Repository → https://github.com/mongodb

**Auth0**

> No Credit Card Required!
>
> Auth0 is an easy to implement, adaptable authentication and authorization platform. Why spend hours building out your own log-in and sign-up flow when Auth0 has already done it for you? Simply signup for a free account and use their API to secure your application and your users’ information. Make login our problem. Not yours.
>
> - The Auth0 Developer Hub → https://hackp.ac/Auth0-developerhub
> - Check out the Auth0 x MLH Getting Started page → https://hackp.ac/auth0-MLH-guides
> - Check out the Auth0 API documentation → https://hackp.ac/auth0-docs
> - Even more Auth0 resources → https://hackp.ac/auth0-dev-center
> - Sign-up for free! → https://hackp.ac/auth0-signup

**GoDaddy Registry** (Software Lab + global catalog; **not** on HackCMU’s six)

> Get a free domain of your choice for 1 year!
>
> GoDaddy Registry is dedicated to advancing innovation, entrepreneurship and the pursuit of big ideas around the world. Empowering hackers with the tools, help and resources necessary to succeed online - starting with the perfect domain name.

- Host a Domain Name from GoDaddy Registry in Minutes! → https://hackp.ac/GoDaddy-medium → stories.mlh.io article (live timed out; Wayback: claim at **www.tech.study**, extensions .co / .us / .biz / .courses / .study, registrar Porkbun, then host on GCP)
- CTA → https://hackp.ac/GoDaddyRegistry → https://www.tech.study/ (title: “Major League Hacking + GoDaddy Registry FREE Domain Name”; form is client-rendered)

**Resolved Software Lab shortlinks (gotchas):**

| shortlink | actual dest |
|---|---|
| https://hackp.ac/github | GitHub Education benefits (login) |
| https://hackp.ac/github-helloworld | https://docs.github.com/en/get-started/using-github/hello-world |
| https://hackp.ac/github-global-campus | GitHub Blog “Introducing GitHub Global Campus” (2021) |
| https://hackp.ac/Auth0-developerhub | https://developer.auth0.com/resources |
| https://hackp.ac/auth0-MLH-guides | https://developer.auth0.com/resources/get-started/mlh |
| https://hackp.ac/auth0-docs | https://auth0.com/docs/ |
| https://hackp.ac/auth0-dev-center | https://community.auth0.com/ |
| https://hackp.ac/auth0-signup | **https://developer.auth0.com/newsletter** (Zero Index newsletter), **not** an Auth0 tenant signup. Use https://auth0.com/signup or https://mlh.link/auth0-signup for an account. |
| https://hackp.ac/auth0-quickstart | https://auth0.com/docs/quickstarts |

### B2. Hardware Lab — https://www.mlh.com/resources/hardware

Hero: “Borrow the latest & greatest hardware devices and components to use in your project this weekend.”

With `?event=hackcmu` the API includes notice `{ "message": "Unfortunately, MLH does not have a Hardware Lab at this event.", "active": false }`. Because `active` is **false**, that sentence is **not** shown. Visible cards still say “Visit the MLH table.” Confirm at the table; do not invent whether devices are stocked.

**Raspberry Pi Pico and RP2040**

> A tried and true classic, the Raspberry Pi is a great way to start your hardware hacking journey. Visit the MLH table to pick up your device, and start hacking away with the tutorials below.

Playlist: https://www.youtube.com/playlist?list=PLEBQazB0HUyQO6rJxKr2umPCgmfAU-cqR — DigiKey “Intro to Raspberry Pi Pico and RP2040”, 11 videos (MicroPython blink/I2C/PIO/asyncio; C/C++ VS Code/Picoprobe/PIO; SPI; SD card; custom PCB).

**Arduino Compatible Software**

> Picking up any Arduino hardware at the MLH hardware lab this weekend? Make sure you download the Arduino IDE so that you can program your hardware directly from your laptop! Compatible with Mac, Windows & Linux.

IDE: https://www.arduino.cc/en/software  
Playlist: https://www.youtube.com/playlist?list=PLEBQazB0HUyQd6Fsf5NQ75M9llbi1_j_8 — DigiKey “Arduino Project to Product” (current/battery/LoRa/sleep), not an IDE 101.

**Echo Dot (4th and 5th Gen)**

> Are you looking to use a smart device in your hardware hack? Swing by the MLH table to pick up an Amazon Echo.

Forum: https://www.amazonforum.com/s/echo-family — community, not a numbered setup guide.

**Google Home Mini Set Up Guide**

> Are you using a Google Home Mini this weekend? Learn more about how to set up your device with the guide below.

https://support.google.com/googlehome/answer/7029485 — Android Home app: plug in → Add Device → QR → finish in-app. Needs Google Account, Android 9+, 2.4/5 GHz Wi-Fi (not WPA-2 Enterprise).

### B3. Learn — https://www.mlh.com/resources/learn

Hero: “We want to make it easier to get started at a hackathon. Check out our hackathon resources.” Two cards.

**Get Started with MongoDB**

> Whether you are new to MongoDB or looking for a little inspiration to get your hackathon project started, the MongoDB Developer Center has all the latest MongoDB tutorials, videos and code examples featuring over a dozen programming languages, and even more technology integrations!

- JS tutorials → Node.js driver docs
- Python tutorials → PyMongo docs
- CTA → https://blog.mlh.com/read-and-write-to-a-mongodb-atlas-database-in-minutes-04-19-2023

**Get Started with Authentication**

> Auth0 is an easy to use authentication and authorization platform! If your hackathon project requires a log in and sign up workflow, Auth0 supports this functionality straight out of the box. Best of all, it's simple and free to get started. Click the link below to learn how to enable user authentication on your hackathon project in as little as ten minutes!

CTA → https://blog.mlh.com/enable-user-authentication-for-your-hackathon-project-in-as-little-as-ten-minutes-05-12-2023 — create tenant → SPA sample → `npm install && npm run` → localhost:3000 login.

### B4. Address Form

Nav: https://hackp.ac/address → **302** → https://majorleaguehacking.typeform.com/to/Mr3QYSi3  
Title: **MLH Address Form**. `isFormClosed: true`.

Closed-screen copy:

> This form has been migrated to MyMLH.  
> Please go to https://my.mlh.io/settings to update your address and t-shirt size preferences.

(`my.mlh.io/settings` → MLH sign-in.)

Embedded (closed) Typeform still contains older copy: “Complete the MLH Address form to get your swag.” / “Update your Major League Hacking Shipping Address” / use the same email as Devpost for I Demoed stickers / carrier may call for prize packages / complete once unless address changes. Because the form is closed, **do not submit here** — use MyMLH.

`challengeClaimLinks` on the prizes page: `{}` when signed out. None of the six HackCMU challenges has `is_address_challenge: true`.

### B5. Global prize catalog — https://www.mlh.com/events/prizes

This is the footer **Prizes & Freebies** target and the header “Prizes” link. **Superset. Not HackCMU’s list.**

| global category | prize | on HackCMU prizes page? |
|---|---|---|
| Best Use of Gemini API | Google Swag Kits | yes |
| Best Use of ElevenLabs | Wireless Earbuds | yes |
| Best Use of Solana | Ledger Nano S Plus | yes |
| Best Use of Tiger Data | Stream Deck Mini | **no** |
| Best Use of Presage | Fitbit Inspire & Presage Perks | **no** |
| Best Use of Gen AI | Assorted Prizes | **no** |
| Best Use of Vultr | Portable Screens | yes |
| Best Use of Backboard | Tile Essentials Pack | **no** |
| Best Use of DigitalOcean | Retro Wireless Mouse | **no** |
| Best Use of Snowflake API | Raspberry Pi 4 | **no** |
| Best Use of Auth0 | Wireless Headphones | yes |
| Best Use of MongoDB Atlas | M5Stack IoT Kit | yes |
| Best .Tech Domain Name | Desktop Microphone & a Free .Tech Domain Name for up to 10 years! | **no** |
| Best Domain Name from GoDaddy Registry | Digital Gift Card | **no** |

### B6. HackCMU event site + Devpost (linked from the prizes API `websiteUrl`)

**https://www.acmatcmu.com/hackcmu2026/** — single-page app. No Devpost URL, no MLH prize list. Nav: Station, Tickets, Tracks, FAQ, Sponsors.

Schedule (verbatim from site JS): Fri 5:00–6:00 Boarding; 6:00–6:30 Departure (opening); 7:00–9:00 Dinner + Sponsor Expo; 12:00–1:00am Midnight Cafe. Sat 12:00–1:00 Lunch; **4:00pm Baggage Check — Google Form — Submit your project description and track selection**; 4:00–6:30 Platform Showcase; 6:30–7:00 Dinner; 7:00–8:00 Arrival. Submission Google Form URL: UNKNOWN (named, not linked).

Tracks: “Track themes will be announced during the Opening Ceremony on Friday, September 11.” 50-word why-this-track. Prize depth scales with how many teams pick the track. Max team **4**. All work original; no building/designing before the event. Judging: real-life usefulness, technological complexity, originality, presentation/demo quality.

FAQ “How do prizes work?”

> We will have prizes for each tracks. In addition, we will select an overall grand prize across all projects. We will also have sponsor-specific prizes that aren't restricted to any track.

Raffle: automatic if you submit by the due date. Organizer: `acm-exec@cs.cmu.edu`. MLH Member Event / MLH Code of Conduct.

**https://hack-cmu-2026.devpost.com/** — challenge id 31074. Deadline **Sep 12, 2026 @ 4:00pm EDT**. Questions: `rachelto@andrew.cmu.edu`. Location: 4765 Forbes Ave, Pittsburgh, PA 15213.

**Devpost prize list (7):**

1. Overall Winner — 1 winner (same FAQ sentence as above)
2. [MLH] Best Use of Gemini API — **1 winner** — Google Swag Kits
3. [MLH] Best Use of ElevenLabs — **1 winner** — Wireless Earbuds
4. [MLH] Best Use of Solana — **1 winner** — Ledger Nano S Plus
5. [MLH] Best Use of Vultr — **1 winner** — Portable Screens
6. [MLH] Best Use of Auth0 — **1 winner** — Wireless Headphones
7. [MLH] Best Use of MongoDB Atlas — **1 winner** — M5Stack IoT Kit

Devpost “1 winner” is the **team**. Prize blurbs still say earbuds for the team / Ledger / headphones / M5Stack **for each teammate**. Same six MLH names as https://www.mlh.com/events/hackcmu/prizes. Overall Winner is **only** on Devpost + event FAQ, not on the MLH prizes page.

### B7. Code of Conduct

http://www.mlh.com/code-of-conduct → https://github.com/MLH/mlh-policies/blob/main/code-of-conduct.md (updated April 16, 2026).

North America incidents: **+1 409 202 6060**, `incidents@mlh.io`. Canada / UK / Europe / APAC / India numbers are on that page. Special: Mary Siebert +1 (516) 362-1835 `mary@mlh.io`; Swift +1 (347) 220-8667 `swift@mlh.io`.

---

## C. Gemini

Partner: https://www.mlh.com/partners/gemini  
CMS name: `Gemini Demo Q1 2025 - Q1 2026`

### C1. Partner page (verbatim)

**Build with Gemini**  
Engineer the future of AI with Gemini!

Build the next generation of AI with Gemini and MLH! Access Google’s most capable AI models, explore developer resources, and win prizes for your hackathon projects.

Tags: AI/ML · Generative AI · LLM · Agentic AI · RAG · Multimodal AI  
CTA: Build with Gemini → http://mlh.link/gemini-quickstart

**Resources**

Build mind-blowing AI apps that can understand language, analyze data, and ignite your creativity with the Gemini API.

**Quick Start Guide** — The fastest way to start building with Google Gemini.

1. **Get a Google student plan for free!**  
   Redeem a student plan for 1 year at no cost. Unlock 4x higher usage limits in Gemini, more storage (5 TB), Gemini Spark, and Gemini Omni for 1 year.  
   → https://mlh.link/gemini-student-plan → https://gemini.google/students/

2. **Activate $10 free credits a month!**  
   Get your $10 in free credits per month by claiming your Google Program Benefits.  
   → https://developers.google.com/program/my-benefits → https://me.developers.google.com/benefits (**login wall**)

3. **$300 in Google credits with a new account!**  
   Not a student? Not a problem. You can claim $300 in free credits with a new account. Check out the program details to get started.  
   → https://docs.cloud.google.com/free/docs/free-cloud-features#free-trial

4. **Google AI Studio**  
   The fastest path from prompt to production with Gemini. Try out Google AI Studio at mlh.link/gemini-aistudio.  
   → https://mlh.link/gemini-aistudio → https://aistudio.google.com/prompts/new_chat (**Google sign-in**)

**Resource cards**

- The Google Gemini Quickstart guide — install Gemini libraries and make your first API request. → https://mlh.link/gemini-quickstart → https://ai.google.dev/gemini-api/docs/quickstart → **301** https://ai.google.dev/gemini-api/docs/get-started
- Reference the Gemini API documentation — “The fastest path from prompt to production with Gemini, Veo, Nano Banana, and more.” → https://mlh.link/gemini-docs → https://ai.google.dev/gemini-api/ → https://ai.google.dev/gemini-api/docs
- Find Gemini API code examples with the Gemini API Cookbook → https://mlh.link/gemini-cookbook → https://github.com/google-gemini/cookbook
- Google Gemini: Free Pro Plan for Students. — “Free for 1 year. Get more access to our most accurate model Gemini 3.1 Pro, unlimited image uploads, Pro-level image generation, customized quizzes and advanced learning tools like NotebookLM, plus 2 TB storage. Just for Students.” → https://mlh.link/gemini-aiprofree-landingpage → https://gemini.google/students/
- Activate your $10 in free credits! → https://mlh.link/gemini-10credits-landingpage → https://developers.google.com/program/my-benefits

### C2. Access / credits (destinations)

**Student Google AI Pro** — https://gemini.google/students/

> Study with Gemini and get unlimited uploads of your own class materials, study notebooks, interactive visualizations, and Gemini Live. And with the free student plan, you can even unlock 4x higher usage limits in Gemini, more storage (5 TB), Gemini Spark, and Gemini Omni for 1 year.

Landing FAQ: “available to eligible **U.S. college students ages 18+**.” Both new users and students whose 2025 AI Pro trial expired can qualify. Verify each year.

Legal line on that page:

> Eligible students only. Offer Terms apply. Redeem until December 31, 2026. Valid form of payment required at sign-up. Unless cancelled earlier, Google AI Pro will automatically charge $19.99/month after the trial ends. Cancel anytime.

Offer terms (https://one.google.com/offer/studentoffer8?g1_landing_page=0, last updated August 19, 2026): 18+; enrolled at a higher-ed institution in a supported country/region (exceptions include Bolivia, Albania, Canada, Hong Kong, Macau, Tunisia); SheerID; personal Google Account; Google Payments account with a qualifying payment method. Not school-issued Workspace. Not combinable with some other Google One situations. This page is a **consumer Gemini / Google AI Pro** plan. It does **not** tell you how to create a Gemini **developer API** key.

**$10 / month credits** — bundled with **Google AI Pro** (or higher Ultra amounts). https://developers.google.com/program/plans-and-pricing: Premium included with Google AI Pro, **$19.99/month**, “$10 GenAI and Cloud monthly credit.” Redeem on a **signed-in** My Benefits page (https://developers.google.com/profile/help/benefits): apply to a Cloud billing account, or paste a promo at https://console.cloud.google.com/billing/redeem. Credits expire a year after grant.

**$300 Cloud Welcome credit** — https://docs.cloud.google.com/free/docs/free-cloud-features#free-trial

> Signing up for the Free Trial creates a Free Trial billing account that is preloaded with $300 in free Welcome credit which is valid for 90 days.

Eligibility: never a paying user of Google Cloud / Maps / Firebase, and never signed up for the Free Trial. Credit card (or other payment) required at signup (authorization hold, not a charge). **During the trial you aren't billed.**

**Critical (same Cloud docs page):**

> The $300 credit can't pay for Gemini API in AI Studio costs. Consider using the Gemini API Free tier, or sign up for a Prepay billing plan.

Billing docs (https://ai.google.dev/gemini-api/docs/billing): new accounts start on Free Tier. Upgrade = link billing + prepay **minimum $5**. “Not all Google Cloud credits, such as the Google Cloud Welcome credit, can be used towards Gemini API and AI Studio.” Prepay credits apply only to Gemini API usage, not other Cloud services. Unused Prepay credits expire after 12 months.

**Gemini 3.1 Pro Preview** pricing page: Free Tier input/output **Not available** (paid only).

### C3. First API request (official get-started)

https://ai.google.dev/gemini-api/docs/get-started

1. Get an API key in Google AI Studio (https://aistudio.google.com/api-keys). New users get a project + key after accepting ToS. `export GEMINI_API_KEY="YOUR_API_KEY"`
2. Python: `pip install -U google-genai` then Interactions API with model **`gemini-3.8-flash`**. JS: `npm install @google/genai`. REST: `POST https://generativelanguage.googleapis.com/v1beta/interactions` with header `x-goog-api-key`.
3. Cookbook start: https://github.com/google-gemini/cookbook — need a Google account + API key; start `quickstarts/Authentication.ipynb` and `quickstarts/Get_started.ipynb`.

Docs hub models named on-page: Gemini 3.8 Flash; Gemini 3.5 Flash-Lite; Gemini 3.1 Pro; Nano Banana 2 / Pro; Gemini Omni Flash; Gemini 3.5 Transcribe; Gemini Robotics. Also Veo 3.1, Live API.

---

## D. ElevenLabs

Partner: https://www.mlh.com/partners/elevenlabs  
CMS: `ElevenLabs Q4 2025 - Q4 2026`

### D1. Partner page (verbatim)

**Build with ElevenLabs**  
Give your Vision a Voice

Instantly add realistic voiceovers and conversational agents to your projects. ElevenLabs provides high-quality text-to-speech technology that will bring your ideas to life!

Tags: AI · Voice API · Voice Agents  
CTA: Build with ElevenLabs → https://elevenlabs.io/

**Resources:** AI voice models and products powering millions of developers, creators, and enterprises. From low‑latency conversational agents to the leading AI voice generator for voiceovers and audiobooks.

**Free ElevenLabs Credits for MLH Hackers!**  
Follow the steps below to get your ElevenLabs promo code.

1. **Register for a Hackathon** — Head over to https://mlh.io/events and register for any of our upcoming events. (redirects to https://www.mlh.com/seasons/2027/events/)
2. **Check your inbox** — The week of your event, you'll receive an email from MLH including your ElevenLabs promo code.
3. **Redeem your promo code** — The promo code link in your email should take you directly to the ElevenLabs signup page. Set up your new account!
4. **Start Hacking!** — Once you have your free **3 month ElevenLabs subscription**, use any of the resources below to get started!

Credit **count** and **which paid SKU** the 3-month sub is: UNKNOWN. Promo code string / redeem URL: email-only, UNKNOWN on the page.

**Resource cards**

| card | dest |
|---|---|
| ElevenLabs Demo Web Application | https://mlh.link/elevenlabs-demo → iframe https://mlh.github.io/elevenlabs-demo/ |
| Major League Hacking ElevenLabs Challenge Video | https://mlh.link/elevenlabs-videos → https://www.youtube.com/watch?v=O6pJnKap8Qg (“Major League Hacking ElevenLabs Challenge - MLH 2026 Season”, published Sep 27, 2025). Watch-page “Learn more about the ElevenLabs Challenge: **TODO**” |
| ElevenLabs Documentation | https://elevenlabs.io/docs/overview → /docs/overview/intro |
| ElevenLabs Agents Documentation | https://mlh.link/ElevenLabs-Agents → https://elevenlabs.io/docs/eleven-agents/overview |
| Developer Quickstart | https://elevenlabs.io/docs/quickstart → /docs/eleven-api/quickstart |
| ElevenLabs API Reference | https://elevenlabs.io/docs/api-reference/introduction |
| Product Guide | https://elevenlabs.io/docs/product-guides/overview → /docs/eleven-creative/overview |

### D2. Product / models (destinations)

Homepage products: ElevenCreative, ElevenAgents, ElevenAPI. TTS / STT / Music / Voice Cloning / SFX / Dubbing / Image & Video.

Homepage model claims: **Eleven Flash** 75ms; **Eleven Multilingual** “Best lifelike consistent speech”; **Eleven v3** “Our most expressive model yet”; **Eleven Scribe** 98% accuracy (STT). TTS “29+ languages.”

Docs overview credits: shared across products; TTS = one credit per character; unused credits roll over up to two months on paid plans (not Free). “See pricing.”

Public pricing FAQ (https://elevenlabs.io/pricing; **hackathon not stated**; `showStarterPromo: false`):

> Monthly price and included credits per plan: Free $0 (10,000 credits); Starter $6 (30,000 credits); Creator $22 (121,000 credits, $11 for the first month); Pro $99 (600,000 credits); Scale $299 (1,800,000 credits, 3 seats); Business $990 (6,000,000 credits, 10 seats); Enterprise is custom.

Billing docs: “When signing up, you will be automatically assigned to the free tier.” Free-plan content: non-commercial with attribution. Mapping of MLH “3 month subscription” → these SKUs: UNKNOWN.

### D3. First API request

Create key: dashboard https://elevenlabs.io/app/developers/api-keys (quickstart still says `/app/settings/api-keys`). Header: `xi-api-key`. Env: `ELEVENLABS_API_KEY`.

Create speech: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`  
Official sample voice: `JBFqnCBsd6RMkjVDRZzb` (“George”). Quickstart model: `eleven_v3`. API default `model_id`: `eleven_multilingual_v2`. `output_format` default `mp3_44100_128`.

Agents: dashboard / widget `<elevenlabs-convai agent-id="…">` / CLI `elevenlabs agents` / API `conversational_ai.agents.create`. Architecture: ASR + your LLM + low-latency TTS + turn-taking. Demo app lists 10 named MLH voice agents (Kai, Elian, Ada, Morgan, Dr. Pitch, Spark, Chloe, Aura, Sparky, Alex).

---

## E. Solana

Partner: https://www.mlh.com/partners/solana  
CMS: `Solana Q4 2025 - Q4 2026`

### E1. Partner page (verbatim)

**Build with Solana**  
The Ultimate Development Layer

Revolutionary digital infrastructure. Blazing speed, low fees, & high throughput for verified ownership, instant payments, and transparent logic in your next project.

Tags: Blockchain · Infrastructure · Web3 · Layer-1 · DeFi  
CTA: Build with Solana → https://mlh.link/solana-quickstart

**Resources:** Let Solana handle the scale and reliability of your hack while you focus on innovation. Use Solana as a powerful backend for any project!

**Quick Start Guide** — Integrate Solana into your next hack to qualify for the Best Use of Solana prize category!

1. **Check out the quick start guide!** — https://mlh.link/solana-quickstart
2. **Fund your DevNet wallet** — Build on the Solana DevNet and fund your wallet at https://mlh.link/solana-faucet
3. **Start Hacking!**

**Resource cards**

| card | dest |
|---|---|
| Solana Agent Skills | https://mlh.link/solana-agent-skills → https://solana.com/skills |
| Solana Hacker Resources | https://mlh.link/solana-resources → Google Drive PDF “Solana Resources” |
| Solana Quick Install Guide | https://mlh.link/solana-quick-install → https://solana.com/docs/intro/installation |
| Solana Documentation | https://mlh.link/solana-docs → https://solana.com/docs |
| Get started with Anchor | https://mlh.link/solana-introduction → https://www.anchor-lang.com/docs |
| Solana Courses on Blueshift | https://mlh.link/solana-tutorials → https://learn.blueshift.gg/en |
| Solana Developer Templates | https://mlh.link/solana-templates → https://solana.com/developers/templates |
| Solana DevNet Faucet | https://mlh.link/solana-faucet → https://faucet.solana.com/ |

Prize hardware is **not** restated on the partner page (only “Best Use of Solana prize category”).

### E2. Quick Start (Playground) — https://solana.com/docs/intro/quick-start

Browser IDE: **https://beta.solpg.io/** (`solpg.io` / `playground.solana.com` do not resolve; `/developers/playground` is 404).

Steps on the official page: open Playground → click 🔴 **Not connected** → **Save keypair** → **Continue**. Cluster shown: **devnet**. Wallet is in browser local storage.

> Use your Playground wallet for testing and development only. Never send real assets (from `mainnet`) to this address.

Add **devnet SOL**:

**Option 1 (Playground terminal):**

```
solana airdrop 5
```

**Option 2:** https://faucet.solana.com/ — enter address, select amount, Confirm Airdrop.

Tutorial will cover: accounts, sending transactions, building/deploying programs, PDAs, CPIs.

### E3. Faucet — https://faucet.solana.com/

Devnet or testnet. **Maximum of 2 requests every 8 hours.** Page payload: `allowedRequests: 2`, `redHours: 8`, `maxAmountPerRequest: 5`. GitHub sign-in unlocks a higher limit. “This tool is designed for development purposes and does not distribute mainnet SOL.” AI agents told not to use this faucet; use CLI / POW / local validator instead.

CLI examples on that page: `solana airdrop 2 <WALLET_ADDRESS> --url devnet`. Local: `solana-test-validator` then airdrop on localhost.

### E4. Local install — https://solana.com/docs/intro/installation

One command (Windows must use WSL first: `wsl --install`):

```
curl --proto '=https' --tlsv1.2 -sSfL https://solana-install.solana.workers.dev | bash
```

Installs Rust, Solana CLI, Anchor, Surfpool, Node.js, Yarn. CLI basics: `solana config set --url devnet` then `solana airdrop 2`. “Devnet airdrops limit requests to 5 SOL per request.”

Agent skills: `npx skills add https://github.com/solana-foundation/solana-dev-skill`  
Anchor: “development framework for building secure Solana programs (smart contracts).” Browser quickstart: https://www.anchor-lang.com/docs/quickstart/solpg

Templates on page: nextjs, nextjs-anchor, Pinocchio Counter, react-vite, react-vite-anchor, Mobile Expo, Phantom Embedded (JS / Next / RN), Supabase Auth, X402 Next.js.

---

## F. Vultr

Partner: https://www.mlh.com/partners/vultr  
CMS: `Vultr Q4 2025` (page `updatedAt` 2026-01-29)

### F1. Partner page (verbatim)

**Build with Vultr**  
The Cloud for Hackers

Vultr offers instant, high-performance cloud infrastructure, from the latest GPUS and Virtual Machines to Managed Kubernetes; built to empower hackers like you!

Tags: AI · Agents · Infrastructure · Cloud  
CTA: Build with Vultr → https://docs.vultr.com/products

**Resources:** Bring your projects to life instantly with Vultr; a cloud platform that offers everything from one-click deployment and cloud compute, to cloud GPUs for AI applications!

**Quick Start Guide**

Follow the steps below to get started with Vultr Cloud!  
(Please note that multiple registrations are not allowed. All registrants must comply with Vultr’s Terms of Service / Acceptable Use Policy)

1. **Signup for a free Vultr account!** — https://mlh.link/vultr-signup → https://www.vultr.com/register/
2. **Verify your email.**
3. **Claim your Gift Code (Step 1 of 2)** — Sign out of your Vultr account and sign back in using https://mlh.link/vultr-giftcode  
   Once you’ve done so, you should see a Gift Code tab populate in the Billing section of your account dashboard.
4. **Claim your Gift Code (Step 2 of 2)** — If you missed it during Opening Ceremony, grab a Gift Code from your **MLH Coach** and apply it to your account in order to claim **$100** worth of Vultr credits, **no credit card required!**
5. **Check out Vultr's cloud platform.** — https://mlh.link/vultr-products → https://docs.vultr.com/products
6. **Start hacking!** — Build & deploy your next AI-powered hack using Vultr Cloud!

Giftcode dest: https://my.vultr.com/billing/?promo=HACKATHON (login). ToS URL on register form: https://www.vultr.com/legal/tos/ · AUP URL: named on MLH page, not linked (UNKNOWN).

**Resource cards:** Reference docs → https://docs.vultr.com/reference · Tech Talks YouTube playlist `PLSbDd9R2e5jgqwd-YBkBUByhOyyOLbhi7` · Marketplace **docs category** https://docs.vultr.com/category/vultr-marketplace · API https://www.vultr.com/api/ · CLI https://github.com/vultr/vultr-cli · Support https://docs.vultr.com/support

### F2. Products catalog (https://docs.vultr.com/products)

Configure and deploy Vultr products: Compute, GPU, storage, networking, and more.

**Compute:** Instances (CPU/GPU VMs) · Clusters · Kubernetes · Serverless Inference  
**Storage:** Block · Object (S3-compatible) · File System · Databases · Storage Gateway · Backups · Snapshots  
**Network:** VPC · Load Balancer · Firewall Groups · BGP · CDN Pull/Push · DNS · Reserved IPs  
**Orchestration:** Container Registry · ISOs · Startup Scripts · SSH Keys

API v2: `https://api.vultr.com/v2`, Bearer `VULTR_API_KEY`, ~30 req/s. CLI env: `VULTR_API_KEY`. Key UI: https://my.vultr.com/settings/#settingsapi

Register form (Wayback 2026-03-23; live GET was Cloudflare 403): email + password, ToS checkbox, “Create free account”, GitHub/Google SSO. Credit card **not on that form**.

**Conflict:** Vultr support article “How can I add a promotional code” says you must have a valid credit card or PayPal. MLH partner page says **$100, no credit card required.** Do not reconcile.

---

## G. Auth0

Partner: https://www.mlh.com/partners/auth0  
CMS: `Auth0 Q4 2025 - Q3 2026`

### G1. Partner page (verbatim)

**Build with Auth0**  
Secure your app in minutes with the ultimate authentication tool.

Stop wasting time on login logic. Use Auth0 and AI Agents to ship secure apps in minutes. Focus on your core features and dominate your next hackathon by building smarter, faster, and safer.

Tags: JWT · OAuth · MFA · SSO · CIAM · AI Agents  
CTAs: Build with Auth0 AI Agents → https://mlh.link/auth0-ai-agents · Build with Auth0 → https://mlh.link/auth0-learn

**Resources:** Don’t build identity from scratch. Leverage Auth0's developer tools and AI Agents to ship a secure, professional app before closing ceremony. Whether you're building a mobile app, a React frontend, a Python backend, or managing Agentic workflows, Auth0 can get you to the finish line faster.

**Get Started with Auth0 & Auth0 AI Agents today!**

1. **Signup for Auth0 today!** — Start building with your free plan. No credit card required. → https://mlh.link/auth0-signup → https://auth0.com/signup?place=header&type=button&text=sign%20up
2. **Setup auth for your AI Applications** — Building with AI? Auth0 for AI Agents is a great way to secure your agentic workflows! → https://mlh.link/auth0-ai-agents → https://auth0.com/ai
3. **Pick your own quick start guide!** → https://mlh.link/auth0-quickstart → https://auth0.com/docs/quickstarts

**Resource cards**

| card | dest |
|---|---|
| Auth0 AI Agents | https://auth0.com/ai |
| Auth0 AI Agents Documentation | https://mlh.link/auth0-ai-agents-docs → https://auth0.com/ai/docs/intro/overview |
| Auth0 AI Agents Sample Application | Assistant0 — https://github.com/auth0-samples/auth0-assistant0 |
| Auth0 Signup | no credit card required → signup |
| Explore Auth0's developer resources | https://mlh.link/auth0-developerhub → https://developer.auth0.com/resources |
| Auth0 Quickstart Guides | https://auth0.com/docs/quickstarts |
| The Hackathon Guide | https://mlh.link/auth0-learn → https://developer.auth0.com/resources/get-started/mlh |

Partner page does **not** restate 7,000 MAU, unlimited logins, Token Vault, or “any Auth0 APIs.” Those phrases are on the **HackCMU prize** blurb.

### G2. Hackathon guide (https://developer.auth0.com/resources/get-started/mlh)

> If you want to set your project apart from the competition and eventually turn it into a portfolio piece, integrating Auth0 into your app is the perfect way to do so. With Auth0 SDKs available in different programming languages, you have everything you need to add sign-up, login, user profiles, and more for free in less than 15 minutes.
>
> First, sign up for a free account. Then, visit the Auth0 quickstarts below for your programming language and stack of choice to learn more.

Interactive quickstarts listed: React, Express.js, Flask, Django, Spring, Android, iOS, Flutter. “What Next?”: Google social (~10 min); breached-password alerts (~2 min); passkeys (~5 min). This guide is **core login**, not Token Vault / CIBA / MCP.

Signup visible copy: “Start building with your free plan / No credit card required.” MAU number **not** on the signup form.

### G3. Auth0 for AI Agents (https://auth0.com/ai + docs)

> Let your AI agents identify users, call APIs, and connect to MCP servers more securely.

Docs overview: user authentication (Universal Login); call **first-party** APIs (registered in the Auth0 Dashboard) on a user’s behalf; call **third-party** APIs (Google, Slack, GitHub, …) via **Token Vault**; **CIBA** human-in-the-loop (Guardian push preferred; email is a paid add-on); **FGA** for RAG document-level access.

**Token Vault / Connected Accounts:** after login, user authorizes a connection; Auth0 stores provider access/refresh tokens; app exchanges an Auth0 token for the provider token; agent never sees the user’s credentials.

**Auth for MCP:** OAuth 2.1 / OIDC for MCP servers; resource-scoped tokens; On-Behalf-Of for your APIs; Token Vault for third-party APIs.

Assistant0: Gmail / Calendar / profile / HITL fake purchase / RAG / GitHub; Token Vault. Stacks: LangGraph JS/Python, Vercel AI, LlamaIndex.

Official pages **do not** use the prize phrase “any Auth0 APIs.” Split is: ordinary Auth0 login + APIs you register, vs Auth0 for AI Agents (Token Vault, CIBA, MCP, FGA).

### G4. Free plan numbers

| claim | HackCMU prize blurb | auth0.com/pricing (fetched) |
|---|---|---|
| No credit card | yes | “No credit card needed to sign up.” |
| Free MAU cap | **up to 7,000 free active users** | **Up to 25,000 monthly active users** |
| Unlimited logins | yes | not stated |

Do not invent which number MLH judges will use. Prize-page eligibility wording is “use any of the Auth0 APIs.”

---

## H. MongoDB Atlas

Partner: https://www.mlh.com/partners/mongodb  
CMS: `MongoDB Q4 2024 - Q4 2025` (`updatedAt` 2026-01-23)

### H1. Partner page (verbatim)

**Build with MongoDB**  
Built for the way you work with data!

MongoDB Atlas is a full developer data platform. Easily deploy on-demand databases and manage your data via the web console, Atlas CLI, or Data API to build faster at your next hackathon.

Tags: NoSQL · Atlas · Vector Database · MDB Flexible Schema  
CTA: Build with MongoDB → https://mlh.link/mongodb-benefits

**Get Started with MongoDB today!**

1. **Signup for a free MongoDB account!** — Get $50 worth of free MongoDB Atlas Credits. → https://mlh.link/mongodb-benefits
2. **Checkout this step by step guide!** → https://mlh.link/mongodb-gettingstarted
3. **The MongoDB Learning Hub** → https://mlh.link/mongodb-learning-hub

**Resource cards**

| card | dest |
|---|---|
| MongoDB Atlas Free Forever Tier | https://mlh.link/mongodb-free → https://www.mongodb.com/cloud/atlas/register (meta: “Get started free. No credit card required.”) |
| MongoDB University | https://mlh.link/mongodb-university → https://learn.mongodb.com/ |
| $50 in MongoDB Atlas Credits! | **https://mlh.lin/mongodb-benefits — TYPO, DNS does not resolve.** Use https://mlh.link/mongodb-benefits |
| MongoDB Getting Started Guide | https://mlh.link/mongodb-gettingstarted → https://blog.mlh.com/read-and-write-to-a-mongodb-atlas-database-in-minutes-04-19-2023 |
| MongoDB Docs | https://mlh.link/mongodb-docs → https://www.mongodb.com/docs/ |
| MongoDB Atlas Learning Hub | https://www.mongodb.com/resources/product/platform/atlas-learning-hub |

### H2. Student / $50 / free tier

https://www.mongodb.com/students and GitHub Pack (https://education.github.com/pack):

> Offer: $50 in MongoDB Atlas Credits, plus access to MongoDB Compass and MongoDB University including free certification valued at $150.

Eligibility (MongoDB FAQ + GitHub Education):

- Enrolled in a degree- or diploma-granting program
- Verifiable school-issued email **or** documentation of student status
- GitHub personal account
- At least 13 years old

**How Atlas promotional codes work (students FAQ, verbatim):**

> MongoDB Atlas is billed hourly based on usage. As part of the GitHub Student Developer Pack, we provide $50 in Atlas credits to apply to your Atlas organization. To redeem this, you'll need a valid credit card or a PayPal account linked to your Atlas account.

Unused codes expire in **90 days**. Redeem once, at organization level. Apply: Atlas org Billing → Apply Code (docs: https://www.mongodb.com/docs/atlas/billing/subscriptions/).

**Free forever / M0** (no GitHub Pack needed):

> Atlas Free clusters (formerly known as M0) provide a small-scale development environment to host your data. Free clusters never expire… You can deploy only one Free cluster per Atlas project.

Pricing: M0 · 512 MB · Shared · **Free forever**. FAQ also: 32MB sort memory, up to 100 operations per second. Register meta + MLH 2023 tutorial: **no credit card required** for free signup. That “no card” phrase is **not** on `/students` (because the $50 promo wants a card/PayPal).

### H3. First cluster (MLH 2023 guide)

https://blog.mlh.com/read-and-write-to-a-mongodb-atlas-database-in-minutes-04-19-2023

Create free Atlas account → deploy **free** instance → admin user + allow IP → create DB/collection → insert a document → Cluster → Connect → Application → `mongodb+srv://` URI. **Do not commit the URI.** Then official driver read/write.

Official now: https://www.mongodb.com/docs/atlas/tutorial/create-atlas-account/ and https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/ · https://www.mongodb.com/docs/get-started/

---

## I. Conflicts / do not invent

Keep both sides. Do not pick a winner unless a judge or MLH Coach says so.

1. **Gemini storage:** partner Quick Start step 1 and gemini.google/students = **5 TB**. Partner “Free Pro Plan for Students” card = **2 TB** + “Gemini 3.1 Pro” + NotebookLM. Official students FAQ does not mention 2 TB, 3.1 Pro, or NotebookLM.
2. **Gemini student eligibility:** students landing = **U.S. college, 18+**. Offer terms = 18+ higher-ed in supported countries (Canada listed as an exception).
3. **$300 Cloud credit ≠ Gemini API in AI Studio.** Use Gemini API Free tier (`gemini-3.8-flash` is free of charge on the pricing page) or Prepay ≥ $5. `gemini-3.1-pro-preview` is not on the Free Tier.
4. **Auth0 MAU:** HackCMU prize blurb **7,000** + unlimited logins. Current https://auth0.com/pricing **25,000 MAUs**. Signup form states neither number.
5. **Vultr card:** MLH = $100, no card, code from **MLH Coach**, sign in via giftcode link. Vultr’s generic promo-code FAQ wants a card or PayPal.
6. **MongoDB $50:** needs card or PayPal. Free M0 does not. Partner $50 card URL `mlh.lin` is broken.
7. **ElevenLabs 3-month sub:** no credit count, no plan name, email-only redeem. Public Free tier is 10,000 credits / month; mapping UNKNOWN.
8. **Prize hardware brands** (earbuds, headphones, portable screens, exact M5Stack SKU): UNKNOWN on all fetched pages.
9. **Address form:** Typeform https://majorleaguehacking.typeform.com/to/Mr3QYSi3 is **closed** (“migrated to MyMLH”). Live path: https://my.mlh.io/settings. `hasDynamicPromoCodes` is false on all six HackCMU challenges.
10. **Global MLH catalog** has eight extra prizes (Tiger Data Stream Deck Mini, Presage Fitbit, Gen AI assorted, Backboard Tile, DigitalOcean retro mouse, Snowflake Pi 4, .Tech mic+domain, GoDaddy gift card). HackCMU API list is the six in section A only.
11. **Devpost** marks each MLH category “1 winner” (the team). Per-person hardware is only in the prize *blurb*.
12. **`hackp.ac/auth0-signup` on Software Lab** lands on Auth0’s **newsletter**, not tenant signup.
13. Hardware Lab JSON has an **inactive** “no Hardware Lab at this event” notice. Visible copy still says visit the MLH table.
14. **Opening vs older pages:** event site / Devpost still omit named HackCMU objects and the fifth judging axis (Relevance). Opening is the live list. Demo length: opening **3 min**; older briefings said 2. Hacking **starts Fri 9:00pm** (boarding is 5–6pm). IFM is **(optional)** on the tracks slide and a **separate IFM Prize**; do not invent whether the Google Form lists IFM as a fifth track.

---

## J. Link map (HackCMU-relevant)

### Prize + partner hubs

| | prize CTA | partner page |
|---|---|---|
| Gemini | https://mlh.link/gemini | https://www.mlh.com/partners/gemini |
| ElevenLabs | https://mlh.link/elevenlabs | https://www.mlh.com/partners/elevenlabs |
| Solana | https://mlh.link/solana | https://www.mlh.com/partners/solana |
| Vultr | https://mlh.link/vultr | https://www.mlh.com/partners/vultr |
| Auth0 | https://mlh.link/auth0 | https://www.mlh.com/partners/auth0 |
| MongoDB | https://mlh.link/mongodb | https://www.mlh.com/partners/mongodb |

### Signup / credits / keys

- Gemini API key: https://aistudio.google.com/api-keys
- Gemini students: https://gemini.google/students/
- Gemini $10 benefits: https://developers.google.com/program/my-benefits
- Gemini $300 trial: https://console.cloud.google.com/freetrial
- ElevenLabs signup: https://elevenlabs.io/app/sign-up — **MLH promo is email-only**
- ElevenLabs API keys: https://elevenlabs.io/app/developers/api-keys
- Solana Playground: https://beta.solpg.io/
- Solana faucet: https://faucet.solana.com/
- Vultr register: https://www.vultr.com/register/
- Vultr giftcode: https://my.vultr.com/billing/?promo=HACKATHON + **physical code from MLH Coach**
- Auth0 signup: https://auth0.com/signup
- MongoDB Atlas register (free, no card): https://www.mongodb.com/cloud/atlas/register
- MongoDB students / $50: https://www.mongodb.com/students
- GitHub Student Pack: https://education.github.com/pack

### Docs a hacker actually opens

- Gemini get-started: https://ai.google.dev/gemini-api/docs/get-started
- Gemini cookbook: https://github.com/google-gemini/cookbook
- ElevenLabs TTS quickstart: https://elevenlabs.io/docs/eleven-api/quickstart
- ElevenLabs agents: https://elevenlabs.io/docs/eleven-agents/overview
- Solana quick start: https://solana.com/docs/intro/quick-start
- Vultr products: https://docs.vultr.com/products
- Auth0 MLH guide: https://developer.auth0.com/resources/get-started/mlh
- Auth0 AI Agents docs: https://auth0.com/ai/docs/intro/overview
- MongoDB first cluster (MLH): https://blog.mlh.com/read-and-write-to-a-mongodb-atlas-database-in-minutes-04-19-2023
- MongoDB free cluster: https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/

### MLH site

- https://www.mlh.com/events/hackcmu/prizes
- https://www.mlh.com/resources/software
- https://www.mlh.com/resources/hardware
- https://www.mlh.com/resources/learn
- https://www.mlh.com/events/prizes (global superset / footer “Prizes & Freebies”)
- https://hackp.ac/address → closed Typeform; use https://my.mlh.io/settings
- Event site: https://www.acmatcmu.com/hackcmu2026/
- Devpost: https://hack-cmu-2026.devpost.com/
- CoC: https://github.com/MLH/mlh-policies/blob/main/code-of-conduct.md
- GoDaddy claim (not a HackCMU prize): https://www.tech.study/
- IFM: https://ifm.ai/
- Querit: https://www.querit.ai/en
- Discord: acmatcmu

---

## K. Opening Ceremony deck (Fri Sep 11, 2026)

Source: `HackCMU_2026_Opening_Ceremony.pdf` (53 slides; posted on Discord). PDF text extract; decorative “ç√” marks omitted. Slides are official ACM@CMU copy.

**Title / delay:** Opening Ceremony. Delayed: 6:15PM.

**Departure / contacts:** Discord (QR). acmatcmu. `acm-exec@cs.cmu.edu`. acmatcmu.com. ACM@CMU.

**About ACM@CMU:** Host HACKCMU, AWAP, and HACKBERRY PI every year. Create game, websites, and servers used in hackathons. Do research, get mentorship, and more!

**What is HackCMU:** 24 Hours. Teams of up to 4 people. Mentorship & Workshops. Hacking. Lots of free food. Prizes.

**Schedule: Friday**

- 05:00 - 06:00 pm Boarding
- 06:00 - 06:30 pm Departure (now)
- 07:00 - 09:00 pm Dinner + Sponsor Expo
- 09:00 pm Hacking Starts!
- 09:00 - 10:00 pm IFM Workshop
- 10:00 - 10:30 pm Cursor Workshop
- 12:00 - 1:00 am Midnight Cafe Halte

**Schedule: Saturday**

- 12:00 - 01:00 pm Lunch
- 04:00 pm Baggage Check
- 04:00 - 06:30 pm Platform Showcase
- 06:30 - 07:00 pm Dinner
- 07:00 - 08:00 pm Arrival

**Tracks (names):** Optimization. Traveling. Multiplayer. Food. IFM (optional).

**Track one-liners (slides 16–19):**

- Optimization: “perhaps optimize something? 0.0”
- Traveling: “what does traveling mean to you? hm….”
- Multiplayer: “this is how you can meet people and touch grass :P”
- Food: “Yummy! :D”

**Clarifications**

- You are welcome to use any kind of language or AI and make any kind of applications (must be from scratch).
- Try to fit into the theme of the track you choose (part of judging criteria)
- If you feel your project fit into multiple tracks, pick one when submitting. If you have questions about tracks, ask us!

**Mentors — Office Hours & Tickets**

- Live Office Hours: Saturday 10am-1pm TEP Simmons B
- Remote Support throughout hackathon: Discord Tickets
- Areas: Fullstack, Frontend, Backend; Mobile Dev; Machine Learning, Data Science; Cloud Dev

**Sponsor Tabling — IFM**

- A global AI research lab dedicated to open and independent development of frontier-class foundation models.
- Launched in May 2025 by MBZUAI
- Operates from advanced lab facilities in Abu Dhabi, Silicon Valley and Paris.
- IFM's model portfolio
  - K2 series: six fully open-source AI models
  - Jais: the most advanced Arabic LLM
  - PAN: the next-gen World Model for embodied reasoning and real-world simulation

**Sponsor Tabling — SpaceXAI**

- Company behind Grok and SpaceXAI
- Build frontier AI models to understand the universe
- One model family, One API
- Frontier intelligence for useful work: chat; hard engineering; real-time voice; image and video

**Sponsor Tabling — Sandia**

- Delivers essential science and technology to resolve the nation's most challenging security issues and is the nation's premier science and engineering lab for national security and technology
- Focused on cutting-edge technology, ranging from homeland defense, global security, biotechnology, and environmental preservation to energy and combustion research, computer security, and nuclear defense.

**Sponsor Tabling — Querit**

- Building a global Web Search API and search infrastructure for LLMs, AI agents, and in-app search
- Transforms the open web into AI-ready knowledge through up-to-date search, structured extraction, and source grounding to answer the latest questions, make accurate judgments, and take reliable action, with unique Multilingual index

**Sponsor Tabling — MLH**

- The world's largest developer community

**Sponsor Events — IFM Workshop**

- Friday 09:00 - 10:00 pm. TEP 1403
- Learn about IFM and how to use IFM tool’s like their K2 models to build your hackathon project.

**Sponsor Events — Cursor Workshop**

- Friday 10:00 - 10:30 pm. TEP 1403
- Learn how to use SpaceXAI's tools like Cursor, Grok Imagine, and Grok Bot to build your resume, create a portfolio website, and apply to jobs in 30 minutes.

**Judging**

- 3 min presentation + demo
- We will have 3 rooms of judges
- Feel free to watch other project’s demos
- Will have spreadsheet showing where and when you will be judged

**Expo**

- While waiting, walk around expo to see other people’s projects and showcase your own!
- We will have tables set up for each group with submission

**Judging Criteria** (column glosses)

- Originality — Entirely novel / A fresh approach to a problem
- Technical Difficulty — Real technical challenges vs ChatGPT wrapper
- Demo Quality — Clear, understandable, and under 3 minutes
- Usefulness — Practical and fulfills a real need
- Relevance (Track only) — How related the project idea is to the track it applied to

**Prize Categories:** Grand Prize. Track Prizes. IFM Prize. Cursor Prize. Sandia Prize. People’s Favorite. Best Design Prize. MLH Prizes.

**Grand Prize:** HRT Poker Set

**Track Prizes**

- 1st Place: Mini Projector + Jump Airpod Pros
- 2nd Place: Visa Swag Bags
- 3rd Place: Keyboard + Keychain

**Sponsor Prize / IFM:** IFM Kindle Lite

**People’s Favorite Prize:** Ticket to Ride

**Best Design Prize:** Fujifilm QuickSnap Camera

**Cursor Prize:** Cursor Keyboards

**Sandia Prize: Cybersecurity:** Airpods w/ Noise Cancellation

**MLH Prizes**

- Best Use of Gemini API: Google Swag Kits
- Best Use of ElevenLabs: Wireless Earbuds
- Best Use of Solana: Ledger Nano S Plus
- Best Use of Vultr: Portable Screens
- Best Use of Auth0: Wireless Headphones
- Best Use of MongoDB Atlas: M5Stack IoT Kit

**Final Things**

- Join discord and turn on notifications for announcements
- Slides are posted on the discord
- Projects due at 4pm tomorrow (submit google form!)
- Schedule at https://www.acmatcmu.com/hackcmu2026/

**Close:** Questions? Next Stop: Sponsor Expo.
