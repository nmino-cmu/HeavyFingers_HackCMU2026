import json
import os
import pathlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BIND = os.environ.get("UMBRA_FHE_VPC_IP", "10.20.0.5")
MACHINE_ID = pathlib.Path("/etc/machine-id").read_text().strip() if pathlib.Path("/etc/machine-id").exists() else "unknown"
HOSTNAME = os.uname().nodename


class Stub(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

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
                {"role": "stub", "machine_id": MACHINE_ID, "hostname": HOSTNAME}
            ).encode()
            self._send(200, body, "application/json")
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        n = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(n) if n else b""
        nonce = self.headers.get("X-Umbra-Nonce", "")
        extra = {"X-Umbra-Nonce": nonce} if nonce else None
        if path != "/eval":
            self._send(404, b"no", extra=extra)
            return
        self._send(200, body, extra=extra)


if __name__ == "__main__":
    ThreadingHTTPServer((BIND, 8081), Stub).serve_forever()
