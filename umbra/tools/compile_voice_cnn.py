#!/usr/bin/env python3
"""S2 Concrete CNN-S: small Conv1d / MLP / Conv2d on farm-heavy. Not TinyS2."""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys
import tempfile
import traceback

import numpy as np
import torch
from torch import nn

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from umbra.circuits.voice_s2 import MEL_A, MEL_B, THRESH, VEC_A, VEC_B, VEC_N, enrolled_weight

STACKS_TRIED: list[str] = []


def _l2(v):
    a = np.asarray(v, dtype=np.float32).ravel()
    n = float(np.linalg.norm(a)) or 1.0
    return a / n


def pool_mel(mel, side: int):
    a = np.asarray(mel, dtype=np.float32)
    g = a.shape[0] // side
    return a.reshape(side, g, side, g).mean(axis=(1, 3))


class TinyConv1d(nn.Module):
    """4-ch Conv1d on 16-D bands, then Linear. Ch0 is center-tap identity."""

    def __init__(self, w, thresh: float = THRESH):
        super().__init__()
        self.conv = nn.Conv1d(1, 4, kernel_size=3, padding=1, bias=False)
        self.fc = nn.Linear(4 * VEC_N, 1)
        with torch.no_grad():
            self.conv.weight.zero_()
            self.conv.weight[0, 0, 1] = 1.0
            self.conv.weight[1, 0] = torch.tensor([0.25, 0.5, 0.25])
            self.conv.weight[2, 0] = torch.tensor([1.0, 0.0, -1.0])
            self.conv.weight[3, 0] = torch.tensor([-1.0, 0.0, 1.0])
            self.fc.weight.zero_()
            self.fc.weight[0, :VEC_N].copy_(torch.tensor(w, dtype=torch.float32))
            self.fc.bias.fill_(-float(thresh))

    def forward(self, x):
        return self.fc(torch.flatten(self.conv(x), 1))


class TinyMLP(nn.Module):
    """Linear(16,4)+ReLU+Linear(4,1). Hidden0 is enrolled projection."""

    def __init__(self, w, thresh: float = THRESH):
        super().__init__()
        self.fc1 = nn.Linear(VEC_N, 4)
        self.fc2 = nn.Linear(4, 1)
        with torch.no_grad():
            self.fc1.weight.zero_()
            self.fc1.bias.zero_()
            self.fc1.weight[0].copy_(torch.tensor(w, dtype=torch.float32))
            self.fc2.weight.zero_()
            self.fc2.weight[0, 0] = 1.0
            self.fc2.bias.fill_(-float(thresh))

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


class TinyConv2d(nn.Module):
    """1-ch 3×3 Conv2d on side×side + Linear. Center tap ≈ identity."""

    def __init__(self, w, thresh: float, side: int):
        super().__init__()
        n = side * side
        self.conv = nn.Conv2d(1, 1, kernel_size=3, padding=1, bias=False)
        self.fc = nn.Linear(n, 1)
        with torch.no_grad():
            self.conv.weight.zero_()
            self.conv.weight[0, 0, 1, 1] = 1.0
            self.fc.weight.copy_(torch.tensor(w, dtype=torch.float32).reshape(1, -1))
            self.fc.bias.fill_(-float(thresh))

    def forward(self, x):
        return self.fc(torch.flatten(self.conv(x), 1))


def cleartext_ok(model, xa, xb):
    with torch.no_grad():
        oa = model(torch.as_tensor(xa)).reshape(-1)
        ob = model(torch.as_tensor(xb)).reshape(-1)
        pa = int((oa >= 0.0).item())
        pb = int((ob >= 0.0).item())
    if pa != 1 or pb != 0:
        raise RuntimeError(f"cleartext mismatch A={pa} rawA={oa.numpy()} B={pb} rawB={ob.numpy()}")
    print(f"cleartext A=1 B=0 raw={float(oa)} {float(ob)}", flush=True)


def vec_calib():
    a = np.asarray(VEC_A, dtype=np.float32)
    b = np.asarray(VEC_B, dtype=np.float32)
    xs = np.stack([a, b, (a + b) / 2, a * 0.8, b * 0.8]).astype(np.float32)
    return xs.reshape(-1, 1, VEC_N), a.reshape(1, 1, VEC_N), b.reshape(1, 1, VEC_N)


def mlp_calib():
    a = np.asarray(VEC_A, dtype=np.float32)
    b = np.asarray(VEC_B, dtype=np.float32)
    xs = np.stack([a, b, (a + b) / 2, a * 0.8, b * 0.8]).astype(np.float32)
    return xs, a.reshape(1, -1), b.reshape(1, -1)


def grid_calib(side: int):
    ga = _l2(pool_mel(MEL_A, side))
    gb = _l2(pool_mel(MEL_B, side))
    thresh = float((1.0 + float(gb @ ga)) / 2.0)
    xa = ga.reshape(1, 1, side, side)
    xb = gb.reshape(1, 1, side, side)
    mid = ((ga + gb) / 2).reshape(1, 1, side, side)
    xs = np.concatenate([xa, xb, mid], axis=0).astype(np.float32)
    return xs, xa.astype(np.float32), xb.astype(np.float32), ga, thresh


# n_bits=8 makes conv/ReLU TLU inputs >16-bit. Keep accumulators small.
COMPILE_CFGS = (
    {"n_bits": 5, "rounding_threshold_bits": 6},
    {"n_bits": 4, "rounding_threshold_bits": 4},
    {
        "n_bits": {"op_inputs": 5, "op_weights": 3, "model_inputs": 5, "model_outputs": 5},
        "rounding_threshold_bits": 5,
        "p_error": 0.05,
    },
)


def compile_one(model, xs, out_dir: pathlib.Path):
    from concrete.ml.deployment import FHEModelDev
    from concrete.ml.torch.compile import compile_torch_model

    last = None
    for cfg in COMPILE_CFGS:
        print(f"compile cfg={cfg}", flush=True)
        try:
            quantized = compile_torch_model(
                model, xs, inputs_encryption_status=("encrypted",), **cfg
            )
            break
        except Exception as e:
            last = e
            print(f"compile fail cfg={cfg}: {type(e).__name__}: {e}", flush=True)
    else:
        raise last
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    FHEModelDev(path_dir=str(out_dir), model=quantized).save()
    print(f"saved artifacts to {out_dir}", flush=True)
    return quantized


def fhe_probe(out_dir: pathlib.Path, xa, xb):
    from concrete.ml.deployment import FHEModelClient, FHEModelServer

    key_dir = pathlib.Path(tempfile.mkdtemp(prefix="umbra-cnn-probe-"))
    try:
        client = FHEModelClient(path_dir=str(out_dir), key_dir=str(key_dir))
        client.generate_private_and_evaluation_keys()
        evk = client.get_serialized_evaluation_keys()
        server = FHEModelServer(path_dir=str(out_dir))
        server.load()

        def bits_of(x):
            ct = client.quantize_encrypt_serialize(np.asarray(x, dtype=np.float64))
            result = server.run(ct, evk)
            if isinstance(result, (list, tuple)):
                result = result[0]
            out = result if isinstance(result, bytes) else bytes(result)
            return (client.deserialize_decrypt_dequantize(out).reshape(-1) >= 0.5).astype(int).tolist()

        bits_a = bits_of(xa)
        bits_b = bits_of(xb)
        if bits_a != [1] or bits_b != [0]:
            raise RuntimeError(f"FHE_PROBE fail A={bits_a} B={bits_b}")
        print("FHE_PROBE=ok bits", bits_a, bits_b, flush=True)
    finally:
        shutil.rmtree(key_dir, ignore_errors=True)


def try_openfhe():
    try:
        import openfhe  # noqa: F401

        print("openfhe import ok", flush=True)
        return "ok"
    except Exception as e:
        print(f"openfhe import fail: {e}", flush=True)
        return f"fail:{e}"


def run_arch(name: str, out_dir: pathlib.Path):
    w = enrolled_weight()
    if name == "conv1d":
        xs, xa, xb = vec_calib()
        model = TinyConv1d(w).eval()
    elif name == "mlp2":
        xs, xa, xb = mlp_calib()
        model = TinyMLP(w).eval()
    elif name == "conv2d8":
        xs, xa, xb, tmpl, thresh = grid_calib(8)
        model = TinyConv2d(tmpl, thresh, 8).eval()
    elif name == "conv2d16":
        xs, xa, xb, tmpl, thresh = grid_calib(16)
        model = TinyConv2d(tmpl, thresh, 16).eval()
    else:
        raise SystemExit(f"unknown arch {name}")
    cleartext_ok(model, xa, xb)
    compile_one(model, xs, out_dir)
    fhe_probe(out_dir, xa, xb)
    return name


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="umbra/artifacts-voice-cnn")
    p.add_argument("--arch", default="auto", choices=["auto", "conv1d", "mlp2", "conv2d8", "conv2d16"])
    args = p.parse_args()
    out = pathlib.Path(args.out)
    if out.resolve().name == "artifacts-voice":
        raise SystemExit("refusing to overwrite live TinyS2 artifacts-voice")
    order = ["conv1d", "mlp2", "conv2d8"] if args.arch == "auto" else [args.arch]
    ofhe = try_openfhe()
    last_err = ""
    for name in order:
        STACKS_TRIED.append(f"concrete:{name}")
        print(f"=== TRY concrete:{name} ===", flush=True)
        try:
            won = run_arch(name, out)
            print(f"STACKS_TRIED={','.join(STACKS_TRIED + ['openfhe'])} RESULT=VULTR_CONCRETE ARCH={won} OPENFHE={ofhe}")
            return
        except Exception:
            last_err = traceback.format_exc()
            print(last_err, file=sys.stderr, flush=True)
            print(f"FAIL concrete:{name}", flush=True)
    STACKS_TRIED.append("openfhe")
    print(f"STACKS_TRIED={','.join(STACKS_TRIED)} RESULT=FAIL OPENFHE={ofhe}", file=sys.stderr)
    raise SystemExit(last_err or "all archs failed")


if __name__ == "__main__":
    main()
