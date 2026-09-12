"""Mac fan-out: encrypt here, POST ciphertext through public orch, decrypt here.

Missing artifacts or a down box → None. decide() already omits those slots.
Print enroll is huge; off unless UMBRA_ASSEMBLE_PRINT=1.
"""
from __future__ import annotations

import os
import sys
import tempfile
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from umbra.decide import decide
from umbra.fixtures import CARD_RRP, REF_OK, V_OK, reference
from umbra.s1 import s1

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS = ["S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S4", "S2", "S3", "S24", "S1", "S19"]
_S1_TEXT = "the lazy dog fox am is hack win"


def orch() -> str:
    return os.environ["UMBRA_WORKER_URL"].rstrip("/")


def post(path: str, body: bytes, timeout: int = 600) -> bytes:
    req = urllib.request.Request(
        orch() + path,
        data=body,
        method="POST",
        headers={"Content-Type": "application/octet-stream", "X-Umbra-Nonce": "assemble"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{path} {e.code} {e.read()[:200]!r}") from e


def _zip(d: Path) -> bool:
    return (d / "client.zip").is_file()


def merge_bits(pairs):
    """Flatten (fhe, local) pairs; drop a lane when either side is None."""
    fhe, local = [], []
    for a, b in pairs:
        if a is None or b is None:
            continue
        fhe.extend(int(x) for x in a)
        local.extend(int(x) for x in b)
    return fhe, local


def _lane(name, fn):
    try:
        return name, fn()
    except Exception as e:
        sys.stderr.write(f"assemble {name} skip: {e}\n")
        return name, (None, None)


def _choreo():
    p3 = Path(os.environ.get("UMBRA_P3_ARTIFACTS", HERE / "artifacts-p3")) / "rrp"
    if not _zip(p3):
        return None, None
    from umbra.client import Client

    client = Client(artifact_dir=p3)
    bits = client.eval_bits(post("/eval3", client.pack_eval_body(V_OK, CARD_RRP)))
    return list(bits), list(reference(V_OK, CARD_RRP))


def _print(*, force=False):
    if not force and os.environ.get("UMBRA_ASSEMBLE_PRINT") != "1":
        return None, None
    art = Path(os.environ.get("UMBRA_PRINT_ARTIFACTS", HERE / "artifacts_print"))
    if not _zip(art):
        return None, None
    from umbra.print_client import PrintClient
    from umbra.print_xyt import parse_xyt

    vec = parse_xyt((HERE / "fixtures/print/pinky.xyt").read_text())
    pc = PrintClient(artifact_dir=art)
    post("/enroll", pc.pack_enroll(vec))
    return [pc.decrypt_bit(post("/print", pc.pack_print(vec, CARD_RRP)))], [1]


def _voice():
    art = Path(os.environ.get("UMBRA_VOICE_ARTIFACTS", HERE / "artifacts-voice"))
    if not _zip(art):
        return None, None
    from umbra.circuits.voice_s2 import VEC_A, reference_s2
    from umbra.client import Client
    from umbra.protocol import pack_request

    client = Client(artifact_dir=art)
    bits = client.eval_bits(post("/audio", pack_request(client.evk, client.quantize_encrypt_serialize(VEC_A))))
    return list(bits), list(reference_s2(VEC_A))


def _voice_cnn():
    art = Path(os.environ.get("UMBRA_VOICE_CNN_ARTIFACTS", HERE / "artifacts-voice-cnn"))
    if not _zip(art):
        return None, None
    import numpy as np
    from concrete.ml.deployment import FHEModelClient

    from umbra.circuits.voice_s2 import VEC_A, reference_s2
    from umbra.protocol import pack_request

    key_dir = tempfile.mkdtemp(prefix="umbra-cnn-")
    c = FHEModelClient(path_dir=str(art), key_dir=key_dir)
    c.generate_private_and_evaluation_keys()
    x = np.asarray(VEC_A, dtype=np.float64).reshape(1, 1, 16)
    out = c.deserialize_decrypt_dequantize(
        post("/audio-cnn", pack_request(c.get_serialized_evaluation_keys(), c.quantize_encrypt_serialize(x)))
    )
    bits = (np.asarray(out).reshape(-1) >= 0.5).astype(int).tolist()
    return bits, list(reference_s2(VEC_A))


def _face():
    from umbra.face_ckks import decrypt_l2, encrypt_vec, evk_bytes, face_a, match_bit, new_context, pack_face

    ctx = new_context()
    a = face_a()
    bit = match_bit(decrypt_l2(ctx, post("/face", pack_face(evk_bytes(ctx), encrypt_vec(ctx, a), encrypt_vec(ctx, a)))))
    return [bit], [1]


def _bid():
    art = Path(os.environ.get("UMBRA_BID_ARTIFACTS", HERE / "artifacts-bid"))
    if not _zip(art):
        return None, None
    import numpy as np
    from concrete.ml.deployment import FHEModelClient

    from umbra.protocol import pack_request

    key_dir = tempfile.mkdtemp(prefix="umbra-bid-")
    c = FHEModelClient(path_dir=str(art), key_dir=key_dir)
    c.generate_private_and_evaluation_keys()
    x = np.asarray([[7391.0, 12457.0]], dtype=np.float64)
    out = c.deserialize_decrypt_dequantize(
        post("/bid", pack_request(c.get_serialized_evaluation_keys(), c.quantize_encrypt_serialize(x)))
    )
    vals = np.asarray(out).reshape(-1)
    idx = 1 if (float(vals[0]) > 0 if vals.size == 1 else float(vals[1]) > float(vals[0])) else 0
    return [idx], [1]


LANES = (("choreo", _choreo), ("print", _print), ("voice", _voice), ("face", _face), ("bid", _bid))

SAMPLES = (
    {
        "id": "choreo",
        "title": "Choreo S5–S15",
        "stack": "Concrete-ML TinyS5 Linear(75,10)",
        "where": "10.20.0.5:8087",
        "path": "/eval3",
        "slow": False,
    },
    {
        "id": "print",
        "title": "Print S4",
        "stack": "Concrete TFHE .xyt (OpenFHE tried)",
        "where": "10.20.0.6:8082",
        "path": "/print",
        "slow": True,
    },
    {
        "id": "voice",
        "title": "Voice S2",
        "stack": "Concrete-ML TinyS2 Linear(16,1)",
        "where": "10.20.0.7:8083",
        "path": "/audio",
        "slow": False,
    },
    {
        "id": "voice_cnn",
        "title": "Voice CNN-S",
        "stack": "Concrete-ML Conv1d(4ch,k=3)+Linear",
        "where": "10.20.0.7:8093",
        "path": "/audio-cnn",
        "slow": False,
    },
    {
        "id": "face",
        "title": "Face S3",
        "stack": "TenSEAL 0.3.16 CKKS L2",
        "where": "10.20.0.6:8084",
        "path": "/face",
        "slow": False,
    },
    {
        "id": "bid",
        "title": "Sealed bid S24",
        "stack": "Concrete-ML Linear(2,2)",
        "where": "10.20.0.6:8085",
        "path": "/bid",
        "slow": False,
    },
    {
        "id": "words",
        "title": "Words S1",
        "stack": "Mac S1 word-order (Whisper on a take)",
        "where": "this laptop",
        "path": None,
        "slow": False,
    },
)


def _words():
    ok = s1(_S1_TEXT, "lazy dog fox")
    return [1 if ok else 0], [1]


def run_lane(name: str):
    """One sample. Print is forced (All still skips it unless env)."""
    if name == "words":
        bits, loc = _words()
        return {"id": name, "bits": bits, "ok": bits == loc == [1], "err": None}
    if name == "print":
        got = _lane("print", lambda: _print(force=True))
        bits, loc = got[1]
    elif name == "voice_cnn":
        bits, loc = _lane("voice_cnn", _voice_cnn)[1]
    else:
        fn = dict(LANES).get(name)
        if fn is None:
            raise KeyError(name)
        bits, loc = _lane(name, fn)[1]
    if bits is None:
        return {"id": name, "bits": None, "ok": False, "err": "skip"}
    return {"id": name, "bits": list(bits), "ok": list(bits) == list(loc), "err": None}


def run(s1_ok=None):
    if s1_ok is None:
        s1_ok = s1(_S1_TEXT, "lazy dog fox")
    got = {}
    with ThreadPoolExecutor(max_workers=len(LANES)) as pool:
        futs = [pool.submit(_lane, name, fn) for name, fn in LANES]
        for fut in as_completed(futs):
            name, pair = fut.result()
            got[name] = pair
    fhe, local = merge_bits(got[name] for name, _ in LANES)
    d = decide(fhe, local, s1_ok)
    extra = [1 if s1_ok else 0, 0 if d.abort else 1]
    # choreo lights stay 10 bits; farm bits follow; missing farm → None (UI dim)
    choreo_f, _ = got["choreo"]
    farm = []
    for name in ("print", "voice", "face", "bid"):
        a, _ = got[name]
        farm.append(None if a is None else int(a[0]))
    lights = list(choreo_f or [None] * 10) + farm + extra
    return d, {
        "ok": d.ok,
        "abort": d.abort,
        "reason": d.reason,
        "bits": lights,
        "ref": list(REF_OK) + [1, 1, 1, 1, 1, 1],
        "lanes": {k: (None if v[0] is None else list(v[0])) for k, v in got.items()},
        "labels": LABELS,
    }


if __name__ == "__main__":
    assert merge_bits([([1, 1], [1, 1]), (None, None), ([1], [1])]) == ([1, 1, 1], [1, 1, 1])
    assert not decide([1, 0], [1, 0], True).ok
    assert decide([1, None], [1, None], True).ok
    print("assemble self-check ok")
    if os.environ.get("UMBRA_ASSEMBLE_LIVE") == "1":
        d, payload = run()
        print(payload)
        print("ok", d.ok, "lanes", payload["lanes"])
