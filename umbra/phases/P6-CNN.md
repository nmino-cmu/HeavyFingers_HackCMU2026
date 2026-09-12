# P6-CNN

Concrete CNN-S sidecar on farm-heavy. Live TinyS2 left on `:8083`.

```
STACKS_TRIED=concrete:conv1d,openfhe RESULT=VULTR_CONCRETE
EVAL_HOST=vultr
ARCH=conv1d
```

- Circuit: `TinyConv1d` 4-ch `Conv1d(k=3, pad=1)` + `Linear(64,1)` on the existing 16-D band vector (`VEC_A`/`VEC_B`). No Adam / no `Linear(75,128)+ReLU`.
- Compile: `n_bits=5` `rounding_threshold_bits=6` (n_bits=8 hit 17-bit TLU).
- Cleartext A=1 B=0. Farm-heavy `FHE_PROBE=ok bits [1] [0]`.
- Bind `10.20.0.7:8093` via `audio_server.py` + `UMBRA_FHE_ARTIFACTS=/opt/umbra/artifacts-voice-cnn`. Artifacts dir `artifacts-voice-cnn` (not `artifacts-voice`).
- `client.zip` pulled to Mac `umbra/artifacts-voice-cnn/`; wiped on the VM with `*.sk`.
- OpenFHE: `No module named 'openfhe.openfhe'` (3.11 vs cp310 wheel). Same ABI miss as TinyS2.
- First n_bits=8 tries failed: Conv1d 17-bit TLU; MLP2 18-bit TLU; Conv2d 8×8 `NoParametersFound`. Did not need Conv2d 16×16.
- Did not touch live `10.20.0.5`, `orch/app.py`, docker, or `:8083` (`pid 8263`, `server.zip` 1780 B unchanged).
