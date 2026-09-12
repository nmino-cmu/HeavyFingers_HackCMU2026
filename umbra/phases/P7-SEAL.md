# P7-SEAL (farm-a)

RESULT=VULTR_SEAL
EVAL_HOST=vultr
eval_host_machine_id=4a7203905c954d08b526760b99c9b441
MAC holds sk.

- **SEAL found:** yes. Microsoft SEAL 3.6.6 from CryptoFace `seal-modified-3.6.6`, `cmake --install` → `/usr/local/lib/cmake/SEAL-3.6/SEALConfig.cmake` + `libseal-3.6.a`. Prior fail was `find_package(SEAL)` with no config file.
- **CryptoFace built:** yes. `cmake -S cnn_ckks -B build` sees `SEAL 3.6.6` / `SEAL::seal`. Binary `/opt/umbra/p7-seal/CryptoFace/cnn_ckks/build/cnn`.
- **CryptoFaceNet4 eval:** not run. `patchcnn` does `KeyGenerator` + `Decryptor` on the host (`infer_seal.cpp`), needs Drive CKKS weights, `logN=16`, paper RAM ~269G. Farm-a is 16 GB. Would put sk on the VM.
- **Eval that landed:** TenSEAL 0.3.16 CKKS **Conv+square** (deeper than live L2). 16×16, one 3×3 `conv2d_im2col`, square, encrypted L2 of features. Mac encrypts / decrypts. Worker never `.decrypt`.
- Bind **10.20.0.4:8094** VPC only. Public `:8094` closed. Did **not** bind farm-fast `:8084`. Live TenSEAL L2 on `10.20.0.6:8084` untouched.
- Tunnel eval: A/A l2≈-0.025 bit=1; A/B l2≈43.36 bit=0; plaintext 16×16 → 400; two-key blocked.
- Did not edit `umbra/orch/app.py`. Did not touch `10.20.0.5` / `umbra-choreo`. No docker rm/build/commit. No `*.sk` / `client.zip` on the VM (SEAL source `secretkey.*` only).
