#!/usr/bin/env python3
"""Client through a record proxy: no V_OK bytes on the wire except ciphertext."""
import os
import struct
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.fixtures import CARD_RRP, V_OK
from umbra.protocol import unpack_request

CHECKS_RUN = 0
RECORDED = []


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


class Rec(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(n) if n else b""
        RECORDED.append(body)
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", "0")
        self.end_headers()


def main():
    if not os.environ.get("UMBRA_FHE_ARTIFACTS"):
        for cand in (
            os.path.join(ROOT, "umbra/artifacts"),
            os.path.join(os.path.dirname(ROOT), "umbra/artifacts"),
        ):
            if os.path.isfile(os.path.join(cand, "client.zip")):
                os.environ["UMBRA_FHE_ARTIFACTS"] = cand
                break
    from umbra.client import Client

    srv = HTTPServer(("127.0.0.1", 0), Rec)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    client = Client()
    body = client.pack_eval_body(V_OK, CARD_RRP)
    import urllib.request

    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/eval",
        data=body,
        method="POST",
        headers={"Content-Type": "application/octet-stream"},
    )
    urllib.request.urlopen(req, timeout=30).read()
    srv.shutdown()
    check(len(RECORDED) == 1, RECORDED)
    wire = RECORDED[0]
    check(b"0.9137" not in wire, "fixture float ascii on wire")
    raw32 = struct.pack("<75f", *V_OK)
    raw64 = struct.pack("<75d", *V_OK)
    evk, ct, card = unpack_request(wire)
    check(raw32 not in evk + card, "V_OK f32 outside ciphertext")
    check(raw64 not in evk + card, "V_OK f64 outside ciphertext")
    check(len(ct) >= 500, "ciphertext present")
    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
