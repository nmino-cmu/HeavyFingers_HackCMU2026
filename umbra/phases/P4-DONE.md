# P4-DONE

- EVAL_HOST=mac for S1 / decide / card (never sent to Vultr)
- `python3 umbra/test_s1_s19.py` CHECKS_RUN=15
- S1 exact-order nonce; capitalize+period True; swap False
- After clean `import umbra.s1`, no `requests` / `urllib.request`
- decide: pass only all-1 AND S1; FHE≠local → abort; abort writes no hop keys
- CLI `python3 -m umbra.card`
- FHE bits still P2 TinyS5 on Vultr (`UMBRA_WORKER_URL=http://207.246.126.149:8080`)
- No Solana
