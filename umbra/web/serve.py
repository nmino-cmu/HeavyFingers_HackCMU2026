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
os.environ.setdefault("UMBRA_WORKER_URL", "http://207.246.126.149:8080")

WEB = Path(__file__).resolve().parent
LAST = ROOT / "umbra/fixtures/last_hops.json"
DECIDE = None
_STATIC = {
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".woff2": "font/woff2",
}


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
        if "html" in ctype or "javascript" in ctype or "css" in ctype:
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _try_static(self, path: str) -> bool:
        rel = path.lstrip("/")
        if not rel or ".." in rel.split("/"):
            return False
        fp = (WEB / rel).resolve()
        try:
            fp.relative_to(WEB.resolve())
        except ValueError:
            return False
        if not fp.is_file():
            return False
        ctype = _STATIC.get(fp.suffix.lower(), "application/octet-stream")
        self._send(200, fp.read_bytes(), ctype)
        return True

    def do_HEAD(self):
        # browsers probe with HEAD; do not 501
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, (WEB / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        if path in ("/enroll", "/enroll.html"):
            self._send(200, (WEB / "enroll.html").read_bytes(), "text/html; charset=utf-8")
            return
        if path in ("/signin", "/signin.html"):
            self._send(200, (WEB / "signin.html").read_bytes(), "text/html; charset=utf-8")
            return
        if path in ("/home", "/home.html"):
            self._send(200, (WEB / "home.html").read_bytes(), "text/html; charset=utf-8")
            return
        if path in ("/favicon.ico", "/favicon.png"):
            self._send(200, (WEB / "assets/logo.png").read_bytes(), "image/png")
            return
        if self._try_static(path):
            return
        if path == "/card":
            from umbra.card import generate

            self._send(200, json.dumps(generate()).encode())
            return
        if path == "/samples":
            from umbra.assemble import SAMPLES

            self._send(200, json.dumps({"samples": list(SAMPLES)}).encode())
            return
        if path == "/umbra.js":
            self._send(200, (WEB / "umbra.js").read_bytes(), "text/javascript; charset=utf-8")
            return
        if path == "/last":
            if LAST.is_file():
                self._send(200, LAST.read_bytes())
            else:
                self._send(200, b"{}")
            return
        if path == "/roster":
            from umbra.enroll import default_roster

            self._send(200, json.dumps({"people": default_roster().summary()}).encode())
            return
        if path == "/escrows":
            escrow_dir = ROOT / "umbra/fixtures/escrows"
            rows = []
            if escrow_dir.is_dir():
                for p in sorted(escrow_dir.glob("*.json")):
                    if p.name.endswith(".keypair.json"):
                        continue
                    rec = json.loads(p.read_text())
                    rows.append(
                        {
                            k: rec.get(k)
                            for k in (
                                "id",
                                "status",
                                "amount_sol",
                                "payer",
                                "payee",
                                "escrow_address",
                                "deposit_explorer",
                                "settle_explorer",
                            )
                        }
                    )
            last = json.loads(LAST.read_text()) if LAST.is_file() else {}
            self._send(200, json.dumps({"escrows": rows, "last_hop": last}).encode())
            return
        self._send(404, b"no")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path == "/sample":
            n = int(self.headers.get("Content-Length") or "0")
            raw = self.rfile.read(n) if n else b"{}"
            lane = (json.loads(raw.decode() or "{}") or {}).get("lane")
            from umbra.assemble import SAMPLES, run_lane

            if lane not in {s["id"] for s in SAMPLES}:
                self._send(400, b"bad lane")
                return
            self._send(200, json.dumps(run_lane(lane)).encode())
            return
        if path == "/fixture":
            os.environ.setdefault("UMBRA_FHE_ARTIFACTS", _artifacts())
            from umbra.assemble import run

            d, payload = run()
            global DECIDE
            DECIDE = d
            self._send(200, json.dumps(payload).encode())
            return
        if path == "/qa/face":
            n = int(self.headers.get("Content-Length") or "0")
            raw = self.rfile.read(n) if n else b""
            try:
                img, pose = _qa_image(self.headers.get("Content-Type", ""), raw)
                from umbra.face_qa import qa_still

                self._send(200, json.dumps(qa_still(img, pose)).encode())
            except Exception as e:
                self._send(400, str(e).encode(), "text/plain; charset=utf-8")
            return
        if path == "/qa/voice":
            n = int(self.headers.get("Content-Length") or "0")
            raw = self.rfile.read(n) if n else b""
            try:
                wav = _qa_voice(self.headers.get("Content-Type", ""), raw)
                from umbra.enroll_extract import VOICE_MIN_S, qa_voice

                self._send(200, json.dumps(qa_voice(wav, min_s=VOICE_MIN_S)).encode())
            except Exception as e:
                self._send(400, str(e).encode(), "text/plain; charset=utf-8")
            return
        if path == "/verify":
            n = int(self.headers.get("Content-Length") or "0")
            raw = self.rfile.read(n) if n else b""
            try:
                take, card, pid, audio_side = _verify_parts(self.headers.get("Content-Type", ""), raw)
                from umbra.verify import run

                out = run(take, card, person_id=pid or "", audio_side=audio_side or None)
            except Exception as e:
                self._send(400, str(e).encode(), "text/plain; charset=utf-8")
                return
            try:
                (ROOT / "umbra/roster_data/last_verify.json").write_text(json.dumps(out))
            except Exception:
                pass
            face = (out.get("lanes") or {}).get("face") or {}
            sys.stderr.write(
                "web verify id=%s ok=%s face=%s l2=%s bits=%s ms=%s\n"
                % (out.get("id"), out.get("ok"), face.get("ok"), face.get("l2"), out.get("bits"), (out.get("ms") or {}).get("total"))
            )
            self._send(200, json.dumps(out).encode())
            return
        if path == "/enroll":
            n = int(self.headers.get("Content-Length") or "0")
            raw = self.rfile.read(n) if n else b""
            try:
                faces, voices, prints, pid = _parts(self.headers.get("Content-Type", ""), raw)
                from umbra.enroll import enroll

                eid, blob = enroll(faces, voices, prints, person_id=pid)
            except Exception as e:
                self._send(400, str(e).encode(), "text/plain; charset=utf-8")
                return
            self._send(
                200,
                json.dumps({"id": eid, "bytes": len(blob), "people": _roster_summary()}).encode(),
            )
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


def _roster_summary():
    from umbra.enroll import default_roster

    return default_roster().summary()


def _parts(content_type: str, body: bytes):
    from email import message_from_bytes
    from email.policy import default as policy

    msg = message_from_bytes(b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + body, policy=policy)
    faces, voices, prints = [], [], []
    pid = None
    if not msg.is_multipart():
        raise ValueError("need multipart")
    for part in msg.iter_parts():
        name = part.get_param("name", header="content-disposition")
        payload = part.get_payload(decode=True) or b""
        if name == "id":
            pid = payload.decode("utf-8", "replace").strip() or None
        elif name == "face" and payload:
            faces.append(payload)
        elif name == "voice" and payload:
            voices.append(payload)
        elif name == "print" and payload:
            prints.append(payload)
    if not faces or not voices:
        raise ValueError("need face and voice")
    return faces, voices, prints, pid


def _verify_parts(content_type: str, body: bytes):
    from email import message_from_bytes
    from email.policy import default as policy

    msg = message_from_bytes(b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + body, policy=policy)
    take, card, pid, audio_side = b"", {}, None, b""
    if not msg.is_multipart():
        raise ValueError("need multipart")
    for part in msg.iter_parts():
        name = part.get_param("name", header="content-disposition")
        payload = part.get_payload(decode=True) or b""
        if name == "take" and payload:
            take = payload
        elif name == "audio" and payload:
            audio_side = payload
        elif name == "card" and payload:
            card = json.loads(payload.decode("utf-8", "replace") or "{}")
        elif name == "id" and payload:
            pid = payload.decode("utf-8", "replace").strip() or None
    if not take:
        raise ValueError("need a recorded take")
    return take, card, pid, audio_side


def _qa_image(content_type: str, body: bytes):
    from email import message_from_bytes
    from email.policy import default as policy

    msg = message_from_bytes(b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + body, policy=policy)
    img, pose = b"", "front"
    if not msg.is_multipart():
        raise ValueError("need multipart")
    for part in msg.iter_parts():
        name = part.get_param("name", header="content-disposition")
        payload = part.get_payload(decode=True) or b""
        if name == "face" and payload:
            img = payload
        elif name == "pose" and payload:
            pose = payload.decode("utf-8", "replace").strip() or "front"
    if not img:
        raise ValueError("need a face still")
    return img, pose


def _qa_voice(content_type: str, body: bytes) -> bytes:
    from email import message_from_bytes
    from email.policy import default as policy

    msg = message_from_bytes(b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + body, policy=policy)
    wav = b""
    if not msg.is_multipart():
        raise ValueError("need multipart")
    for part in msg.iter_parts():
        name = part.get_param("name", header="content-disposition")
        payload = part.get_payload(decode=True) or b""
        if name == "voice" and payload:
            wav = payload
    if not wav:
        raise ValueError("need voice")
    return wav


if __name__ == "__main__":
    import threading

    def _warm():
        try:
            from umbra.verify import warm

            warm()
            sys.stderr.write("web warmup done\n")
        except Exception as e:
            sys.stderr.write("web warmup %s\n" % e)

    threading.Thread(target=_warm, daemon=True).start()
    port = int(os.environ.get("UMBRA_WEB_PORT", "8765"))
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
