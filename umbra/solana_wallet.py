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
    wallet: Keypair | str | Path,
    receiver_address: str,
    amount: float,
    rpc: str = DEFAULT_RPC,
) -> str:
    """Send `amount` SOL from `wallet` to `receiver_address`.

    `wallet` can be a Keypair or a path to a keypair JSON file.
    Returns the transaction signature.

    Example:
        send_sol(r"c:\\Users\\hello\\Downloads\\wallet-1-keypair(2).json",
                 "DfgYv1sw56hVBtz753Hn6pKMg5kWiJjWUCJ91ek7af2K",
                 0.1)
    """
    if amount <= 0:
        raise ValueError("amount must be positive")
    sender = wallet if isinstance(wallet, Keypair) else load_wallet(wallet)
    return _run(_send_sol(sender, receiver_address, amount, rpc))


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

#Test code
def test_transfer(
    from_wallet_path: str | Path,
    to_wallet_path: str | Path,
    amount_sol: float = 0.1,
    rpc: str = DEFAULT_RPC,
) -> dict:
    """Send amount_sol from one keypair file to another and report balances.

    Example:
        from umbra.solana_wallet import test_transfer
        result = test_transfer(
            r"c:\\Users\\hello\\Downloads\\wallet-1-keypair(2).json",
            r"c:\\Users\\hello\\Downloads\\wallet-1-keypair.json",
            amount_sol=0.1,
        )
        print(result["explorer"])
    """
    sender = load_wallet(from_wallet_path)
    receiver = load_wallet(to_wallet_path)
    from_addr = receive_address(sender)
    to_addr = receive_address(receiver)
    if from_addr == to_addr:
        raise ValueError("from and to wallets are the same address")

    before_from = get_balance(sender, rpc=rpc)
    before_to = get_balance(receiver, rpc=rpc)
    if before_from < amount_sol:
        raise ValueError(
            f"sender balance {before_from} SOL is less than amount {amount_sol} SOL"
        )

    sig = send_sol(sender, to_addr, amount_sol, rpc=rpc)
    after_from = get_balance(sender, rpc=rpc)
    after_to = get_balance(receiver, rpc=rpc)
    ok = after_to >= before_to + amount_sol * 0.999  # tiny float slack

    return {
        "ok": ok,
        "signature": sig,
        "explorer": explorer_url(sig),
        "from": from_addr,
        "to": to_addr,
        "amount_sol": amount_sol,
        "before": {"from": before_from, "to": before_to},
        "after": {"from": after_from, "to": after_to},
    }


def _pubkey(address: str | Keypair | Pubkey) -> Pubkey:
    if isinstance(address, Keypair):
        return address.pubkey()
    if isinstance(address, Pubkey):
        return address
    return Pubkey.from_string(address)
