#!/usr/bin/env python3
"""Unbreakable Umbra halt. Exit 99 = stop the orchestrator and every phase."""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
HARD_STOP_FILE = ROOT / "umbra" / "HARD_STOP"
STOPPED = ROOT / "umbra" / "STOPPED.md"
DEADLINE = datetime(2026, 9, 12, 15, 30, 0, tzinfo=ZoneInfo("America/New_York"))


def stopped_reason() -> str | None:
    now = datetime.now(ZoneInfo("America/New_York"))
    if HARD_STOP_FILE.exists():
        return f"umbra/HARD_STOP present at {now.isoformat()}"
    if now >= DEADLINE:
        return f"wall clock {now.isoformat()} >= {DEADLINE.isoformat()}"
    return None


def main() -> int:
    why = stopped_reason()
    if not why:
        print("hard_stop: continue")
        return 0
    STOPPED.parent.mkdir(parents=True, exist_ok=True)
    STOPPED.write_text(
        f"# STOPPED\n\n{why}\n\nNo further phases. Do not spawn Tasks.\n",
        encoding="utf-8",
    )
    print(f"hard_stop: HALT {why}", file=sys.stderr)
    return 99


if __name__ == "__main__":
    raise SystemExit(main())
