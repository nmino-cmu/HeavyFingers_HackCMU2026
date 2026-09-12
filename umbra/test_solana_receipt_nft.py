"""Smoke-test encrypted auction receipt NFTs.

Usage:
  python umbra/test_solana_receipt_nft.py <minter.json> <winner.json> <loser.json|address>

Example:
  python umbra/test_solana_receipt_nft.py ^
    "c:\\Users\\hello\\Downloads\\wallet-1-keypair(2).json" ^
    "c:\\Users\\hello\\Downloads\\wallet-1-keypair.json" ^
    "c:\\Users\\hello\\Downloads\\wallet-1-keypair(2).json"
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from umbra.solana_wallet import (
    decrypt_receipt,
    get_balance,
    issue_auction_receipts,
    receive_address,
    load_wallet,
)


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    minter, winner, loser = sys.argv[1], sys.argv[2], sys.argv[3]
    print(f"minter bal: {get_balance(minter):.6f} SOL")

    receipts = issue_auction_receipts(
        minter,
        auction_id="demo-auction-1",
        participants=[
            {"recipient": winner, "won": True, "details": {"item": "demo-lot"}},
            {"recipient": loser, "won": False, "details": {"item": "demo-lot"}},
        ],
    )

    for r in receipts:
        print("---")
        print(f"recipient {r['recipient']}")
        print(f"won       {r['won']}")
        print(f"mint      {r['mint']}")
        print(f"explorer  {r['explorer']}")

    # Decrypt with each participant's keypair (paths).
    w_plain = decrypt_receipt(winner, receipts[0]["mint"])
    l_plain = decrypt_receipt(loser, receipts[1]["mint"])
    print("---")
    print("winner decrypted:", w_plain["outcome"], w_plain["message"])
    print("loser decrypted: ", l_plain["outcome"], l_plain["message"])

    ok = w_plain["won"] is True and l_plain["won"] is False
    print("ok" if ok else "fail")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
