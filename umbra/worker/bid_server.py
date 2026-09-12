"""FHE sealed-bid worker: server.zip only. Binds VPC IP :8085."""
from __future__ import annotations

import json
import os
import pathlib
import sys

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from concrete.ml.deployment import FHEModelServer

from umbra.protocol import unpack_request

BIND = os.environ.get("UMBRA_FHE_VPC_IP", "")
PORT = int(os.environ.get("UMBRA_FHE_PORT", "8085"))
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


def looks_like_plaintext_bid(body: bytes, ctype: str) -> bool:
    if "json" in ctype:
        return True
    if not body or len(body) <= 32:
        return True
    if body[:1] in (b"{", b"["):
        return True
    return False


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        # path + status only; never request bodies
        sys.stderr.write("bid %s\n" % (fmt % args))

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
                {"role": "bid", "machine_id": MACHINE_ID, "hostname": HOSTNAME}
            ).encode()
            self._send(200, body, "application/json")
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        nonce = self.headers.get("X-Umbra-Nonce", "")
        extra = {"X-Umbra-Nonce": nonce} if nonce else None
        if path != "/bid":
            self._send(404, b"no", extra=extra)
            return
        n = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(n) if n else b""
        ctype = (self.headers.get("Content-Type") or "").lower()
        if looks_like_plaintext_bid(body, ctype):
            self._send(400, b"plaintext rejected", extra=extra)
            return
        try:
            evk, ct, _card = unpack_request(body)
        except ValueError:
            self._send(400, b"bad wire", extra=extra)
            return
        try:
            result = get_server().run(ct, evk)
            if isinstance(result, (list, tuple)):
                result = result[0]
            out = result if isinstance(result, bytes) else bytes(result)
        except Exception as e:
            self._send(422, type(e).__name__.encode(), extra=extra)
            return
        self._send(200, out, extra=extra)


if __name__ == "__main__":
    if not BIND:
        raise SystemExit("UMBRA_FHE_VPC_IP required")
    print(f"bid bind {BIND}:{PORT} artifacts={ARTIFACT}", flush=True)
    ThreadingHTTPServer((BIND, PORT), Handler).serve_forever()
