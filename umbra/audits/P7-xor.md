# P7 XOR (Codex Sol)

Runtime: worker `eval_l2_ciphertext` on public CKKS context only; `sk` on Mac; plaintext 64×64 rejected.

Codex `gpt-5.6-sol` 2026-09-12:

- Narrow XOR privacy gate passes: the worker does not decrypt or plaintext-classify biometrics.
- The server rejects plaintext-looking payloads, then only unpacks blobs and invokes encrypted evaluation.
- Evaluation rejects contexts containing a secret key and homomorphically computes `(template−probe)²`.
- Decryption, summation, and thresholding occur only in client/test code; the server never calls them.
- Caveat: encrypted L2, not CryptoFaceNet4. Two-key test was patched after this audit (no longer swallows its own AssertionError).

VERDICT: PASS
