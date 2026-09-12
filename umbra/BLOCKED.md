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
