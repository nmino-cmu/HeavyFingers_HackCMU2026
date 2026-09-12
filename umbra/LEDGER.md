# Umbra LEDGER

ROW S5 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
EVAL_HOST=vultr
cmd: docker exec umbra-choreo python3 -c "import openfhe"
stderr:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'openfhe'
No OpenFHE wheel in the Concrete-ML worker image.
SEAL not required for S5.

Notes:
- Concrete-ML 1.7.0 / concrete-python 2.8.1 on umbra-worker (16 GB, 10.20.0.5)
- Circuit: TinyS5 Linear(75,10); bit0 = (v[0] >= 0.5); bits 1-9 constant-1
- 128-wide torch net compiled on worker but V_LEFT bit0 failed after FHE quantize; replaced by TinyS5
- docker build/commit hangs on this host (BuildKit stdin + containerd). Live container + docker exec :8086
- server.zip via_mlir, is_simulated=0, fhe_execution=true
- client.zip on Mac only; worker find has no client.zip / *.sk
- orch public :8080 → VPC 10.20.0.5:8086
