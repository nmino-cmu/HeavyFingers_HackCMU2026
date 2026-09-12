# P5 OpenFHE XOR

Sol (`codex exec -m gpt-5.6-sol`) hit ChatGPT usage limit 2026-09-12 09:26 ET (`try again at 11:12 AM`). No Cursor OpenAI fallback.

Mechanical:

- `umbra/worker/print_openfhe.py` has no `Decrypt`, `secretKey`, `PrivateKey`, `print_xyt`.
- POST path: reject plaintext `.xyt` / json; two-key token mismatch → 422; else `EvalSub` + serialize.
- `Decrypt` lives only in `umbra/print_openfhe_client.py`.
- Deploy tree `/opt/umbra/print-openfhe` has protocol + worker + `pinky.ct` (787425 B). No `client.zip` / `*.sk`.
- Eval host: farm-a VPC `:8092`. Not a Mac-local eval.

Sol verdict: unavailable (usage limit).
