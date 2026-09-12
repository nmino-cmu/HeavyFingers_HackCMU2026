# P5-OPENFHE

ROW S4 STACKS_TRIED=openfhe,concrete RESULT=VULTR_OPENFHE
EVAL_HOST=vultr
MAC_FHE_PROBE=fail

Host: farm-a `207.246.94.252` VPC `$UMBRA_FHE_VPC_IP=10.20.0.4` Python 3.10.12.
`import openfhe` OK on host and in a throwaway `venv` (`pip install openfhe` → `VENV_IMPORT_OK`). Bind `10.20.0.4:8092` (8081 already taken by existing choreo_server; left running).

Worker `umbra/worker/print_openfhe.py`: Deserialize + `EvalSub` only. No `Decrypt`. Templates at rest are ciphertext (`pinky.ct` 787425 B). Two-key token mismatch → 422. Plaintext `.xyt` → 400.

Client `umbra/print_openfhe_client.py` holds `sk`. Mac has no OpenFHE native module (3.11/ARM wheel). Encrypt/decrypt for `test_print_openfhe.py` ran on farm-a 3.10 then the temp tree was deleted. No `client.zip` / `*.sk` left on the VM.

`test_print_openfhe.py` `CHECKS_RUN=9` `EVAL_HOST=vultr`: same finger → 1; index vs pinky tmpl → 0; two-key → 4xx; plaintext → 4xx. Public `:8092` closed.

Did not overwrite `P5-DONE` Concrete path (`10.20.0.6:8082`). Did not touch live choreo `10.20.0.5` / `:8086` / `:8087`. Did not edit `umbra/orch/app.py`. Did not docker rm/build/commit.
