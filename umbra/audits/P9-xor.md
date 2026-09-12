# P9 XOR (Codex Sol)

First verdict: **FAIL** — `/hop` fabricated `decide([1]*10, …)` so hops could run after an S19 abort.

Patched: `/hop` requires the last `/fixture` `decide()` to be `ok` and not `abort`. `hops.run()` still returns `None` on abort and writes no keys.

Re-run Codex Sol (`gpt-5.6-sol`, ephemeral, read-only): **PASS**

PASS
