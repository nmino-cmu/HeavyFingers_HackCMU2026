"""FHE print worker: server.zip only. Binds VPC IP :8082. Templates at rest are ciphertext."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import struct
import sys

from concrete.fhe import EvaluationKeys, Server
from concrete.fhe.compilation.value import Value
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from umbra.protocol import CARD_BYTES, looks_like_plaintext_v, looks_like_plaintext_xyt, unpack_request

BIND = os.environ.get("UMBRA_PRINT_VPC_IP") or os.environ.get("UMBRA_FHE_VPC_IP", "10.20.0.6")
PORT = int(os.environ.get("UMBRA_PRINT_PORT", "8082"))
ARTIFACT = os.environ.get("UMBRA_PRINT_ARTIFACTS", "/opt/umbra/print/artifacts")
STORE = pathlib.Path(os.environ.get("UMBRA_PRINT_STORE", "/opt/umbra/print/templates"))
MACHINE_ID = (
    pathlib.Path("/etc/machine-id").read_text().strip()
    if pathlib.Path("/etc/machine-id").exists()
    else "unknown"
)
HOSTNAME = os.uname().nodename

_server: Server | None = None
_evk_cache: dict[str, EvaluationKeys] = {}


def get_server() -> Server:
    global _server
    if _server is None:
        _server = Server.load(str(pathlib.Path(ARTIFACT) / "server.zip"))
    return _server


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
        sys.stderr.write("print %s\n" % (fmt % args))

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
                {"role": "print", "machine_id": MACHINE_ID, "hostname": HOSTNAME}
            ).encode()
            self._send(200, body, "application/json")
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        nonce = self.headers.get("X-Umbra-Nonce", "")
        extra = {"X-Umbra-Nonce": nonce} if nonce else None
        n = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(n) if n else b""
        ctype = (self.headers.get("Content-Type") or "").lower()
        if "json" in ctype or looks_like_plaintext_v(body) or looks_like_plaintext_xyt(body):
            self._send(400, b"plaintext rejected", extra=extra)
            return
        if path == "/enroll":
            self._enroll(body, extra)
            return
        if path != "/print":
            self._send(404, b"no", extra=extra)
            return
        try:
            evk, ct, card_raw = unpack_request(body)
        except ValueError as e:
            self._send(400, str(e).encode(), extra=extra)
            return
        digit = digit_from_card(card_raw)
        tmpl_path = STORE / f"{digit}.ct"
        evk_path = STORE / f"{digit}.evk"
        if not tmpl_path.is_file() or not evk_path.is_file():
            self._send(422, b"no template", extra=extra)
            return
        stored_evk = evk_path.read_bytes()
        if evk != hashlib.sha256(stored_evk).digest():
            self._send(422, b"wrong key", extra=extra)
            return
        try:
            evk_obj = _evk_cache.get(digit)
            if evk_obj is None:
                evk_obj = EvaluationKeys.deserialize(stored_evk)
                _evk_cache[digit] = evk_obj
            probe = Value.deserialize(ct)
            tmpl = Value.deserialize(tmpl_path.read_bytes())
            result = get_server().run((probe, tmpl), evaluation_keys=evk_obj)
            out = result.serialize() if hasattr(result, "serialize") else bytes(result)
        except Exception as e:
            self._send(422, str(e).encode()[:500], extra=extra)
            return
        self._send(200, out, extra=extra)

    def _enroll(self, body: bytes, extra):
        digit = (self.headers.get("X-Umbra-Digit") or "pinky").strip().lower()
        if digit not in ("pinky", "index", "thumb"):
            self._send(400, b"bad digit", extra=extra)
            return
        try:
            evk, ct, _card = unpack_request(body)
        except ValueError as e:
            self._send(400, str(e).encode(), extra=extra)
            return
        if len(ct) < 50_000:
            self._send(400, b"template too small", extra=extra)
            return
        STORE.mkdir(parents=True, exist_ok=True)
        (STORE / f"{digit}.ct").write_bytes(ct)
        (STORE / f"{digit}.evk").write_bytes(evk)
        _evk_cache.pop(digit, None)
        self._send(200, b"ok", extra=extra)


if __name__ == "__main__":
    print(f"print bind {BIND}:{PORT} artifacts={ARTIFACT} store={STORE}", flush=True)
    ThreadingHTTPServer((BIND, PORT), Handler).serve_forever()
