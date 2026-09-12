# For Sandia

Sandia National Laboratories’ cybersecurity prize. No Sandia SDK. The artifact is a **compromised-cloud** design that still functions.

## Threat

Treat the remote host as already lost: disk image, process memory, packet capture, operator. The attacker gets every byte Vultr received. They must still be unable to recover a face, a voice, a bid amount, or the FHE secret key.

That is a harder claim than “HTTPS + hash the embedding.” The server is *supposed* to compute. It is not supposed to understand.

## What holds under that threat

- **FHE is the trust boundary.** Face, voice, print, and bid-compare run as lattice evaluation on Vultr. The worker is given evaluation keys only. A secret key on the wire is rejected. Farm tests fail on `*.sk` / `client.zip`.
- **Ciphertext-only ingress.** The public orchestrator 400s JSON, text, `/s1`, `/nonce`. The face worker 400s images. The bid worker 400s raw integers. There is no “plaintext fallback” path labeled as FHE.
- **No theater.** Steps lattices cannot evaluate (open-vocab ASR, oval lock) stay on the Mac. We did not upload a wav and call it encrypted.
- **Fail closed before money.** `umbra/decide.py` ANDs the encrypted bits with the local word check. Mismatch aborts. Fail wipes hop keys. No hop, no escrow release, on a failed seal.
- **The ledger is not an identity dump.** No memo. No roster on-chain. Receipt NFTs are 1/1 mints whose purchase outcome is AES-GCM; the chain sees a burned mint authority, not a receipt in the clear. HTTP cutout will not re-emit keys, payer/payee, or ciphertext (`umbra/privacy.py`).

## Stated limit

FHE hides the server from the biometric and the price. It does not certify impersonation resistance. Thresholds are local. Escrow is a key file, not an audited program. The public desk is browser SEAL plus `/face-web`; words/wave lights on that page are local UI. Those are the real edges. Inside them, the cloud that scores you cannot see you.
