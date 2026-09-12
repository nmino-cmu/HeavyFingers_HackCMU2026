"""FHE eval worker: server.zip only. Binds VPC IP :8081."""
from __future__ import annotations

import json
import os
import pathlib
import sys

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from concrete.ml.deployment import FHEModelServer

import numpy as np

from umbra.protocol import CARD_BYTES, looks_like_plaintext_v, unpack_request

BIND = os.environ.get("UMBRA_FHE_VPC_IP", "10.20.0.5")
PORT = int(os.environ.get("UMBRA_FHE_PORT", "8081"))
ARTIFACT = os.environ.get("UMBRA_FHE_ARTIFACTS", "/opt/umbra/artifacts")
MACHINE_ID = (
    pathlib.Path("/etc/machine-id").read_text().strip()
    if pathlib.Path("/etc/machine-id").exists()
    else "unknown"
)
HOSTNAME = os.uname().nodename

_server: FHEModelServer | None = None


def get_server() -> FHEModelServer:
    global _server
    if _server is None:
        _server = FHEModelServer(path_dir=ARTIFACT)
        _server.load()
    return _server


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("choreo %s\n" % (fmt % args))

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
                {"role": "choreo", "machine_id": MACHINE_ID, "hostname": HOSTNAME}
            ).encode()
            self._send(200, body, "application/json")
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        nonce = self.headers.get("X-Umbra-Nonce", "")
        extra = {"X-Umbra-Nonce": nonce} if nonce else None
        if path != "/eval":
            self._send(404, b"no", extra=extra)
            return
        n = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(n) if n else b""
        ctype = (self.headers.get("Content-Type") or "").lower()
        if "json" in ctype or looks_like_plaintext_v(body):
            self._send(400, b"plaintext rejected", extra=extra)
            return
        try:
            evk, ct, card_raw = unpack_request(body)
        except ValueError as e:
            self._send(400, str(e).encode(), extra=extra)
            return
        if len(card_raw) not in (0, CARD_BYTES):
            self._send(400, b"bad card trailer", extra=extra)
            return
        try:
            if card_raw:
                import struct

                card = np.asarray(struct.unpack(">5d", card_raw), dtype=np.float64).reshape(1, -1)
                result = get_server().run(ct, evk, card)
            else:
                result = get_server().run(ct, evk)
            if isinstance(result, (list, tuple)):
                result = result[0]
            out = result if isinstance(result, bytes) else bytes(result)
        except Exception as e:
            self._send(422, str(e).encode()[:500], extra=extra)
            return
        self._send(200, out, extra=extra)


if __name__ == "__main__":
    print(f"choreo bind {BIND}:{PORT} artifacts={ARTIFACT}", flush=True)
    ThreadingHTTPServer((BIND, PORT), Handler).serve_forever()
