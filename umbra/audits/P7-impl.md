# P7 impl packet (XOR input)

Files:
- `/Users/nicholasmino/ProgrammingFiles/HackCMU/.worktrees/p7/umbra/face_ckks.py`
- `/Users/nicholasmino/ProgrammingFiles/HackCMU/.worktrees/p7/umbra/worker/face_server.py`
- `/Users/nicholasmino/ProgrammingFiles/HackCMU/.worktrees/p7/umbra/test_face.py`
- `/Users/nicholasmino/ProgrammingFiles/HackCMU/.worktrees/p7/umbra/phases/P7-DONE.md`
- `/Users/nicholasmino/ProgrammingFiles/HackCMU/.worktrees/p7/umbra/LEDGER.md`

Worker: TenSEAL `context_from(evk)` with `save_secret_key=False`. Computes encrypted `(tmpl-probe)^2`. No `.decrypt`. No insightface/torch/onnx. Rejects plaintext 64×64. Bind VPC `:8084`.

Client (Mac): holds `sk`, encrypts 64×64, decrypts L2, `bit = L2 < 1`.

Shipped host: `umbra-farm-fast` `10.20.0.6:8084` machine-id `7b4c001601ba4fbaa4aa2b236a1d0f23`. RESULT=`VULTR_SEAL` not `LOCAL_CLEAR`.
