#!/usr/bin/env python3
"""Enroll: local crops, encrypt on Mac, roster stores ciphertext only."""
from __future__ import annotations

import io
import json
import os
import struct
import subprocess
import sys
import tempfile
import wave

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def _bmp_64(shade: int) -> bytes:
    """24-bit 64×64 BMP, bottom-up, BGR."""
    w = h = 64
    row = bytes((shade, shade, shade)) * w
    pad = (4 - (w * 3) % 4) % 4
    pixels = (row + b"\x00" * pad) * h
    off = 54
    size = off + len(pixels)
    hdr = b"BM" + struct.pack("<IHHI", size, 0, 0, off)
    dib = struct.pack("<IiiHHIIiiII", 40, w, h, 1, 24, 0, len(pixels), 0, 0, 0, 0)
    return hdr + dib + pixels


def _wav_tone(freq=220, seconds=0.4, rate=16000, amp=12000) -> bytes:
    n = int(rate * seconds)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        frames = bytearray()
        for i in range(n):
            import math

            x = int(amp * math.sin(2 * math.pi * freq * i / rate))
            frames += struct.pack("<h", x)
        w.writeframes(bytes(frames))
    return buf.getvalue()


def test_extract():
    from umbra.enroll_extract import image_to_grid, wav_to_voice, image_to_print

    dark = image_to_grid(_bmp_64(10))
    lite = image_to_grid(_bmp_64(200))
    check(len(dark) == 4096, len(dark))
    check(all(0.0 <= x <= 1.0 for x in dark), "grid range")
    check(sum(lite) > sum(dark), (sum(lite), sum(dark)))

    v = wav_to_voice(_wav_tone())
    check(len(v) == 16, len(v))
    check(abs(sum(x * x for x in v) - 1.0) < 1e-3, v)
    from umbra.enroll_extract import VOICE_MIN_S, qa_voice

    check(VOICE_MIN_S >= 12, VOICE_MIN_S)
    check(not qa_voice(_wav_tone(seconds=4))["ok"], "short clip fails qa")
    # a real 12s take: speech-level tone plus one loud syllable. The old peak-relative gate counted only samples
    # above 12% of that spike and said "need 12s of speech, got 3s"; length is the recording now.
    spiky = bytearray(_wav_tone(seconds=12.5, amp=4000))
    spiky[44 + 2 * 16000 : 44 + 2 * 16000 + 2] = struct.pack("<h", 30000)
    q = qa_voice(bytes(spiky))
    check(q["ok"], q)
    check(not qa_voice(_wav_tone(seconds=12.5, amp=400))["ok"], "near-silent take still fails")
    check(not qa_voice(_wav_tone(seconds=11.0))["ok"], "11s is not 12s")
    from umbra.enroll_extract import crop_grid

    boxed = crop_grid(_bmp_64(80), {"x": 0.1, "y": 0.1, "w": 0.8, "h": 0.8})
    check(len(boxed) == 4096, len(boxed))
    from umbra.enroll_extract import prep_face

    face = [(((i * 17 + 9) % 251) / 255.0) for i in range(4096)]
    bright = [min(1.0, x + 0.25) for x in face]
    other = [((i * 41 + 3) % 197) / 255.0 for i in range(4096)]
    raw_same = sum((a - b) ** 2 for a, b in zip(face, bright))
    n_same = sum((a - b) ** 2 for a, b in zip(prep_face(face), prep_face(bright)))
    n_other = sum((a - b) ** 2 for a, b in zip(prep_face(face), prep_face(other)))
    check(n_same < raw_same * 0.2, (n_same, raw_same))
    check(n_same < 90, n_same)
    check(n_other > n_same * 4, (n_same, n_other))
    from umbra.face_qa import qa_still

    # green oval == Vision found a face; a flat gray frame has none
    miss = qa_still(_bmp_64(80), "front")
    check(not miss["ok"] and miss["face"] is None and miss["reason"], miss)
    check(not qa_still(_bmp_64(80), "left")["ok"], "side pose with no face")
    # fake a Vision box: front is green for any face; a side only goes gold when yaw is clearly the other way
    import umbra.face_qa as fq

    real_inspect = fq.inspect_bytes
    box = {"x": 0.3, "y": 0.2, "w": 0.4, "h": 0.5, "yaw": 0.4}
    fq.inspect_bytes = lambda data: {"faces": [box], "hands": []}
    try:
        hit = qa_still(b"x", "front")
        check(hit["ok"] and hit["face"] is box and hit["yaw"] == 0.4, hit)
        check(qa_still(b"x", "left")["ok"], "left accepts +yaw (your left)")
        wrong = qa_still(b"x", "right")
        check(not wrong["ok"] and wrong["face"] is box and "other way" in wrong["reason"], wrong)
        box["yaw"] = 0.1
        check(qa_still(b"x", "right")["ok"], "right tolerates near-front yaw")
    finally:
        fq.inspect_bytes = real_inspect
    from umbra.face_qa import POSES

    check(POSES["front"](0.0) and POSES["front"](0.5), "front always")
    check(POSES["left"](0.4) and POSES["left"](0.0) and not POSES["left"](-0.4), "left blocks only far right")
    check(POSES["right"](-0.4) and POSES["right"](0.0) and not POSES["right"](0.4), "right blocks only far left")

    p = image_to_print(_bmp_64(80))
    check(len(p) == 48, len(p))


def test_roster_rejects_media():
    from umbra.roster import Roster, looks_like_plaintext_enroll

    check(looks_like_plaintext_enroll(_bmp_64(20)), "bmp")
    check(looks_like_plaintext_enroll(_wav_tone()), "wav")
    check(looks_like_plaintext_enroll(b"\x89PNG\r\n\x1a\n" + b"x" * 80), "png")
    r = Roster(tempfile.mkdtemp(prefix="umbra-roster-"))
    try:
        r.put(_bmp_64(20))
        check(False, "bmp stored")
    except ValueError:
        check(True, "bmp reject")


def test_roster_two_people():
    from umbra.roster import Roster, pack_record, unpack_record

    face_ct = b"\x00CTFACE" + os.urandom(80_000)
    voice_ct = b"\x00CTVOIC" + os.urandom(80_000)
    print_ct = b"\x00CTPRNT" + os.urandom(80_000)
    body = pack_record("p1", [("face", "front", face_ct), ("voice", "line0", voice_ct), ("print", "i0", print_ct)])
    check(b"BM" not in body[:8], "no bmp magic")
    r = Roster(tempfile.mkdtemp(prefix="umbra-roster-"))
    pid = r.put(body)
    check(pid == "p1", pid)
    got = r.get("p1")
    check(got == body, "roundtrip")
    rec = unpack_record(got)
    check(rec["id"] == "p1", rec["id"])
    check(len(rec["items"]) == 3, rec["items"])
    check(all(it[2][:3] == b"\x00CT" for it in rec["items"]), "cts")
    other = pack_record("p2", [("face", "front", b"\x00CTFACE" + os.urandom(80_000))])
    r.put(other)
    check(set(r.ids()) == {"p1", "p2"}, r.ids())
    check(r.get("p1") != r.get("p2"), "isolated")


def _isolate_keys():
    d = tempfile.mkdtemp(prefix="umbra-keys-")
    os.environ["UMBRA_ENROLL_KEYDIR"] = d
    return d


def test_live_profile():
    from umbra.live_person import live_id
    from umbra.roster import Roster, looks_like_plaintext_enroll, unpack_record

    r = Roster(os.path.join(ROOT, "umbra", "roster_data"))
    pid = live_id()
    if not pid:
        print("LIVE_PROFILE skip (empty roster)")
        return
    check(pid in r.ids(), r.ids())
    raw = r.get(pid)
    check(not looks_like_plaintext_enroll(raw), "live stored media")
    rec = unpack_record(raw)
    kinds = {it[0] for it in rec["items"]}
    check("face" in kinds and "voice" in kinds, kinds)
    check(sum(1 for it in rec["items"] if it[0] == "face") >= 3, rec["items"])
    sk = os.path.join(ROOT, "umbra", "enroll_keys", pid, "ctx.bin")
    check(os.path.isfile(sk), "live sk missing")


def test_mac_enroll_no_media_on_wire():
    from umbra.enroll import enroll_bytes
    from umbra.roster import Roster, looks_like_plaintext_enroll, unpack_record

    _isolate_keys()
    store = Roster(tempfile.mkdtemp(prefix="umbra-roster-"))
    faces = [_bmp_64(30), _bmp_64(40), _bmp_64(50)]
    voices = [_wav_tone(180), _wav_tone(440)]
    prints = [_bmp_64(90), _bmp_64(110)]
    pid, raw = enroll_bytes(faces, voices, prints, person_id="nick")
    check(pid == "nick", pid)
    auto, _ = enroll_bytes(faces, voices, prints)
    check(auto.isdigit() and 6 <= len(auto) <= 9, auto)
    check(not looks_like_plaintext_enroll(raw), "wire is media")
    check(raw[0:4] != b"RIFF", "wav leaked")
    check(b"\xff\xd8\xff" not in raw[:16], "jpeg leaked")
    store.put(raw)
    rec = unpack_record(store.get("nick"))
    kinds = {it[0] for it in rec["items"]}
    check(kinds == {"face", "voice", "print"}, kinds)
    check(sum(1 for it in rec["items"] if it[0] == "face") == 3, rec["items"])
    check(all(len(it[2]) >= 50_000 for it in rec["items"]), "cts too small")


def test_mac_store_persists():
    """This laptop is the roster. Reopen the dir; ciphertext still there. No Vultr."""
    from umbra.enroll import enroll
    from umbra.roster import Roster, unpack_record

    _isolate_keys()
    root = tempfile.mkdtemp(prefix="umbra-roster-")
    pid, raw = enroll(
        [_bmp_64(30)],
        [_wav_tone(200)],
        [_bmp_64(90)],
        person_id="keep",
        roster=Roster(root),
    )
    check(pid == "keep", pid)
    again = Roster(root)
    check(again.get("keep") == raw, "lost after reopen")
    rec = unpack_record(again.get("keep"))
    check({it[0] for it in rec["items"]} == {"face", "voice", "print"}, rec)
    sums = again.summary()
    check(sums == [{"id": "keep", "face": 1, "voice": 1, "print": 1}], sums)


def test_jpeg_crop():
    from umbra.enroll_extract import image_to_grid

    td = tempfile.mkdtemp()
    src = os.path.join(td, "a.bmp")
    dst = os.path.join(td, "a.jpg")
    open(src, "wb").write(_bmp_64(120))
    subprocess.check_call(["sips", "-s", "format", "jpeg", src, "--out", dst], stdout=subprocess.DEVNULL)
    g = image_to_grid(open(dst, "rb").read())
    check(len(g) == 4096, len(g))
    check(all(0.0 <= x <= 1.0 for x in g), "jpeg range")


def test_http_enroll_mac_only():
    import importlib.util
    import threading
    import urllib.request
    from http.server import ThreadingHTTPServer

    spec = importlib.util.spec_from_file_location("umbra_serve", os.path.join(ROOT, "umbra/web/serve.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _isolate_keys()
    root = tempfile.mkdtemp(prefix="umbra-roster-")
    os.environ["UMBRA_ROSTER"] = root
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), mod.H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    port = httpd.server_address[1]
    try:
        bound = "----UmbraTest"
        chunks = []

        def field(name, data, filename=None, ctype="application/octet-stream"):
            dispo = f'name="{name}"'
            if filename:
                dispo += f'; filename="{filename}"'
            chunks.append(
                f"--{bound}\r\nContent-Disposition: form-data; {dispo}\r\nContent-Type: {ctype}\r\n\r\n".encode()
                + data
                + b"\r\n"
            )

        field("id", b"http1", ctype="text/plain")
        field("face", _bmp_64(40), "f.bmp", "image/bmp")
        field("voice", _wav_tone(260), "v.wav", "audio/wav")
        field("print", _bmp_64(90), "p.bmp", "image/bmp")
        chunks.append(f"--{bound}--\r\n".encode())
        body = b"".join(chunks)
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/enroll",
            data=body,
            method="POST",
            headers={"Content-Type": f"multipart/form-data; boundary={bound}"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            out = json.loads(resp.read().decode())
        check(out["id"] == "http1", out)
        check(out["bytes"] > 50_000, out["bytes"])
        listed = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/roster", timeout=8).read())
        check(any(p["id"] == "http1" for p in listed["people"]), listed)
        from umbra.roster import Roster, looks_like_plaintext_enroll

        raw = Roster(root).get("http1")
        check(not looks_like_plaintext_enroll(raw), "http stored media")
    finally:
        httpd.shutdown()


def test_pages_split():
    enroll = open(os.path.join(ROOT, "umbra/web/enroll.html"), encoding="utf-8").read().lower()
    sign = open(os.path.join(ROOT, "umbra/web/index.html"), encoding="utf-8").read().lower()
    do = open(os.path.join(ROOT, "umbra/web/signin.html"), encoding="utf-8").read().lower()
    for w in ("begin sign up", "capture face", "record voice", "save encrypted", "clear category"):
        check(w in enroll, w)
    check("oval" in enroll and "well lit" in enroll, "face oval")
    check("qavoice" in enroll or "qa/voice" in enroll, "voice qa")
    check("birch canoe" in enroll and "rainbow" in enroll, "voice enroll passage")
    check("play back" in enroll or "playback" in enroll or "voiceplay" in enroll, "voice playback")
    check("recwave" in enroll or "rec-dot" in enroll, "recording meter")
    check("getaudiotracks" in enroll or "getusermedia" in enroll, "mic path")
    check("finished" in enroll and "voiceui" in enroll, "voice stays until finished")
    check('type="file"' in enroll and "accept=\"audio" in enroll, "voice file submit")
    check("choose voice file" in enroll, "voice file label")
    check("dev mode" not in enroll and "skipvoice" not in enroll and "skipfinger" not in enroll, "dev skip")
    check("capture finger" not in enroll and "step === \"finger\"" not in enroll, "finger step")
    check("skip to home" not in enroll and "skip to home" not in sign and "skip to home" not in do, "skip home")
    recfn = enroll[enroll.find("async function recordvoice"):enroll.find("function clearcategory")]
    check(recfn.find('stopvoice").onclick') < recfn.find("getusermedia"), "stop bound before mic wait")
    check(recfn.find("getusermedia") < recfn.find("newctx()"), "mic before audiocontext")
    check(recfn.find("getusermedia") < recfn.find("startclock()"), "clock after mic grant")
    # Stop during the mic grant is a cancel (clock not running), never an end-of-take with a stale recStarted
    check(0 <= recfn.find("recstarted = 0") < recfn.find('stopvoice").onclick'), "stop during mic wait cancels")
    check(recfn.find("rec.start()") < recfn.find("startclock()"), "clock starts with the recorder")
    check("new mediarecorder(mic)" in recfn and "createscriptprocessor" not in enroll, "mediarecorder is the take")
    check("createanalyser" in recfn and "paintlevel" in recfn, "live meter")
    check("getaudiotracks" in recfn, "enroll reuses live mic")
    check("readfaces" in enroll and "grabframe" in recfn, "reading-gaze stills while they read")
    # Desktop face window owns the camera; passage + rec deck still sit together and shrink the view while reading.
    check("face-view" in enroll and 'id="stage"' in enroll, "enroll camera is the face window")
    check(enroll.find('id="script"') < enroll.find('id="recdeck"'), "passage then rec deck")
    check('classlist.toggle("short", step === "voice")' in enroll, "small camera while reading")
    check('classlist.toggle("rest"' in enroll, "enroll preview rests after stills")
    check('classlist.toggle("rest"' in do, "signin preview rests after take")
    check("paintlanes" in enroll and "sealviz" in do, "encrypt bars / fhe blocks")
    save = enroll[enroll.find("async function saveencrypted"):]
    check(0 <= save.find("paintlanes(") < save.find("umbra.enroll"), "enroll bars then encrypt")
    check("sealviz" not in save, "enroll has no fhe eval viz")
    check('id="enter"' in enroll and "enrolled=" in enroll, "enroll enter after save")
    send = do[do.find('getelementbyid("send").onclick'):]
    check("paintlanes(" in send and "settimeout(startfhe, 1000)" in send, "encrypt bars 1s then fhe")
    check("startfhe" in send and "heldout" in send, "result waits if encrypt is still up")
    fhe = do[do.find("function startfhe"):do.find("function startfhe") + 500]
    check("sealviz(" in fhe and 'paintlights("idle")' in fhe, "fhe is the block eval")
    check('data-fhe="eval"' in do and 'data-fhe="probe"' in do, "fhe is probe ⋆ roster")
    check('id="enter"' in do and 'location.assign("/home")' in do, "enter to desk")
    check("settimeout(() => location.assign(\"/home\")" not in do, "no auto enter")
    camfn = enroll[enroll.find("async function opencam"):enroll.find("async function tickqa")]
    gum = camfn.find("getusermedia({")
    check(gum >= 0 and "audio: true" in camfn[gum:gum + 140], "begin asks for mic")
    check('id="card"' not in enroll, "card on enroll page")
    check("/card" not in enroll, "enroll fetches card")
    check("snapface" not in sign and "doenroll" not in sign, "enroll controls on sign-in")
    check("sign in" in sign, "sign in")
    check("/signin" in sign, "sign in goes to challenge")
    check("say:" in do and "send" in do, "challenge says what to do")
    check("look straight" in do and "oval" in do, "signin front + oval")
    check("takeplay" in do and "settake" in do and "createobjecturl" in do, "signin plays the send blob")
    check("rectok" in do, "stale recorder cannot overwrite take")
    check("audio: true" in do, "one av stream for the take")
    check('fd.append("audio"' in do, "safari mic sidecar on send")
    check("getaudiotracks" in do, "signin retries mic if camera stream is silent")
    # Safari: a mic request without a click fails and poisons the mic for the page, and a second getUserMedia while a
    # camera-only stream is live is not granted. So: load is video only; Record (a click) releases the camera, then asks for both.
    camfn = do[do.find("async function opencam"):do.find("function settake")]
    gum = camfn.find("getusermedia({")
    check(gum >= 0 and "audio: false" in camfn[gum:gum + 140] and "audio: true" not in camfn, "signin load asks for the mic")
    recclick = do[do.find('getelementbyid("rec").onclick'):do.find('getelementbyid("send").onclick')]
    gum = recclick.find("getusermedia({")
    check(gum >= 0 and "audio: true" in recclick[gum:gum + 140], "record click asks for the mic in the gesture")
    check(gum >= 0 and ".stop()" in recclick[:gum], "record click asks for the mic while the camera stream is live")
    check("ensuremic" not in do and "addtrack" not in do, "signin bolts a second gum onto a live stream")
    check("grabframe" in enroll, "enroll stores full frames like verify")
    check('id="send" disabled' in do, "send starts gated")
    check("qaface" in do or "qa/face" in do, "signin face qa")
    check("end on your" not in do, "card finger spot blank")
    check("umbra.verify" in do or "verify(fd)" in do, "signin sends verify")
    check("issecurecontext" in enroll or "mediadevices" in enroll, "camera error path")
    check("enrolled user" in enroll or "enrolled user" in sign, "enroll number copy")
    check("save this number to sign in later" in sign, "number on sign-in")
    check("justenrolled" in sign, "just enrolled banner")
    check("stopcam" in enroll and "enrolled=" in enroll, "camera off then sign-in")
    check('paintthumbs("print")' not in enroll, "no finger preview")
    # live QA drives the oval on both pages; capture never waits on it
    check("setinterval(tickqa" in enroll and 'classlist.toggle("ok"' in enroll, "enroll live oval")
    check("setinterval(tickqa" in do and 'classlist.toggle("ok"' in do, "signin live oval")
    snapfn = enroll[enroll.find("async function snap("):enroll.find("function acceptvoice")]
    check(snapfn and "throw new error(q.reason" not in snapfn and "qaface" not in snapfn, "snap gated on qa")
    check("q.ok && q.face" in enroll and "q.ok && q.face" in do, "green needs a face box")
    css = open(os.path.join(ROOT, "umbra/web/style.css"), encoding="utf-8").read().lower()
    check("#guide.ok .oval" in css and "var(--ok)" in css, "green oval rule in shared css")
    check("#stage.short" in css or ".face-view.short" in css, "reading camera can shrink")
    check(".face-view.rest" in css and ".seal-viz" in css, "rest preview + encrypt strip")
    check(".lane-track" in css and ".fhe-pair" in css, "encrypt bars + fhe blocks")
    check('id="stage"' in do and "face-view" in do, "signin camera is the face window")
    check("[hidden] { display: none !important; }" in css, "hidden rows/oval must actually hide (display:flex beats ua hidden)")


def main():
    test_extract()
    test_live_profile()
    test_roster_rejects_media()
    test_roster_two_people()
    test_mac_enroll_no_media_on_wire()
    test_mac_store_persists()
    test_jpeg_crop()
    test_http_enroll_mac_only()
    test_pages_split()
    print(f"CHECKS_RUN={CHECKS_RUN}")


if __name__ == "__main__":
    main()
