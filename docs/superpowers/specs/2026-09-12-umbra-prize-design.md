# Umbra — max-FHE spec

**Working name:** Umbra.

**You implement. This file is the preview.** It wins over `docs/superpowers/plans/2026-09-12-fhe-liveness-auction.md` if they disagree.

**Clock:** Saturday ~2:00am → submit **4:00pm**. Demo **3 minutes.**

**Success:** **Vultr screens**, by running as much **real FHE** on their CPU as physics allows. Poker set is irrelevant.

---

## The law (non-negotiable)

For **every** security control:

1. If a lattice FHE circuit can evaluate it on a ciphertext (even at ~20 min) → **FHE on Vultr.** Client encrypts. Vultr never decrypts. Client decrypts the bit.
2. If FHE cannot do it (open-vocab ASR, raw mp4, raw wav, Secure Enclave export, signing keys) → **local AI / local crypto on the Mac.** Plaintext never goes to Vultr.
3. **Never** a plaintext model on the server “to save time.” If an FHE job is not up yet, that control is **local** or **omitted**. It does not become a cleartext API.

Extractors (Whisper, MediaPipe, mel, minutiae, face align) are **not** security decisions. They are crops. Crops are local because FHE cannot ingest the sensor stream. The **decision** on those crops is FHE whenever a circuit exists.

---

## 0. What you are building

A site asks: *same enrolled human, right now, doing a challenge we just invented?*

Every check that can be a circuit **is** a circuit, on Vultr, on ciphertext. A pass is not an account. It grows a throwaway hop path. The chain cannot walk back to the video. Bid amounts can be compared under FHE so the server never sees prices either.

**Pitch:**

> You stay the same person. Nobody — including the cloud — can tie you to the bid. Every check we can run under lattice FHE, we do. The rest never leaves the laptop. The worker is Vultr.

**Do not say:** unhackable, FHE watched the video, FHE transcribed the sentence, Touch ID.

---

## 1. Prize (where the circuits live)

MLH Best Use of Vultr = **visible private compute**. Max FHE is the Vultr story: many cores, long job, ciphertext in/out, no GPU.

| Prize | Chase |
|---|---|
| **Vultr screens** | Hero. All FHE processes on one fat **CPU** box (16–32 GB+). Dashboard + `htop`. |
| Solana Ledgers | After first FHE job is green: 3 hop txs. |
| Sandia | The table in §4 *is* the threat model. |
| Everything else | Off the critical path. |

Mac M4 48 GB: compile circuits, run extractors, hold `sk`, backup eval if the VM dies. **Demo FHE on Vultr**, not only on the Mac.

---

## 2. Approach

**Max FHE on Vultr (this spec).** Every row in §4 that says FHE is in-scope. Several processes (Concrete ≠ OpenFHE ≠ CryptoFace SEAL). Do not link them.

Not “one tiny circuit and stop.” One circuit is only the **first** job that must be rehearsed so you have a screen-winning proof. Then you add every other FHE row you can compile.

GPU theater: reject. HEAR: reject (wrong labels). Plaintext server models: reject.

---

## 3. Product pieces

**Persistent ID.** Enroll face, voice, each fingertip you might request. Store **only ciphertexts** on Vultr. Auth = FHE match vs those templates + FHE choreography vs a **new** public card.

**Generated video prompt.**

```
say:    <8–12 token nonce>
hand:   left | right
motion: clench_unclench
where:  in_front_of_face
side:   left | right
end:    pinky | index | thumb
```

Example: *“the lazy dog fox am is hack win project asterisk” + right hand clench/unclench in front of the right side of the face + pinky closeup.*

**Untrackable auction.** After AND of all enabled bits: `ingress → cutout → bid` (`settle` if you have time). No reuse, no memo, no user id on chain. Server never sees spend keys.

**Sealed price (FHE).** Encrypt bid amounts; Vultr FHE-argmax; client decrypts win/lose. Server never sees prices.

**“Any website.”** Pitch. Ship one auction page. Optional dummy `<script src="/umbra.js">`.

---

## 4. Every security control (FHE or local)

Crops (always local, never uploaded as plaintext): Whisper transcript + timestamps; MediaPipe face/hands/world; aligned 64×64 face; 64×64 log-mel; end-crop; `.xyt` minutiae; feature vector `v`; optional AV-sync scalar; person-count.

`v` (encrypted as one blob):

```
handedness_right_frac
openness[32]
iou_hand_face
hand_x_minus_face_cx
speech_mask[32]
end_finger_frac
end_digit_oh[3]
n_faces
n_hands
av_sync          # lip-energy vs speech-energy correlation, if you extract it
order_ok         # speech-active before end-closeup (0/1)
```

| ID | Control | Threat | FHE or local | Circuit / tool |
|---|---|---|---|---|
| S1 | Exact nonce words, in order | wrong phrase, TTS attack without the card | **Local** | Whisper. FHE cannot transcribe a new sentence. |
| S2 | Voice = enrolled | impostor audio | **FHE** | Concrete CNN-S on encrypted log-mel vs enrolled |
| S3 | Face = enrolled | photo / other person | **FHE** | CryptoFaceNet4 on encrypted 64×64 (~15–25 min). Start before the talk. |
| S4 | Print = enrolled digit | stolen still / wrong finger | **FHE** | OpenFHE `.xyt` vs `ct_print_tmpl[card.end]` |
| S5 | Hand laterality matches card | left/right swap, mirror cheat | **FHE** | Concrete/OpenFHE predicate on encrypted handedness |
| S6 | Clench **and** unclench | frozen fist, still image | **FHE** | peaks/troughs on encrypted `openness[32]` |
| S7 | Hand in front of face | hand at chest / off-screen | **FHE** | IoU / z on encrypted boxes |
| S8 | Face **side** matches card | wrong side | **FHE** | sign of encrypted `hand_x - face_cx` (selfie-aware) |
| S9 | Motion **while** speaking | do motion, then talk | **FHE** | Jaccard of encrypted speech_mask × motion_mask |
| S10 | Ends on a closeup | no zoom | **FHE** | `end_finger_frac` > θ |
| S11 | Closeup digit matches card | thumb instead of pinky | **FHE** | Concrete 5-way on encrypted end-crop, or digit one-hot in `v` |
| S12 | Temporal order (talk/motion before end) | reverse clip | **FHE** | encrypted `order_ok` |
| S13 | One face, expected hands | second person in frame | **FHE** | thresholds on encrypted `n_faces`, `n_hands` |
| S14 | AV sync (mouth vs audio) | dubbed video | **FHE** if you emit a scalar; else **local** | encrypt `av_sync` > θ |
| S15 | Bind bits to **this** card | replay last night’s ciphertext | **FHE** | circuit takes public card constants; bits are “matches **this** laterality/digit” |
| S16 | Templates only as ciphertext | stolen DB is usable biometrics | **FHE at rest** | no plaintext templates on disk |
| S17 | Client-only `sk` | Vultr decrypts you | **Local** | keygen/encrypt/decrypt on Mac |
| S18 | Eval keys only on worker | client can be impersonated as server | **Local policy** | `evk` on Vultr, `sk` never uploaded |
| S19 | Cross-check FHE bit vs local extract | malicious VM flips a bit | **Local** | if local predicate ≠ decrypted bit → **abort, do not bid** |
| S20 | No plaintext fallback on server | “just this once” leak | **Policy** | fail closed |
| S21 | Fresh hop keys per pass | standing wallet = identity | **Local** | new keypairs; wipe after |
| S22 | Hop path, no memo, no reuse | graph “this user” | **Local** (chain) | `ingress → cutout → bid` [→ `settle`] |
| S23 | Server cannot sign | stolen VM drains funds | **Local** | no spend key on Vultr |
| S24 | Sealed bid amount | server sees price | **FHE** | encrypt amount; FHE argmax / compare |
| S25 | Bid addr ≠ faucet addr | trivial link | **Local** | `settle` or at least 3 hops |
| S26 | Pass does not include a biometric hash on chain | join face↔tx | **Local** | no commitment to face/mel on-chain |
| S27 | Challenge is public, biometrics are not | — | split | card in the clear; tensors encrypted |
| S28 | Recapture / screen-in-screen | phone pointed at a laptop | **Local** | optional; no good FHE screen-detect. Skip if weak. |
| S29 | Touch ID / Secure Enclave | — | **Impossible** | cannot export. Camera pinky only. |
| S30 | Encrypted mp4 / wav nets | “FHE watched the take” | **Impossible** | do not schedule |
| S31 | TLS to Vultr | in-flight | **Local** (TLS) | still encrypt payloads; TLS is extra |
| S32 | Rate-limit / one in-flight pass | grind enroll | **Local** | orchestrator metadata only (no biometrics) |

**Pass** = AND of every **enabled** FHE bit plus S1 and S19. Disable a row only if that circuit is not compiled. Do not replace it with a server-side clear model.

**Impossible (keep off the board):** FHE Whisper; FHE on raw video/wav; HEAR as this choreography; MCC-FHE prints (~3 h); Apple fingerprint; one process for all schemes.

---

## 5. Vultr processes (max FHE = several jobs)

One Ubuntu **CPU** box. Four runtimes, four containers. Orchestrator is a blob router. **No decrypt.**

```
/opt/umbra/
  face/     CryptoFace SEAL 3.6.6     S3
  audio/    Concrete-ML               S2, S11
  choreo/   Concrete or OpenFHE       S5–S10, S12–S15, S14
  print/    OpenFHE                   S4
  bid/      Concrete or OpenFHE       S24
  orch/     FastAPI                   routes blobs, CPU logs
```

Start **S3** before the 3-minute talk. Live shot can be choreo + print + `htop`.

---

## 6. Decision audit

| Decision | Call | Why |
|---|---|---|
| How much FHE | **Every possible control** | You asked. Physics is the only off-ramp |
| Where | **Vultr CPU** | Screens + honest-but-curious cloud |
| Words (S1) | Local Whisper | Only forced local *decision* |
| Face (S3) | **In.** CryptoFace | FHE face net is possible; 20 min is allowed |
| Voice (S2) | **In.** Encrypted mel CNN | Not raw wav |
| Print (S4) | **In.** Encrypted `.xyt` | Not Touch ID, not MCC-3h |
| Choreography | **In.** Encrypted `v` | Not HEAR, not encrypted mp4 |
| Sealed price (S24) | **In** | FHE can compare numbers |
| Wallets | Local hops | Signing is not an FHE circuit |
| S19 abort | **In** | Stops a lying VM |
| “Unhackable” | Banned | Stolen `sk` still wins |
| Track | Multiplayer | Two bidders |
| GPU | No | Wrong stack |
| Auth0 / Atlas / Gemini | Out | Fight the story |

---

## 7. Track + 50 words

**Track: Multiplayer**

> Umbra is a sealed two-sided room: several people bid on one lot, but each must first prove they are a live human without revealing who. The pass is shared state (who may sit at the table); the wallets are not. That is the multiplayer contract — a table you can enter only as a person, never as a trackable name.

---

## 8. Three-minute script

| T | Shot | Words |
|---|---|---|
| 0:00–0:20 | Prompt | “New sentence, new motion.” |
| 0:20–0:50 | Take / extract | “Crops on the laptop. Decisions on ciphertext.” |
| 0:50–1:40 | **Vultr** `htop` + several job logs | “Lattice FHE. Face, voice, print, motion, price. They never open the data.” |
| 1:40–2:10 | Decrypt lights | “AND. Words were local — FHE cannot transcribe.” |
| 2:10–2:50 | Explorer hops | “Pass grows a path. Not an account.” |
| 2:50–3:00 | Out | “Worker is a CPU. Today, Vultr.” |

Never cut the Vultr pane. Pre-start CryptoFace.

---

## 9. Threat model (short)

- Vultr: ciphertexts + `evk`, not `sk`. Cannot read templates or `v`. Can lie → S19 abort.
- Chain: hops, no name, no biometric hash.
- Replay/deepfake: new nonce + new laterality + FHE identity.
- Stolen laptop: they are you. Say that.
- Second person in frame: S13.

---

## 10. What you run

**Vultr:** MLH $100 code. High-CPU Ubuntu, no GPU. All containers above. Panel open.

**Mac:** ARM Python 3.11/3.12, Concrete-ML, MediaPipe, Whisper, CryptoFace build if it compiles, OpenFHE client, Solana web3. `sk` never uploaded.

**Solana:** devnet, hop keypairs, faucet, explorer links.

---

## 11. Build order (max FHE; first green job still saves the screens)

1. Vultr VM + `htop`.
2. Toy encrypt → Vultr eval → Mac decrypt. **Prize floor.**
3. Choreo circuit on real `v` (S5–S10, S12–S15).
4. Card + prompt + Whisper (S1) + S19.
5. OpenFHE print (S4).
6. Concrete speaker (S2).
7. Concrete digit (S11) / AV scalar (S14).
8. CryptoFace (S3).
9. FHE bid compare (S24).
10. Hops S21–S23, S25–S26.
11. Auction UI.

If step 2 is dead at **noon**, you have no Vultr prize. Keep adding §4 rows after 2 is green. Do not skip to wallets before 3.

---

## 12. Claims

**True if the FHE rows you shipped actually ran on Vultr**

- Persistent ID without a readable biometric DB.
- Those identity/liveness/price checks were lattice FHE.
- Words were local.
- Bid path is not the biometric id.
- Vultr did the private compute.

**False anyway**

- Unhackable / FHE saw the mp4 or the sentence / Touch ID / every website / the VM cannot lie (S19 exists because it can).

---

## 13. Score if max-FHE rows that compile are on Vultr

| Axis | /10 |
|---|---|
| **Vultr / screens** | **8–9** (more real jobs = better `htop`, until the demo overruns 3 min) |
| Technical difficulty | **9** |
| Originality | 7 |
| Demo | 6–7 (pre-start S3; show 2–3 logs, not twelve) |
| Usefulness / track | 4 — ignore |

Demo discipline: **many jobs in the background, two on camera.** That is still max FHE.

---

## 14. Name / form

- **Umbra** — Persistent person. Unlinkable bid. Every possible check is lattice FHE on Vultr.
- Track Multiplayer + §7.
- Tags: Vultr. Solana if hops shipped.
