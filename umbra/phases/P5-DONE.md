# P5-DONE

Encrypted .xyt match (S4) on farm-fast Concrete (`10.20.0.6:8082`). Templates at rest are ciphertext. Wrong finger / wrong key → 0.

| Row | EVAL_HOST | Notes |
|---|---|---|
| S4 | vultr | Concrete-FHE print matcher; OpenFHE also tried (see LEDGER) |

`RESULT=VULTR_CONCRETE`. `test_print.py` `CHECKS_RUN=24` `EVAL_HOST=vultr` (2026-09-12 orchestrator re-run, ~351s keygen).

Orch `POST /print` and `POST /enroll` → farm-fast. Did not cut P2 `/eval`.

Farm Task on umbra-p5 reported `CHECKS_RUN=30` (same host). Orchestrator re-run from main was 24 after a long keygen.
