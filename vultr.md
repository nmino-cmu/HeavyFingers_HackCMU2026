# For Vultr

We use Vultr as the FHE compute plane. The laptop encrypts face, voice, print, and bid values with fully homomorphic encryption (CKKS / TFHE). Vultr evaluates those ciphertexts. The laptop decrypts. Secret keys are not on any instance.

```bash
curl -sS http://207.246.126.149:8080/health
curl -sS -X POST http://207.246.126.149:8080/face -H 'Content-Type: application/json' --data '{}'
curl -sS -X POST https://207.246.126.149.sslip.io/face-web --data-binary 'xxxx'
```

`EVAL_HOST` defaults to `vultr` ([`umbra/eval_host.py`](umbra/eval_host.py)). A row in [`umbra/LEDGER.md`](umbra/LEDGER.md) marked `EVAL_HOST=vultr` ran on this farm, not on the Mac.

Live map: [`umbra/FARM.md`](umbra/FARM.md). Region: `ewr`.

## How many VMs, and why

**Five Cloud Compute instances** on one VPC (`10.20.0.0/24`).

FHE compile and eval need RAM and CPU that a single small droplet does not have. We also would not compile a new circuit on the live matcher — one OOM would take sign-in down. So the farm is split by role: a cheap public router, a frozen live worker, and three larger boxes for the circuits that actually shipped.

| VM | Plan | Public | VPC | Role |
|---|---|---|---|---|
| `umbra-orch` | vc2-1c-1gb | 207.246.126.149 | 10.20.0.3 | Only public entry. Ciphertext router on `:8080`. |
| live P2 | vc2-6c-16gb | 64.176.200.124 | 10.20.0.5 | Frozen TinyS5 + P3 sidecar. Do not compile here. |
| `farm-a` | 16 GB | 207.246.94.252 | 10.20.0.4 | Second-stack probes: OpenFHE print, TenSEAL conv. |
| `farm-fast` | vc2-8c-32gb | 45.32.5.249 | 10.20.0.6 | Print, CKKS face, sealed bid. |
| `farm-heavy` | vc2-8c-32gb | 104.156.226.53 | 10.20.0.7 | Voice (TinyS2 + Conv1d). |

An earlier 1 GB worker was left locked after a failed resize. It is not in the path.

## What each VM runs

### 1. Orchestrator — public IPv4, 1 GB

[`umbra/orch/app.py`](umbra/orch/app.py) listens on `0.0.0.0:8080`. It does not decrypt. It rejects JSON, `text/*`, `/s1`, and `/nonce` with 400, then POSTs the raw body to a worker on the VPC.

Client URL: `http://207.246.126.149:8080` (`UMBRA_WORKER_URL`).

| Public path | Forwards to | Worker code |
|---|---|---|
| `/eval` | 10.20.0.5:8086 (live TinyS5; code default `:8081` is the old stub) | [`umbra/worker/choreo_server.py`](umbra/worker/choreo_server.py) |
| `/eval3` | 10.20.0.5:8087 | same host, P3 sidecar |
| `/print` | 10.20.0.6:8082 | [`umbra/worker/print_server.py`](umbra/worker/print_server.py) |
| `/print-ofhe` | 10.20.0.4:8092 | [`umbra/worker/print_openfhe.py`](umbra/worker/print_openfhe.py) |
| `/audio` | 10.20.0.7:8083 | [`umbra/worker/audio_server.py`](umbra/worker/audio_server.py) |
| `/audio-cnn` | 10.20.0.7:8093 | same host, Conv1d circuit |
| `/face` | 10.20.0.6:8084 | [`umbra/worker/face_server.py`](umbra/worker/face_server.py) |
| `/face-conv` | 10.20.0.4:8094 | [`umbra/worker/face_seal_server.py`](umbra/worker/face_seal_server.py) |
| `/bid` | 10.20.0.6:8085 | [`umbra/worker/bid_server.py`](umbra/worker/bid_server.py) |

Wire format: evaluation keys + ciphertext ([`umbra/protocol.py`](umbra/protocol.py)).

### 2. Live P2 — 16 GB, left alone

TinyS5 Concrete-ML on `:8086` and the P3 choreography sidecar on `:8087`. This is the original matcher. Later circuits were compiled on `farm-*` so this box could keep serving.

### 3. farm-fast — 8 vCPU / 32 GB

The main FHE box for sign-in and settlement:

- **Print** — Concrete-ML TFHE ([`umbra/worker/print_server.py`](umbra/worker/print_server.py)).
- **Face** — TenSEAL CKKS. [`eval_l2_ciphertext`](umbra/face_ckks.py) loads a public context from the evaluation key, errors if a secret key is present, subtracts the two sealed templates, returns sealed squared error. The laptop decrypts and sums ([`umbra/verify.py`](umbra/verify.py)). JPEG/PNG/JSON are 400 ([`looks_like_plaintext_face`](umbra/face_ckks.py)).
- **Sealed bid** — Concrete-ML, `fhe_execution=true` (not the simulator). Two encrypted amounts in; encrypted winner index out ([`umbra/worker/bid_server.py`](umbra/worker/bid_server.py), [`umbra/test_bid.py`](umbra/test_bid.py)). The VM never holds `sk` and never sees the numbers.

### 4. farm-heavy — 8 vCPU / 32 GB

Voice. TinyS2 on `:8083`, Conv1d sidecar on `:8093` ([`umbra/worker/audio_server.py`](umbra/worker/audio_server.py)). Same rule: ciphertext in, ciphertext out.

### 5. farm-a — 16 GB

Where we tried the stacks that did not win the live path: OpenFHE print (`:8092`) and TenSEAL conv+square face (`:8094`). Still on the VPC so a judge can hit them through orch. Live sign-in uses farm-fast `/face` and farm-heavy `/audio`.

## What we used that is specifically Vultr

- **Cloud Compute, sized per role.** 1 GB is enough to route. CKKS and Concrete-ML are not. The 32 GB / 8 vCPU instances are there because FHE eval is the product, not because we needed a web server.
- **Private VPC.** Workers bind `10.20.0.x`. FHE ports are not on the public NIC. Orch is the only public IPv4 the laptop talks to. [`umbra/test_vpc.py`](umbra/test_vpc.py) checks that URL is a public address in **AS20473** (Vultr) and that orch can ping the worker on the VPC.
- **Parallel instances instead of one overloaded droplet.** Live P2 stays up while farm-fast / farm-heavy compile. That is why there are five boxes and not one.
- **CPU eval, not a screenshot of localhost.** Workers report `eval_host: "vultr"`. Tests refuse a laptop playback labeled as remote ([`umbra/eval_host.py`](umbra/eval_host.py), [`umbra/test_sk_absent.py`](umbra/test_sk_absent.py)).

Usual Vultr hackathon use is “our site is on a droplet.” Here the droplets *are* the FHE engine: VPC-isolated, ciphertext-only, and still unable to read a face, a voice, or a bid.

## What is never on a VM

Secret keys, `client.zip`, enroll JPEGs, wavs, hop spend keys, Solana keypairs. [`umbra/test_sk_absent.py`](umbra/test_sk_absent.py) SSHs into the worker and fails if it finds `*.sk` or `client.zip` under `/opt/umbra` or `/tmp`.
