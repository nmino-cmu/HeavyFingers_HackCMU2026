# Umbra P9 — Hops + one-lot UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crypto wallet / hop path — **last**, but important. After a verification pass, `ingress → cutout → bid` on Solana devnet (S21–S23, S25–S26). One page. No memo, no biometric hash on chain, no spend key on Vultr.

**Architecture:** Keygen + sign on the Mac. Orch never sees secret keys. UI is decide() lights + explorer links.

**Tech Stack:** Solana web3/CLI, one static page.

## Global Constraints

Obey RULES. **Builder:** Grok 4.6 xhigh FAST (`cursor-grok-4.6-xhigh-fast`, empty history). Requires **P4-DONE**. Do **not** start this Goal until verification works. If the clock is short after P4, **this phase beats P5–P8**. RPC down → exit 1, not skip. Faucet empty → BLOCKED with stderr, do not fake txs. `test_sk_absent.py` already exists from P2 — extend it with hop key hashes.

---

### Task 1: Hops

**Files:** `umbra/test_hops.py`, `umbra/hops.py`, `umbra/fixtures/prev_pubkeys.json`

- [ ] Fetch three txs; no Memo program; `{bid,cutout,ingress,faucet}` has 4 addrs; new pubkeys disjoint from prev; no template sha256 in ix data; hop keydir gone after bid; `test_sk_absent.py` includes hop key hashes.

### Task 2: UI

**Files:** `umbra/web/` one page — card text, record/upload crop buttons, lights for bits, explorer links. Copy has no banned words.

- [ ] Manual: open the page, fixture path still produces the same FHE bits as P2/P3.
- [ ] `umbra/test_egress.py` if not already: client through a record proxy, no `V_OK` bytes on the wire except ciphertext.
- [ ] Product `umbra/DONE.md` only if P2 is green **on Vultr** and P4 exists. Fresh cursor-grok-4.6-xhigh-fast runs **every** `umbra/test_*.py`. Clock: do not start this phase after 15:30.
