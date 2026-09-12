# P3 XOR (Codex Sol, 2026-09-12)

`codex exec --ephemeral -s read-only -m gpt-5.6-sol` on choreo_cards / orch / client / protocol.

Worker never decrypts `v`. Orch forwards opaque bytes. Client encrypts `v` and decrypts bits. Public card only selects which Linear. `FHEModelServer.run(ct, evk)` is the worker success path.

```
VERDICT: PASS
```
