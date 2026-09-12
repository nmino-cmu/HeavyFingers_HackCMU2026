# BLOCKED

P9 hops implemented (Mac keygen/sign, no memo, no biometric hash on chain, no spend key on Vultr).
**No real devnet txs.** Public faucet refused. Did not fake transactions.

RPC `https://api.devnet.solana.com` health was `ok`. `requestAirdrop` and `solana airdrop` (CLI 4.2.2) both failed.

Also tried: Ankr (needs API key), Triangle faucet (503 suspended), `faucet.solana.com/api/request` (GitHub + captcha), Coinbase CDP (401), `devnet-pow` (crate will not compile on current Rust).

stderr:

```
{"error": {"code": 429, "message": " {\"jsonrpc\":\"2.0\",\"error\":{\"code\": 429,\"message\":\"You've either reached your airdrop limit today or the airdrop faucet has run dry. Please visit https://faucet.solana.com for alternate sources of test SOL\"}, \"id\": 1 } \r\n"}}
---
{"error": {"code": 429, "message": " {\"jsonrpc\":\"2.0\",\"error\":{\"code\": 429,\"message\":\"You've either reached your airdrop limit today or the airdrop faucet has run dry. Please visit https://faucet.solana.com for alternate sources of test SOL\"}, \"id\": 1 } \r\n"}}
---
{"error": {"code": 429, "message": " {\"jsonrpc\":\"2.0\",\"error\":{\"code\": 429,\"message\":\"You've either reached your airdrop limit today or the airdrop faucet has run dry. Please visit https://faucet.solana.com for alternate sources of test SOL\"}, \"id\": 1 } \r\n"}}
---
Requesting airdrop of 1 SOL
Error: airdrop request failed. This can happen when the rate limit is reached.

---
Requesting airdrop of 0.1 SOL
Error: airdrop request failed. This can happen when the rate limit is reached.

---
Requesting airdrop of 0.02 SOL
Error: airdrop request failed. This can happen when the rate limit is reached.
```

Unblock: fund ingress from a working devnet faucet (or wait out the 8h cap), then `python3 umbra/test_hops.py`.

## 2026-09-12 09:25 EDT

Retried for real SOL. Still dry. Did not fake txs. Did not put spend keys on Vultr. Did not edit orch. `test_hops.py` not run.

- RPC `https://api.devnet.solana.com` health still `ok`.
- `requestAirdrop` 1 / 0.1 / 0.02 SOL → 429 faucet dry or daily cap. 0.001 SOL → -32603 Internal error.
- `solana airdrop` CLI 4.2.2 (1 / 0.1 / 0.02) → rate-limit error.
- No repo test keypair and no `~/.config/solana/id.json`; nothing local to use as faucet→ingress.
- Also still refused: Triangle 503 suspended; Ankr needs API key; Coinbase CDP 401; `faucet.solana.com/api/request` Cloudflare 1010 / GitHub+captcha (browser UA → GitHub required); solfaucet `/api/airdrop` 404; Pine Stake and QuickNode faucet APIs 404/403 and their UIs need wallet+GitHub/captcha. DevnetFaucet.org is GitHub-gated.

Unblock unchanged: working captcha-solved faucet or wait out the cap, then `python3 umbra/test_hops.py`.
