#!/usr/bin/env python3
"""TinyS5-style choreo: bilinear card bits + Linear S6/S9. No MLP train."""
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

from umbra.circuits.choreo_floor import bits_from_v
from umbra.fixtures import CARD_LRP, CARD_RLP, CARD_RRI, CARD_RRP, MUTANTS, V_OK, encode_card, mutant


def _fit_slice(X: np.ndarray, y: np.ndarray):
    xa = np.concatenate([X, np.ones((len(X), 1), dtype=np.float32)], axis=1)
    t = 20.0 * y - 10.0
    w, *_ = np.linalg.lstsq(xa, t, rcond=None)
    return w[:-1].astype(np.float32), np.float32(w[-1])


class TinyChoreo(nn.Module):
    def __init__(self, w6, b6, w9, b9):
        super().__init__()
        self.s6 = nn.Linear(32, 1)
        self.s9 = nn.Linear(66, 1)
        with torch.no_grad():
            self.s6.weight.copy_(torch.tensor(w6).reshape(1, -1))
            self.s6.bias.copy_(torch.tensor([b6]))
            self.s9.weight.copy_(torch.tensor(w9).reshape(1, -1))
            self.s9.bias.copy_(torch.tensor([b9]))

    def forward(self, x, card):
        hand = 2 * card[:, 0:1] - 1
        side = 2 * card[:, 1:2] - 1
        s5 = (20 * x[:, 0:1] - 10) * hand
        s6 = self.s6(x[:, 1:33])
        s7 = 20 * x[:, 33:34] - 2
        s8 = (20 * x[:, 34:35]) * side
        s9 = self.s9(x[:, 1:67])
        s10 = 20 * x[:, 67:68] - 8
        s11 = 20 * (x[:, 68:71] * card[:, 2:5]).sum(dim=1, keepdim=True) - 10
        s12 = 20 * x[:, 74:75] - 10
        s13 = 20 * (1.0 - 2 * x[:, 71:72] + 2 * x[:, 72:73])
        s14 = 20 * x[:, 73:74] - 6
        # no torch.cat — Concrete-ML rejects mixed qparams on concat
        eye = torch.eye(10, device=x.device, dtype=x.dtype)
        parts = (s5, s6, s7, s8, s9, s10, s11, s12, s13, s14)
        out = parts[0] * eye[0]
        for i in range(1, 10):
            out = out + parts[i] * eye[i]
        return out


def training_set():
    cards = [CARD_RRP, CARD_LRP, CARD_RLP, CARD_RRI]
    xs, cs, ys = [], [], []
    vectors = [V_OK] + [mutant(m) for m in MUTANTS]
    for card in cards:
        cvec = encode_card(card)
        for v in vectors:
            xs.append(v)
            cs.append(cvec)
            ys.append(bits_from_v(v, card))
    return (
        np.asarray(xs, dtype=np.float32),
        np.asarray(cs, dtype=np.float32),
        np.asarray(ys, dtype=np.float32),
    )


def fit_and_check():
    xs, cs, ys = training_set()
    w6, b6 = _fit_slice(xs[:, 1:33], ys[:, 1])
    w9, b9 = _fit_slice(xs[:, 1:67], ys[:, 4])
    model = TinyChoreo(w6, b6, w9, b9).eval()
    with torch.no_grad():
        logits = model(torch.tensor(xs), torch.tensor(cs)).numpy()
    pred = (logits >= 0).astype(np.int32)
    want = ys.astype(np.int32)
    if not np.array_equal(pred, want):
        raise SystemExit(f"tiny choreo miss bits={(pred != want).sum(axis=0).tolist()}")
    print("tiny choreo exact fit")
    return model, xs, cs


def compile_concrete(out_dir: pathlib.Path):
    from concrete.ml.deployment import FHEModelDev
    from concrete.ml.torch.compile import compile_torch_model

    model, xs, cs = fit_and_check()
    quantized = compile_torch_model(
        model,
        (xs, cs),
        n_bits=8,
        inputs_encryption_status=("encrypted", "clear"),
    )
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    FHEModelDev(path_dir=str(out_dir), model=quantized).save()
    print(f"saved artifacts to {out_dir}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="umbra/artifacts-p3")
    p.add_argument("--fit-only", action="store_true")
    args = p.parse_args()
    if args.fit_only:
        fit_and_check()
        return
    compile_concrete(pathlib.Path(args.out))


if __name__ == "__main__":
    main()
