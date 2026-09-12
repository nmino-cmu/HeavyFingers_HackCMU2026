"""Send and receive SOL on Solana (devnet by default).

Requires: pip install solana solders cryptography

Receive = share your public address; others send to it. Use get_balance /
wait_for_incoming to see funds land.

Also: custodial escrow + encrypted 1/1 receipt NFTs for auction outcomes
(winners and losers both get a receipt).
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
import time
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solders.instruction import AccountMeta, Instruction
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.system_program import CreateAccountParams, create_account
from solders.system_program import ID as SYSTEM_PROGRAM_ID
from solders.token.associated import get_associated_token_address
from solders.transaction import VersionedTransaction
from solders.system_program import TransferParams, transfer

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


# --- Encrypted auction / purchase receipt NFTs (1/1 SPL tokens) ---
# On-chain: mint + ATA + amount 1. Off-chain: AES-GCM ciphertext of the receipt.
# If recipient is a keypair, only they can derive the decrypt key.
# If recipient is an address only, a one-time decrypt_key_hex is returned to the caller.

TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
ATA_PROGRAM_ID = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
MINT_SIZE = 82
RECEIPT_DIR = Path(
    os.environ.get("UMBRA_RECEIPT_DIR", Path(__file__).resolve().parent / "fixtures" / "receipts")
)


def _receipt_key_from_wallet(recipient: Keypair, mint: Pubkey) -> bytes:
    return hashlib.sha256(b"umbra-receipt-v1" + bytes(recipient)[:32] + bytes(mint)).digest()


def _encrypt_receipt_payload(payload: dict, key: bytes) -> tuple[str, str]:
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, json.dumps(payload, sort_keys=True).encode(), b"umbra-receipt")
    return base64.b64encode(nonce).decode(), base64.b64encode(ct).decode()


def _decrypt_receipt_payload(nonce_b64: str, ct_b64: str, key: bytes) -> dict:
    aes = AESGCM(key)
    raw = aes.decrypt(
        base64.b64decode(nonce_b64),
        base64.b64decode(ct_b64),
        b"umbra-receipt",
    )
    return json.loads(raw.decode())


def _ix_initialize_mint2(mint: Pubkey, decimals: int, mint_authority: Pubkey) -> Instruction:
    # spl-token InitializeMint2 (tag 20): decimals + authority + no freeze
    data = bytes([20, decimals & 0xFF]) + bytes(mint_authority) + bytes([0])
    return Instruction(TOKEN_PROGRAM_ID, data, [AccountMeta(mint, False, True)])


def _ix_mint_to(mint: Pubkey, dest: Pubkey, authority: Pubkey, amount: int) -> Instruction:
    data = bytes([7]) + int(amount).to_bytes(8, "little")
    return Instruction(
        TOKEN_PROGRAM_ID,
        data,
        [
            AccountMeta(mint, False, True),
            AccountMeta(dest, False, True),
            AccountMeta(authority, True, False),
        ],
    )


def _ix_set_authority_none(account: Pubkey, current_authority: Pubkey, authority_type: int) -> Instruction:
    # SetAuthority tag 6; authority_type 0 = MintTokens; new authority = None
    data = bytes([6, authority_type & 0xFF, 0])
    return Instruction(
        TOKEN_PROGRAM_ID,
        data,
        [
            AccountMeta(account, False, True),
            AccountMeta(current_authority, True, False),
        ],
    )


def _ix_create_ata_idempotent(payer: Pubkey, owner: Pubkey, mint: Pubkey, ata: Pubkey) -> Instruction:
    # Associated Token Program: CreateIdempotent = 1
    return Instruction(
        ATA_PROGRAM_ID,
        bytes([1]),
        [
            AccountMeta(payer, True, True),
            AccountMeta(ata, False, True),
            AccountMeta(owner, False, False),
            AccountMeta(mint, False, False),
            AccountMeta(SYSTEM_PROGRAM_ID, False, False),
            AccountMeta(TOKEN_PROGRAM_ID, False, False),
        ],
    )


async def _mint_receipt_nft(
    minter: Keypair,
    recipient: Pubkey,
    rpc: str,
) -> tuple[str, str, str]:
    """Create a 1/1 token mint and deliver it to recipient. Returns (mint, ata, sig)."""
    mint_kp = Keypair()
    ata = get_associated_token_address(recipient, mint_kp.pubkey())
    last_err: Exception | None = None
    async with AsyncClient(rpc) as client:
        rent = (await client.get_minimum_balance_for_rent_exemption(MINT_SIZE)).value
        for attempt in range(6):
            try:
                blockhash = (await client.get_latest_blockhash()).value.blockhash
                ixs = [
                    create_account(
                        CreateAccountParams(
                            from_pubkey=minter.pubkey(),
                            to_pubkey=mint_kp.pubkey(),
                            lamports=rent,
                            space=MINT_SIZE,
                            owner=TOKEN_PROGRAM_ID,
                        )
                    ),
                    _ix_initialize_mint2(mint_kp.pubkey(), 0, minter.pubkey()),
                    _ix_create_ata_idempotent(minter.pubkey(), recipient, mint_kp.pubkey(), ata),
                    _ix_mint_to(mint_kp.pubkey(), ata, minter.pubkey(), 1),
                    _ix_set_authority_none(mint_kp.pubkey(), minter.pubkey(), 0),
                ]
                msg = MessageV0.try_compile(
                    payer=minter.pubkey(),
                    instructions=ixs,
                    address_lookup_table_accounts=[],
                    recent_blockhash=blockhash,
                )
                tx = VersionedTransaction(msg, [minter, mint_kp])
                sig = (await client.send_raw_transaction(bytes(tx))).value
                await client.confirm_transaction(sig, commitment=Confirmed)
                return str(mint_kp.pubkey()), str(ata), str(sig)
            except Exception as e:
                last_err = e
                msg = str(e)
                if "AccountNotFound" in msg or "no record of a prior credit" in msg:
                    await asyncio.sleep(1.5 * (attempt + 1))
                    continue
                raise
    raise RuntimeError(last_err)


def mint_encrypted_receipt(
    minter: Keypair | str | Path,
    recipient: Keypair | str | Path,
    *,
    won: bool,
    auction_id: str,
    details: dict | None = None,
    store_dir: str | Path | None = None,
    rpc: str = DEFAULT_RPC,
) -> dict:
    """Mint a 1/1 receipt NFT to `recipient` with an encrypted win/lose payload.

    Everyone who bids should get one — set won=False for losers.
    """
    minter_kp = _as_wallet(minter)
    store = Path(store_dir) if store_dir else RECEIPT_DIR
    store.mkdir(parents=True, exist_ok=True)

    recipient_kp: Keypair | None = None
    if isinstance(recipient, Keypair):
        recipient_kp = recipient
        recipient_addr = receive_address(recipient)
    else:
        path = Path(recipient)
        if path.is_file():
            recipient_kp = load_wallet(path)
            recipient_addr = receive_address(recipient_kp)
        else:
            recipient_addr = str(recipient)
            Pubkey.from_string(recipient_addr)

    mint, ata, sig = _run(_mint_receipt_nft(minter_kp, Pubkey.from_string(recipient_addr), rpc))
    mint_pk = Pubkey.from_string(mint)

    payload = {
        "auction_id": auction_id,
        "won": bool(won),
        "outcome": "won" if won else "lost",
        "message": (
            "You won this auction."
            if won
            else "You did not win this auction. This NFT is your encrypted participation receipt."
        ),
        "recipient": recipient_addr,
        "mint": mint,
        "details": details or {},
    }

    decrypt_key_hex = None
    if recipient_kp is not None:
        key = _receipt_key_from_wallet(recipient_kp, mint_pk)
        key_scheme = "recipient_keypair_v1"
    else:
        key = AESGCM.generate_key(bit_length=256)
        decrypt_key_hex = key.hex()
        key_scheme = "caller_held_v1"

    nonce_b64, ct_b64 = _encrypt_receipt_payload(payload, key)
    record = {
        "mint": mint,
        "ata": ata,
        "recipient": recipient_addr,
        "auction_id": auction_id,
        "signature": sig,
        "explorer": explorer_url(sig),
        "key_scheme": key_scheme,
        "nonce_b64": nonce_b64,
        "ciphertext_b64": ct_b64,
        # never store plaintext outcome on disk
    }
    (store / f"{mint}.json").write_text(json.dumps(record, indent=2))
    out = {
        "mint": mint,
        "ata": ata,
        "recipient": recipient_addr,
        "auction_id": auction_id,
        "won": bool(won),
        "signature": sig,
        "explorer": explorer_url(sig),
        "receipt_path": str(store / f"{mint}.json"),
        "key_scheme": key_scheme,
    }
    if decrypt_key_hex:
        out["decrypt_key_hex"] = decrypt_key_hex
    return out


def issue_auction_receipts(
    minter: Keypair | str | Path,
    auction_id: str,
    participants: list[dict],
    store_dir: str | Path | None = None,
    rpc: str = DEFAULT_RPC,
) -> list[dict]:
    """Issue encrypted receipt NFTs to every auction participant.

    Each item in `participants`:
      {"recipient": Keypair|path|address, "won": bool, "details": optional dict}

    Losers must be included with won=False so they still receive a receipt NFT.
    """
    if not participants:
        raise ValueError("participants must be non-empty")
    winners = sum(1 for p in participants if p.get("won"))
    if winners > 1:
        raise ValueError("at most one participant may have won=True")

    receipts = []
    for p in participants:
        if "recipient" not in p or "won" not in p:
            raise ValueError("each participant needs recipient and won")
        receipts.append(
            mint_encrypted_receipt(
                minter,
                p["recipient"],
                won=bool(p["won"]),
                auction_id=auction_id,
                details=p.get("details"),
                store_dir=store_dir,
                rpc=rpc,
            )
        )
    return receipts


def decrypt_receipt(
    recipient: Keypair | str | Path,
    mint_address: str,
    decrypt_key_hex: str | None = None,
    store_dir: str | Path | None = None,
) -> dict:
    """Decrypt a receipt NFT payload. Prefer recipient keypair; else pass decrypt_key_hex."""
    store = Path(store_dir) if store_dir else RECEIPT_DIR
    path = store / f"{mint_address}.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    record = json.loads(path.read_text())

    if decrypt_key_hex:
        key = bytes.fromhex(decrypt_key_hex)
    else:
        recipient_kp = _as_wallet(recipient)
        key = _receipt_key_from_wallet(recipient_kp, Pubkey.from_string(mint_address))

    return _decrypt_receipt_payload(record["nonce_b64"], record["ciphertext_b64"], key)


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
