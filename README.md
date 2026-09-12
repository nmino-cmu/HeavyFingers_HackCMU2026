# Umbra

Umbra is a private identity desk. Face and voice are checked with **fully homomorphic encryption** on [Vultr](vultr.md). The secret key never leaves this laptop. Their CPUs compute on ciphertexts they cannot read — the matcher and the sealed bid compare included.

If you pass, this laptop settles on [Solana](solana.md): one-use hop wallets, custodial escrow, and **encrypted 1/1 receipt NFTs** for the purchase. The chain sees transfers and a token whose mint authority is burned. It does not see your face, your bid, or whether you won.

[For Vultr](vultr.md) · [For Solana](solana.md) · [For Sandia](sandia.md)

## Live farm

The matcher is on the VPC, not in this repo’s screenshots.

```bash
curl -sS http://207.246.126.149:8080/health
# {"role":"orch","hostname":"umbra-orch",...}

curl -sS -X POST http://207.246.126.149:8080/face \
  -H 'Content-Type: application/json' --data '{}'
# plaintext rejected

curl -sS -X POST https://207.246.126.149.sslip.io/face-web \
  --data-binary 'xxxx'
# Offset is outside the bounds of the DataView
```

A JSON face upload is refused. A short binary body hits a CKKS unpacker, not an HTML app. Desk: [nickmino.com/hackCMU2026](https://nickmino.com/hackCMU2026/). Receipt mint (devnet, supply 1, authority burned): [explorer](https://explorer.solana.com/tx/286JqM8pMwXdavrPdU3WaDQUxUfULCQJGFnmsvdNTJPavpF6ZHdQxQC4uVbUQfPgQzXw4eX5esHRp314QU8zDJxd?cluster=devnet).

## Details

- Enroll (`umbra/enroll.py`): crops become TenSEAL CKKS ciphertext in `roster_data`. `sk` stays in `enroll_keys/` on this machine.
- Sign-in (`umbra/verify.py`): encrypted face and voice distance on Vultr; spoken card (Whisper + `umbra/s1.py`) and wave liveness on the Mac. If a circuit cannot do a step, that step is not a plaintext cloud API.
- Sealed bids (`/bid`): two amounts stay encrypted on Vultr; this laptop decrypts the winner index.
- Purchase receipts (`umbra/solana_wallet.py`): one-transaction 1/1 SPL mint, supply frozen, AES-GCM outcome keyed to the recipient. Winners and losers both receive an NFT. Desk lists hashes + explorer links only.
- Hops (`umbra/hops.py`): faucet → ingress → cutout → bid, no memo. Fail wipes keys (`umbra/decide.py`).
- Cutout HTTP (`umbra/privacy.py`): no spend keys, no roster, no plaintext lot ids.
- Five Vultr VMs in `ewr` on one VPC — router + live matcher + three FHE boxes. See [vultr.md](vultr.md).
- UI: `umbra/web/` (`python umbra/web/serve.py`).
