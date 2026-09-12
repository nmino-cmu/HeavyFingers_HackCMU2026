import json
import os
import pathlib
import urllib.error
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
        ctype = (self.headers.get("Content-Type") or "").lower()
        if path in ("/s1", "/nonce") or ctype.startswith("text/") or "json" in ctype:
            self._send(400, b"plaintext rejected", {"X-Umbra-Nonce": nonce} if nonce else None)
            return
        routes = {
            "/eval": (UPSTREAM, "/eval"),
            "/eval3": (os.environ.get("UMBRA_P3_UPSTREAM", "http://10.20.0.5:8087"), "/eval"),
            "/print": (os.environ.get("UMBRA_PRINT_UPSTREAM", "http://10.20.0.6:8082"), "/print"),
            "/enroll": (os.environ.get("UMBRA_PRINT_UPSTREAM", "http://10.20.0.6:8082"), "/enroll"),
            "/audio": (os.environ.get("UMBRA_AUDIO_UPSTREAM", "http://10.20.0.7:8083"), "/audio"),
            "/face": (os.environ.get("UMBRA_FACE_UPSTREAM", "http://10.20.0.6:8084"), "/face"),
            "/bid": (os.environ.get("UMBRA_BID_UPSTREAM", "http://10.20.0.6:8085"), "/bid"),
        }
        if path not in routes:
            self._send(404, b"no", {"X-Umbra-Nonce": nonce} if nonce else None)
            return
        up, dest = routes[path]
        req = urllib.request.Request(
            up.rstrip("/") + dest,
            data=body,
            method="POST",
            headers={"X-Umbra-Nonce": nonce, "Content-Type": "application/octet-stream"},
        )
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                out = resp.read()
                echoed = resp.headers.get("X-Umbra-Nonce") or nonce
                self._send(resp.status, out, {"X-Umbra-Nonce": echoed} if echoed else None)
        except urllib.error.HTTPError as e:
            out = e.read()
            echoed = e.headers.get("X-Umbra-Nonce") or nonce
            self._send(e.code, out, {"X-Umbra-Nonce": echoed} if echoed else None)
        except Exception as e:
            self._send(502, str(e).encode(), {"X-Umbra-Nonce": nonce} if nonce else None)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Orch).serve_forever()
