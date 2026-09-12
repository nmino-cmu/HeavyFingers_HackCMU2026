# P4 XOR (Codex Sol, 2026-09-12)

`codex exec --ephemeral -s read-only -m gpt-5.6-sol` on s1/decide/card/test_s1_s19 + orch/worker/client.

S1 is a network-free local string match. Whisper is Mac-only in `card.transcribe`. S19 mismatch wipes keydir and returns `rpc=0`. Worker success path is `FHEModelServer.run` on ciphertext. Nonce `/eval` body is 4xx.

Residual (from Sol): protocol helpers not in the read set; orch is a blind proxy; empty bit lists can vacuously pass; nonce has no expiry.

```
VERDICT: PASS
```
