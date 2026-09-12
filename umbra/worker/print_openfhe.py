"""OpenFHE print worker: EvalSub only. Never decrypts. Bind VPC :8092."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import struct
import sys

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from openfhe import BINARY, DeserializeCiphertextString, DeserializeCryptoContextString, Serialize

_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from umbra.protocol import CARD_BYTES, looks_like_plaintext_v, looks_like_plaintext_xyt, unpack_request

BIND = os.environ.get("UMBRA_FHE_VPC_IP") or os.environ.get("UMBRA_OPENFHE_PRINT_VPC_IP")
PORT = int(os.environ.get("UMBRA_OPENFHE_PRINT_PORT", "8092"))
STORE = pathlib.Path(os.environ.get("UMBRA_OPENFHE_PRINT_STORE", "/opt/umbra/print-openfhe/templates"))
MACHINE_ID = (
    pathlib.Path("/etc/machine-id").read_text().strip()
    if pathlib.Path("/etc/machine-id").exists()
    else "unknown"
)
HOSTNAME = os.uname().nodename

TOKEN_LEN = 32
_cc_cache: dict[str, object] = {}


def digit_from_card(card_raw: bytes) -> str:
    if len(card_raw) != CARD_BYTES:
        return "pinky"
    vals = struct.unpack(">5d", card_raw)
    if vals[3] >= 0.5:
        return "index"
    if vals[4] >= 0.5:
        return "thumb"
    return "pinky"


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("print-openfhe %s\n" % (fmt % args))

    def _send(self, code, body: bytes, ctype="application/octet-stream", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/health":
            body = json.dumps(
                {"role": "print-openfhe", "machine_id": MACHINE_ID, "hostname": HOSTNAME}
            ).encode()
            self._send(200, body, "application/json")
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        n = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(n) if n else b""
        ctype = (self.headers.get("Content-Type") or "").lower()
        if "json" in ctype or looks_like_plaintext_v(body) or looks_like_plaintext_xyt(body):
            self._send(400, b"plaintext rejected")
            return
        if path == "/enroll":
            self._enroll(body)
            return
        if path != "/print":
            self._send(404, b"no")
            return
        try:
            evk, ct, card_raw = unpack_request(body)
        except ValueError as e:
            self._send(400, str(e).encode())
            return
        digit = digit_from_card(card_raw)
        tok_path = STORE / f"{digit}.tok"
        cc_path = STORE / f"{digit}.cc"
        tmpl_path = STORE / f"{digit}.ct"
        if not tok_path.is_file() or not cc_path.is_file() or not tmpl_path.is_file():
            self._send(422, b"no template")
            return
        stored = tok_path.read_bytes()
        if evk != stored and evk != hashlib.sha256(stored).digest():
            self._send(422, b"wrong key")
            return
        try:
            cc = _cc_cache.get(digit)
            if cc is None:
                cc = DeserializeCryptoContextString(cc_path.read_bytes(), BINARY)
                _cc_cache[digit] = cc
            probe = DeserializeCiphertextString(ct, BINARY)
            tmpl = DeserializeCiphertextString(tmpl_path.read_bytes(), BINARY)
            out = Serialize(cc.EvalSub(probe, tmpl), BINARY)
        except Exception as e:
            self._send(422, str(e).encode()[:200])
            return
        self._send(200, out)

    def _enroll(self, body: bytes):
        digit = (self.headers.get("X-Umbra-Digit") or "pinky").strip().lower()
        if digit not in ("pinky", "index", "thumb"):
            self._send(400, b"bad digit")
            return
        try:
            evk, ct, _card = unpack_request(body)
        except ValueError as e:
            self._send(400, str(e).encode())
            return
        if len(evk) < TOKEN_LEN + 16 or len(ct) < 1000:
            self._send(400, b"enroll too small")
            return
        STORE.mkdir(parents=True, exist_ok=True)
        (STORE / f"{digit}.tok").write_bytes(evk[:TOKEN_LEN])
        (STORE / f"{digit}.cc").write_bytes(evk[TOKEN_LEN:])
        (STORE / f"{digit}.ct").write_bytes(ct)
        _cc_cache.pop(digit, None)
        self._send(200, b"ok")


if __name__ == "__main__":
    if not BIND:
        raise SystemExit("UMBRA_FHE_VPC_IP required")
    print(f"print-openfhe bind {BIND}:{PORT} store={STORE}", flush=True)
    ThreadingHTTPServer((BIND, PORT), Handler).serve_forever()
