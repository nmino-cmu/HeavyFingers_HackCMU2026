"""Mac static page + fixture eval. Spend keys never leave this process."""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

WEB = Path(__file__).resolve().parent
LAST = ROOT / "umbra/fixtures/last_hops.json"
DECIDE = None


def _artifacts():
    env = os.environ.get("UMBRA_FHE_ARTIFACTS")
    if env:
        return env
    for cand in (ROOT / "umbra/artifacts", ROOT.parent / "umbra/artifacts"):
        if (cand / "client.zip").is_file():
            return str(cand)
    return str(ROOT / "umbra/artifacts")


class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("web %s\n" % (fmt % args))

    def _send(self, code, body: bytes, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, (WEB / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/card":
            from umbra.card import generate

            self._send(200, json.dumps(generate()).encode())
            return
        if path == "/last":
            if LAST.is_file():
                self._send(200, LAST.read_bytes())
            else:
                self._send(200, b"{}")
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path == "/fixture":
            os.environ.setdefault("UMBRA_FHE_ARTIFACTS", _artifacts())
            from umbra.client import Client
            from umbra.decide import decide
            from umbra.fixtures import CARD_RRP, REF_OK, V_OK, reference
            from umbra.s1 import s1

            url = os.environ["UMBRA_WORKER_URL"].rstrip("/") + "/eval"
            client = Client()
            body = client.pack_eval_body(V_OK, CARD_RRP)
            import urllib.request

            req = urllib.request.Request(
                url, data=body, method="POST", headers={"Content-Type": "application/octet-stream"}
            )
            with urllib.request.urlopen(req, timeout=600) as resp:
                bits = client.eval_bits(resp.read())
            local = reference(V_OK, CARD_RRP)
            d = decide(bits, local, s1("the lazy dog fox am is hack win", "lazy dog fox"))
            global DECIDE
            DECIDE = d
            s1_bit = 1
            s19_bit = 0 if d.abort else 1
            self._send(200, json.dumps({"bits": list(bits) + [s1_bit, s19_bit], "ref": REF_OK, "ok": d.ok}).encode())
            return
        if path == "/hop":
            from umbra.hops import run

            if DECIDE is None or not DECIDE.ok or DECIDE.abort:
                self._send(400, b"no pass")
                return
            hop = run(DECIDE)
            if hop is None:
                self._send(400, b"no pass")
                return
            self._send(200, json.dumps({k: hop[k] for k in ("sigs", "addrs", "explorers")}).encode())
            return
        self._send(404, b"no")


if __name__ == "__main__":
    port = int(os.environ.get("UMBRA_WEB_PORT", "8765"))
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
