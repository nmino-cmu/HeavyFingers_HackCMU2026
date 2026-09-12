# P4 tests

`umbra/test_s1_s19.py` (no skip-if-no-Vultr, no localhost worker):

- `s1("The lazy dog fox.", nonce)` True; swap fox/dog False
- `import umbra.s1` in a subprocess: `requests` and `urllib.request` absent
- `decide` all-1 AND S1 pass; any matched 0 fails; FHE≠local abort; abort/fail wipe keydir; `rpc=0`
- missing P3 `None` bits omitted
- `python3 -m umbra.card` prints public say/hand/motion/where/side/end (8–12 word nonce)
- Mac Whisper `tiny.en` on `say` audio; `s1` on the transcript
- POST nonce string to `$UMBRA_WORKER_URL/eval` is 4xx
- live P2 TinyS5 bits AND local `reference()` + S1; flip local → abort

Run: `source ~/.umbra-vultr.env && PYTHONPATH=. .venv-umbra/bin/python umbra/test_s1_s19.py`
