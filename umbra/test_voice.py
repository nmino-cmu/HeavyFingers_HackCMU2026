#!/usr/bin/env python3
"""P6 S2 encrypted log-mel speaker. S11/S14 stay in P3 choreo — not a second net."""
import ipaddress
import os
import socket
import struct
import subprocess
import sys

if not __debug__:
    sys.exit("refusing -O")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from umbra.circuits.voice_s2 import MEL_A, MEL_B, VEC_A, VEC_B, reference_s2
from umbra.client import Client, second_client
from umbra.eval_host import get_eval_host
from umbra.fixtures import CARD_RRP, IDX, mutant, reference
from umbra.protocol import looks_like_plaintext_mel, pack_request

CHECKS_RUN = 0


def check(cond, msg):
    global CHECKS_RUN
    if not cond:
        raise AssertionError(msg)
    CHECKS_RUN += 1


def audio_ssh():
    return os.environ.get("UMBRA_AUDIO_SSH", "root@104.156.226.53")


def audio_vpc_url():
    ip = os.environ.get("UMBRA_FHE_VPC_IP", "10.20.0.7")
    port = os.environ.get("UMBRA_AUDIO_PORT", "8083")
    return f"http://{ip}:{port}"


def artifacts_dir():
    return os.environ.get("UMBRA_VOICE_ARTIFACTS", os.path.join(ROOT, "umbra/artifacts-voice"))


def host_gate():
    host = audio_ssh().rsplit("@", 1)[-1]
    ip = ipaddress.ip_address(socket.gethostbyname(host))
    check(ip.version == 4 and ip.is_global, "audio SSH host must be public IPv4")
    want = os.environ.get("VULTR_AUDIO_IP", "104.156.226.53")
    check(str(ip) == want, f"SSH host {ip} != {want}")
    vpc = ipaddress.ip_address(os.environ.get("UMBRA_FHE_VPC_IP", "10.20.0.7"))
    check(vpc.is_private, "audio bind must be VPC")
    check(str(vpc) != "10.20.0.4", "do not steal farm-a")
    check(str(vpc) != "10.20.0.5", "do not touch live choreo")


def ssh(cmd, data=None, timeout=300):
    args = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=20",
        audio_ssh(),
        cmd,
    ]
    return subprocess.run(args, input=data, capture_output=True, timeout=timeout)


def post_audio(body: bytes, nonce: str = "umbra-p6"):
    """POST via SSH hop — worker binds VPC only; orch has no /audio in this farm Task."""
    url = audio_vpc_url() + "/audio"
    remote = "/tmp/umbra-audio-req.bin"
    out_r = "/tmp/umbra-audio-out.bin"
    hdr_r = "/tmp/umbra-audio-hdr.txt"
    put = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", audio_ssh(), f"cat > {remote}"],
        input=body,
        capture_output=True,
        timeout=60,
    )
    check(put.returncode == 0, put.stderr.decode()[:200])
    curl = (
        f"curl -sS -D {hdr_r} -o {out_r} -w '%{{http_code}}' "
        f"-H 'Content-Type: application/octet-stream' -H 'X-Umbra-Nonce: {nonce}' "
        f"--data-binary @{remote} {url}"
    )
    run = ssh(curl)
    check(run.returncode == 0, run.stderr.decode()[:300])
    code = int(run.stdout.decode().strip() or "0")
    got = ssh(f"cat {out_r}")
    hdr = ssh(f"cat {hdr_r}")
    return code, got.stdout, hdr.stdout.decode(errors="replace")


def flatten_mel(mel):
    return [x for row in mel for x in row]


def worker_find_clean():
    run = ssh(
        "rm -rf /opt/umbra/build/umbra/artifacts-voice-mac-probe; "
        "find /opt/umbra/artifacts-voice /opt/umbra/build -type f "
        "\\( -name '*.pt' -o -name '*.onnx' -o -name client.zip -o -name '*.sk' \\) 2>/dev/null"
    )
    check(run.returncode == 0, run.stderr.decode()[:200])
    hits = [ln.strip() for ln in run.stdout.decode().splitlines() if ln.strip()]
    check(not hits, f"forbidden files on audio VM: {hits}")


def main():
    check(get_eval_host() in ("vultr", "mac"), f"EVAL_HOST={get_eval_host()}")
    # S11/S14 live in P3 choreo — fixture contract only, do not compile a second net
    check(reference(mutant("V_INDEX"), CARD_RRP)[IDX["S11"]] == 0, "V_INDEX S11 choreo")
    check(reference(mutant("V_DUB"), CARD_RRP)[IDX["S14"]] == 0, "V_DUB S14 choreo")
    check(reference_s2(VEC_A) == [1], "ref A")
    check(reference_s2(VEC_B) == [0], "ref B")

    if get_eval_host() != "vultr":
        print("EVAL_HOST=mac LOCAL_CLEAR path — no Vultr audio bind")
        print(f"CHECKS_RUN={CHECKS_RUN}")
        print(f"EVAL_HOST={get_eval_host()}")
        return

    host_gate()
    worker_find_clean()

    client = Client(artifact_dir=artifacts_dir())
    body_a = pack_request(client.evk, client.quantize_encrypt_serialize(VEC_A))
    check(len(body_a) >= 256, f"crypto wire {len(body_a)}")
    check(len(body_a) != 64 * 64 * 4, "must not be raw 64x64")
    code, out, hdrs = post_audio(body_a, nonce="voice-nonce-1")
    check(code == 200, f"audio A {code} {out[:200]}")
    check(b"RIFF" not in out and b"0.92" not in out, "no mel in response")
    bits_a = client.eval_bits(out)
    check(bits_a == [1], f"enrolled A bits {bits_a}")
    check("voice-nonce-1" in hdrs, "nonce freshness")

    body_b = pack_request(client.evk, client.quantize_encrypt_serialize(VEC_B))
    code_b, out_b, _ = post_audio(body_b)
    check(code_b == 200, f"audio B {code_b} {out_b[:200]}")
    bits_b = client.eval_bits(out_b)
    check(bits_b == [0], f"mel_B vs A must be 0 got {bits_b}")

    alt = second_client(artifact_dir=artifacts_dir())
    ct_a = client.quantize_encrypt_serialize(VEC_A)
    ct_b = alt.quantize_encrypt_serialize(VEC_A)
    check(ct_a != ct_b, "two-key ciphertexts must differ")
    body_alt = pack_request(alt.evk, ct_b)
    code_k, out_k, _ = post_audio(body_alt)
    check(code_k == 200, f"two-key eval {code_k}")
    # Leveled Tiny Linear: evk is a 64-byte header (no bootstrap). Wrong sk is garbage.
    import numpy as np

    raw_wrong = client._client.deserialize_decrypt_dequantize(out_k)
    raw_right = alt._client.deserialize_decrypt_dequantize(out_k)
    check(not np.allclose(raw_wrong, raw_right, atol=1e-3), (raw_wrong, raw_right))

    plain = struct.pack(">" + "f" * (64 * 64), *flatten_mel(MEL_A))
    check(looks_like_plaintext_mel(plain), "64x64 detector")
    code_p, _, _ = post_audio(plain)
    check(code_p >= 400, f"float32 64x64 must 4xx got {code_p}")
    wav = b"RIFF" + b"\x00" * 12 + b"WAVE" + b"\x00" * 32
    check(looks_like_plaintext_mel(wav), "wav detector")
    code_w, _, _ = post_audio(wav)
    check(code_w >= 400, f"wav must 4xx got {code_w}")
    # 64×64 of speaker B (impostor crop) also rejected as plaintext
    plain_b = struct.pack(">" + "f" * (64 * 64), *flatten_mel(MEL_B))
    code_pb, _, _ = post_audio(plain_b)
    check(code_pb >= 400, f"mel_B plaintext must 4xx got {code_pb}")

    worker_find_clean()
    print(f"CHECKS_RUN={CHECKS_RUN}")
    print(f"EVAL_HOST={get_eval_host()}")


if __name__ == "__main__":
    main()
