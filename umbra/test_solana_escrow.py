"""Smoke-test custodial escrow in solana_wallet.

Usage:
  python umbra/test_solana_escrow.py <payer.json> <payee.json|address> [amount]

Example:
  python umbra/test_solana_escrow.py ^
    "c:\\Users\\hello\\Downloads\\wallet-1-keypair(2).json" ^
    "c:\\Users\\hello\\Downloads\\wallet-1-keypair.json" ^
    0.05
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow `python umbra/test_solana_escrow.py` without installing the package.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from umbra.solana_wallet import (
    create_escrow,
    escrow_balance,
    get_balance,
    load_wallet,
    receive_address,
    release_escrow,
)


def _payee_address(arg: str) -> str:
    p = Path(arg)
    if p.is_file():
        return receive_address(load_wallet(p))
    return arg


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    payer = sys.argv[1]
    payee = _payee_address(sys.argv[2])
    amount = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05

    print(f"payer bal before: {get_balance(payer):.6f} SOL")
    print(f"payee            {payee}")
    print(f"payee bal before: {get_balance(payee):.6f} SOL")

    esc = create_escrow(payer, payee, amount)
    print(f"escrow id        {esc['id']}")
    print(f"escrow address   {esc['escrow_address']}")
    print(f"held             {escrow_balance(esc['id']):.6f} SOL")
    print(f"deposit          {esc['deposit_explorer']}")

    out = release_escrow(esc["id"])
    print(f"status           {out['status']}")
    print(f"settled          {out['settled_sol']:.6f} SOL -> {out['settled_to']}")
    print(f"release          {out['settle_explorer']}")
    print(f"payer bal after: {get_balance(payer):.6f} SOL")
    print(f"payee bal after: {get_balance(payee):.6f} SOL")
    print("ok" if out["status"] == "released" else "fail")
    return 0 if out["status"] == "released" else 1


if __name__ == "__main__":
    raise SystemExit(main())
