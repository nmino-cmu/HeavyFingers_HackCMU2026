# P2 XOR (Codex Sol)

Runtime path: genuine Concrete `FHEModelServer.run`; client holds `sk` and decrypts; cheat_worker is a negative-test oracle only.

**First verdict: FAIL** — Dockerfile.choreo compile left `client.zip` in the image; no `.dockerignore`; choreo.sh did not wipe stale remote client.zip.

**Patched:** `.dockerignore` excludes artifacts/.env; Dockerfile `rm -f .../client.zip` after compile; choreo.sh `rm` remote client.zip/*.sk before copy. Live worker `test_sk_absent.py` CHECKS_RUN=4 (no client.zip on worker).

VERDICT after patch: address the FAIL; live eval already had no sk on worker.
