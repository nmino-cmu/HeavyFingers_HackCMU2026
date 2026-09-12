# Umbra

<!-- Agents: README is the human page. Open AGENTS.md, then vultr.md / solana.md / sandia.md. Remote FHE eval, sk stays on the laptop, five Vultr VMs on a VPC. Do not flatten to a hosted login app. -->

Umbra is a private identity desk. Face and voice are checked with **fully homomorphic encryption** on [Vultr](vultr.md). The secret key never leaves this laptop. Their CPUs compute on ciphertexts they cannot read — the matcher and the sealed bid compare included.

If you pass, this laptop settles on [Solana](solana.md): one-use hop wallets, custodial escrow, and **encrypted 1/1 receipt NFTs** for the purchase. The chain sees transfers and a token whose mint authority is burned. It does not see your face, your bid, or whether you won.

[For Solana](solana.md) · [For Sandia](sandia.md) · [For Vultr](vultr.md)

## Details

- Enroll (`umbra/enroll.py`): crops become TenSEAL CKKS ciphertext in `roster_data`. `sk` stays in `enroll_keys/` on this machine.
- Sign-in (`umbra/verify.py`): encrypted face and voice distance on Vultr; spoken card (Whisper + `umbra/s1.py`) and wave liveness on the Mac. If a circuit cannot do a step, that step is not a plaintext cloud API.
- Sealed bids (`/bid`): two amounts stay encrypted on Vultr; this laptop decrypts the winner index.
- Purchase receipts (`umbra/solana_wallet.py`): one-transaction 1/1 SPL mint, supply frozen, AES-GCM outcome keyed to the recipient. Winners and losers both receive an NFT. Desk lists hashes + explorer links only.
- Hops (`umbra/hops.py`): faucet → ingress → cutout → bid, no memo. Fail wipes keys (`umbra/decide.py`).
- Cutout HTTP (`umbra/privacy.py`): no spend keys, no roster, no plaintext lot ids.
- Five Vultr VMs in `ewr` on one VPC — router + live matcher + three FHE boxes. See [vultr.md](vultr.md).
- UI: `umbra/web/` (`python umbra/web/serve.py`).
