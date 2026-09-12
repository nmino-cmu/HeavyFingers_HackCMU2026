"""P3 farm/sidecar: pick Linear(75,10) by public card. server.zip only."""
from __future__ import annotations

import json
import os
import pathlib
import struct
import sys

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from concrete.ml.deployment import FHEModelServer

from umbra.protocol import CARD_BYTES, looks_like_plaintext_v, unpack_request

BIND = os.environ.get("UMBRA_FHE_VPC_IP", "10.20.0.5")
PORT = int(os.environ.get("UMBRA_FHE_PORT", "8087"))
ROOT = pathlib.Path(os.environ.get("UMBRA_FHE_ARTIFACTS", "/tmp/p3art"))
MACHINE_ID = (
    pathlib.Path("/etc/machine-id").read_text().strip()
    if pathlib.Path("/etc/machine-id").exists()
    else "unknown"
)
HOSTNAME = os.uname().nodename

_servers: dict[str, FHEModelServer] = {}


def card_key(card_raw: bytes) -> str:
    if not card_raw:
        return "rrp"
    hand, side, pinky, index, thumb = struct.unpack(">5d", card_raw)
    if hand < 0.5:
        return "lrp"
    if side < 0.5:
        return "rlp"
    if index >= 0.5:
        return "rri"
    return "rrp"


def get_server(name: str) -> FHEModelServer:
    if name not in _servers:
        path = ROOT / name
        srv = FHEModelServer(path_dir=str(path))
        srv.load()
        _servers[name] = srv
    return _servers[name]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("choreo-cards %s\n" % (fmt % args))

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
                {"role": "choreo-cards", "machine_id": MACHINE_ID, "hostname": HOSTNAME}
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
        if "json" in ctype or looks_like_plaintext_v(body) or ctype.startswith("text/"):
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
            name = card_key(card_raw)
            sys.stderr.write("choreo-cards pick %s card_len=%d\n" % (name, len(card_raw)))
            result = get_server(name).run(ct, evk)
            if isinstance(result, (list, tuple)):
                result = result[0]
            out = result if isinstance(result, bytes) else bytes(result)
        except Exception as e:
            self._send(422, str(e).encode()[:500], extra=extra)
            return
        self._send(200, out, extra=extra)


if __name__ == "__main__":
    print(f"choreo-cards bind {BIND}:{PORT} artifacts={ROOT}", flush=True)
    ThreadingHTTPServer((BIND, PORT), Handler).serve_forever()
