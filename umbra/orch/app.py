import json
import os
import pathlib
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = os.environ.get("UMBRA_FHE_UPSTREAM", "http://10.20.0.5:8081")
MACHINE_ID = pathlib.Path("/etc/machine-id").read_text().strip() if pathlib.Path("/etc/machine-id").exists() else "unknown"
HOSTNAME = os.uname().nodename


class Orch(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys_stderr = __import__("sys").stderr
        sys_stderr.write("orch %s\n" % (fmt % args))

    def _send(self, code, body: bytes, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/health":
            body = json.dumps(
                {"role": "orch", "machine_id": MACHINE_ID, "hostname": HOSTNAME}
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        n = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(n) if n else b""
        nonce = self.headers.get("X-Umbra-Nonce", "")
        if path != "/eval":
            self._send(404, b"no", {"X-Umbra-Nonce": nonce} if nonce else None)
            return
        req = urllib.request.Request(
            UPSTREAM.rstrip("/") + "/eval",
            data=body,
            method="POST",
            headers={"X-Umbra-Nonce": nonce, "Content-Type": "application/octet-stream"},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                out = resp.read()
                echoed = resp.headers.get("X-Umbra-Nonce") or nonce
        except Exception as e:
            self._send(502, str(e).encode(), {"X-Umbra-Nonce": nonce} if nonce else None)
            return
        extra = {"X-Umbra-Nonce": echoed} if echoed else None
        self._send(200, out, extra)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Orch).serve_forever()
