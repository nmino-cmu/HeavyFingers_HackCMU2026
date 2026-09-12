# P2-DONE

- `EVAL_HOST=vultr` S5 on umbra-worker Concrete-ML (`ROW S5 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE`)
- OpenFHE: `import openfhe` ModuleNotFoundError in the worker image (stderr in LEDGER)
- Tests: `test_vpc.py` CHECKS_RUN=10; `test_sk_absent.py` CHECKS_RUN=4; `test_fhe_roundtrip.py` CHECKS_RUN=20; `test_harness_negative.py` CHECKS_RUN=6
- `UMBRA_WORKER_URL=http://207.246.126.149:8080` (Vultr ASN); FHE bind `10.20.0.5:8086` (tiny S5); old stub/128-net still on :8081 unused
- Public worker :8081 closed from Mac; two-key / evk mismatch / cheat_worker fail decrypt
- V_OK → REF_OK; V_LEFT bit0=0
- No wallets
- XOR: first FAIL (client.zip in Dockerfile image); patched `.dockerignore` + `rm client.zip` after compile; live worker had no sk (`test_sk_absent`)

