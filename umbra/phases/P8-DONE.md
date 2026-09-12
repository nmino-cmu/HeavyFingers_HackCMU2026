# P8-DONE

- `EVAL_HOST=vultr` S24 on farm-fast Concrete-ML (`ROW S24 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE`)
- Mac FHE probe: TinyS5-style Linear(2,2) compile ~2s; enc/eval/decrypt idx 1 then 0; `is_simulated=0` `fhe_execution=true`
- OpenFHE: farm-a host `import openfhe` failed pre-pip (stderr in LEDGER); `pip3 install openfhe` then BFV `EvalSub` probe ok
- Farm-a `10.20.0.4` was P3-busy (pip); shipped `10.20.0.6:8085` (farm-fast). Never live `10.20.0.5`
- Bind VPC only. Tests hop orch → `$UMBRA_FHE_VPC_IP:8085`. Did not edit `umbra/orch/app.py`
- `python3 umbra/test_bid.py` CHECKS_RUN=23: enc pair → idx 1; swapped → 0; two-key; int64 POST 4xx; logs have no sealed amounts; no client.zip/*.sk in deploy tree
- Tie policy: equal amounts → index 0 (first wins). Single-key Concrete caveat in test docstring
- No plaintext prices on the VM. No docker build. No docker commit. No sk
