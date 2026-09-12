# P7-DONE

- `EVAL_HOST=vultr` S3 on farm-fast TenSEAL CKKS (`ROW S3 STACKS_TRIED=cryptoface,tenseal,concrete RESULT=VULTR_SEAL`)
- **Not CLEAR.** Encrypted 64×64 L2 on Vultr. Not plaintext ArcFace. Not CryptoFaceNet4 CNN.
- `eval_host_machine_id=7b4c001601ba4fbaa4aa2b236a1d0f23` == `umbra-farm-fast` `/etc/machine-id`
- Bind `10.20.0.6:8084` VPC only. Public `:8084` closed. UFW 22 + `10.20.0.0/24`
- Mac FHE probe: `MAC_FHE_PROBE=ok` (one CKKS encrypt→eval→decrypt, then Vultr)
- CryptoFace: `libseal-3.6.a` built from `seal-modified-3.6.6`; CNN cmake failed (no `SEALConfig.cmake`); no Drive weights; paper RAM ~269G
- Concrete: tiny `add` compiled on farm-fast after first `pkg_resources` miss (stderr in LEDGER)
- Tests: `UMBRA_EVAL_HOST=vultr UMBRA_FACE_URL=http://127.0.0.1:18084` (SSH tunnel) `python umbra/test_face.py` → `CHECKS_RUN=26`
- Two-key; face_B → 0; plaintext 64×64 → 400; `len(r.content)>=1_000_000`
- Did not edit `umbra/orch/app.py`. Did not touch `10.20.0.5` / `umbra-choreo`
- farm-heavy (`10.20.0.7`) left to P6 after they started `:8083`
- XOR Codex Sol: `VERDICT: PASS` (`umbra/audits/P7-xor.md`)
- No `sk` on the face tree. No docker build/commit
