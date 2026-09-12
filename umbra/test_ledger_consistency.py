#!/usr/bin/env python3
"""LEDGER rows must match shipped eval host and stack policy."""
import os
import re
import sys

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "umbra/LEDGER.md")

CHECKS_RUN = 0
ROW_RE = re.compile(
    r"^ROW (S\d+) STACKS_TRIED=([^\s]+) RESULT=(VULTR_CONCRETE|VULTR_OPENFHE|VULTR_SEAL|LOCAL_FHE|LOCAL_CLEAR)\s*$"
)


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def main():
    text = open(LEDGER, encoding="utf-8").read()
    rows = ROW_RE.findall(text)
    check(rows, "LEDGER must contain ROW lines with STACKS_TRIED and RESULT")

    eval_host = None
    for line in text.splitlines():
        if line.startswith("EVAL_HOST="):
            eval_host = line.split("=", 1)[1].strip()
    check(eval_host in ("vultr", "mac"), f"EVAL_HOST missing or invalid: {eval_host}")

    for row_id, stacks, result in rows:
        tried = [s.strip() for s in stacks.split(",") if s.strip()]
        check(len(tried) >= 2 or result.startswith("LOCAL"), f"{row_id} needs >=2 stacks or LOCAL_*")
        if result.startswith("VULTR_"):
            check(eval_host == "vultr", f"{row_id} VULTR_* but EVAL_HOST={eval_host}")
            check("cmd:" in text, f"{row_id} missing cmd block")
            check("stderr:" in text, f"{row_id} missing stderr block")
        if result.startswith("LOCAL_"):
            check(eval_host == "mac", f"{row_id} LOCAL_* but EVAL_HOST={eval_host}")

    # P3 ships S5–S14 on one choreo row until split
    shipped = {r[0] for r in rows}
    check("S5" in shipped, "missing ROW S5")

    print(f"CHECKS_RUN={CHECKS_RUN}")
    print(f"LEDGER_ROWS={len(rows)}")


if __name__ == "__main__":
    main()
