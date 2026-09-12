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


def get_balance(address: str | Path | Keypair | Pubkey, rpc: str = DEFAULT_RPC) -> float:
    """Return balance in SOL. `address` may be a pubkey, Keypair, or keypair file path."""
    return _run(_get_balance(address, rpc))


async def _get_balance(address: str | Path | Keypair | Pubkey, rpc: str) -> float:
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
    lamports = int(round(amount_sol * LAMPORTS_PER_SOL))
    if lamports <= 0:
        raise ValueError("amount too small")
    dest = Pubkey.from_string(to_address)
    last_err: Exception | None = None
    async with AsyncClient(rpc) as client:
        for attempt in range(8):
            try:
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
            except Exception as e:
                last_err = e
                msg = str(e)
                # Public RPC can lag after funding a brand-new account.
                if "AccountNotFound" in msg or "no record of a prior credit" in msg:
                    await asyncio.sleep(1.5 * (attempt + 1))
                    continue
                raise
    raise RuntimeError(last_err)


def airdrop(address: str | Path | Keypair | Pubkey, amount_sol: float = 1.0, rpc: str = DEFAULT_RPC) -> str:
    """Request free devnet SOL (rate-limited; use https://faucet.solana.com if this fails)."""
    return _run(_airdrop(address, amount_sol, rpc))


async def _airdrop(address: str | Path | Keypair | Pubkey, amount_sol: float, rpc: str) -> str:
    pk = _pubkey(address)
    lamports = int(amount_sol * LAMPORTS_PER_SOL)
    async with AsyncClient(rpc) as client:
        sig = (await client.request_airdrop(pk, lamports)).value
        await client.confirm_transaction(sig, commitment=Confirmed)
    return str(sig)


def wait_for_incoming(
    address: str | Path | Keypair | Pubkey,
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


# --- Escrow (custodial: library holds a dedicated escrow keypair) ---
# Not an on-chain program. Release/refund require the escrow secret stored locally.

ESCROW_DIR = Path(os.environ.get("UMBRA_ESCROW_DIR", Path(__file__).resolve().parent / "fixtures" / "escrows"))
_FEE_SOL = 0.000005  # ~5000 lamports


def _as_wallet(wallet: Keypair | str | Path) -> Keypair:
    return wallet if isinstance(wallet, Keypair) else load_wallet(wallet)


def _escrow_paths(escrow_id: str, store_dir: Path) -> tuple[Path, Path]:
    base = store_dir / escrow_id
    return base.with_suffix(".json"), Path(str(base) + ".keypair.json")


def create_escrow(
    payer: Keypair | str | Path,
    payee_address: str,
    amount: float,
    store_dir: str | Path | None = None,
    rpc: str = DEFAULT_RPC,
) -> dict:
    """Lock `amount` SOL from `payer` into a fresh escrow wallet for `payee_address`.

    Returns escrow record (id, address, deposit signature, paths). Funds stay
    locked until release_escrow or refund_escrow.
    """
    if amount <= 0:
        raise ValueError("amount must be positive")
    Pubkey.from_string(payee_address)  # validate

    store = Path(store_dir) if store_dir else ESCROW_DIR
    store.mkdir(parents=True, exist_ok=True)

    payer_kp = _as_wallet(payer)
    payer_addr = receive_address(payer_kp)
    if payer_addr == payee_address:
        raise ValueError("payer and payee must differ")

    bal = get_balance(payer_kp, rpc=rpc)
    if bal < amount + _FEE_SOL:
        raise ValueError(f"payer needs ~{amount + _FEE_SOL} SOL, has {bal}")

    escrow_kp = create_wallet()
    escrow_addr = receive_address(escrow_kp)
    escrow_id = escrow_addr[:16]
    meta_path, key_path = _escrow_paths(escrow_id, store)
    save_wallet(escrow_kp, key_path)

    deposit_sig = send_sol(payer_kp, escrow_addr, amount, rpc=rpc)
    wait_for_incoming(escrow_addr, amount * 0.999, timeout_s=90, rpc=rpc)

    record = {
        "id": escrow_id,
        "status": "funded",
        "payer": payer_addr,
        "payee": payee_address,
        "amount_sol": amount,
        "escrow_address": escrow_addr,
        "keypair_path": str(key_path),
        "deposit_sig": deposit_sig,
        "deposit_explorer": explorer_url(deposit_sig),
        "settle_sig": None,
        "settle_explorer": None,
        "rpc": rpc,
    }
    meta_path.write_text(json.dumps(record, indent=2))
    record["meta_path"] = str(meta_path)
    return record


def load_escrow(escrow_id: str, store_dir: str | Path | None = None) -> dict:
    """Load escrow metadata by id (first 16 chars of escrow address)."""
    store = Path(store_dir) if store_dir else ESCROW_DIR
    meta_path, _ = _escrow_paths(escrow_id, store)
    if not meta_path.is_file():
        raise FileNotFoundError(f"escrow not found: {meta_path}")
    record = json.loads(meta_path.read_text())
    record["meta_path"] = str(meta_path)
    return record


def escrow_balance(escrow_id: str, store_dir: str | Path | None = None, rpc: str | None = None) -> float:
    """On-chain SOL held in the escrow address."""
    record = load_escrow(escrow_id, store_dir)
    return get_balance(record["escrow_address"], rpc=rpc or record.get("rpc", DEFAULT_RPC))


def release_escrow(escrow_id: str, store_dir: str | Path | None = None, rpc: str | None = None) -> dict:
    """Pay the locked funds to the payee and mark escrow released."""
    return _settle_escrow(escrow_id, to="payee", store_dir=store_dir, rpc=rpc)


def refund_escrow(escrow_id: str, store_dir: str | Path | None = None, rpc: str | None = None) -> dict:
    """Return the locked funds to the payer and mark escrow refunded."""
    return _settle_escrow(escrow_id, to="payer", store_dir=store_dir, rpc=rpc)


def _settle_escrow(
    escrow_id: str,
    to: str,
    store_dir: str | Path | None,
    rpc: str | None,
) -> dict:
    store = Path(store_dir) if store_dir else ESCROW_DIR
    record = load_escrow(escrow_id, store)
    if record["status"] != "funded":
        raise ValueError(f"escrow status is {record['status']}, expected funded")

    rpc_url = rpc or record.get("rpc", DEFAULT_RPC)
    dest = record["payee"] if to == "payee" else record["payer"]
    escrow_kp = load_wallet(record["keypair_path"])
    if receive_address(escrow_kp) != record["escrow_address"]:
        raise RuntimeError("escrow keypair does not match escrow address")

    wait_for_incoming(escrow_kp, min_sol=_FEE_SOL * 2, timeout_s=90, rpc=rpc_url)
    held = get_balance(escrow_kp, rpc=rpc_url)
    send_amount = round(held - _FEE_SOL, 9)
    if send_amount <= 0:
        raise ValueError(f"escrow balance {held} SOL too low to settle")

    sig = send_sol(escrow_kp, dest, send_amount, rpc=rpc_url)
    record["status"] = "released" if to == "payee" else "refunded"
    record["settle_sig"] = sig
    record["settle_explorer"] = explorer_url(sig)
    record["settled_sol"] = send_amount
    record["settled_to"] = dest
    meta_path = Path(record["meta_path"])
    to_save = {k: v for k, v in record.items() if k != "meta_path"}
    meta_path.write_text(json.dumps(to_save, indent=2))
    return record


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


def _pubkey(address: str | Path | Keypair | Pubkey) -> Pubkey:
    if isinstance(address, Keypair):
        return address.pubkey()
    if isinstance(address, Pubkey):
        return address
    path = Path(address)
    if path.is_file():
        return load_wallet(path).pubkey()
    return Pubkey.from_string(str(address))
