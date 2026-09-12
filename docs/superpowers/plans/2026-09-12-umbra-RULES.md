# Umbra — shared law (every phase Goal)

**This file + the current phase plan are authoritative.** They win over the prize spec, the physics note, and `umbra-fable-goal.md` when those disagree.

Read only: this file, the **one** phase plan you were given, [`docs/superpowers/specs/2026-09-12-umbra-prize-design.md`](../specs/2026-09-12-umbra-prize-design.md) **§4 table and XOR law only**, `umbra/LEDGER.md`, `umbra/GATHERED.md`. Do **not** open the physics note or `umbra-fable-goal.md`.

Stop only at `umbra/phases/P<N>-DONE.md`, `umbra/BLOCKED.md`, `umbra/STOPPED.md`, the user saying pause, or **hard stop**.

**Unbreakable hard stop:** run `python3 umbra/hard_stop.py` before any work. Exit 99 = halt. Fires at **2026-09-12 15:30 America/New_York** or if `umbra/HARD_STOP` exists. After that, no more Tasks, no “one more compile.”

**Builder is `composer-2.5`**, never `*-fast`. **Not** a Fable one-shot. Spawn Fable 5.1 only if lattice compile is stuck (one Task + one retry), then next stack or `LOCAL_*`.

**Now:** verification (same person, live challenge). **Wallets (P9) are last.** Do not start P8 or P9 until P4 is green.

## Topology (keep two VMs)

| Box | Live (2026-09-12 smoke) | Job |
|---|---|---|
| umbra-orch | public `207.246.126.149`, VPC `10.20.0.3` | `orch` only. Public `:8080`. No `sk`. |
| umbra-worker | public `207.246.94.252`, VPC `10.20.0.4` | FHE. Bind **`$UMBRA_FHE_VPC_IP` only**. |

VPC `ba995955-e979-4a6e-bc06-76a100949f34` `10.20.0.0/24` ewr. `UMBRA_WORKER_URL=http://207.246.126.149:8080`. After P0 upgrade, **re-read GATHERED** — VPC IPs may change. Never hardcode `10.20.0.4` in tests; use `$UMBRA_FHE_VPC_IP`.

Do not merge onto one VM.

## Orch routes (extend, do not replace)

One public listener. Later phases **edit** `umbra/orch/app.py` and redeploy orch.

| Path | Upstream |
|---|---|
| `POST /eval` | `http://$UMBRA_FHE_VPC_IP:8081` choreo |
| `POST /print` | `:8082` |
| `POST /audio` | `:8083` |
| `POST /face` | `:8084` |
| `POST /bid` | `:8085` |
| `GET /health` | orch local |

## XOR

Circuit can decide it → try **FHE on umbra-worker** first. Client encrypts. Worker never decrypts. Client decrypts bits. Whisper / raw mp4 / wav / Secure Enclave / spend keys → Mac. **Never** a plaintext classifier on either VM. Crops stay local.

## Multiple FHE stacks (required)

For every FHE row, **try more than one library** before you give up. Do not stop at the first import error.

Order unless the phase says otherwise:

1. **Concrete / Concrete-ML** (`concrete-python`)
2. **OpenFHE**
3. **SEAL / CryptoFace** — required try for S3; optional extra try for other rows if 1–2 died

LEDGER every row:

```
ROW S5 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
```

`RESULT` is one of: `VULTR_CONCRETE` | `VULTR_OPENFHE` | `VULTR_SEAL` | `LOCAL_FHE` | `LOCAL_CLEAR`.

A phase that only ever launches one stack and then omits is **illegal**.

## Local only if FHE absolutely cannot work

Not “slow.” Not “Mac is easier.” Not “no time to wait for compile.”

**Absolutely cannot** for a row means all of:

1. Worker is **≥16 GB** (`free -m`) and reachable. If it is still 1 GB, **upgrade (P0)** — that is not a local-fallback ticket.
2. You tried **at least two** stacks from the list above (S3: CryptoFace/SEAL + one other, or two build attempts).
3. Each try is a real compile or `docker build` on the **worker**. Composer-2.5 first; **one** Fable 5.1 Task + one retry only if that compile is stuck.
4. LEDGER has `cmd:` and ≥5 lines `stderr:` per failed stack.

Then, **on the Mac only**, in this order:

1. **`LOCAL_FHE`** — same circuit, eval on the Mac, `sk` never uploaded. Tests still go through encrypt → (local server) → decrypt. Prefer this.
2. **`LOCAL_CLEAR`** — numpy / local model on the Mac, same `reference()` bits. Last resort so verification still works.

Illegal: plaintext matcher **on umbra-worker**. Illegal: writing `RESULT=VULTR_*` for a local eval. Illegal: skipping the two-stack try.

Phase-DONE must say `EVAL_HOST=vultr` or `EVAL_HOST=mac` per shipped row. Vultr screens need **at least one** verification bit with `EVAL_HOST=vultr`. If P2 is entirely local, say so in DONE — still ship verification, do not pretend it ran on Vultr.

## Mac as Vultr stand-in (infra down)

Separate from “FHE will not compile.” If the **VMs** are dead (API/credit/SSH fail and recreate fails — see below), the Mac may host the HTTP worker so you can keep coding. Same rule: no Vultr-screens claim. When VMs return, re-run every test on `$UMBRA_WORKER_URL`.

Vultr infra is impossible only if you have BLOCKED.md with stderr and:

1. `vultr-cli account info` fails, **or** both GATHERED instance IDs are gone and create fails, **or** SSH to both public IPs fails and create fails.
2. One recreate/upgrade attempt failed.
3. `VULTR_IMPOSSIBLE=1` is in BLOCKED.md.

Illegal: `UMBRA_WORKER_URL=http://127.0.0.1:8080` while the two VMs are up. Illegal: skip-if-no-Vultr. Illegal: default URL to localhost.

## Scope: verification first, wallets last

| Now | Later |
|---|---|
| P0–P4 identity + liveness (card, FHE `v`, Whisper, S19) | P5–P7 more verification if P4 is green |
| | P8 sealed bid amounts (not the wallet) |
| | **P9 hops / crypto wallet — last, required before submit if time** |

Do not implement Solana, keypairs, faucet, or explorer links before P4-DONE. P9 is important; it is not how you start.

## UFW (both VMs, every deploy)

```bash
# orch
ufw allow 22/tcp
ufw allow 8080/tcp
ufw allow from 10.20.0.0/24
ufw --force enable
# worker — no public 8080–8090
ufw allow 22/tcp
ufw allow from 10.20.0.0/24
ufw --force enable
```

## Worker RAM

Smoke worker is **1 GB**. FHE needs **`vc2-6c-16gb`**. If `free -m` Mem < 12000, upgrade or BLOCKED — do not use that as a local-fallback ticket.

## Audits (every phase, new context)

| Step | Who | Fail if |
|---|---|---|
| Tests written | composer-2.5 (never `*-fast`) | mock FHE, skip-if-no-Vultr, localhost while VMs up, one stack only then omit, missing two-key/evk/freshness on a `VULTR_*` row |
| Hard compile | composer-2.5 first; **Fable 5.1 only if stuck** | Fable used for P0/P1/P4/P9 or as the overnight Goal |
| Tests green | **new** composer-2.5 | builder stdout only; `VULTR_*` but host is not orch public IP |
| XOR | `codex exec --ephemeral -s read-only -m gpt-5.6-sol "…" </dev/null` | worker decrypts/classifies plaintext `v`/face/mel/xyt/`sk` |
| Phase DONE | **new** composer-2.5 | `python -O`; LEDGER row with no `STACKS_TRIED`; local eval labeled Vultr |

Verdict = last line only. Save `umbra/audits/`. Builder never self-PASS. No Cursor-hosted OpenAI. No `git commit` unless asked.

## Clocks (unbreakable)

`python3 umbra/hard_stop.py` — exit 99 is **final**. Deadline **15:30 America/New_York 2026-09-12**, or `umbra/HARD_STOP`. If P2 has no working verification at halt → `BLOCKED.md`. If P4 is green before halt, **P9 wallets next**.

Commits: when the user asked to commit/push (this run), commit each phase DONE with a detailed message; never add `umbra/.env`.

## Pitch bans

Do not write: unhackable, FHE watched the video, FHE transcribed the sentence, Touch ID, any website already works. If a row is `LOCAL_*`, do not say it ran on Vultr.

## Fixtures (P2+)

`umbra/fixtures.py` — non-round, greppable. `len(V_OK)==75`.

- `handedness_right_frac=0.9137`
- `openness[32]=0.5+0.45*sin(2*pi*2*t/32)`
- `iou_hand_face=0.4271`
- `hand_x_minus_face_cx=+0.1873`
- `speech_mask[32]=1` for `t in [2,26)`
- `end_finger_frac=0.7319`
- `end_digit_oh=[1,0,0]` (pinky, index, thumb)
- `n_faces=1`; `n_hands=1`; `av_sync=0.6127`; `order_ok=1`
- `CARD_RRP={hand:right, side:right, end:pinky}`; `REF_OK=[1]*10`; `IDX={S5:0,…,S14:9}`
- Mutants of `V_OK`: `V_LEFT=0.0863`, `V_FIST` openness 0.12, `V_ONECYCLE`, `V_RAMP`, `V_FAR` iou 0.0213, `V_WRONGSIDE=-0.1873`, `V_TALKTHENMOVE` speech [0,12) motion [16,32), `V_NOZOOM=0.1187`, `V_INDEX=[0,1,0]`, `V_REVERSE`, `V_TWOFACES`, `V_NOHANDS`, `V_DUB` av_sync 0.0421
