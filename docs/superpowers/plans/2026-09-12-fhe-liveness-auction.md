# FHE liveness auction — generated video-prompt architecture

> **For agentic workers:** implement only after a human says go. Architecture, not a TDD file-edit plan.

**Goal:** A generated video prompt tells you exactly what to say and do. Local models extract crops and landmarks. Every **identity net / matcher / choreography predicate** that can run under FHE does. Vultr never sees plaintext video, audio, or prints. Pass unlocks a shadow wallet.

**Architecture:** One clip. Challenge is a random choreography, not a HEAR class. MediaPipe + Whisper run on-device. Encrypted face crop, mel, minutiae, and a landmark feature vector go to Vultr. Client decrypts bits, ANDs them, bids.

**Tech Stack:** local Whisper · MediaPipe · local LLM (challenge text) · CryptoFace · Concrete-ML · OpenFHE · Solana devnet · Vultr CPU

## Global Constraints

- **XOR law:** each check is **local-AI XOR FHE**. Never plaintext on Vultr. FHE if a circuit can do it, even at ~20 min. Local only for capture, crops FHE cannot ingest, open-vocab ASR, keygen, wallet UX.
- **This challenge is not HEAR.** “Clench/unclench right hand in front of the right side of your face, end on a pinky closeup” is **not** in HEAR’s clap/wave/jump set. Do not force HEAR. Choreography = MediaPipe features ± tiny FHE predicates.
- **The spoken line is open-vocab.** “the lazy dog fox am is hack win project asterisk” is a nonce, not a 12-class bank. **Phrase text = local Whisper.** No FHE Whisper.
- **Pinky closeup is the fingerprint probe.** No Touch ID export. Last frames → minutiae → OpenFHE match. Enroll the same way.
- **Four FHE runtimes, four processes** if you use all of them: CryptoFace SEAL 3.6.6 · Concrete-ML · OpenFHE · (optional extra Concrete circuits). HEAR omitted unless you later add a HEAR-legal action as a bonus check.
- Client holds secret keys. Templates stored only as ciphertexts.
- Face ~20 min allowed. MCC-FHE prints (~192 min) forbidden.

---

## 1. The prompt (what the user sees)

Local model samples a card, then plays a **video prompt** (TTS of the line + stick-figure / overlay of the motion). Example card:

```
say:    "the lazy dog fox am is hack win project asterisk"
hand:   right
motion: clench_unclench
where:  in_front_of_face
side:   right
end:    pinky_closeup
```

Grammar (all fields random per attempt):

| Slot | Values |
|---|---|
| `say` | nonce word-salad from a local LLM or shuffled word list (8–12 tokens) |
| `hand` | left \| right |
| `motion` | clench_unclench (v1; add more later only if you have a detector) |
| `where` | in_front_of_face |
| `side` | left \| right |
| `end` | pinky \| ring \| middle \| index \| thumb closeup |

The card is **public** (anti-replay). The **video and biometrics** are not.

User records one take that must satisfy the whole card, then stop.

---

## 2. Atoms — every part of that example

Local extractors (clear, never uploaded): Whisper transcript, MediaPipe face+hands+world landmarks per frame, log-mel, one unoccluded face 64×64, last-second finger crop → `.xyt`.

Then each atom is local XOR FHE:

| # | What “that video” requires | Extract on device | Verify |
|---|---|---|---|
| 1 | Said **exactly** the nonce words, in order | Whisper | **Local.** String-normalize + match. FHE cannot transcribe this. |
| 2 | Voice is the enrolled person | log-mel 64×64 | **FHE** Concrete CNN-S vs enrolled speakers |
| 3 | Face is the enrolled person | 64×64 from a frame where the hand is **not** covering the face | **FHE** CryptoFaceNet4 (~20 min) |
| 4 | **Right** hand, not left | MediaPipe `handedness` time series | **FHE** threshold on encrypted handedness majority (tiny circuit). Local fallback: `mean(right) > 0.8` |
| 5 | **Clench and unclench** (cycle, not a frozen fist) | per-frame pinch/open: distance thumb–index or fist classifier | **FHE** tiny CNN or polynomial on encrypted openness[T]: ≥2 peaks (open) and ≥2 troughs (closed). Local fallback: same math in numpy |
| 6 | Hand is **in front of the face** | face box, hand box, optional z | **FHE** IoU / z-compare on encrypted boxes. Local fallback: IoU > θ |
| 7 | **Right side** of the face | hand centroid x vs face center x (mirrored for selfie) | **FHE** compare two encrypted scalars. Local fallback: `hand_x > face_cx` |
| 8 | Motion happens **while speaking** | Whisper word timestamps ∪ openness peaks | **FHE** overlap of two encrypted binary masks (speech frame vs motion frame). Local fallback: Jaccard > θ |
| 9 | Clip **ends** on a closeup | last 15–30 frames: finger area / face area | **FHE** ratio > θ. Local fallback: same |
| 10 | Closeup is a **pinky**, not another digit | MediaPipe finger name in those frames, or tiny crop CNN | **FHE** if you compile a 5-way digit CNN on the encrypted end-crop. Local fallback: MediaPipe pinky tip is the largest / nearest landmark |
| 11 | That pinky is **their** print | `.xyt` from the end crop | **FHE** OpenFHE match vs `ct_print_tmpl` |

Identity = {2, 3, 11}. Liveness/choreography = {1, 4, 5, 6, 7, 8, 9, 10}. Replay/deepfake dies because the nonce + laterality + end digit were not known at enroll.

Pass = AND of all enabled atoms. If an FHE job dies, that atom becomes **local** or is dropped. It does **not** become a plaintext server model.

---

## 3. XOR map (updated)

| Computation | Local AI | FHE | Why |
|---|---|---|---|
| Challenge text + video prompt | yes (LLM + TTS + canvas) | no | Not secret |
| Camera / mic | yes | no | Sensors |
| Whisper (nonce phrase) | **yes** | no | Open vocab |
| MediaPipe landmarks / boxes | yes | no | FHE cannot eat the video |
| Face align 64×64 | yes | no | CryptoFace ingest |
| Wav → log-mel | yes | no | Raw-wav FHE is hours/64 ms |
| End crop → `.xyt` | yes | no | Matcher is FHE |
| **Face net** | no | **CryptoFace** | Identity |
| **Speaker net** | no | **Concrete CNN-S** | Identity |
| **Print match** | no | **OpenFHE `.xyt`** | Identity |
| **Handedness / clench / side / IoU / timing / end-zoom** | fallback | **Concrete or OpenFHE predicates on encrypted feature vector `v`** | Most-FHE choreography |
| **Pinky-class net** | fallback | **Concrete 5-way on encrypted end-crop** | Digit check |
| HEAR action net | — | omit | Wrong label set |
| Closed-set phrase CNN | — | omit | Phrase is a nonce |
| Wallet sign | yes | no | Keys stay local |
| Sealed bid argmax | no | optional OpenFHE | Amounts |

`v` is a short clear-then-encrypted vector, e.g.

```
v = {
  handedness_right_frac,   # 1
  openness[0:32],          # resampled
  iou_hand_face,           # 1
  hand_x_minus_face_cx,    # 1  (sign = side)
  speech_mask[0:32],
  end_finger_frac,         # 1
  end_digit_onehot[5]
}
```

One Concrete circuit `choreography(v, challenge_public_params) → bits[4..10]` is enough. Challenge laterality/end-digit are public constants in the circuit (or multiplied in the clear after decrypt — weaker). Prefer: encrypt `v`, FHE-compare to the public card.

---

## 4. Enrollment

On device, then encrypt:

1. Face still, unoccluded → CryptoFace `ct_face_tmpl`
2. Pinky (and optionally each digit you might request at `end`) closeup → `.xyt` → `ct_print_tmpl[digit]`
3. ~10 voice clips, any words → train CNN-S locally → compile FHE. Do not upload wavs.

No phrase bank. No HEAR enroll.

---

## 5. Auth loop

1. Local LLM emits a card. Client plays the video prompt.
2. User records one take.
3. Local: Whisper, MediaPipe, pick face frame, build `v`, build `mel`, build end `.xyt`.
4. Encrypt `{face, mel, xyt, v, end_crop?}`. Upload ciphertexts + the **public card**.
5. Vultr jobs in parallel:

```
F  CryptoFace(ct_face, tmpl)                 ~15–25 min
S  CNN-S(ct_mel)                             minutes
R  OpenFHE(ct_xyt, tmpl[card.end])           seconds–minutes
C  choreography(ct_v, card)                  seconds–minutes
D  optional CNN-digit(ct_end_crop)           minutes
```

6. Client already has Whisper match (atom 1) locally.
7. Decrypt F/S/R/C/D. AND with atom 1.
8. Fresh Solana keypair. Bid.

Start Job F before the 3-minute talk.

---

## 6. Auction

Unchanged: shadow wallet after pass. Optional FHE sealed-price if the biometric path is already green.

---

## 7. Infra

```
/opt/fhe/
  face/     CryptoFace
  audio/    Concrete CNN-S (+ optional digit CNN)
  choreo/   Concrete/OpenFHE predicates on v
  print/    OpenFHE minutiae
  orch/     blob router, no decrypt
```

Client: prompt player, recorder, per-atom traffic lights (local vs FHE labeled), then bid.

---

## 8. Demo line

Play the prompt video. Record the take. Show ciphertext sizes leaving the machine. Lights: phrase (local Whisper), voice (FHE), face (FHE), right-hand clench on the right of the face while speaking (FHE on landmarks), pinky closeup (local digit + FHE print). New wallet bids.

**Say:** “The sentence was new. The choreography was new. The models that identify you and check the motion ran on ciphertext. The words were checked on-device because FHE cannot transcribe.”

**Do not say:** FHE watched the video or understood the sentence.

---

## 9. Build order

1. Card generator + video prompt (text + TTS + stick figure is enough)
2. Local Whisper exact-match
3. MediaPipe atoms 4–10 in numpy (so the demo works even if FHE choreo slips)
4. Encrypt `v` + one Concrete/OpenFHE predicate (start with handedness or side — one compare)
5. OpenFHE pinky `.xyt` self-match
6. Concrete CNN-S
7. CryptoFace fixture
8. Glue one recording through all lights
9. Solana shadow bid
10. Promote remaining numpy atoms into the FHE `choreography` circuit

Kill rule: FHE dies → keep the **local** check. Never stand up a server that sees the video.

---

## 10. Impossible (do not schedule)

- FHE Whisper / encrypted wav → words
- Encrypted raw video → “clench in front of face”
- HEAR as the motion model for this card
- Touch ID as the pinky
- One unified FHE net over the mp4
