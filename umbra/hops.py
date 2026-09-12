"""Mac-only Solana devnet hops. Keygen + sign here. No memo. No spend key on Vultr."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RPC = os.environ.get("UMBRA_SOLANA_RPC", "https://api.devnet.solana.com")
SYSTEM = "11111111111111111111111111111111"
MEMO_PROGRAMS = {
    "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr",
    "Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo",
}
_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_PKCS8 = bytes.fromhex("302e020100300506032b657004220420")
EXPLORER = "https://explorer.solana.com/tx/{sig}?cluster=devnet"
PREV_PATH = os.path.join(HERE, "fixtures/prev_pubkeys.json")
HASH_PATH = os.path.join(HERE, "fixtures/hop_key_hashes.json")
LAST_PATH = os.path.join(HERE, "fixtures/last_hops.json")


def b58encode(data: bytes) -> str:
    n = int.from_bytes(data, "big")
    enc = ""
    while n:
        n, r = divmod(n, 58)
        enc = _B58[r] + enc
    pad = 0
    for b in data:
        if b:
            break
        pad += 1
    return "1" * pad + enc


def b58decode(s: str) -> bytes:
    n = 0
    for c in s:
        n = n * 58 + _B58.index(c)
    pad = 0
    for c in s:
        if c != "1":
            break
        pad += 1
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\x00" * pad + raw


assert b58encode(bytes(32)) == SYSTEM


def compact_u16(n: int) -> bytes:
    out = bytearray()
    while True:
        elem = n & 0x7F
        n >>= 7
        if n == 0:
            out.append(elem)
            return bytes(out)
        out.append(elem | 0x80)


def _pem(seed: bytes) -> str:
    der = _PKCS8 + seed
    return "-----BEGIN PRIVATE KEY-----\n" + base64.encodebytes(der).decode() + "-----END PRIVATE KEY-----\n"


def _openssl_pub(seed: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "k.pem")
        open(p, "w").write(_pem(seed))
        der = subprocess.check_output(["openssl", "pkey", "-in", p, "-pubout", "-outform", "DER"])
    return der[-32:]


def _sign(seed: bytes, msg: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as td:
        k, m, s = os.path.join(td, "k.pem"), os.path.join(td, "m"), os.path.join(td, "s")
        open(k, "w").write(_pem(seed))
        open(m, "wb").write(msg)
        subprocess.check_call(
            ["openssl", "pkeyutl", "-sign", "-inkey", k, "-rawin", "-in", m, "-out", s],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        sig = open(s, "rb").read()
    if len(sig) != 64:
        raise RuntimeError("ed25519 sig")
    return sig


def _keypair():
    seed = os.urandom(32)
    pub = _openssl_pub(seed)
    return seed, pub


def hop_secret_hash() -> str:
    seed, pub = _keypair()
    return hashlib.sha256(seed + pub).hexdigest()


def load_hop_key_hashes() -> list:
    if not os.path.isfile(HASH_PATH):
        return []
    return json.load(open(HASH_PATH))


def template_hashes() -> list[bytes]:
    out = []
    for name in ("pinky.xyt", "index.xyt"):
        p = os.path.join(HERE, "fixtures/print", name)
        out.append(hashlib.sha256(open(p, "rb").read()).digest())
    from umbra.fixtures import V_OK

    out.append(hashlib.sha256(struct.pack("<75d", *V_OK)).digest())
    out.append(hashlib.sha256(struct.pack("<75f", *V_OK)).digest())
    return out


def _rpc(method, params=None):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", "replace")
        if method == "requestAirdrop":
            return {"error": {"code": e.code, "message": err}}
        print(f"rpc down: HTTP {e.code} {err}", file=sys.stderr)
        sys.exit(1)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"rpc down: {e}", file=sys.stderr)
        sys.exit(1)


def _require_rpc():
    h = _rpc("getHealth")
    if h.get("result") != "ok":
        print(f"rpc down: {h}", file=sys.stderr)
        sys.exit(1)


def fetch_tx(sig: str):
    params = [sig, {"encoding": "json", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}]
    for _ in range(20):
        r = _rpc("getTransaction", params)
        if r.get("result"):
            return r["result"]
        time.sleep(1)
    print(f"rpc down or tx missing: {sig}", file=sys.stderr)
    sys.exit(1)


def inspect_ix_data(tx) -> dict:
    msg = tx["transaction"]["message"]
    keys = []
    for k in msg["accountKeys"]:
        keys.append(k["pubkey"] if isinstance(k, dict) else k)
    programs = set()
    blob = b""
    for ix in msg["instructions"]:
        programs.add(keys[ix["programIdIndex"]])
        data = ix.get("data") or ""
        if data:
            blob += b58decode(data)
    return {"programs": programs, "ix_data": blob, "keys": keys}


def _blocked(stderr: str):
    path = os.path.join(HERE, "BLOCKED.md")
    open(path, "w").write("# BLOCKED\n\nfaucet empty or refused\n\n```\n" + stderr + "\n```\n")
    print(stderr, file=sys.stderr)
    sys.exit(2)


def _wait(sig: str, timeout=90):
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = _rpc("getSignatureStatuses", [[sig], {"searchTransactionHistory": True}])
        val = (r.get("result") or {}).get("value") or [None]
        st = val[0]
        if st and st.get("err"):
            raise RuntimeError(st)
        if st and st.get("confirmationStatus") in ("confirmed", "finalized"):
            return
        time.sleep(1.5)
    raise TimeoutError(sig)


def _blockhash() -> bytes:
    r = _rpc("getLatestBlockhash", [{"commitment": "confirmed"}])
    if "error" in r or not r.get("result"):
        print(f"rpc down: {r}", file=sys.stderr)
        sys.exit(1)
    raw = b58decode(r["result"]["value"]["blockhash"])
    if len(raw) != 32:
        print("rpc down: bad blockhash", file=sys.stderr)
        sys.exit(1)
    return raw


def _transfer(seed: bytes, src: bytes, dst: bytes, lamports: int) -> str:
    data = (2).to_bytes(4, "little") + int(lamports).to_bytes(8, "little")
    keys = src + dst + bytes(32)
    msg = bytes([1, 0, 1]) + compact_u16(3) + keys + _blockhash()
    ix = bytes([2]) + compact_u16(2) + bytes([0, 1]) + compact_u16(len(data)) + data
    msg += compact_u16(1) + ix
    tx = compact_u16(1) + _sign(seed, msg) + msg
    r = _rpc("sendTransaction", [base64.b64encode(tx).decode(), {"encoding": "base64", "preflightCommitment": "confirmed"}])
    if "error" in r:
        raise RuntimeError(r)
    sig = r["result"]
    _wait(sig)
    return sig


def _fresh(prev: set):
    for _ in range(16):
        seed, pub = _keypair()
        pk = b58encode(pub)
        if pk not in prev:
            return seed, pub, pk
    raise RuntimeError("key collision")


def _cli_airdrop(pubkey: str, sol: float):
    exe = os.path.expanduser("~/.local/share/solana/install/active_release/bin/solana")
    if not os.path.isfile(exe):
        exe = "solana"
    try:
        return subprocess.run(
            [exe, "airdrop", str(sol), pubkey, "--url", RPC],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return e


def _airdrop(pubkey: str, lamports=1_000_000_000) -> str:
    errs = []
    for lam in (lamports, 100_000_000, 10_000_000):
        r = _rpc("requestAirdrop", [pubkey, lam])
        if r.get("result"):
            sig = r["result"]
            try:
                _wait(sig)
                return sig
            except Exception as e:
                errs.append(str(e))
                continue
        errs.append(json.dumps(r))
        time.sleep(2)
    for sol in (1, 0.1, 0.02):
        p = _cli_airdrop(pubkey, sol)
        out = getattr(p, "stdout", "") + getattr(p, "stderr", str(p))
        errs.append(out)
        if getattr(p, "returncode", 1) == 0:
            for tok in out.split():
                if len(tok) > 80:
                    try:
                        _wait(tok)
                        return tok
                    except Exception as e:
                        errs.append(str(e))
        time.sleep(1)
    _blocked("\n---\n".join(errs))


def _faucet_addr(airdrop_tx, ingress: str) -> str:
    keys = inspect_ix_data(airdrop_tx)["keys"]
    for p in keys:
        if p not in (ingress, SYSTEM) and p not in MEMO_PROGRAMS:
            return p
    raise RuntimeError("no faucet addr")


def run(result, keydir=None):
    if not getattr(result, "ok", False) or getattr(result, "abort", False):
        return None
    _require_rpc()
    prev = json.load(open(PREV_PATH))
    prev_set = set(prev) if isinstance(prev, list) else set(prev["pubkeys"])
    if keydir is None:
        keydir = tempfile.mkdtemp(prefix="umbra-hop-")
    os.makedirs(keydir, exist_ok=True)
    try:
        i_seed, i_pub, i_pk = _fresh(prev_set)
        c_seed, c_pub, c_pk = _fresh(prev_set | {i_pk})
        b_seed, b_pub, b_pk = _fresh(prev_set | {i_pk, c_pk})
        hashes = []
        for name, seed, pub in (("ingress", i_seed, i_pub), ("cutout", c_seed, c_pub), ("bid", b_seed, b_pub)):
            raw = seed + pub
            open(os.path.join(keydir, name), "wb").write(raw)
            hashes.append(hashlib.sha256(raw).hexdigest())
        air = _airdrop(i_pk)
        air_tx = fetch_tx(air)
        faucet = _faucet_addr(air_tx, i_pk)
        if len({faucet, i_pk, c_pk, b_pk}) != 4:
            raise RuntimeError("addr collision")
        bal = (_rpc("getBalance", [i_pk]).get("result") or {}).get("value") or 0
        fee = 5000
        if bal < 3 * fee + 2:
            _blocked(f"ingress balance {bal} after airdrop")
        cut = _transfer(i_seed, i_pub, c_pub, bal - fee - 1)
        cbal = (_rpc("getBalance", [c_pk]).get("result") or {}).get("value") or 0
        if cbal < fee + 1:
            _blocked(f"cutout balance {cbal}")
        bid = _transfer(c_seed, c_pub, b_pub, cbal - fee)
        old = load_hop_key_hashes()
        json.dump(old + hashes, open(HASH_PATH, "w"), indent=2)
        hop = {
            "sigs": [air, cut, bid],
            "addrs": {"faucet": faucet, "ingress": i_pk, "cutout": c_pk, "bid": b_pk},
            "key_hashes": hashes,
            "explorers": [EXPLORER.format(sig=s) for s in (air, cut, bid)],
        }
        json.dump({k: hop[k] for k in ("sigs", "addrs", "explorers")}, open(LAST_PATH, "w"), indent=2)
        return hop
    finally:
        shutil.rmtree(keydir, ignore_errors=True)
