#!/usr/bin/env python3
"""Illegal plaintext worker — must fail harness negative tests."""
from __future__ import annotations

import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = __import__("pathlib").Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from umbra.fixtures import CARD_RRP, V_OK, reference


class Cheat(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or "0")
        self.rfile.read(n) if n else b""
        nonce = self.headers.get("X-Umbra-Nonce", "")
        # ponytail: oracle ignores ciphertext and emits fixture bits
        out = bytes(reference(V_OK, CARD_RRP))
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(len(out)))
        if nonce:
            self.send_header("X-Umbra-Nonce", nonce)
        self.end_headers()
        self.wfile.write(out)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18081
    ThreadingHTTPServer(("127.0.0.1", port), Cheat).serve_forever()


if __name__ == "__main__":
    main()
