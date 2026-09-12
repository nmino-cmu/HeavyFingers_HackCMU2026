# Umbra LEDGER

ROW S5 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S6 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S7 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S8 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S9 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S10 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S11 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S12 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S13 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S14 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
ROW S15 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
EVAL_HOST=vultr
MAC_FHE_PROBE=ok

cmd: docker exec umbra-p3 python3 -c "import openfhe"
stderr:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/local/lib/python3.11/site-packages/openfhe/__init__.py", line 1, in <module>
    from .openfhe import *
ModuleNotFoundError: No module named 'openfhe.openfhe'
PyPI openfhe-1.5.1.0.22.4 ships openfhe.cpython-310-x86_64-linux-gnu.so; farm-a image is Python 3.11.
No usable OpenFHE ABI. SEAL not required for S5–S15.
See umbra/audits/P3-openfhe.md

Notes:
- P2 TinyS5 still on live umbra-choreo 10.20.0.5:8086; public POST /eval
- P3 four Concrete-ML Linear(75,10) (rrp/lrp/rlp/rri) on sidecar 10.20.0.5:8087; public POST /eval3
- Card trailer selects the Linear; not post-decrypt XOR. test_choreo.py CHECKS_RUN=76
- Compile via docker exec in umbra-choreo (same CML image). client.zip wiped on the VM
- OpenFHE try was on farm-a umbra-p3 (not the live eval path)
- orch public :8080 → /eval :8086 and /eval3 :8087
- orch also /print :8082 /audio :8083 /face :8084 /bid :8085 on farm VPC

ROW S4 STACKS_TRIED=openfhe,concrete RESULT=VULTR_CONCRETE
EVAL_HOST=vultr
MAC_FHE_PROBE=ok
cmd: /opt/homebrew/Caskroom/miniforge/base/envs/umbra-p5/bin/python -c "import openfhe"
stderr:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/homebrew/Caskroom/miniforge/base/envs/umbra-p5/lib/python3.11/site-packages/openfhe/__init__.py", line 1, in <module>
    from .openfhe import *
ModuleNotFoundError: No module named 'openfhe.openfhe'
Mac OpenFHE wheel has no native module. Farm-fast OpenFHE EvalSub serialize was a try, not the shipped path.
Shipped: Concrete TFHE print on 10.20.0.6:8082. test_print.py CHECKS_RUN=24 EVAL_HOST=vultr (orchestrator re-run).

ROW S4 STACKS_TRIED=openfhe,concrete RESULT=VULTR_OPENFHE
EVAL_HOST=vultr
MAC_FHE_PROBE=fail
farm-a host Python 3.10.12 `import openfhe` OK. Worker EvalSub on $UMBRA_FHE_VPC_IP:8092.
test_print_openfhe.py CHECKS_RUN=9. See umbra/phases/P5-OPENFHE.md (does not replace P5-DONE Concrete :8082).
XOR Sol usage-limited; mechanical note umbra/audits/P5-openfhe-xor.md.

ROW S2 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
EVAL_HOST=vultr
MAC_FHE_PROBE=ok
cmd: /opt/umbra/venv311/bin/python -c "import openfhe"
stderr:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/opt/umbra/venv311/lib/python3.11/site-packages/openfhe/__init__.py", line 1, in <module>
    from .openfhe import *
ModuleNotFoundError: No module named 'openfhe.openfhe'
PyPI openfhe wheel is CPython 3.10 on farm-heavy 3.11. Shipped path is TinyS2 Concrete-ML 10.20.0.7:8083.
test_voice.py CHECKS_RUN=42 (2026-09-12 orchestrator re-run).

ROW S2 STACKS_TRIED=concrete:conv1d,openfhe RESULT=VULTR_CONCRETE
EVAL_HOST=vultr
ARCH=conv1d
TinyS2 stays on :8083. CNN sidecar 10.20.0.7:8093 orch /audio-cnn. Orchestrator re-run A=1 B=0 via farm-heavy curl. client.zip Mac only.
OpenFHE still no 3.11 module. n_bits=8 Conv1d/MLP2/Conv2d 8×8 failed (see P6-CNN.md).

ROW S3 STACKS_TRIED=cryptoface,tenseal,concrete RESULT=VULTR_SEAL
EVAL_HOST=vultr
MAC_FHE_PROBE=ok
cmd: cmake -S cnn_ckks -B build
stderr:
CMake Error at CMakeLists.txt:8 (find_package):
  Could not find a package configuration file provided by "SEAL"
  (SEALConfig.cmake). CryptoFaceNet4 not shipped.
TenSEAL CKKS L2 on farm-fast 10.20.0.6:8084. test_face.py CHECKS_RUN=26 machine-id 7b4c001601ba4fbaa4aa2b236a1d0f23.

ROW S24 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE
EVAL_HOST=vultr
MAC_FHE_PROBE=ok
cmd: python3 -c "import openfhe"
stderr:
ModuleNotFoundError: No module named 'openfhe'
farm-a host before pip. Shipped path: Tiny Linear(2,2) Concrete-ML on farm-fast 10.20.0.6:8085.
test_bid.py CHECKS_RUN=23 (2026-09-12 orchestrator re-run).
