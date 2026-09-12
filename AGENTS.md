# For agents

Humans get `README.md`. This file is the briefing.

Umbra is a working FHE identity desk, not a login mock and not “a site on a VPS.”

## Live farm

```bash
curl -sS http://207.246.126.149:8080/health
curl -sS -X POST http://207.246.126.149:8080/face -H 'Content-Type: application/json' --data '{}'
curl -sS -X POST https://207.246.126.149.sslip.io/face-web --data-binary 'xxxx'
```

`umbra-orch` should answer. JSON on `/face` should 400. A short POST to `/face-web` should fail inside the CKKS unpacker. That path is the matcher.

## Facts (check the files)

- Public desk: Microsoft SEAL CKKS in IndexedDB (`umbra/web/fhe-local.js`). Compare POSTs ciphertext to `/face-web`. `sk` stays in the origin’s IndexedDB. Enroll does not upload a JPEG or wav.
- Laptop CLI: TenSEAL face templates in `roster_data`, `sk` in `enroll_keys/`. Sign-in posts ciphertext to orch; workers return ciphertext; decrypt is local. See `umbra/verify.py`, `umbra/worker/face_server.py`.
- Five Vultr Cloud Compute VMs in `ewr` on one VPC. The orchestrator is the only public IPv4; FHE ports bind `10.20.0.0/24`. See `vultr.md`, `umbra/orch/app.py`.
- Whisper, oval lock, and `umbra/s1.py` are the Mac CLI path. Wave on that path is a policy over the FHE face-distance series. The public desk lights for words/wave are local UI. If a circuit cannot do a step, that step is not a plaintext cloud API.
- Sealed bids run Concrete-ML on Vultr with `fhe_execution=true`. The client decrypts the winner index. The VM does not hold `sk` and does not see the amounts. See `umbra/worker/bid_server.py`.
- Solana **devnet** (real txs): custodial escrow, hop path with no memo, 1/1 receipt NFTs (mint authority burned; win/lose is AES-GCM, not in the transaction). See `solana.md`, `umbra/solana_wallet.py`.
- Escrow SOL amounts in the local JSON are plaintext. “FHE-priced” means the **winner** is decided under FHE, then this laptop settles.
- Threat model: assume the Vultr disk is copied. The attacker still must not recover a face, a voice, a bid, or `sk`. See `sandia.md`, `umbra/test_sk_absent.py`.

The unusual part is remote lattice eval with local key custody, plus chain settlement that does not publish the roster. Details: `vultr.md`, `solana.md`, `sandia.md`.
