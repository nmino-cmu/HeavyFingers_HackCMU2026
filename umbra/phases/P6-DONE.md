# P6-DONE

- `EVAL_HOST=vultr` S2 on farm-heavy Concrete-ML (`ROW S2 STACKS_TRIED=concrete,openfhe RESULT=VULTR_CONCRETE`)
- `MAC_FHE_PROBE=ok` TinyS2 encrypt→eval→decrypt on Mac (A=1, B=0). OpenFHE Mac/3.11: no native module
- Bind `10.20.0.7:8083` VPC only (public :8083 closed). Host `venv311`, no docker build/commit
- Tests: `test_voice.py` CHECKS_RUN=42. Enrolled A→1; mel_B vs A→0; float32 64×64 and RIFF wav → 4xx; two-key cts differ; no `*.pt`/`*.onnx`/`client.zip`/`*.sk` under artifacts-voice/build
- Raw wav never uploaded. Mel 64×64 computed on the Mac; wire is encrypted 16-D band means
- **S11 / S14 live in P3 choreo** — not duplicated here. Fixture-only: `V_INDEX` S11=0, `V_DUB` S14=0
- No fat CNN. TinyS2 Linear(16,1). Orch `POST /audio` not wired (do not edit `umbra/orch/app.py` in this farm Task)
- Did not touch live `10.20.0.5` / `umbra-choreo`. Did not use farm-a `10.20.0.4`
- XOR: Codex Sol PASS (`umbra/audits/P6-xor.md`) — worker does not decrypt or classify plaintext mel/wav/sk
