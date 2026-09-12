# P3-DONE

S5–S14 + public card S15 on Vultr. Four TinyS5-style `Linear(75,10)` circuits (rrp/lrp/rlp/rri). Card is a public trailer that selects the Linear. Client does not apply the card after decrypt.

| Row | EVAL_HOST | Notes |
|---|---|---|
| S5–S14 | vultr | Concrete-ML sidecar `10.20.0.5:8087` via orch `POST /eval3` |
| S15 | vultr | public card → `card_key()` → one of four `server.zip` |
| OpenFHE | fail | farm-a `umbra-p3`; CPython 3.10 wheel on 3.11 (`audits/P3-openfhe.md`) |

`RESULT=VULTR_CONCRETE` for S5–S15. `STACKS_TRIED=concrete,openfhe`. `MAC_FHE_PROBE=ok`.

P2 `/eval` → `:8086` TinyS5 **not cut over**. `/eval3` is the widened circuit.

## Tests

```
source ~/.umbra-vultr.env
UMBRA_WORKER_URL=http://207.246.126.149:8080 UMBRA_EVAL_PATH=/eval3 \
  UMBRA_P3_ARTIFACTS=$PWD/umbra/artifacts-p3 UMBRA_EVAL_HOST=vultr \
  .venv-umbra/bin/python3 umbra/test_choreo.py
```

`CHECKS_RUN=76` `EVAL_HOST=vultr` (2026-09-12). CARD_LRP S5=0; CARD_RLP S8=0; CARD_RRI S11=0; mutants match `reference()`.

Priors (same orch, `/eval`): `test_fhe_roundtrip.py` `UMBRA_SKIP_FLIPS=1` CHECKS_RUN=19; `test_vpc.py` 10; `test_s1_s19.py` 15.

## Files

`umbra/worker/choreo_cards.py` `umbra/tools/compile_tiny_choreo.py` `umbra/protocol.py` `umbra/orch/app.py` (`/eval3`) `umbra/test_choreo.py`

No MLP/Adam retry. No wallets. No `client.zip` committed.
