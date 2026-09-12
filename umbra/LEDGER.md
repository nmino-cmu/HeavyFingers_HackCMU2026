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
