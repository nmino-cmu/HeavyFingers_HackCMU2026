"""Send and receive SOL on Solana (devnet by default).

Requires: pip install solana solders

Receive = share your public address; others send to it. Use get_balance /
wait_for_incoming to see funds land.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import VersionedTransaction

LAMPORTS_PER_SOL = 1_000_000_000
DEFAULT_RPC = os.environ.get("UMBRA_SOLANA_RPC", "https://api.devnet.solana.com")
EXPLORER = "https://explorer.solana.com/tx/{sig}?cluster=devnet"


def _run(coro):
    return asyncio.run(coro)


def create_wallet() -> Keypair:
    """Generate a new keypair. Save it before losing the process."""
    return Keypair()


def save_wallet(keypair: Keypair, path: str | Path) -> Path:
    """Write the secret key as a Solana CLI-style JSON byte array."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(list(bytes(keypair))))
    return path


def load_wallet(path: str | Path) -> Keypair:
    """Load a keypair from a Solana CLI JSON file or raw 64-byte secret."""
    path = Path(path)
    raw = path.read_text().strip()
    if raw.startswith("["):
        return Keypair.from_bytes(bytes(json.loads(raw)))
    return Keypair.from_bytes(bytes.fromhex(raw) if all(c in "0123456789abcdefABCDEF" for c in raw) else path.read_bytes())


def receive_address(keypair: Keypair) -> str:
    """Public address others use to send you SOL."""
    return str(keypair.pubkey())


def get_balance(address: str | Keypair | Pubkey, rpc: str = DEFAULT_RPC) -> float:
    """Return balance in SOL."""
    return _run(_get_balance(address, rpc))


async def _get_balance(address: str | Keypair | Pubkey, rpc: str) -> float:
    pk = _pubkey(address)
    async with AsyncClient(rpc) as client:
        resp = await client.get_balance(pk, commitment=Confirmed)
    return resp.value / LAMPORTS_PER_SOL


def send_sol(
    from_wallet: Keypair,
    to_address: str,
    amount_sol: float,
    rpc: str = DEFAULT_RPC,
) -> str:
    """Transfer SOL. Returns the transaction signature."""
    if amount_sol <= 0:
        raise ValueError("amount_sol must be positive")
    return _run(_send_sol(from_wallet, to_address, amount_sol, rpc))


async def _send_sol(from_wallet: Keypair, to_address: str, amount_sol: float, rpc: str) -> str:
    lamports = int(amount_sol * LAMPORTS_PER_SOL)
    dest = Pubkey.from_string(to_address)
    async with AsyncClient(rpc) as client:
        blockhash = (await client.get_latest_blockhash()).value.blockhash
        ix = transfer(
            TransferParams(
                from_pubkey=from_wallet.pubkey(),
                to_pubkey=dest,
                lamports=lamports,
            )
        )
        msg = MessageV0.try_compile(
            payer=from_wallet.pubkey(),
            instructions=[ix],
            address_lookup_table_accounts=[],
            recent_blockhash=blockhash,
        )
        tx = VersionedTransaction(msg, [from_wallet])
        sig = (await client.send_raw_transaction(bytes(tx))).value
        await client.confirm_transaction(sig, commitment=Confirmed)
    return str(sig)


def airdrop(address: str | Keypair | Pubkey, amount_sol: float = 1.0, rpc: str = DEFAULT_RPC) -> str:
    """Request free devnet SOL (rate-limited; use https://faucet.solana.com if this fails)."""
    return _run(_airdrop(address, amount_sol, rpc))


async def _airdrop(address: str | Keypair | Pubkey, amount_sol: float, rpc: str) -> str:
    pk = _pubkey(address)
    lamports = int(amount_sol * LAMPORTS_PER_SOL)
    async with AsyncClient(rpc) as client:
        sig = (await client.request_airdrop(pk, lamports)).value
        await client.confirm_transaction(sig, commitment=Confirmed)
    return str(sig)


def wait_for_incoming(
    address: str | Keypair | Pubkey,
    min_sol: float,
    timeout_s: float = 120,
    poll_s: float = 2,
    rpc: str = DEFAULT_RPC,
) -> float:
    """Poll until balance >= min_sol. Returns final balance in SOL."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        bal = get_balance(address, rpc=rpc)
        if bal >= min_sol:
            return bal
        time.sleep(poll_s)
    raise TimeoutError(f"balance still below {min_sol} SOL after {timeout_s}s")


def explorer_url(signature: str) -> str:
    return EXPLORER.format(sig=signature)


def _pubkey(address: str | Keypair | Pubkey) -> Pubkey:
    if isinstance(address, Keypair):
        return address.pubkey()
    if isinstance(address, Pubkey):
        return address
    return Pubkey.from_string(address)


if __name__ == "__main__":
    # Tiny demo: create wallet, print receive address, optionally airdrop + send.
    wallet = create_wallet()
    path = Path(__file__).resolve().parent / "fixtures" / "demo_wallet.json"
    save_wallet(wallet, path)
    addr = receive_address(wallet)
    print(f"receive address: {addr}")
    print(f"saved keypair:   {path}")
    print(f"balance:         {get_balance(wallet)} SOL")
    print("Fund via faucet: https://faucet.solana.com/")
    print("Then: send_sol(load_wallet(path), '<dest>', 0.01)")
