#!/usr/bin/env python3
"""Compile TinyS2 Linear(16,1) — enrolled speaker A as weights. No CNN."""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

import numpy as np
import torch
from torch import nn

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from umbra.circuits.voice_s2 import THRESH, VEC_A, VEC_B, VEC_N, enrolled_weight, reference_s2


class TinyS2(nn.Module):
    def __init__(self, w, thresh: float = THRESH):
        super().__init__()
        self.fc = nn.Linear(VEC_N, 1, bias=True)
        with torch.no_grad():
            self.fc.weight.copy_(torch.tensor(w, dtype=torch.float32).reshape(1, -1))
            self.fc.bias.fill_(-float(thresh))

    def forward(self, x):
        return self.fc(x)


def training_xy():
    xs = np.asarray([VEC_A, VEC_B], dtype=np.float32)
    ys = np.asarray([reference_s2(VEC_A), reference_s2(VEC_B)], dtype=np.float32)
    return xs, ys


def cleartext_ok(model: TinyS2, xs, ys):
    with torch.no_grad():
        out = model(torch.tensor(xs)).reshape(-1)
        pred = (out >= 0.0).int().numpy()
        want = ys.reshape(-1).astype(int)
        if not np.array_equal(pred, want):
            raise SystemExit(f"cleartext mismatch pred={pred} want={want} raw={out.numpy()}")


def compile_concrete(out_dir: pathlib.Path):
    from concrete.ml.deployment import FHEModelDev
    from concrete.ml.torch.compile import compile_torch_model

    xs, ys = training_xy()
    model = TinyS2(enrolled_weight()).eval()
    cleartext_ok(model, xs, ys)
    quantized = compile_torch_model(model, xs, n_bits=8, inputs_encryption_status=("encrypted",))
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    FHEModelDev(path_dir=str(out_dir), model=quantized).save()
    print(f"saved artifacts to {out_dir}")
    return quantized


def mac_probe(out_dir: pathlib.Path):
    """One encrypt → eval → decrypt on this machine. sk stays here."""
    from concrete.ml.deployment import FHEModelClient, FHEModelServer

    compile_concrete(out_dir)
    key_dir = out_dir / "probe-keys"
    key_dir.mkdir(exist_ok=True)
    client = FHEModelClient(path_dir=str(out_dir), key_dir=str(key_dir))
    client.generate_private_and_evaluation_keys()
    evk = client.get_serialized_evaluation_keys()
    server = FHEModelServer(path_dir=str(out_dir))
    server.load()
    x = np.asarray(VEC_A, dtype=np.float64).reshape(1, -1)
    ct = client.quantize_encrypt_serialize(x)
    result = server.run(ct, evk)
    if isinstance(result, (list, tuple)):
        result = result[0]
    out = result if isinstance(result, bytes) else bytes(result)
    bits = (client.deserialize_decrypt_dequantize(out).reshape(-1) >= 0.5).astype(int).tolist()
    if bits != [1]:
        raise SystemExit(f"MAC_FHE_PROBE fail A bits={bits}")
    xb = np.asarray(VEC_B, dtype=np.float64).reshape(1, -1)
    ctb = client.quantize_encrypt_serialize(xb)
    resultb = server.run(ctb, evk)
    if isinstance(resultb, (list, tuple)):
        resultb = resultb[0]
    outb = resultb if isinstance(resultb, bytes) else bytes(resultb)
    bits_b = (client.deserialize_decrypt_dequantize(outb).reshape(-1) >= 0.5).astype(int).tolist()
    if bits_b != [0]:
        raise SystemExit(f"MAC_FHE_PROBE fail B bits={bits_b}")
    print("MAC_FHE_PROBE=ok bits", bits, bits_b)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="umbra/artifacts-voice")
    p.add_argument("--probe", action="store_true")
    args = p.parse_args()
    out = pathlib.Path(args.out)
    if args.probe:
        mac_probe(out)
    else:
        compile_concrete(out)


if __name__ == "__main__":
    main()
