# P4-DONE

Public card + Mac Whisper S1 + local `decide()` AND + S19 abort. No Solana. No wallets. Orch `app.py` not edited (nonce POST already 4xx via worker `unpack_request`).

| Row | EVAL_HOST | Notes |
|---|---|---|
| S1 | mac | Whisper `tiny.en` + exact-order `s1(transcript, nonce)` |
| S19 | mac | FHE bit ≠ local predicate → abort, empty keydir, `rpc=0` |
| S5 (consumed) | vultr | P2 TinyS5 bit0 at `UMBRA_WORKER_URL=http://207.246.126.149:8080` |

Missing P3 bits (S2/S3/S4 and unset choreo) omitted from AND. Do not block.

## Tests

```
source ~/.umbra-vultr.env
PYTHONPATH=. UMBRA_EVAL_HOST=vultr \
  /Users/nicholasmino/ProgrammingFiles/HackCMU/.venv-umbra/bin/python umbra/test_s1_s19.py
```

`CHECKS_RUN=43` exit 0.

Priors (same env, `UMBRA_SKIP_FLIPS=1`): `test_vpc.py` CHECKS_RUN=10; `test_fhe_roundtrip.py` CHECKS_RUN=19 EVAL_HOST=vultr; `test_harness_negative.py` CHECKS_RUN=6.

`test_sk_absent.py` failed on `/opt/umbra/build/umbra/artifacts/client.zip` (P3 compile tree). Not removed — P3 still running; live `:8086` / `umbra-choreo` not touched.

## XOR

Codex Sol `gpt-5.6-sol` read-only: `umbra/audits/P4-xor.md` **VERDICT: PASS**. Worker does not see the nonce as a classify. Whisper never on Vultr.

## CLI

`python3 -m umbra.card` prints the public video card.

## Files

`umbra/s1.py` `umbra/decide.py` `umbra/card.py` `umbra/test_s1_s19.py`
