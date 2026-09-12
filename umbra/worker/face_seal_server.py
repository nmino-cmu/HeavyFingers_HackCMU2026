"""Encrypted 16x16 Conv+square face match. Bind VPC :8094. Never decrypt. No clear net."""
from __future__ import annotations

import json
import os
import pathlib
import sys

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.face_ckks_conv import eval_conv_sq_l2, looks_like_plaintext_face, unpack_face

BIND = os.environ.get("UMBRA_FACE_VPC_IP") or os.environ.get("UMBRA_FHE_VPC_IP") or "10.20.0.4"
PORT = int(os.environ.get("UMBRA_FACE_PORT", "8094"))
MACHINE_ID = (
    pathlib.Path("/etc/machine-id").read_text().strip()
    if pathlib.Path("/etc/machine-id").exists()
    else "unknown"
)
HOSTNAME = os.uname().nodename


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("face-seal %s\n" % (fmt % args))

    def _send(self, code, body: bytes, ctype="application/octet-stream", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Umbra-Machine-Id", MACHINE_ID)
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/health":
            body = json.dumps(
                {
                    "role": "face-seal",
                    "stack": "tenseal-conv-square",
                    "machine_id": MACHINE_ID,
                    "hostname": HOSTNAME,
                    "eval_host": "vultr",
                }
            ).encode()
            self._send(200, body, "application/json")
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        nonce = self.headers.get("X-Umbra-Nonce", "")
        extra = {"X-Umbra-Nonce": nonce} if nonce else None
        if path not in ("/face", "/eval"):
            self._send(404, b"no", extra=extra)
            return
        n = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(n) if n else b""
        ctype = self.headers.get("Content-Type") or ""
        if looks_like_plaintext_face(body, ctype):
            self._send(400, b"plaintext rejected", extra=extra)
            return
        try:
            evk, tmpl, probe = unpack_face(body)
            out = eval_conv_sq_l2(evk, tmpl, probe)
        except ValueError as e:
            self._send(400, str(e).encode()[:200], extra=extra)
            return
        except Exception as e:
            self._send(422, str(e).encode()[:500], extra=extra)
            return
        self._send(200, out, extra=extra)


if __name__ == "__main__":
    if BIND in ("0.0.0.0", "::", "127.0.0.1"):
        sys.exit("face-seal must bind VPC IP")
    if PORT == 8084:
        sys.exit("do not bind over farm-fast :8084")
    print(f"face-seal bind {BIND}:{PORT} machine={MACHINE_ID}", flush=True)
    ThreadingHTTPServer((BIND, PORT), Handler).serve_forever()
