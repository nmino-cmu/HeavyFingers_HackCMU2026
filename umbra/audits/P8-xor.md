# P8 XOR (Codex Sol)

Runtime path: Concrete `FHEModelServer.run` on VPC `:8085`; client holds `sk` and decrypts winner index. Worker rejects short/JSON/int64 plaintext with 400. `log_message` is path+status only.

```
No. The client encrypts both amounts and derives the winner index after decrypting the FHE result. The worker only evaluates ciphertext, rejects short/JSON/int64 plaintext with 400, and neither logs request bodies nor emits either amount.

PASS
```
